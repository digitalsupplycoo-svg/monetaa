/* Moneta — resize image */
(function () {
  'use strict';
  var T = window.MonetaTools;
  var root = document.getElementById('resize-root');
  if (!root) return;

  var dropzone = document.getElementById('dropzone');
  var widthInput = document.getElementById('width');
  var heightInput = document.getElementById('height');
  var lockAspect = document.getElementById('lock-aspect');
  var resultPanel = document.getElementById('resize-result');
  var downloadBtn = document.getElementById('download-btn');
  var compare = document.getElementById('compare');
  var imgBefore = document.getElementById('img-before');
  var imgAfter = document.getElementById('img-after');
  var warn = document.getElementById('warn');

  var srcBitmap = null;
  var srcFile = null;
  var aspect = 1;
  var resultCanvas = null;
  var resultMime = 'image/png';

  function setDims(w, h) {
    widthInput.value = w;
    heightInput.value = h;
  }

  function onFile(file) {
    warn.hidden = true;
    srcFile = file;
    resultMime = file.type && file.type.indexOf('png') !== -1 ? 'image/png' : 'image/jpeg';
    T.readAsImageBitmap(file).then(function (bitmap) {
      srcBitmap = bitmap;
      aspect = bitmap.width / bitmap.height;
      setDims(bitmap.width, bitmap.height);
      var dz = document.querySelector('.dz-filename');
      if (dz) dz.textContent = file.name + ' — ' + bitmap.width + '×' + bitmap.height;
      imgBefore.src = URL.createObjectURL(file);
      resultPanel.hidden = false;
      render();
    }).catch(function () {
      warn.hidden = false;
      warn.textContent = 'Could not read that file as an image.';
    });
  }

  function render() {
    if (!srcBitmap) return;
    var w = Math.max(1, Math.round(parseFloat(widthInput.value) || 1));
    var h = Math.max(1, Math.round(parseFloat(heightInput.value) || 1));
    resultCanvas = T.stepDownDraw(srcBitmap, w, h);
    if (w > srcBitmap.width || h > srcBitmap.height) {
      var c = document.createElement('canvas');
      c.width = w;
      c.height = h;
      c.getContext('2d').drawImage(srcBitmap, 0, 0, w, h);
      resultCanvas = c;
    }
    imgAfter.src = resultCanvas.toDataURL(resultMime);
    document.getElementById('r-dims').textContent = w + ' × ' + h + ' px';
  }

  widthInput.addEventListener('input', function () {
    if (lockAspect.checked) {
      heightInput.value = Math.round((parseFloat(widthInput.value) || 0) / aspect);
    }
    render();
  });
  heightInput.addEventListener('input', function () {
    if (lockAspect.checked) {
      widthInput.value = Math.round((parseFloat(heightInput.value) || 0) * aspect);
    }
    render();
  });

  downloadBtn.addEventListener('click', function () {
    if (!resultCanvas) return;
    T.toBlobChecked(resultCanvas, resultMime, 0.92).then(function (result) {
      var ext = resultMime === 'image/png' ? 'png' : 'jpg';
      T.downloadBlob(result.blob, 'resized.' + ext);
    });
  });

  T.initDropzone(dropzone, { accept: 'image/*', onFile: onFile });
})();
