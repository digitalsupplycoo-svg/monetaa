window.MonetaTools = (function () {
  'use strict';

  function initDropzone(el, opts) {
    opts = opts || {};
    var input = el.querySelector('input[type=file]');
    if (!input) {
      input = document.createElement('input');
      input.type = 'file';
      if (opts.accept) input.accept = opts.accept;
      el.appendChild(input);
    }

    function handleFiles(files) {
      if (!files || !files.length) return;
      if (opts.onFile) opts.onFile(files[0]);
    }

    el.addEventListener('click', function () { input.click(); });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); }
    });
    input.addEventListener('change', function () { handleFiles(input.files); });

    ['dragenter', 'dragover'].forEach(function (evt) {
      el.addEventListener(evt, function (e) {
        e.preventDefault();
        e.stopPropagation();
        el.classList.add('drag-over');
      });
    });
    ['dragleave', 'drop'].forEach(function (evt) {
      el.addEventListener(evt, function (e) {
        e.preventDefault();
        e.stopPropagation();
        el.classList.remove('drag-over');
      });
    });
    el.addEventListener('drop', function (e) {
      handleFiles(e.dataTransfer && e.dataTransfer.files);
    });
  }

  function readAsImageBitmap(file) {
    if (window.createImageBitmap) {
      return createImageBitmap(file, { imageOrientation: 'from-image' }).catch(function () {
        return createImageBitmap(file);
      });
    }
    return new Promise(function (resolve, reject) {
      var img = new Image();
      var url = URL.createObjectURL(file);
      img.onload = function () { URL.revokeObjectURL(url); resolve(img); };
      img.onerror = function (e) { URL.revokeObjectURL(url); reject(e); };
      img.src = url;
    });
  }

  function toBlobChecked(canvas, mime, quality) {
    return new Promise(function (resolve, reject) {
      canvas.toBlob(function (blob) {
        if (!blob) { reject(new Error('toBlob failed')); return; }
        resolve({ blob: blob, actualMime: blob.type, requestedMime: mime, fellBack: blob.type !== mime });
      }, mime, quality);
    });
  }

  function stepDownDraw(bitmap, targetW, targetH) {
    var srcW = bitmap.width, srcH = bitmap.height;
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    var curW = srcW, curH = srcH, curSrc = bitmap;

    while (curW / 2 > targetW && curH / 2 > targetH) {
      var stepW = Math.max(targetW, Math.floor(curW / 2));
      var stepH = Math.max(targetH, Math.floor(curH / 2));
      var stepCanvas = document.createElement('canvas');
      stepCanvas.width = stepW;
      stepCanvas.height = stepH;
      stepCanvas.getContext('2d').drawImage(curSrc, 0, 0, stepW, stepH);
      curSrc = stepCanvas;
      curW = stepW;
      curH = stepH;
    }

    canvas.width = targetW;
    canvas.height = targetH;
    ctx.drawImage(curSrc, 0, 0, targetW, targetH);
    return canvas;
  }

  function compressToTarget(canvas, targetBytes, mime) {
    var min = 0.05, max = 0.98, best = null;
    var deadline = Date.now() + 8000; // hard time budget so slow devices degrade gracefully

    function attempt(q, depth) {
      return toBlobChecked(canvas, mime, q).then(function (result) {
        if (!best || Math.abs(result.blob.size - targetBytes) < Math.abs(best.blob.size - targetBytes)) {
          best = result;
        }
        if (depth >= 5 || Date.now() > deadline) return best;
        if (result.blob.size > targetBytes) {
          max = q;
        } else {
          min = q;
        }
        return attempt((min + max) / 2, depth + 1);
      });
    }

    return attempt((min + max) / 2, 0);
  }

  function downloadBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function formatBytes(n) {
    if (n < 1024) return n + ' B';
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB';
    return (n / (1024 * 1024)).toFixed(2) + ' MB';
  }

  function showProgress(el, pct, label) {
    el.hidden = false;
    var fill = el.querySelector('.fill');
    var lbl = el.querySelector('.label');
    if (fill) fill.style.width = Math.max(0, Math.min(100, pct)) + '%';
    if (lbl && label) lbl.textContent = label;
  }

  function hideProgress(el) {
    el.hidden = true;
  }

  return {
    initDropzone: initDropzone,
    readAsImageBitmap: readAsImageBitmap,
    toBlobChecked: toBlobChecked,
    stepDownDraw: stepDownDraw,
    compressToTarget: compressToTarget,
    downloadBlob: downloadBlob,
    formatBytes: formatBytes,
    showProgress: showProgress,
    hideProgress: hideProgress
  };
})();
