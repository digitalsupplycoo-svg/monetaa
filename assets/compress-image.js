/* Moneta — compress image */
(function () {
  'use strict';
  var T = window.MonetaTools;
  var root = document.getElementById('compress-root');
  if (!root) return;

  var dropzone = document.getElementById('dropzone');
  var formatSelect = document.getElementById('format');
  var qualitySlider = document.getElementById('quality');
  var targetInput = document.getElementById('target-kb');
  var modeButtons = document.querySelectorAll('[data-mode]');
  var resultPanel = document.getElementById('compress-result');
  var downloadBtn = document.getElementById('download-btn');
  var imgBefore = document.getElementById('img-before');
  var imgAfter = document.getElementById('img-after');
  var warn = document.getElementById('warn');

  var srcBitmap = null;
  var srcFile = null;
  var srcCanvas = null;
  var mode = 'quality';
  var resultBlob = null;

  function mimeFor(format) {
    if (format === 'png') return 'image/png';
    if (format === 'webp') return 'image/webp';
    return 'image/jpeg';
  }

  function onFile(file) {
    warn.hidden = true;
    srcFile = file;
    T.readAsImageBitmap(file).then(function (bitmap) {
      srcBitmap = bitmap;
      srcCanvas = document.createElement('canvas');
      srcCanvas.width = bitmap.width;
      srcCanvas.height = bitmap.height;
      srcCanvas.getContext('2d').drawImage(bitmap, 0, 0);
      var dz = document.querySelector('.dz-filename');
      if (dz) dz.textContent = file.name + ' — ' + T.formatBytes(file.size);
      imgBefore.src = URL.createObjectURL(file);
      document.getElementById('r-before').textContent = T.formatBytes(file.size);
      resultPanel.hidden = false;
      updateFormatControls();
      render();
    }).catch(function () {
      warn.hidden = false;
      warn.textContent = 'Could not read that file as an image.';
    });
  }

  function updateFormatControls() {
    var isPng = formatSelect.value === 'png';
    qualitySlider.disabled = isPng;
    if (isPng) {
      var note = document.getElementById('png-note');
      if (note) note.hidden = false;
    } else {
      var note2 = document.getElementById('png-note');
      if (note2) note2.hidden = true;
    }
  }

  var renderToken = 0;

  function render() {
    if (!srcCanvas) return;
    var token = ++renderToken;
    var mime = mimeFor(formatSelect.value);
    var isTarget = mode === 'target' && mime !== 'image/png';
    var promise;
    if (isTarget) {
      downloadBtn.disabled = true;
      document.getElementById('r-after').textContent = 'Compressing…';
      var targetBytes = (parseFloat(targetInput.value) || 200) * 1024;
      promise = T.compressToTarget(srcCanvas, targetBytes, mime);
    } else {
      var q = mime === 'image/png' ? undefined : (parseFloat(qualitySlider.value) || 80) / 100;
      promise = T.toBlobChecked(srcCanvas, mime, q);
    }
    promise.then(function (result) {
      if (token !== renderToken) return; // a newer render() superseded this one
      downloadBtn.disabled = false;
      resultBlob = result.blob;
      if (result.fellBack) {
        warn.hidden = false;
        warn.textContent = 'This browser could not encode ' + formatSelect.value.toUpperCase() +
          ' — saved as PNG instead.';
      } else {
        warn.hidden = true;
      }
      imgAfter.src = URL.createObjectURL(result.blob);
      document.getElementById('r-after').textContent = T.formatBytes(result.blob.size);
      var pct = srcFile ? Math.round((1 - result.blob.size / srcFile.size) * 100) : 0;
      document.getElementById('r-saved').textContent = (pct >= 0 ? pct : 0) + '% smaller';
    });
  }

  var debounceTimer = null;
  function renderDebounced() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(render, 400);
  }

  formatSelect.addEventListener('change', function () { updateFormatControls(); render(); });
  qualitySlider.addEventListener('input', render);
  targetInput.addEventListener('input', renderDebounced);
  modeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      mode = btn.dataset.mode;
      modeButtons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      document.getElementById('quality-field').hidden = mode !== 'quality';
      document.getElementById('target-field').hidden = mode !== 'target';
      render();
    });
  });

  downloadBtn.addEventListener('click', function () {
    if (!resultBlob) return;
    var ext = resultBlob.type === 'image/png' ? 'png' : resultBlob.type === 'image/webp' ? 'webp' : 'jpg';
    T.downloadBlob(resultBlob, 'compressed.' + ext);
  });

  T.initDropzone(dropzone, { accept: 'image/*', onFile: onFile });
})();
