/* Moneta — loan calculator */
(function () {
  'use strict';
  var M = window.Moneta;
  var form = document.getElementById('loan-form');
  if (!form) return;

  var view = 'year';
  var cur = document.getElementById('currency');
  M.fillCurrencySelect(cur);

  function payment(P, r, n) {
    if (n <= 0) return 0;
    if (r === 0) return P / n;
    return P * r / (1 - Math.pow(1 + r, -n));
  }

  /** Runs the loan month by month. Returns rows + totals. */
  function schedule(P, r, pay, extra, maxMonths) {
    var bal = P, rows = [], totalInterest = 0, m = 0;
    while (bal > 0.005 && m < maxMonths) {
      m++;
      var interest = bal * r;
      var principal = pay + extra - interest;
      if (principal <= 0) return null;            // payment never covers interest
      if (principal > bal) principal = bal;
      bal -= principal;
      totalInterest += interest;
      rows.push({ m: m, interest: interest, principal: principal, balance: bal });
    }
    return { rows: rows, totalInterest: totalInterest, months: m };
  }

  function yearly(rows) {
    var out = [], acc = null;
    rows.forEach(function (row, i) {
      if (i % 12 === 0) { acc = { y: out.length + 1, interest: 0, principal: 0, balance: 0 }; out.push(acc); }
      acc.interest += row.interest;
      acc.principal += row.principal;
      acc.balance = row.balance;
    });
    return out;
  }

  function calculate() {
    M.setCurrency(cur.value);
    var P = M.num('amount');
    var rate = M.num('rate') / 100 / 12;
    var years = M.num('years');
    var extra = M.num('extra');
    var n = Math.round(years * 12);

    var base = payment(P, rate, n);
    var plain = schedule(P, rate, base, 0, 1200);
    var withExtra = schedule(P, rate, base, extra, 1200);

    var warn = document.getElementById('warn');
    if (!plain || !withExtra || P <= 0 || n <= 0) {
      warn.hidden = false;
      warn.textContent = 'Enter a loan amount and a term above zero. If the rate is very high, the monthly payment must at least cover the monthly interest.';
      return;
    }
    warn.hidden = true;

    var totalPaid = base * plain.months;
    document.getElementById('r-payment').textContent = M.money(base, 2);
    document.getElementById('r-interest').textContent = M.money(plain.totalInterest);
    document.getElementById('r-total').textContent = M.money(P + plain.totalInterest);
    document.getElementById('r-term').textContent = M.months(withExtra.months);
    document.getElementById('r-ratio').textContent =
      Math.round(plain.totalInterest / P * 100) + '% of principal';

    var saved = plain.totalInterest - withExtra.totalInterest;
    var savedBox = document.getElementById('saved-box');
    if (extra > 0) {
      savedBox.hidden = false;
      document.getElementById('r-saved').textContent = M.money(saved);
      document.getElementById('r-sooner').textContent = M.months(plain.months - withExtra.months) + ' sooner';
      document.getElementById('r-outlay').textContent = M.money(base + extra, 2);
    } else {
      savedBox.hidden = true;
    }

    /* chart: remaining balance, with and without extra payments */
    var a = plain.rows.map(function (x) { return x.balance; });
    var b = withExtra.rows.map(function (x) { return x.balance; });
    while (b.length < a.length) b.push(0);
    a.unshift(P); b.unshift(P);
    var series = [{ points: a, color: '#8FD9F0', fill: false }];
    if (extra > 0) series.push({ points: b, color: '#7CE0A6', fill: true });
    var yrs = Math.max(1, Math.ceil(plain.months / 12));
    var ticks = Math.min(6, yrs);
    var labels = [];
    for (var i = 0; i <= ticks; i++) labels.push('Yr ' + Math.round(yrs * i / ticks));
    M.lineChart(document.getElementById('chart'), series, labels, function (v) {
      return v >= 1000 ? Math.round(v / 1000) + 'k' : Math.round(v);
    });
    document.getElementById('legend-extra').hidden = extra <= 0;

    /* table */
    var rows = view === 'year' ? yearly(withExtra.rows) : withExtra.rows;
    var body = document.getElementById('sched');
    body.innerHTML = '';
    rows.forEach(function (row) {
      var tr = document.createElement('tr');
      var label = view === 'year' ? 'Year ' + row.y : 'Month ' + row.m;
      [label, M.money(row.principal), M.money(row.interest), M.money(row.balance)]
        .forEach(function (cell) {
          var td = document.createElement('td');
          td.textContent = cell;
          tr.appendChild(td);
        });
      body.appendChild(tr);
    });
  }

  var rateInput = document.getElementById('rate');
  var rateRange = document.getElementById('rate-range');
  if (rateRange) {
    rateRange.addEventListener('input', function () { rateInput.value = rateRange.value; });
    rateInput.addEventListener('input', function () { rateRange.value = rateInput.value; });
  }

  form.addEventListener('input', calculate);
  document.querySelectorAll('[data-view]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      view = btn.dataset.view;
      document.querySelectorAll('[data-view]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
      calculate();
    });
  });
  calculate();
})();
