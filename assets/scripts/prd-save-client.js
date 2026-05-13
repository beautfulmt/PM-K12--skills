(function () {
  var SERVER = window.PRD_SAVE_SERVER || window.PROTOTYPE_EXPORT_SERVER || 'http://localhost:8765';
  var LAUNCHER = window.PRD_SAVE_LAUNCHER || window.PROTOTYPE_EXPORT_LAUNCHER || 'http://localhost:8766';
  var running = false;

  function findSaveButton() {
    return document.getElementById('saveBtn')
      || document.getElementById('downloadBtn')
      || document.querySelector('.save-btn');
  }

  function findStatusNode() {
    return document.getElementById('saveStatus');
  }

  function setButton(button, text, disabled) {
    if (!button) return;
    button.textContent = text;
    button.disabled = !!disabled;
    button.style.opacity = disabled ? '0.75' : '';
    button.style.pointerEvents = disabled ? 'none' : '';
  }

  function showStatus(message, isError) {
    var status = findStatusNode();
    if (!status) return;
    status.textContent = message;
    status.classList.toggle('error', !!isError);
    status.classList.add('show');
    clearTimeout(showStatus.timer);
    showStatus.timer = setTimeout(function () {
      status.classList.remove('show');
    }, 3200);
  }

  function sleep(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  function currentHtmlPath() {
    return decodeURIComponent(window.location.pathname || '');
  }

  async function waitForServer(timeoutMs) {
    var deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        var response = await fetch(SERVER + '/api/status?ts=' + Date.now(), { cache: 'no-store' });
        if (response.ok) return true;
      } catch (e) {}
      await sleep(700);
    }
    return false;
  }

  async function launchServer() {
    try {
      await fetch(LAUNCHER + '/api/launch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{}'
      });
    } catch (e) {}
  }

  function markChanged(cell) {
    cell.dataset.changed = 'true';
    cell.classList.add('edited-cell');
  }

  function bindEditableTracking() {
    document.querySelectorAll('[contenteditable="true"]').forEach(function (cell) {
      if (!cell.dataset.original) cell.dataset.original = cell.innerHTML;
      if (cell.dataset.prdSaveBound === 'true') return;
      cell.dataset.prdSaveBound = 'true';
      cell.addEventListener('blur', function () {
        if (cell.innerHTML !== cell.dataset.original) {
          markChanged(cell);
        }
      });
    });
  }

  function clearEditedState(root) {
    (root || document).querySelectorAll('.edited-cell, [data-changed="true"]').forEach(function (cell) {
      cell.dataset.original = cell.innerHTML;
      cell.classList.remove('edited-cell');
      delete cell.dataset.changed;
    });
  }

  function buildSavedHtml() {
    var clone = document.documentElement.cloneNode(true);
    var saveBtn = clone.querySelector('#saveBtn, #downloadBtn, .save-btn');
    var saveStatus = clone.querySelector('#saveStatus');

    if (saveBtn) {
      saveBtn.disabled = false;
      saveBtn.textContent = '💾 保存并通知AI';
      saveBtn.style.opacity = '';
      saveBtn.style.pointerEvents = '';
    }

    if (saveStatus) {
      saveStatus.textContent = '';
      saveStatus.classList.remove('show', 'error');
    }

    clone.querySelectorAll('[data-prd-save-bound]').forEach(function (node) {
      delete node.dataset.prdSaveBound;
    });
    clearEditedState(clone);

    return '<!DOCTYPE html>\n' + clone.outerHTML;
  }

  async function saveViaLocalServer(html) {
    var ready = await waitForServer(1200);
    if (!ready) {
      showStatus('正在启动本地保存服务...');
      await launchServer();
      ready = await waitForServer(15000);
    }

    if (!ready) {
      throw new Error('本地保存服务未启动，请双击项目根目录的「启动原型导出服务.command」后再保存。');
    }

    var response = await fetch(SERVER + '/api/save-html', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        path: currentHtmlPath(),
        url: window.location.href,
        content: html
      })
    });
    var data = await response.json().catch(function () { return {}; });
    if (!response.ok || data.error) {
      throw new Error(data.error || '本地保存服务写入失败');
    }
    return data;
  }

  function downloadFallback(html, message) {
    var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    var name = decodeURIComponent((window.location.pathname || '').split('/').pop() || 'PRD.html');
    link.href = url;
    link.download = name;
    link.click();
    URL.revokeObjectURL(url);
    showStatus((message || '无法直接写回本地文件') + ' 已下载一份 HTML 兜底。', true);
  }

  async function savePrdDocument() {
    if (running) return;
    running = true;

    var button = findSaveButton();
    var html = buildSavedHtml();
    setButton(button, '⏳ 保存中...', true);

    try {
      await saveViaLocalServer(html);
      clearEditedState(document);
      setButton(button, '✅ 已写回文件', false);
      showStatus('已写回本地 PRD 文件，可以让 AI 根据改动同步原型/流程图。');
    } catch (error) {
      console.error('[prd save]', error);
      setButton(button, '⬇️ 已下载', false);
      downloadFallback(html, error && error.message);
    } finally {
      setTimeout(function () {
        setButton(button, '💾 保存并通知AI', false);
      }, 1800);
      running = false;
    }
  }

  document.addEventListener('click', function (event) {
    var button = event.target && event.target.closest && event.target.closest('#saveBtn, #downloadBtn, .save-btn');
    if (!button) return;
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    savePrdDocument();
  }, true);

  bindEditableTracking();
  window.savePrdDocument = savePrdDocument;
})();
