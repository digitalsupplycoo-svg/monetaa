#!/usr/bin/env python3
"""Builds the Moneta static site. Run: python3 build.py"""
import os, re, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://moneta.tools"          # <- replace with your real domain
BRAND = "Moneta"
TODAY = "2026-09-02"

NAV = [("/loan-calculator", "Loans"), ("/income-calculator", "Income"),
       ("/guides/", "Guides"), ("/about", "About")]

FOOT = {
    "Calculators": [("/loan-calculator", "Loan repayment"),
                    ("/loan-calculator#schedule", "Amortisation table"),
                    ("/income-calculator", "Income and budget"),
                    ("/income-calculator#goal", "Savings goal")],
    "Guides": [("/guides/", "All guides"),
               ("/guides/emergency-fund", "Emergency fund"),
               ("/guides/budget-50-30-20", "The 50/30/20 budget"),
               ("/guides/pay-off-debt-faster", "Paying off debt"),
               ("/guides/compound-interest", "Compound interest")],
    "Site": [("/about", "About"), ("/contact", "Contact"),
             ("/privacy", "Privacy policy"), ("/terms", "Terms of use"),
             ("/disclaimer", "Editorial disclaimer")],
}

ADSENSE_CLIENT = "ca-pub-0000000000000000"   # <- replace after AdSense approval


def head(title, desc, path, image="/img/og.png"):
    canon = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#0C0C0C">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}{image}">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/base.css">
<!-- AdSense: uncomment after your account is approved and the publisher ID is filled in.
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
-->
</head>
<body>
<a class="sr" href="#main">Skip to content</a>
"""


def nav(active=""):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=page" if h == active else ""}>{t}</a></li>' for h, t in NAV
    )
    return f"""<nav class="nav reveal" style="--ry:-20px">
<a class="brand" href="/">{BRAND}</a>
<ul>{links}</ul>
</nav>"""


def ad(slot, label="Advertisement"):
    return f"""<aside class="ad-slot" aria-label="{label}">
<!-- <ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}"
     data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script> -->
</aside>"""


def footer(extra_js=""):
    cols = ""
    for title, links in FOOT.items():
        items = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
        cols += f"<div><h4>{title}</h4><ul>{items}</ul></div>"
    js = "".join(f'<script src="{s}" defer></script>' for s in extra_js) if extra_js else ""
    return f"""<footer class="footer">
<div>
  <span class="brand">{BRAND}</span>
  <p class="small">Free loan and income calculators and plain-English guides to keeping more of
  what you earn. Everything runs in your browser: no sign-up, no data leaves your device.</p>
</div>
{cols}
<div class="copyright">&copy; <span data-year>2026</span> {BRAND}. Educational information only,
not financial advice. See our <a href="/disclaimer">editorial disclaimer</a>.</div>
</footer>
<script src="/assets/site.js" defer></script>{js}
</body>
</html>"""


def write(path, html):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)


# ===================================================================== index
CURRENCY_TILES = [f"/img/cur-{i:02d}.svg" for i in range(21)]

TOOLS = [
    ("01", "Loan repayment", "/loan-calculator",
     "Enter the amount, the rate and the term, and see the monthly payment, the total interest and how much an extra payment each month would save you."),
    ("02", "Amortisation schedule", "/loan-calculator#schedule",
     "A year-by-year or month-by-month breakdown of where each payment goes, so you can see the point at which you start paying off the loan instead of the interest."),
    ("03", "Income breakdown", "/income-calculator",
     "Convert an hourly, weekly, monthly or annual figure into every other one, after deductions, so you can compare offers on the same terms."),
    ("04", "Budget split", "/income-calculator#budget",
     "Split your take-home pay into needs, wants and savings, and adjust the shares until the numbers match the life you actually live."),
    ("05", "Savings goal", "/income-calculator#goal",
     "See how long a target takes to reach at your current savings rate, and what compounding adds on top over ten years."),
]

GUIDE_CARDS = [
    ("01", "Saving", "Build an emergency fund that actually holds", "/guides/emergency-fund",
     ["/img/g1a.svg", "/img/g1b.svg", "/img/g1c.svg"]),
    ("02", "Budgeting", "The 50/30/20 rule, and when to break it", "/guides/budget-50-30-20",
     ["/img/g2a.svg", "/img/g2b.svg", "/img/g2c.svg"]),
    ("03", "Debt", "Pay off debt faster without earning more", "/guides/pay-off-debt-faster",
     ["/img/g3a.svg", "/img/g3b.svg", "/img/g3c.svg"]),
]

ABOUT_TEXT = ("Money advice usually arrives as either a sales pitch or a lecture. This is neither. "
              "Moneta is a small set of calculators that show the arithmetic behind loans, pay and "
              "savings, plus guides that explain what the numbers mean once you have them. "
              "Nothing is hidden behind an account, and nothing you type is sent anywhere.")


def build_index():
    rows = [CURRENCY_TILES[:11], CURRENCY_TILES[11:]]
    marquee = ""
    for r in rows:
        imgs = "".join(
            f'<img src="{s}" alt="" loading="lazy" width="420" height="270" aria-hidden="true">'
            for s in r * 3
        )
        marquee += f'<div class="marquee-row">{imgs}</div>'

    tools = "".join(
        f'<a class="tool reveal" style="--d:{i*0.08}s" href="{href}">'
        f'<span class="num">{n}</span><span><h3>{name}</h3><p>{desc}</p></span></a>'
        for i, (n, name, href, desc) in enumerate(TOOLS)
    )

    cards = ""
    for i, (n, cat, name, href, imgs) in enumerate(GUIDE_CARDS):
        cards += f"""<div class="stack-item">
  <article class="card">
    <div class="card-top">
      <span class="num hero-heading">{n}</span>
      <div class="card-meta"><p class="eyebrow">{cat}</p><h3>{name}</h3></div>
      <a class="btn btn-ghost" href="{href}">Read guide</a>
    </div>
    <div class="card-grid">
      <div class="card-col-1"><img src="{imgs[0]}" alt="" loading="lazy"><img src="{imgs[1]}" alt="" loading="lazy"></div>
      <div class="card-col-2"><img src="{imgs[2]}" alt="" loading="lazy"></div>
    </div>
  </article>
</div>"""

    ld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebSite","name":"{BRAND}","url":"{SITE}",
"description":"Free loan and income calculators and plain-English money guides.",
"publisher":{{"@type":"Organization","name":"{BRAND}","url":"{SITE}",
"logo":{{"@type":"ImageObject","url":"{SITE}/img/favicon.svg"}}}}}}
</script>"""

    body = f"""<main id="main">
<section class="hero">
  {nav()}
  <div class="hero-mid">
    <div class="hero-title-clip">
      <h1 class="display hero-heading reveal" style="--d:.15s;--ry:40px">B7bk Ya Marwa🫀</h1>
    </div>
    <img class="hero-art magnet reveal" style="--d:.6s" data-magnet data-magnet-pad="150"
         data-magnet-strength="3" src="/img/hero-orb.svg" alt="" aria-hidden="true">
    <div class="hero-bottom">
      <p class="hero-lede reveal" style="--d:.35s;--ry:20px">free calculators and plain-english guides for loans, pay and saving</p>
      <a class="btn btn-primary reveal" style="--d:.5s;--ry:20px" href="/loan-calculator">Open a calculator</a>
    </div>
  </div>
</section>

<section class="marquee" data-marquee aria-hidden="true">{marquee}</section>

<section class="about" id="about">
  <img class="decor tl reveal" style="--d:.1s;--rx:-80px;--ry:0" src="/img/decor-stack.svg" alt="" aria-hidden="true">
  <img class="decor tr reveal" style="--d:.15s;--rx:80px;--ry:0" src="/img/decor-chart.svg" alt="" aria-hidden="true">
  <img class="decor bl reveal" style="--d:.25s;--rx:-80px;--ry:0" src="/img/decor-piggy.svg" alt="" aria-hidden="true">
  <img class="decor br reveal" style="--d:.3s;--rx:80px;--ry:0" src="/img/decor-vault.svg" alt="" aria-hidden="true">
  <h2 class="display section-title hero-heading reveal">what this is</h2>
  <p class="lead" data-chars>{ABOUT_TEXT}</p>
  <a class="btn btn-primary reveal" href="/guides/">Read the guides</a>
</section>

{ad("1111111111")}

<section class="light" id="tools">
  <h2 class="display section-title">Calculators</h2>
  <div class="tools">{tools}</div>
</section>

<section class="guides" data-stack>
  <h2 class="display section-title hero-heading">Guides</h2>
  {cards}
</section>

{ad("2222222222")}
</main>
{ld}"""
    write("index.html", head(
        "Moneta \u2014 loan and income calculators, plain-English money guides",
        "Free loan repayment and income calculators with amortisation tables, budget splits and savings goals, plus guides on emergency funds, budgeting and paying off debt.",
        "/") + body + footer())


# ============================================================ loan calculator
def build_loan():
    body = f"""{nav("/loan-calculator")}
<main id="main">
<header class="page-head">
  <h1 class="display hero-heading reveal">Loan calculator</h1>
  <p class="reveal" style="--d:.1s">Work out the monthly payment on any fixed-rate loan, see the
  full interest bill before you sign, and check what one extra payment a month would do to the
  term. Everything is calculated in your browser.</p>
</header>

<div class="calc wrap">
  <form class="panel" id="loan-form" autocomplete="off">
    <h2>Loan details</h2>
    <div class="field">
      <label for="currency">Currency</label>
      <div class="control"><select id="currency"></select></div>
    </div>
    <div class="field">
      <label for="amount">Amount borrowed</label>
      <div class="control"><span class="unit">Total</span><input id="amount" type="number" min="0" step="100" value="250000" inputmode="decimal"></div>
    </div>
    <div class="field">
      <label for="rate">Annual interest rate</label>
      <div class="control"><span class="unit">%</span><input id="rate" type="number" min="0" max="60" step="0.05" value="5.5" inputmode="decimal"></div>
      <input type="range" id="rate-range" min="0" max="20" step="0.05" value="5.5" aria-label="Interest rate slider">
    </div>
    <div class="row-2">
      <div class="field">
        <label for="years">Term (years)</label>
        <div class="control"><input id="years" type="number" min="1" max="40" step="1" value="25"></div>
      </div>
      <div class="field">
        <label for="extra">Extra per month</label>
        <div class="control"><input id="extra" type="number" min="0" step="25" value="0"></div>
      </div>
    </div>
    <p class="note">A fixed rate is assumed for the whole term. Fees, insurance and early-repayment
    charges are not included, so treat the result as the arithmetic of the loan rather than the
    final cost of the deal.</p>
  </form>

  <div>
    <section class="result">
      <p class="eyebrow">Contractual monthly payment</p>
      <p class="headline-figure" id="r-payment">&mdash;</p>
      <p class="note" id="warn" hidden></p>
      <dl class="stats">
        <div class="stat"><dt>Total interest</dt><dd id="r-interest">&mdash;</dd></div>
        <div class="stat"><dt>Total repaid</dt><dd id="r-total">&mdash;</dd></div>
        <div class="stat"><dt>Interest vs. loan</dt><dd id="r-ratio">&mdash;</dd></div>
        <div class="stat"><dt>Paid off in</dt><dd id="r-term">&mdash;</dd></div>
      </dl>
      <dl class="stats" id="saved-box" hidden>
        <div class="stat"><dt>Interest saved by paying extra</dt><dd class="pos" id="r-saved">&mdash;</dd></div>
        <div class="stat"><dt>Debt-free</dt><dd class="pos" id="r-sooner">&mdash;</dd></div>
        <div class="stat"><dt>You actually pay monthly</dt><dd id="r-outlay">&mdash;</dd></div>
      </dl>
      <svg class="chart" id="chart" aria-label="Remaining balance over the life of the loan"></svg>
      <p class="legend"><span><i style="background:#8FD9F0"></i>Balance on the standard payment</span>
      <span id="legend-extra" hidden><i style="background:#7CE0A6"></i>Balance with the extra payment</span></p>
    </section>

    <section class="panel" id="schedule" style="margin-top:clamp(16px,2.4vw,28px)">
      <h2>Amortisation schedule</h2>
      <div class="toggle">
        <button type="button" data-view="year" aria-pressed="true">By year</button>
        <button type="button" data-view="month" aria-pressed="false">By month</button>
      </div>
      <div class="tablewrap">
        <table>
          <thead><tr><th>Period</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead>
          <tbody id="sched"></tbody>
        </table>
      </div>
      <p class="note">Early payments are mostly interest because interest is charged on the balance
      you still owe. As the balance falls, the same payment buys you more principal, which is why
      overpaying early is worth far more than overpaying late.</p>
    </section>
  </div>
</div>

{ad("3333333333")}

<section class="wrap" style="max-width:900px;margin-bottom:clamp(50px,8vw,90px)">
  <h2 class="display" style="font-size:clamp(1.6rem,4vw,2.4rem);margin-bottom:.8em">How the payment is worked out</h2>
  <p style="line-height:1.8;opacity:.85;margin-bottom:1.1em">A fixed-rate loan uses one formula. The
  monthly payment is the amount that reduces the balance to exactly zero over the term, given the
  monthly interest rate. Written out, the payment equals the principal multiplied by the monthly
  rate, divided by one minus (one plus the monthly rate) raised to the power of minus the number of
  months.</p>
  <p style="line-height:1.8;opacity:.85;margin-bottom:1.1em">The monthly rate is the annual rate
  divided by twelve. Every month the lender charges interest on whatever you still owe, and the rest
  of your payment reduces the balance. That is the whole mechanism, and it is why two loans with the
  same monthly payment can cost wildly different amounts once the term changes.</p>
  <p style="line-height:1.8;opacity:.85">Stretching a loan over more years lowers the payment and
  raises the total interest, sometimes by more than the original amount borrowed. Shortening it does
  the reverse. Try both in the calculator above before you decide which trade you want.</p>
</section>
</main>"""
    write("loan-calculator.html", head(
        "Loan calculator with amortisation schedule \u2014 Moneta",
        "Free loan repayment calculator: monthly payment, total interest, full amortisation table and the savings from paying extra each month. Works in 18 currencies.",
        "/loan-calculator", "/img/art-loan.svg") + body +
        footer(["/assets/money.js", "/assets/loan.js"]))


# ========================================================== income calculator
def build_income():
    body = f"""{nav("/income-calculator")}
<main id="main">
<header class="page-head">
  <h1 class="display hero-heading reveal">Income calculator</h1>
  <p class="reveal" style="--d:.1s">Turn any pay figure into every other one, split your take-home
  pay into needs, wants and savings, and see how long your goal takes at the rate you are actually
  saving.</p>
</header>

<div class="calc wrap">
  <form class="panel" id="income-form" autocomplete="off">
    <h2>Your pay</h2>
    <div class="field">
      <label for="currency">Currency</label>
      <div class="control"><select id="currency"></select></div>
    </div>
    <div class="row-2">
      <div class="field">
        <label for="amount">Amount</label>
        <div class="control"><input id="amount" type="number" min="0" step="100" value="8000" inputmode="decimal"></div>
      </div>
      <div class="field">
        <label for="period">Per</label>
        <div class="control"><select id="period">
          <option value="hour">Hour</option><option value="day">Day</option>
          <option value="week">Week</option><option value="month" selected>Month</option>
          <option value="year">Year</option></select></div>
      </div>
    </div>
    <div class="row-2">
      <div class="field">
        <label for="hours">Hours a week</label>
        <div class="control"><input id="hours" type="number" min="1" max="90" step="1" value="40"></div>
      </div>
      <div class="field">
        <label for="weeks">Paid weeks a year</label>
        <div class="control"><input id="weeks" type="number" min="1" max="52" step="1" value="52"></div>
      </div>
    </div>
    <div class="row-2">
      <div class="field">
        <label for="deductions">Deductions</label>
        <div class="control"><span class="unit">%</span><input id="deductions" type="number" min="0" max="90" step="0.5" value="0"></div>
      </div>
      <div class="field">
        <label for="other">Other income / month</label>
        <div class="control"><input id="other" type="number" min="0" step="50" value="0"></div>
      </div>
    </div>
    <p class="note">Deductions is a single percentage covering income tax, social contributions and
    anything else taken before the money reaches you. Rates differ by country and by bracket, so
    check your own payslip rather than assuming a figure.</p>

    <h2 style="margin-top:2rem">Budget split</h2>
    <div class="field">
      <label for="needs">Needs <output id="needs-out">50%</output></label>
      <input type="range" id="needs" min="20" max="80" step="1" value="50">
    </div>
    <div class="field">
      <label for="wants">Wants <output id="wants-out">30%</output></label>
      <input type="range" id="wants" min="0" max="60" step="1" value="30">
    </div>
    <p class="note">Whatever is left over is your savings share: <output id="save-out">20%</output>.</p>

    <h2 style="margin-top:2rem">Savings goal</h2>
    <div class="row-2">
      <div class="field">
        <label for="goal">Target amount</label>
        <div class="control"><input id="goal" type="number" min="0" step="500" value="30000"></div>
      </div>
      <div class="field">
        <label for="return">Return a year</label>
        <div class="control"><span class="unit">%</span><input id="return" type="number" min="0" max="20" step="0.25" value="4"></div>
      </div>
    </div>
  </form>

  <div>
    <section class="result">
      <p class="eyebrow">Take-home each month</p>
      <p class="headline-figure" id="r-monthly">&mdash;</p>
      <dl class="stats">
        <div class="stat"><dt>Gross a year</dt><dd id="r-gross">&mdash;</dd></div>
        <div class="stat"><dt>Net a year</dt><dd id="r-net">&mdash;</dd></div>
        <div class="stat"><dt>Deducted a year</dt><dd id="r-tax">&mdash;</dd></div>
        <div class="stat"><dt>Net a week</dt><dd id="r-weekly">&mdash;</dd></div>
        <div class="stat"><dt>Net an hour</dt><dd id="r-hourly">&mdash;</dd></div>
      </dl>
    </section>

    <section class="panel" id="budget" style="margin-top:clamp(16px,2.4vw,28px)">
      <h2>Where the money goes</h2>
      <div style="display:flex;gap:1.5rem;flex-wrap:wrap;align-items:center">
        <div style="position:relative;flex:0 0 auto;width:min(260px,72vw)">
          <svg id="donut" aria-label="Budget split between needs, wants and savings"></svg>
          <p style="position:absolute;inset:0;display:grid;place-content:center;text-align:center;font-weight:500;font-size:1.15rem"
             id="donut-center">&mdash;</p>
        </div>
        <dl class="stats" style="flex:1 1 220px;margin-top:0">
          <div class="stat"><dt>Needs</dt><dd id="b-needs">&mdash;</dd></div>
          <div class="stat"><dt>Wants</dt><dd id="b-wants">&mdash;</dd></div>
          <div class="stat"><dt>Savings</dt><dd class="pos" id="b-save">&mdash;</dd></div>
        </dl>
      </div>
      <p class="legend"><span><i style="background:#8FD9F0"></i>Needs</span>
      <span><i style="background:#E9C25C"></i>Wants</span>
      <span><i style="background:#7CE0A6"></i>Savings</span></p>
    </section>

    <section class="panel" id="goal" style="margin-top:clamp(16px,2.4vw,28px)">
      <h2>Time to reach your goal</h2>
      <p class="headline-figure" style="font-size:clamp(2rem,6vw,3.4rem)" id="r-goal">&mdash;</p>
      <p class="note" id="goal-note"></p>
      <svg class="chart" id="chart" aria-label="Savings growth over ten years"></svg>
      <p class="legend"><span><i style="background:#8FD9F0"></i>Money you put in</span>
      <span><i style="background:#7CE0A6"></i>With compounding</span></p>
    </section>
  </div>
</div>

{ad("4444444444")}

<section class="wrap" style="max-width:900px;margin-bottom:clamp(50px,8vw,90px)">
  <h2 class="display" style="font-size:clamp(1.6rem,4vw,2.4rem);margin-bottom:.8em">Comparing two offers properly</h2>
  <p style="line-height:1.8;opacity:.85;margin-bottom:1.1em">Job offers are rarely quoted on the same
  basis. One is hourly, another is monthly, a third is annual with a bonus attached. Converting all
  of them to the same unit, after deductions, is the only way to see which one actually pays more.</p>
  <p style="line-height:1.8;opacity:.85">Then adjust for the hours. A monthly salary that assumes
  fifty hours a week is a different job from one that assumes thirty-five, even when the annual
  figures match. The net hourly figure above is the number that makes them comparable.</p>
</section>
</main>"""
    write("income-calculator.html", head(
        "Income and budget calculator \u2014 Moneta",
        "Convert hourly, weekly, monthly and annual pay after deductions, split take-home pay into needs, wants and savings, and see how long a savings goal takes.",
        "/income-calculator", "/img/art-income.svg") + body +
        footer(["/assets/money.js", "/assets/income.js"]))


# ==================================================================== guides
ARTICLES = []


def article(slug, title, desc, art_img, minutes, updated, sections, related):
    ARTICLES.append((slug, title, desc, art_img, minutes))
    rel = "".join(
        f'<a class="gcard" href="/guides/{s}"><div class="body"><h3>{t}</h3><p>{d}</p></div></a>'
        for s, t, d in related
    )
    ld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}",
"description":"{desc}","datePublished":"{updated}","dateModified":"{updated}",
"image":"{SITE}{art_img}","mainEntityOfPage":"{SITE}/guides/{slug}",
"author":{{"@type":"Organization","name":"{BRAND}"}},
"publisher":{{"@type":"Organization","name":"{BRAND}","logo":{{"@type":"ImageObject","url":"{SITE}/img/favicon.svg"}}}}}}
</script>"""
    body = f"""{nav("/guides/")}
<main id="main">
<header class="page-head">
  <h1 class="display hero-heading reveal" style="font-size:clamp(2rem,6vw,4.6rem);line-height:1.02">{title}</h1>
</header>
<article class="article">
  <img class="article-hero" src="{art_img}" alt="" aria-hidden="true">
  <p class="meta"><span>Updated {updated}</span><span>{minutes} min read</span><span>Moneta guides</span></p>
  {sections}
</article>
{ad("5555555555")}
<section style="padding:0 var(--pad) clamp(50px,8vw,90px)">
  <h2 class="display" style="font-size:clamp(1.4rem,3.4vw,2rem);margin:0 auto clamp(20px,3vw,32px);max-width:1180px">Keep reading</h2>
  <div class="grid-cards">{rel}</div>
</section>
</main>
{ld}"""
    write(f"guides/{slug}.html", head(title + " \u2014 Moneta", desc, f"/guides/{slug}", art_img) + body + footer())


# ---------------------------------------------------------------- article 1
article(
    "emergency-fund",
    "Build an emergency fund that actually holds",
    "How much to keep in an emergency fund, where to keep it, and how to rebuild it after you spend it \u2014 with the arithmetic worked out.",
    "/img/art-emergency.svg", 7, "2026-08-14",
    """
<p>An emergency fund is the least exciting money you will ever hold and the only money that reliably
stops a bad month from turning into a bad decade. Its entire job is to sit still and be boring until
the day the car dies, the contract ends, or the landlord asks for a new deposit.</p>

<h2>How much you actually need</h2>
<p>The usual advice is three to six months of expenses. That range is wide because the right number
depends on how fragile your income is, not on how much you earn. Two people on identical salaries
can need very different cushions.</p>
<p>Start with your essential monthly spend, not your income. Rent or mortgage, utilities, food,
transport, insurance, minimum debt payments, childcare. Leave out restaurants, subscriptions and
holidays. That total is your survival number, and it is usually far smaller than people expect,
which is exactly why using it makes the goal reachable.</p>
<p>Then adjust it for how quickly you could replace your income:</p>
<ul>
<li><strong>Salaried, in-demand skill, dual-income household:</strong> three months is defensible.</li>
<li><strong>Single income, or a specialised role with a slow job market:</strong> six months.</li>
<li><strong>Freelance, commission-based or seasonal income:</strong> nine to twelve months, because
your bad months and the economy's bad months tend to arrive together.</li>
<li><strong>Visa or residency tied to your job:</strong> add the cost of relocating, which for many
people is the largest single line item on the list.</li>
</ul>

<div class="example">
<h4>Worked example</h4>
<p>Essential spend of 4,200 a month. A freelancer targeting nine months needs 37,800. Saving 900 a
month, that is forty-two months away, which sounds hopeless. Splitting it changes the picture: a
first milestone of one month's spend takes under five months, and one month of cash removes most of
the small emergencies that otherwise go on a credit card at twenty-something percent.</p>
</div>

<h2>Where to keep it</h2>
<p>Two properties matter and nothing else does: you can reach the money within a day or two, and the
amount does not fall. That rules out anything with a market price attached, which means stocks,
funds, crypto and anything described as an opportunity.</p>
<p>A separate savings account at a different bank from your current account works well. The friction
of a transfer is a feature, not a bug: it stops the fund from quietly becoming your overdraft
buffer. If your market offers a notice account or money market fund with same-week access and no
capital risk, that is fine too. Interest is a bonus here, not the objective.</p>
<div class="callout">
<p>An emergency fund that is invested is not an emergency fund. The most likely time you need it is
also the most likely time markets are down, which is precisely when you would have to sell at a
loss.</p>
</div>

<h2>Filling it without a raise</h2>
<p>The reliable method is automation plus a floor. Set a standing transfer for the day after payday,
even if it is small, and treat it as a bill. Money that never lands in your current account is money
you never decide about, and decisions are where budgets die.</p>
<p>The second lever is irregular income. Bonuses, tax refunds, a client paying late, a gift. Send a
fixed share of every windfall straight to the fund before the money has a chance to acquire a
purpose. Half is a common split and is high enough to matter without feeling punitive.</p>
<p>Use the <a href="/income-calculator">income calculator</a> to see what a given savings percentage
looks like as a monthly figure, then set the standing transfer to that amount rather than to a round
number you picked by feel.</p>

<h2>When to spend it, and how to rebuild</h2>
<p>An emergency is unexpected, necessary and urgent. All three. A boiler failing is an emergency. A
holiday that has been in the calendar for eight months is not, even if you failed to save for it.
Being strict about this is what keeps the fund available for the thing it was built for.</p>
<p>After you spend it, rebuild deliberately. Set a date, restart the standing transfer at the old
amount or higher, and accept that other goals pause. The fund is the foundation the other goals
stand on, so rebuilding it first is not a delay: it is the order of operations.</p>

<h2>One common mistake</h2>
<p>Holding a large emergency fund while carrying expensive debt is usually the wrong shape. If you
have one month of cash and a credit card at twenty-four percent, every extra month you add to the
fund is earning maybe four percent while costing twenty-four. The usual answer is to hold a smaller
starter buffer, clear the expensive debt, then build the full fund. The
<a href="/guides/pay-off-debt-faster">debt guide</a> works through the arithmetic.</p>
""",
    [("budget-50-30-20", "The 50/30/20 rule, and when to break it",
      "A simple budget split, its real weaknesses, and how to adjust it for a high-rent city."),
     ("pay-off-debt-faster", "Pay off debt faster without earning more",
      "Avalanche versus snowball, and why the order you pay debts in changes the total."),
     ("compound-interest", "Compound interest, explained with actual numbers",
      "Why the first ten years feel pointless and the last ten do all the work.")])

# ---------------------------------------------------------------- article 2
article(
    "budget-50-30-20",
    "The 50/30/20 rule, and when to break it",
    "The 50/30/20 budget explained: what counts as a need, why the rule fails in expensive cities, and how to adapt the split without abandoning it.",
    "/img/art-budget.svg", 6, "2026-08-21",
    """
<p>The 50/30/20 rule says to spend half your take-home pay on needs, three tenths on wants, and save
the remaining fifth. Its value is not the accuracy of those numbers. It is that it replaces
forty-line spreadsheets with three decisions, and three decisions are a habit you might actually
keep.</p>

<h2>The three buckets, defined properly</h2>
<h3>Needs \u2014 50%</h3>
<p>Costs you cannot stop this month without serious consequences: housing, utilities, groceries,
transport to work, insurance, childcare, and the minimum payment on every debt. Minimums go here
because missing them has consequences; anything above the minimum is a savings decision, not a
need.</p>
<h3>Wants \u2014 30%</h3>
<p>Everything that improves your life and could stop tomorrow. Eating out, streaming, travel,
clothes beyond replacement, hobbies, the upgraded phone. This bucket is not a moral failing to be
minimised to zero. A budget with no wants is a diet you quit in March.</p>
<h3>Savings and debt payoff \u2014 20%</h3>
<p>Emergency fund, retirement contributions, investments, and every extra payment above the minimum
on your debts. Grouping savings and extra debt payments together is the rule's smartest move: paying
down a loan at eighteen percent is a guaranteed eighteen percent return, which beats almost anything
you could buy with the money.</p>

<div class="example">
<h4>Worked example</h4>
<p>Take-home of 9,000 a month. The split gives 4,500 for needs, 2,700 for wants and 1,800 for
savings. If rent alone is 4,000, needs are already at 89% of the target before a single grocery
run, and the honest conclusion is that the housing cost, not the coffee habit, is the problem to
solve.</p>
</div>

<h2>Where the rule breaks</h2>
<p>It breaks in expensive cities. In Dubai, London, Singapore or San Francisco, rent alone can take
forty percent of take-home pay, and a strict fifty percent for all needs is arithmetically
impossible for most earners. It also breaks at low incomes, where needs can exceed a hundred percent
of income and the failure is structural rather than behavioural.</p>
<p>It breaks in the other direction too. On a high income, fifty percent for needs is far more than
you require, and following the rule literally means inflating your lifestyle to fill a bucket. High
earners usually get more out of a fixed spending number and everything above it saved.</p>

<h2>Adapting it without losing the point</h2>
<p>Change the ratios, keep the structure. A 60/20/20 works in a high-rent city and protects the
savings share, which is the number that actually determines your future. A 40/20/40 suits someone
with a paid-off home and a short runway to retirement. What you should not do is let the savings
bucket absorb every shock, because that is how a budget quietly becomes a spending log.</p>
<div class="callout">
<p>Protect the savings percentage first and let needs and wants fight over the rest. If the savings
share is the number that flexes, the rule has stopped doing anything.</p>
</div>
<p>The <a href="/income-calculator#budget">budget split calculator</a> lets you drag the needs and
wants shares and see the money figures update, which is faster than arguing with percentages in the
abstract.</p>

<h2>Making it survive contact with real life</h2>
<p>Run it on take-home pay, not gross. Automate the savings transfer on payday so the fifth is gone
before you can plan around it. Review the split every six months and after any change in income or
rent, because a budget written for a salary you no longer earn is a work of fiction.</p>
<p>If your income is irregular, budget on your lowest recent month rather than the average, and treat
everything above that as windfall to be split between savings and the buffer. It feels
overcautious in a good month and saves you in a bad one.</p>

<h2>The one number that matters</h2>
<p>If you track nothing else, track your savings rate: the share of take-home pay you keep. It is a
single figure, it is hard to fool yourself about, and it moves only when something real changes.
Every other budget metric is a way of getting that one number up.</p>
""",
    [("emergency-fund", "Build an emergency fund that actually holds",
      "How much to keep, where to keep it, and how to rebuild after you spend it."),
     ("compound-interest", "Compound interest, explained with actual numbers",
      "Why the first ten years feel pointless and the last ten do all the work."),
     ("pay-off-debt-faster", "Pay off debt faster without earning more",
      "Avalanche versus snowball, and why the order you pay debts in changes the total.")])

# ---------------------------------------------------------------- article 3
article(
    "pay-off-debt-faster",
    "Pay off debt faster without earning more",
    "Avalanche versus snowball, why overpaying early is worth more than overpaying late, and how to check whether refinancing is worth it.",
    "/img/art-debt.svg", 8, "2026-08-28",
    """
<p>Interest is charged on the balance you still owe. Every other fact about paying off debt follows
from that one sentence, including why an extra payment in year one is worth several times the same
payment in year fifteen.</p>

<h2>Why early payments are worth more</h2>
<p>On a twenty-five year loan at five and a half percent, the first payment is mostly interest and
barely touches the balance. By year twenty the same payment is almost entirely principal. An extra
amount paid in month one removes that principal from every future interest calculation \u2014 three
hundred of them. The same amount paid in month two hundred removes it from a handful.</p>
<p>This is why the standard advice to overpay early is not a moral preference for discipline. It is
arithmetic, and you can watch it happen in the <a href="/loan-calculator#schedule">amortisation
table</a>: enter your loan, add an extra monthly amount, and compare the total interest figure with
and without it.</p>

<h2>Avalanche or snowball</h2>
<p>When you have several debts, you pay the minimum on all of them and send every spare amount to
one. Which one is the whole question.</p>
<h3>Avalanche: highest rate first</h3>
<p>Target the debt with the highest interest rate, regardless of size. This is mathematically
optimal: it always produces the lowest total interest and the shortest payoff time. If you will
stick to it, nothing beats it.</p>
<h3>Snowball: smallest balance first</h3>
<p>Target the smallest balance, regardless of rate. You clear individual debts faster, which frees up
their minimum payments and produces visible wins early. It costs more in interest, sometimes
meaningfully.</p>
<div class="example">
<h4>Worked example</h4>
<p>Three debts: 1,200 at 8%, 6,000 at 24%, 3,500 at 14%, with 600 a month spare. Avalanche clears
the 24% card first and saves roughly a few hundred in interest over the run. Snowball clears the
1,200 balance in two months, which for many people is the difference between continuing and quitting
in month four.</p>
</div>
<p>Pick avalanche if the gap between your highest and lowest rate is large, which is usually the case
when a credit card is involved. Pick snowball if you have abandoned a payoff plan before. The best
method is the one still running in month nine.</p>

<h2>Refinancing: when it is worth it</h2>
<p>Refinancing replaces an expensive debt with a cheaper one. It genuinely works, and it is also
where most of the traps live.</p>
<ul>
<li><strong>Compare total cost, not the monthly payment.</strong> A lower payment over a longer term
usually costs more overall. Run both in the loan calculator and read the total interest line.</li>
<li><strong>Count the fees.</strong> Arrangement fees, valuation fees and early-repayment charges on
the old loan can erase the saving. Add them to the new loan's cost before deciding.</li>
<li><strong>Watch the term reset.</strong> Refinancing eighteen years into a twenty-five year
mortgage back to a fresh twenty-five years is often a loss dressed as a saving.</li>
<li><strong>Balance-transfer cards.</strong> The zero percent window is real, and so is the transfer
fee and the rate that applies afterwards. It only works if you clear the balance inside the window,
so divide the balance by the number of months and check that the payment is one you can make.</li>
</ul>

<h2>The order to attack, once and for all</h2>
<ol>
<li>Pay every minimum, every month. Missed payments cost more than any strategy saves.</li>
<li>Hold a small cash buffer, one month of essential spend, so a surprise does not go back on the
card you are trying to clear.</li>
<li>Clear anything above roughly ten percent aggressively. No investment reliably beats a guaranteed
return of that size.</li>
<li>Capture any employer retirement match, which is an immediate return no debt rate matches.</li>
<li>Then choose: keep attacking mid-rate debt, or start investing, depending on whether the rate is
above or below what you would realistically earn.</li>
</ol>
<div class="callout">
<p>Low-rate debt is not an emergency. A subsidised loan at two percent while inflation runs higher is
a debt you can pay on schedule while your money works elsewhere. Not all debt deserves the same
urgency.</p>
</div>

<h2>Making the extra payment count</h2>
<p>Tell the lender the extra amount is for the principal. Some lenders otherwise treat it as an early
payment of next month's instalment, which does far less for you. Check the balance after the first
overpayment to confirm it was applied the way you intended, and keep checking for the first few
months.</p>
""",
    [("emergency-fund", "Build an emergency fund that actually holds",
      "How much to keep, where to keep it, and how to rebuild after you spend it."),
     ("budget-50-30-20", "The 50/30/20 rule, and when to break it",
      "A simple budget split, its real weaknesses, and how to adjust it."),
     ("compound-interest", "Compound interest, explained with actual numbers",
      "Why the first ten years feel pointless and the last ten do all the work.")])

# ---------------------------------------------------------------- article 4
article(
    "compound-interest",
    "Compound interest, explained with actual numbers",
    "How compounding really works, why the first decade feels pointless, and what fees and inflation quietly take from the result.",
    "/img/art-compound.svg", 7, "2026-08-30",
    """
<p>Compounding is earning a return on your returns. Described that way it sounds mild. Watched over
thirty years it is the single largest force in personal finance, and the reason two people saving the
same amount can end up with wildly different results.</p>

<h2>The shape of the curve</h2>
<p>Put aside 1,000 a month at seven percent a year. After ten years you have around 173,000, of which
120,000 is your own money. After twenty years, roughly 521,000 against 240,000 contributed. After
thirty, about 1,220,000 against 360,000 contributed.</p>
<p>Read those three numbers again. In the first decade, growth adds about half of what you put in. In
the third decade it adds more than twice. Nothing changed about the rate or the contribution. The
only variable was time, and time is the input people spend most freely when they are young and cannot
buy back later.</p>
<div class="callout">
<p>The first ten years feel like nothing is happening. They are not wasted \u2014 they are the base
the third decade multiplies. This is why starting small beats waiting until you can start
properly.</p>
</div>
<p>The <a href="/income-calculator#goal">savings calculator</a> plots your own contribution against
the compounded total, so you can see where the two lines separate for your numbers rather than
these.</p>

<h2>What the rate does</h2>
<p>Small differences in rate become large differences in outcome, because the rate is applied
repeatedly. The rule of 72 gives you a quick estimate: divide 72 by the annual return to get the
years it takes to double. At six percent, twelve years. At nine percent, eight years. Over a
forty-year horizon that gap is the difference between three doublings and five.</p>

<h2>What quietly takes it away</h2>
<h3>Fees</h3>
<p>A fund charging one and a half percent a year against one charging nought point two does not cost
you one point three percent. It costs you one point three percent compounded for as long as you
hold it, which over thirty years can remove a quarter or more of the final balance. Fees are the
one variable in investing you control completely.</p>
<h3>Inflation</h3>
<p>A seven percent return with three percent inflation is roughly four percent in real purchasing
power. Both figures are correct; only one tells you what the money will buy. When you set a savings
goal decades away, set it in today's money and assume the target rises with inflation.</p>
<h3>Interruptions</h3>
<p>Withdrawing and restarting resets the part of the curve that does the work. This is the practical
argument for a separate emergency fund: it lets long-term money stay untouched through the months
when something goes wrong.</p>

<h2>Compounding works against you too</h2>
<p>The same mechanism runs in reverse on debt. A credit card at twenty-four percent compounds
monthly, so a balance left alone roughly doubles in three years even if you never spend another
amount on it. This is why clearing high-rate debt is usually the highest-certainty return available
to you, and why it comes before investing in almost every sensible order of operations.</p>

<div class="example">
<h4>Worked example</h4>
<p>Two savers, same 500 a month, same seven percent. One starts at 25 and stops at 35, contributing
60,000 in total. The other starts at 35 and contributes until 65, putting in 180,000. At 65 the
first is often still ahead. The extra decade at the start outweighs twenty extra years of
contributions.</p>
</div>

<h2>What to actually do with this</h2>
<p>Start with any amount, because the start date matters more than the size. Automate it so the
decision is made once. Keep costs low, since fees compound against you exactly as returns compound
for you. And leave it alone, which is the hardest part and the one that does the most work.</p>
""",
    [("emergency-fund", "Build an emergency fund that actually holds",
      "How much to keep, where to keep it, and how to rebuild after you spend it."),
     ("budget-50-30-20", "The 50/30/20 rule, and when to break it",
      "A simple budget split, its real weaknesses, and how to adjust it."),
     ("pay-off-debt-faster", "Pay off debt faster without earning more",
      "Avalanche versus snowball, and why the order you pay debts in changes the total.")])


def build_guide_index():
    cards = "".join(
        f'<a class="gcard" href="/guides/{s}"><img src="{img}" alt="" loading="lazy">'
        f'<div class="body"><p class="eyebrow">{m} min read</p><h3>{t}</h3><p>{d}</p></div></a>'
        for s, t, d, img, m in ARTICLES
    )
    body = f"""{nav("/guides/")}
<main id="main">
<header class="page-head">
  <h1 class="display hero-heading reveal">Guides</h1>
  <p class="reveal" style="--d:.1s">Plain-English writing on the parts of personal finance that
  actually move the number: what to save, what to pay off first, and what compounding does while
  you are not looking.</p>
</header>
<div class="grid-cards">{cards}</div>
{ad("6666666666")}
</main>"""
    write("guides/index.html", head(
        "Money guides \u2014 Moneta",
        "Plain-English guides to emergency funds, budgeting, paying off debt and compound interest, written to be used alongside free calculators.",
        "/guides/") + body + footer())


# ============================================================== simple pages
def simple(path, title, desc, h1, html):
    body = f"""{nav()}
<main id="main">
<header class="page-head">
  <h1 class="display hero-heading reveal" style="font-size:clamp(2.2rem,7vw,5rem)">{h1}</h1>
</header>
<article class="article">{html}</article>
</main>"""
    write(path, head(title, desc, "/" + path.replace(".html", "").replace("index", "")) + body + footer())


simple("about.html", "About Moneta", "Who builds Moneta, how the calculators work, and how the site is funded.", "About", """
<p>Moneta is a small, independent site built around one idea: most money decisions get easier once
you can see the arithmetic. Not a course, not a newsletter funnel, not a lead-generation form for a
broker. Calculators that work, and writing that explains what the output means.</p>
<h2>How the calculators work</h2>
<p>Every calculation runs in your browser using plain JavaScript. Nothing you type is transmitted,
stored or logged. You can close the tab and it is gone, and you can read the code by viewing the
page source if you want to check the formulas yourself.</p>
<p>The loan calculator uses the standard fixed-rate annuity formula and then simulates the loan month
by month to build the amortisation table, which is why the extra-payment comparison reflects the
real path of the balance rather than an approximation.</p>
<h2>Editorial approach</h2>
<p>Guides are written to be specific. Where a rule of thumb has a known weakness, the guide says so.
Where the right answer depends on your situation, it says that instead of pretending otherwise. We
do not recommend individual products, banks or brokers, and we do not accept payment for
placement.</p>
<h2>How the site is funded</h2>
<p>Through display advertising. Advertisers have no input into what is written, and no advertiser is
told about, or shown, anything you enter into a calculator. See the
<a href="/privacy">privacy policy</a> for how advertising cookies work and how to opt out.</p>
<h2>Corrections</h2>
<p>If you find an error in a formula or an article, tell us and it gets fixed and dated. Write to us
via the <a href="/contact">contact page</a>.</p>
""")

simple("contact.html", "Contact Moneta", "How to reach Moneta about corrections, questions or advertising.", "Contact", """
<p>The fastest way to reach us is by email.</p>
<h2>General and corrections</h2>
<p><a href="mailto:hello@moneta.tools">hello@moneta.tools</a> \u2014 questions about a calculator, a
suspected error in an article, or a suggestion for something to build. Corrections are prioritised;
if a formula is wrong we want to know before anyone else relies on it.</p>
<h2>Privacy requests</h2>
<p><a href="mailto:privacy@moneta.tools">privacy@moneta.tools</a> \u2014 requests about data,
cookies or advertising preferences.</p>
<h2>Advertising</h2>
<p><a href="mailto:ads@moneta.tools">ads@moneta.tools</a> \u2014 display advertising enquiries. We do
not sell links, sponsored posts or product placement inside guides.</p>
<h2>What we cannot do</h2>
<p>We cannot give personal financial advice, review your specific loan agreement, or tell you what to
invest in. Those require a licensed adviser who knows your full circumstances. See the
<a href="/disclaimer">editorial disclaimer</a>.</p>
<p>We usually reply within a few working days.</p>
""")

simple("privacy.html", "Privacy policy \u2014 Moneta", "What Moneta collects, what it does not, and how advertising and analytics cookies are used.", "Privacy policy", """
<p class="meta"><span>Last updated 2 September 2026</span></p>
<p>This policy explains what happens to information when you use this site. It is written to be read,
not to be survived.</p>
<h2>What the calculators do with your numbers</h2>
<p>Nothing leaves your device. Every calculation runs locally in your browser. Amounts, rates, salary
figures and goals are never sent to a server, never stored, and never visible to us or to anyone
else.</p>
<h2>What we collect</h2>
<p>We do not ask you to create an account and we do not run a mailing list. If you email us, we hold
that email in order to reply to it.</p>
<h2>Cookies and advertising</h2>
<p>This site is funded by display advertising. Third-party vendors, including Google, use cookies to
serve ads based on your prior visits to this and other websites.</p>
<ul>
<li>Google's use of advertising cookies enables it and its partners to serve ads to you based on your
visits to this site and other sites on the internet.</li>
<li>You can opt out of personalised advertising by visiting
<a href="https://www.google.com/settings/ads" rel="nofollow noopener">Google Ads Settings</a>.</li>
<li>You can opt out of some third-party vendors' use of cookies for personalised advertising at
<a href="https://www.aboutads.info/choices/" rel="nofollow noopener">aboutads.info/choices</a>.</li>
<li>Visitors in the EEA, UK and Switzerland are shown a consent notice before non-essential cookies
are set, and can change or withdraw consent at any time through that notice.</li>
</ul>
<h2>Analytics</h2>
<p>We may use privacy-respecting analytics to count page views and understand which guides are read.
This records aggregate information such as page URL, referrer, approximate country and device type.
It is not used to identify individuals.</p>
<h2>Your rights</h2>
<p>Depending on where you live you may have the right to access, correct or delete personal data we
hold, to object to processing, or to withdraw consent. Because we hold almost nothing, most requests
resolve quickly. Write to <a href="mailto:privacy@moneta.tools">privacy@moneta.tools</a>.</p>
<h2>Children</h2>
<p>This site is not directed at children under 13 and we do not knowingly collect their data.</p>
<h2>Changes</h2>
<p>If this policy changes, the date at the top changes with it. Material changes will be noted on the
page rather than made quietly.</p>
""")

simple("terms.html", "Terms of use \u2014 Moneta", "The terms that apply to using the Moneta website and its calculators.", "Terms of use", """
<p class="meta"><span>Last updated 2 September 2026</span></p>
<h2>Using this site</h2>
<p>You may use Moneta for personal, non-commercial purposes. You may link to any page. You may not
scrape the site at a rate that degrades it for others, republish articles in full, or present the
calculators as your own.</p>
<h2>Accuracy</h2>
<p>The calculators implement standard financial formulas and are tested, but results depend entirely
on the assumptions you enter. Real agreements include fees, insurance requirements, variable rates,
rounding conventions and early-repayment charges that a general calculator cannot know about. Always
check the figures against the documents your lender or employer gives you.</p>
<h2>No advice</h2>
<p>Content on this site is general information, not financial, tax or legal advice, and it does not
take your circumstances into account. See the <a href="/disclaimer">editorial disclaimer</a>.</p>
<h2>Third-party links</h2>
<p>We link to outside sources where they are useful. We do not control them and are not responsible
for their content or their policies.</p>
<h2>Intellectual property</h2>
<p>Text, illustrations and code on this site belong to Moneta unless stated otherwise. Short quotes
with a link back are welcome.</p>
<h2>Liability</h2>
<p>The site is provided as it is, without warranties. To the extent permitted by law we are not
liable for losses arising from decisions made on the basis of information or calculations found
here.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:hello@moneta.tools">hello@moneta.tools</a>.</p>
""")

simple("disclaimer.html", "Editorial disclaimer \u2014 Moneta", "Why Moneta is information rather than financial advice, and how the content is produced.", "Editorial disclaimer", """
<p>Everything on Moneta is general educational information about how money works. It is not financial
advice, investment advice, tax advice or legal advice, and it cannot be, because advice requires
knowing your income, obligations, jurisdiction, risk tolerance and goals.</p>
<h2>What that means in practice</h2>
<ul>
<li>No article recommends a specific product, lender, bank, fund or platform.</li>
<li>Calculator results are illustrations based on the numbers you enter, not offers or quotes.</li>
<li>Tax and social contribution rates differ by country and change over time; the income calculator
takes a percentage you supply rather than assuming one.</li>
<li>Investment returns used in examples are illustrative. Past returns do not predict future
ones, and the value of investments can fall.</li>
</ul>
<h2>Before you act on anything here</h2>
<p>For decisions with real consequences \u2014 a mortgage, a refinance, a pension, a large investment,
anything with tax implications \u2014 speak to a licensed professional in your own jurisdiction who
can see your full picture.</p>
<h2>How content is produced</h2>
<p>Guides are written and edited in-house, checked against the formulas used in the calculators, and
dated when updated. Where a claim depends on a figure, the figure is shown so you can test it. If
something is wrong, we correct it and note the change rather than editing silently.</p>
<h2>Advertising</h2>
<p>The site carries display advertising. Advertisers do not review, commission or influence editorial
content, and no article is written in exchange for payment.</p>
""")

write("404.html", head("Page not found \u2014 Moneta", "That page does not exist.", "/404") + f"""
{nav()}
<main id="main">
<header class="page-head">
  <h1 class="display hero-heading">404</h1>
  <p>That page does not exist. Try a calculator or a guide instead.</p>
  <p style="margin-top:2rem"><a class="btn btn-primary" href="/">Back to the front page</a></p>
</header>
</main>""" + footer())


# ================================================================== metadata
def build_meta():
    urls = ["/", "/loan-calculator", "/income-calculator", "/guides/", "/about", "/contact",
            "/privacy", "/terms", "/disclaimer"] + ["/guides/" + a[0] for a in ARTICLES]
    items = "".join(
        f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{'weekly' if u in ('/', '/guides/') else 'monthly'}</changefreq>"
        f"<priority>{'1.0' if u == '/' else '0.8' if 'calculator' in u else '0.7'}</priority></url>"
        for u in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + '</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("ads.txt", "# Replace with the line AdSense gives you after approval:\n"
                     "# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n")
    write("site.webmanifest",
          '{"name":"Moneta","short_name":"Moneta","start_url":"/","display":"standalone",'
          '"background_color":"#0C0C0C","theme_color":"#0C0C0C",'
          '"icons":[{"src":"/img/favicon.svg","sizes":"any","type":"image/svg+xml"}]}')
    write("vercel.json",
          '{\n  "cleanUrls": true,\n  "trailingSlash": false,\n'
          '  "headers": [\n    {\n      "source": "/(.*)\\\\.(svg|png|css|js)",\n'
          '      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]\n'
          '    }\n  ]\n}')


build_index()
build_loan()
build_income()
build_guide_index()
build_meta()
print("built", sum(len(f) for _, _, f in os.walk(ROOT)), "files")
