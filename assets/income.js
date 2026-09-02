/* Moneta — income, budget and savings calculator */
(function () {
  'use strict';
  var M = window.Moneta;
  var form = document.getElementById('income-form');
  if (!form) return;

  var cur = document.getElementById('currency');
  M.fillCurrencySelect(cur);

  function annualise(amount, period, hours, weeks) {
    switch (period) {
      case 'hour': return amount * hours * weeks;
      case 'day': return amount * 5 * weeks;
      case 'week': return amount * weeks;
      case 'month': return amount * 12;
      default: return amount;
    }
  }

  function calculate() {
    M.setCurrency(cur.value);
    var amount = M.num('amount');
    var period = document.getElementById('period').value;
    var hours = M.num('hours') || 40;
    var weeks = M.num('weeks') || 52;
    var deduct = Math.min(90, Math.max(0, M.num('deductions'))) / 100;
    var other = M.num('other');

    var gross = annualise(amount, period, hours, weeks) + other * 12;
    var net = gross * (1 - deduct);
    var monthly = net / 12;

    document.getElementById('r-monthly').textContent = M.money(monthly);
    document.getElementById('r-gross').textContent = M.money(gross);
    document.getElementById('r-net').textContent = M.money(net);
    document.getElementById('r-weekly').textContent = M.money(net / weeks);
    document.getElementById('r-hourly').textContent = M.money(net / (hours * weeks), 2);
    document.getElementById('r-tax').textContent = M.money(gross - net);

    /* budget split — user-adjustable, defaults to 50/30/20 */
    var needs = M.num('needs'), wants = M.num('wants');
    var save = Math.max(0, 100 - needs - wants);
    document.getElementById('needs-out').textContent = needs + '%';
    document.getElementById('wants-out').textContent = wants + '%';
    document.getElementById('save-out').textContent = save + '%';
    document.getElementById('b-needs').textContent = M.money(monthly * needs / 100);
    document.getElementById('b-wants').textContent = M.money(monthly * wants / 100);
    document.getElementById('b-save').textContent = M.money(monthly * save / 100);

    M.donut(document.getElementById('donut'), [
      { value: needs, color: '#8FD9F0' },
      { value: wants, color: '#E9C25C' },
      { value: save, color: '#7CE0A6' }
    ]);
    document.getElementById('donut-center').textContent = M.money(monthly * save / 100);

    /* savings goal + growth */
    var contribution = monthly * save / 100;
    var goal = M.num('goal');
    var apr = M.num('return') / 100 / 12;
    var bal = 0, m = 0, points = [0];
    while (m < 600) {
      m++;
      bal = bal * (1 + apr) + contribution;
      if (m % 3 === 0 || m === 1) points.push(bal);
      if (goal > 0 && bal >= goal) break;
    }
    var goalEl = document.getElementById('r-goal');
    if (goal <= 0 || contribution <= 0) {
      goalEl.textContent = '\u2014';
      document.getElementById('goal-note').textContent =
        contribution <= 0 ? 'Set a savings share above zero to see a target date.' : 'Enter a savings goal.';
    } else if (m >= 600) {
      goalEl.textContent = '50+ yrs';
      document.getElementById('goal-note').textContent = 'At this rate the goal is more than 50 years away.';
    } else {
      goalEl.textContent = M.months(m);
      document.getElementById('goal-note').textContent =
        'Saving ' + M.money(contribution) + ' a month at ' + M.num('return') + '% a year.';
    }

    /* 10-year growth curve of the savings share */
    var grow = [], v = 0;
    for (var i = 0; i <= 120; i++) { grow.push(v); v = v * (1 + apr) + contribution; }
    var flat = [];
    for (var j = 0; j <= 120; j++) flat.push(contribution * j);
    M.lineChart(document.getElementById('chart'), [
      { points: flat, color: '#8FD9F0', fill: false, width: 2 },
      { points: grow, color: '#7CE0A6', fill: true }
    ], ['Now', 'Yr 2', 'Yr 4', 'Yr 6', 'Yr 8', 'Yr 10'], function (x) {
      return x >= 1000 ? Math.round(x / 1000) + 'k' : Math.round(x);
    });
  }

  form.addEventListener('input', calculate);
  calculate();
})();
