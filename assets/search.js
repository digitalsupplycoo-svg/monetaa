(function () {
  var trigger = document.querySelector('[data-search-trigger]');
  var overlay = document.querySelector('[data-search-overlay]');
  var input = document.querySelector('[data-search-input]');
  var results = document.querySelector('[data-search-results]');
  if (!trigger || !overlay || !input || !results) return;

  var indexData = null;

  function loadIndex() {
    if (indexData) return Promise.resolve(indexData);
    return fetch('/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (d) { indexData = d; return d; })
      .catch(function () { indexData = []; return []; });
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function render(matches) {
    if (!matches.length) {
      results.innerHTML = '<p class="search-empty">No matches.</p>';
      return;
    }
    results.innerHTML = matches.map(function (m) {
      return '<a href="' + m.url + '"><strong>' + escapeHtml(m.title) + '</strong>' +
        '<span>' + escapeHtml(m.desc) + '</span></a>';
    }).join('');
  }

  function search(q) {
    q = q.trim().toLowerCase();
    if (!indexData || q.length < 2) { results.innerHTML = ''; return; }
    var matches = indexData.filter(function (item) {
      return item.title.toLowerCase().indexOf(q) !== -1 ||
        (item.desc || '').toLowerCase().indexOf(q) !== -1;
    }).slice(0, 8);
    render(matches);
  }

  function open() {
    overlay.classList.add('open');
    input.value = '';
    results.innerHTML = '';
    loadIndex().then(function () { input.focus(); });
  }

  function close() {
    overlay.classList.remove('open');
  }

  trigger.addEventListener('click', open);
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('open')) close();
  });
  input.addEventListener('input', function () { search(input.value); });
})();
