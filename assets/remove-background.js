/* Moneta — remove background */
(function () {
  'use strict';
  var T = window.MonetaTools;
  var root = document.getElementById('bgremove-root');
  if (!root) return;

  var dropzone = document.getElementById('dropzone');
  var progress = document.getElementById('progress');
  var resultPanel = document.getElementById('bgremove-result');
  var downloadBtn = document.getElementById('download-btn');
  var imgBefore = document.getElementById('img-before');
  var imgAfter = document.getElementById('img-after');
  var warn = document.getElementById('warn');

  var resultBlob = null;
  var removeBackground = null;

  function loadLibrary() {
    if (removeBackground) return Promise.resolve(removeBackground);
    T.showProgress(progress, 5, 'Loading background removal model…');
    return import('https://esm.sh/@imgly/background-removal@1.5.5').then(function (mod) {
      removeBackground = mod.removeBackground;
      return removeBackground;
    });
  }

  var fileToken = 0;

  function onFile(file) {
    var token = ++fileToken;
    warn.hidden = true;
    resultPanel.hidden = true;
    imgBefore.src = URL.createObjectURL(file);
    var dz = document.querySelector('.dz-filename');
    if (dz) dz.textContent = file.name;

    loadLibrary().then(function (removeBg) {
      if (token !== fileToken) return Promise.reject({ superseded: true });
      T.showProgress(progress, 20, 'Removing background…');
      return removeBg(file, {
        progress: function (key, current, total) {
          if (token !== fileToken) return;
          var pct = total ? Math.round((current / total) * 80) + 20 : 50;
          T.showProgress(progress, pct, 'Removing background…');
        }
      });
    }).then(function (blob) {
      if (token !== fileToken) return; // a newer file supersedes this result
      resultBlob = blob;
      T.hideProgress(progress);
      imgAfter.src = URL.createObjectURL(blob);
      document.getElementById('r-size').textContent = T.formatBytes(blob.size);
      resultPanel.hidden = false;
    }).catch(function (err) {
      if (err && err.superseded) return;
      T.hideProgress(progress);
      warn.hidden = false;
      warn.textContent = 'Background removal failed in this browser (' +
        (err && err.message ? err.message : 'unknown error') +
        '). Try a smaller image or a different browser.';
    });
  }

  downloadBtn.addEventListener('click', function () {
    if (!resultBlob) return;
    T.downloadBlob(resultBlob, 'no-background.png');
  });

  T.initDropzone(dropzone, { accept: 'image/*', onFile: onFile });
})();
