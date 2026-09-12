/**
 * 原型 / PRD 页面里的导出客户端。
 *
 * 端口不再固定：由 pm-runtime-config.js 下发（该文件在每次端口变化时被服务端重写），
 * 所以这里必须动态加载它，不能把端口写死。
 *
 * 所有报错文案只指向「双击项目根目录的启动脚本」——那是两个平台上唯一保证
 * 存在于项目里的东西。历史文案里出现过的 scripts/initialize.py、python3 命令
 * 在用户的项目里根本不存在（前者从不安装进项目，后者在 Windows 上没有）。
 */
(function () {
  'use strict';

  const IS_WINDOWS = /Windows/i.test(navigator.userAgent);
  const ENTRY = IS_WINDOWS ? '「启动原型导出服务.bat」' : '「启动原型导出服务.command」';
  const HOW_TO_START = '请双击项目根目录的' + ENTRY + '，保持那个窗口开着，再点一次导出。';
  // 升级路径：双击入口在两个平台上都必然可用，所以它留给上面那条文案。
  // 这里是「双击了也不行」时的下一步，面向已经打开终端的人。macOS 多给一条
  // 重注册命令：那边点导出本该自动起服务，走到这一步通常是注册掉了。
  const HOW_TO_DIAGNOSE = IS_WINDOWS
    ? '若仍不行，在项目目录执行：py -3 scripts\\start_service.py --doctor'
    : '若仍不行，在项目目录执行：bash scripts/install_launcher.sh 重新注册自动启动，'
      + '或 python3 scripts/start_service.py --doctor 看体检报告';

  let cfg = window.PM_RUNTIME || {};
  let server = cfg.server;
  let launcher = cfg.launcher;
  const clientScriptSrc = document.currentScript && document.currentScript.src;
  let configLoadPromise = null;
  let readyPromise = null;
  let exporting = false;
  const revisions = new Map();

  const path = () => decodeURIComponent(location.pathname || '');

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  function configured() {
    return !!(server && cfg.projectId && cfg.token);
  }

  function loadRuntimeConfig() {
    if (configured()) return Promise.resolve();
    if (!clientScriptSrc) {
      return Promise.reject(new Error('缺少项目运行配置。' + HOW_TO_START));
    }
    // 失败后不缓存 promise：用户按提示启动服务后，下一次点击应当能重新加载到配置。
    if (!configLoadPromise) {
      configLoadPromise = new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = new URL('pm-runtime-config.js', clientScriptSrc).href
          + '?ts=' + Date.now();  // 端口换过之后不能吃浏览器缓存里的旧配置
        script.onload = () => {
          cfg = window.PM_RUNTIME || {};
          server = cfg.server;
          launcher = cfg.launcher;
          configured() ? resolve() : reject(new Error('项目运行配置不完整。' + HOW_TO_START));
        };
        script.onerror = () => reject(new Error('读不到项目运行配置。' + HOW_TO_START));
        document.head.appendChild(script);
      }).catch((error) => {
        configLoadPromise = null;
        throw error;
      });
    }
    return configLoadPromise;
  }

  function configCheck() {
    if (cfg.readOnly) throw new Error('当前是只读分享模式，导出需要在本地项目里操作。');
    if (!configured()) throw new Error('项目运行配置缺失。' + HOW_TO_START);
  }

  async function request(url, payload) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 120000);
    try {
      const response = await fetch(url, {
        method: payload === undefined ? 'GET' : 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-PM-Project': cfg.projectId,
          'X-PM-Token': cfg.token
        },
        body: payload === undefined ? undefined : JSON.stringify(payload),
        cache: 'no-store',
        signal: controller.signal
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || data.error) throw new Error(data.error || ('HTTP ' + response.status));
      return data;
    } finally {
      clearTimeout(timer);
    }
  }

  async function health() {
    const response = await fetch(server + '/api/health', {
      cache: 'no-store', signal: AbortSignal.timeout(3000)
    });
    if (response.status === 404) {
      // 老版本服务没有 /api/health。它还占着端口，所以必须先让用户停掉它。
      const error = new Error('这个端口上是旧版导出服务。请关掉它的终端窗口（或重启电脑），再'
        + HOW_TO_START);
      error.identity = true;
      throw error;
    }
    if (!response.ok) throw new Error('导出服务健康检查失败（HTTP ' + response.status + '）');
    const state = await response.json();
    if (state.project_id !== cfg.projectId) {
      const error = new Error('这个端口被另一个项目的导出服务占着。请关掉它，再' + HOW_TO_START);
      error.identity = true;
      throw error;
    }
    if (state.read_only) {
      const error = new Error('当前服务是只读模式，不能导出或写回文件。');
      error.identity = true;
      throw error;
    }
    return state;
  }

  async function ensureReady() {
    await loadRuntimeConfig();
    configCheck();
    if (readyPromise) return readyPromise;
    // 成功后保留缓存：PRD「一键复制全文」会对每个 iframe 各调一次，不该每次都重新体检。
    readyPromise = (async () => {
      try {
        return await health();
      } catch (error) {
        if (error.identity) throw error;  // 端口上有东西但不是我们要的，唤起也没用
      }
      // 服务没在跑。macOS 上若装过常驻启动器，它能帮我们拉起来；没装就直接给指引。
      let launch;
      try {
        launch = await request(launcher + '/api/launch', {});
      } catch (error) {
        throw new Error('导出服务没有启动。' + HOW_TO_START);
      }
      if (!launch.ok) throw new Error(launch.error || ('导出服务启动失败。' + HOW_TO_START));
      // 首次启动要装依赖、冷启动浏览器，给足 45s
      const deadline = Date.now() + 45000;
      while (Date.now() < deadline) {
        try {
          return await health();
        } catch (error) {
          if (error.identity) throw error;
        }
        await sleep(600);
      }
      throw new Error('导出服务启动超时。' + HOW_TO_DIAGNOSE);
    })().catch((error) => {
      readyPromise = null;  // 只在失败时清空，让用户修好问题后能重试
      throw error;
    });
    return readyPromise;
  }

  async function api(route, payload) {
    await ensureReady();
    return request(server + route, payload);
  }

  // ── 浏览器内编辑写回 ─────────────────────────────────────────────
  async function revision(file) {
    const target = file || path();
    const data = await api('/api/revision', { path: target });
    revisions.set(target, data.revision);
    return data.revision;
  }

  async function save(content, file) {
    const target = file || path();
    if (!revisions.has(target)) throw new Error('尚未读取文件版本，请重新加载页面后再保存');
    const data = await api('/api/save-html', {
      path: target, content, revision: revisions.get(target)
    });
    revisions.set(target, data.revision);
    return data;
  }

  // ── 单页取图：给 PRD「一键复制全文」把原型 iframe 换成 base64 图片 ──
  // file:// 下浏览器既不能 fetch 本地 PNG、canvas 也会被污染，base64 只能由本地服务下发。
  async function snapshot(src, opts) {
    if (!src) throw new Error('缺少 iframe src');
    opts = opts || {};
    return api('/api/snapshot', {
      src, base: opts.base || path(), scale: opts.scale || 2,
      viewport: opts.viewport, force: !!opts.force
    });
  }

  // 本地 <img>（详细方案「原型」列的截图版）→ base64，同样只能由服务下发
  async function asset(src, opts) {
    if (!src) throw new Error('缺少 img src');
    return api('/api/asset', { src, base: (opts || {}).base || path() });
  }

  // ── 导出按钮 ────────────────────────────────────────────────────
  // 按钮识别沿用旧版的宽匹配：已经生成出去的原型里，有的只有文案没有 id/class。
  function isExportButton(target) {
    if (!target || target.nodeType !== 1) return null;
    const button = target.closest('button, [role="button"], a');
    if (!button) return null;
    const text = (button.textContent || '').trim();
    const matched = button.id === 'exportFab'
      || button.classList.contains('export-fab')
      || button.classList.contains('export-btn')
      || text.indexOf('一键导出所有截图') !== -1
      || text.indexOf('导出PNG截图') !== -1;
    return matched ? button : null;
  }

  function findExportButton() {
    return document.getElementById('exportFab')
      || document.querySelector('.export-fab, .export-btn')
      || Array.from(document.querySelectorAll('button')).find(isExportButton);
  }

  // 不用 button.disabled：导出按钮可能是 <a> 或 [role=button]，那上面 disabled 无效。
  function setButton(button, text, background, busy) {
    if (!button) return;
    button.textContent = text;
    if (background !== undefined) button.style.background = background;
    button.style.opacity = busy ? '0.75' : '1';
    button.style.pointerEvents = busy ? 'none' : '';
  }

  function notifyParent(message) {
    if (window.parent && window.parent !== window) window.parent.postMessage(message, '*');
  }

  async function exportAll(button) {
    if (exporting) return;
    exporting = true;
    const originalText = button ? button.textContent : '';
    const originalBackground = button ? button.style.background : '';
    const restore = () => setTimeout(
      () => setButton(button, originalText, originalBackground, false), 2600);

    try {
      setButton(button, '正在连接导出服务…', undefined, true);
      const job = await api('/api/screenshot', {
        path: path(),
        viewport: {
          width: Math.max(1, Math.round(innerWidth || 1440)),
          height: Math.max(1, Math.round(innerHeight || 900))
        }
      });
      if (!job.started) throw new Error('导出任务没有启动');

      const deadline = Date.now() + 300000;
      while (Date.now() < deadline) {
        const state = await request(server + '/api/status');
        if (state.job_id !== job.job_id) throw new Error('导出任务已切换，请重新确认结果');
        setButton(button, '正在导出 ' + state.progress + '/' + state.total, undefined, true);
        if (state.done) {
          setButton(button, '已导出 ' + state.success_count + '/' + state.total + ' 张 PNG',
            '#22c55e', false);
          notifyParent('export-success');
          restore();
          return state;
        }
        await sleep(700);
      }
      throw new Error('导出等待超时，请查看项目里的 .pm-workflow/service.log');
    } catch (error) {
      console.error('[prototype export]', error);
      setButton(button, '导出失败', '#ef4444', false);
      window.alert(error.message);
      notifyParent('export-error');
      restore();
    } finally {
      exporting = false;
    }
  }

  document.addEventListener('click', (event) => {
    const button = isExportButton(event.target);
    if (!button) return;
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    exportAll(button);
  }, true);

  window.addEventListener('message', (event) => {
    if (event.data !== 'trigger-export') return;
    exportAll(findExportButton());
  }, true);

  window.PMService = { revision, save, api, health };
  window.exportPrototypeViaServer = exportAll;
  window.snapshotPrototypeViaServer = snapshot;
  window.inlineAssetViaServer = asset;
  window.ensureExportServerReady = ensureReady;
})();
