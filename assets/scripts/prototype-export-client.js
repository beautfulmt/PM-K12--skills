(function () {
  var SERVER = window.PROTOTYPE_EXPORT_SERVER || 'http://localhost:8765';
  var running = false;

  function isExportButton(target) {
    if (!target || target.nodeType !== 1) return null;
    var button = target.closest('button, [role="button"], a');
    if (!button) return null;
    var text = (button.textContent || '').trim();
    var matched = button.id === 'exportFab'
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

  function setButton(button, text, background, disabled) {
    if (!button) return;
    button.textContent = text;
    if (background !== undefined) button.style.background = background;
    button.style.opacity = disabled ? '0.75' : '1';
    button.style.pointerEvents = disabled ? 'none' : '';
  }

  function currentHtmlPath() {
    return decodeURIComponent(window.location.pathname || '');
  }

  function currentViewport() {
    return {
      width: Math.max(1, Math.round(window.innerWidth || document.documentElement.clientWidth || 1440)),
      height: Math.max(1, Math.round(window.innerHeight || document.documentElement.clientHeight || 900))
    };
  }

  function sleep(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  async function fetchStatus() {
    var response = await fetch(SERVER + '/api/status?ts=' + Date.now(), { cache: 'no-store' });
    if (!response.ok) throw new Error('导出服务状态读取失败');
    return response.json();
  }

  async function waitForServerReady(button) {
    var deadline = Date.now() + 16000;
    var attempt = 0;
    while (Date.now() < deadline) {
      attempt += 1;
      try {
        return await fetchStatus();
      } catch (error) {
        setButton(button, attempt === 1 ? '正在启动导出服务...' : '等待导出服务启动...', undefined, true);
        await sleep(900);
      }
    }
    throw new Error('导出服务未启动');
  }

  async function pollStatus(button) {
    var lastStatus = null;
    while (true) {
      var status = await fetchStatus();
      lastStatus = status;

      if (status.error) throw new Error(status.error);

      var progress = status.progress || 0;
      var total = status.total || 0;
      var current = status.current || '截图中...';
      setButton(button, total ? ('正在导出 ' + progress + '/' + total + ' · ' + current) : current, undefined, true);

      if (status.done) return status;
      await new Promise(function (resolve) { setTimeout(resolve, 900); });
    }
  }

  async function exportViaServer(button) {
    if (running) return;
    running = true;

    var originalText = button ? button.textContent : '';
    var originalBackground = button ? button.style.background : '';

    try {
      setButton(button, '正在连接导出服务...', undefined, true);
      await waitForServerReady(button);

      var response = await fetch(SERVER + '/api/screenshot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          path: currentHtmlPath(),
          url: window.location.href,
          title: document.title || '',
          viewport: currentViewport()
        })
      });

      var started = await response.json().catch(function () { return {}; });
      if (!response.ok || started.error) {
        throw new Error(started.error || '导出服务启动失败');
      }

      var finalStatus = await pollStatus(button);
      var successCount = finalStatus.success_count || 0;
      var total = finalStatus.total || successCount;
      setButton(button, '已导出 ' + successCount + '/' + total + ' 张 PNG', '#22c55e', false);
      if (window.parent && window.parent !== window) {
        window.parent.postMessage('export-success', '*');
      }

      setTimeout(function () {
        setButton(button, originalText, originalBackground, false);
      }, 2600);
    } catch (error) {
      console.error('[prototype export]', error);
      setButton(button, '导出服务未启动', '#ef4444', false);
      window.alert('导出服务还没启动成功。\\n\\n我已经给项目加了后台守护启动逻辑；如果仍失败，请双击项目根目录的「启动原型导出服务.command」，再点一次导出。');
      if (window.parent && window.parent !== window) {
        window.parent.postMessage('export-error', '*');
      }
      setTimeout(function () {
        setButton(button, originalText, originalBackground, false);
      }, 3200);
    } finally {
      running = false;
    }
  }

  document.addEventListener('click', function (event) {
    var button = isExportButton(event.target);
    if (!button) return;
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    exportViaServer(button);
  }, true);

  window.addEventListener('message', function (event) {
    if (event.data !== 'trigger-export') return;
    event.preventDefault && event.preventDefault();
    event.stopPropagation && event.stopPropagation();
    event.stopImmediatePropagation && event.stopImmediatePropagation();
    exportViaServer(findExportButton());
  }, true);

  window.exportPrototypeViaServer = exportViaServer;
})();
