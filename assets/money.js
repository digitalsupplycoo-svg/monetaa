/* Moneta — shared money helpers. No dependencies. */
window.Moneta = (function () {
  'use strict';

  var CURRENCIES = [
    ['USD', '$', 'US dollar'], ['EUR', '\u20ac', 'Euro'], ['GBP', '\u00a3', 'British pound'],
    ['AED', 'AED', 'UAE dirham'], ['SAR', 'SAR', 'Saudi riyal'], ['JPY', '\u00a5', 'Japanese yen'],
    ['INR', '\u20b9', 'Indian rupee'], ['CAD', 'CA$', 'Canadian dollar'], ['AUD', 'A$', 'Australian dollar'],
    ['CHF', 'CHF', 'Swiss franc'], ['TRY', '\u20ba', 'Turkish lira'], ['EGP', 'EGP', 'Egyptian pound'],
    ['ZAR', 'R', 'South African rand'], ['NGN', '\u20a6', 'Nigerian naira'], ['BRL', 'R$', 'Brazilian real'],
    ['PKR', 'Rs', 'Pakistani rupee'], ['PHP', '\u20b1', 'Philippine peso'], ['SEK', 'kr', 'Swedish krona']
  ];

  var state = { code: 'USD', symbol: '$' };

  function fillCurrencySelect(sel) {
    CURRENCIES.forEach(function (c) {
      var o = document.createElement('option');
      o.value = c[0];
      o.textContent = c[0] + ' \u2014 ' + c[2];
      sel.appendChild(o);
    });
    sel.value = state.code;
  }

  function setCurrency(code) {
    for (var i = 0; i < CURRENCIES.length; i++) {
      if (CURRENCIES[i][0] === code) { state.code = code; state.symbol = CURRENCIES[i][1]; return; }
    }
  }

  function money(n, decimals) {
    if (!isFinite(n)) n = 0;
    var d = decimals === undefined ? 0 : decimals;
    return state.symbol + ' ' + n.toLocaleString('en-US', {
      minimumFractionDigits: d, maximumFractionDigits: d
    });
  }

  function num(id) {
    var el = document.getElementById(id);
    var v = parseFloat(String(el.value).replace(/,/g, ''));
    return isFinite(v) ? v : 0;
  }

  function months(m) {
    var y = Math.floor(m / 12), r = Math.round(m % 12);
    if (y && r) return y + ' yr ' + r + ' mo';
    if (y) return y + (y === 1 ? ' year' : ' years');
    return r + ' mo';
  }

  /* --- tiny SVG chart builders ------------------------------------------ */
  function el(name, attrs, text) {
    var n = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (text !== undefined) n.textContent = text;
    return n;
  }

  /** series: [{points:[y...], color, fill}] over an x index 0..len-1 */
  function lineChart(svg, series, labels, formatter) {
    var W = 640, H = 280, L = 58, R = 12, T = 14, B = 30;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('role', 'img');
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var max = 0, len = 0;
    series.forEach(function (s) {
      len = Math.max(len, s.points.length);
      s.points.forEach(function (v) { max = Math.max(max, v); });
    });
    if (max <= 0) max = 1;
    var nice = Math.pow(10, Math.floor(Math.log(max) / Math.LN10)) || 1;
    var top = Math.ceil(max / nice) * nice;
    function X(i) { return L + (W - L - R) * (len < 2 ? 0 : i / (len - 1)); }
    function Y(v) { return T + (H - T - B) * (1 - v / top); }
    for (var g = 0; g <= 4; g++) {
      var yv = top * g / 4;
      svg.appendChild(el('line', { x1: L, x2: W - R, y1: Y(yv), y2: Y(yv), stroke: '#D7E2EA', 'stroke-opacity': .12 }));
      svg.appendChild(el('text', {
        x: L - 8, y: Y(yv) + 4, 'text-anchor': 'end', fill: '#D7E2EA',
        'fill-opacity': .5, 'font-size': 11, 'font-family': 'inherit'
      }, formatter ? formatter(yv) : Math.round(yv).toLocaleString('en-US')));
    }
    series.forEach(function (s) {
      var d = s.points.map(function (v, i) { return (i ? 'L' : 'M') + X(i).toFixed(1) + ' ' + Y(v).toFixed(1); }).join(' ');
      if (s.fill) {
        svg.appendChild(el('path', {
          d: d + ' L' + X(s.points.length - 1) + ' ' + Y(0) + ' L' + X(0) + ' ' + Y(0) + ' Z',
          fill: s.color, 'fill-opacity': .14
        }));
      }
      svg.appendChild(el('path', { d: d, fill: 'none', stroke: s.color, 'stroke-width': s.width || 2.5, 'stroke-linejoin': 'round' }));
    });
    (labels || []).forEach(function (lb, i) {
      var idx = Math.round((len - 1) * i / Math.max(1, labels.length - 1));
      svg.appendChild(el('text', {
        x: X(idx), y: H - 8, 'text-anchor': i === 0 ? 'start' : (i === labels.length - 1 ? 'end' : 'middle'),
        fill: '#D7E2EA', 'fill-opacity': .5, 'font-size': 11, 'font-family': 'inherit'
      }, lb));
    });
  }

  /** slices: [{value, color, label}] */
  function donut(svg, slices) {
    var S = 260, c = S / 2, r = 96, w = 34;
    svg.setAttribute('viewBox', '0 0 ' + S + ' ' + S);
    svg.setAttribute('role', 'img');
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var total = slices.reduce(function (a, s) { return a + Math.max(0, s.value); }, 0) || 1;
    var a0 = -Math.PI / 2;
    slices.forEach(function (s) {
      var frac = Math.max(0, s.value) / total;
      if (frac <= 0) return;
      var a1 = a0 + frac * Math.PI * 2;
      var large = frac > .5 ? 1 : 0;
      var p = [
        'M', c + r * Math.cos(a0), c + r * Math.sin(a0),
        'A', r, r, 0, large, 1, c + r * Math.cos(a1), c + r * Math.sin(a1)
      ].join(' ');
      svg.appendChild(el('path', {
        d: p, fill: 'none', stroke: s.color, 'stroke-width': w,
        'stroke-linecap': frac < .999 ? 'butt' : 'round'
      }));
      a0 = a1;
    });
    return svg;
  }

  return {
    CURRENCIES: CURRENCIES, fillCurrencySelect: fillCurrencySelect, setCurrency: setCurrency,
    money: money, num: num, months: months, lineChart: lineChart, donut: donut,
    get symbol() { return state.symbol; }
  };
})();
