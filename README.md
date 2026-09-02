# Moneta — money calculators + guides

Static site. No build step, no framework, no npm install. Drop the folder on Vercel and it runs.

## Deploy

```bash
npx vercel --prod          # or: drag the folder into vercel.com/new
```

`vercel.json` turns on clean URLs, so `/loan-calculator.html` serves at `/loan-calculator`.

## Before you go live — 3 find-and-replace jobs

1. **Domain.** Open `build.py`, change `SITE = "https://moneta.tools"` to your real domain, then
   run `python3 build.py`. This fixes every canonical tag, OG URL and the sitemap at once.
2. **Email addresses.** `hello@ / privacy@ / ads@` appear in `build.py` (contact, privacy, terms).
   They must be addresses you can actually receive mail on — AdSense reviewers check.
3. **AdSense IDs.** In `build.py`, set `ADSENSE_CLIENT` to your `ca-pub-…` value, then uncomment
   the loader `<script>` in `head()` and the `<ins>` block in `ad()`. Put the line AdSense gives
   you into `ads.txt`. Do this *after* approval, not before.

## Regenerating things

| Command | What it does |
|---|---|
| `python3 gen_art.py` | Redraws all 44 money SVGs into `img/` |
| `python3 gen_og.py`  | Redraws `img/og.png` (1200×630 social preview) |
| `python3 build.py`   | Rebuilds every `.html` page from the templates |

Edit `build.py`, not the generated HTML — a rebuild overwrites the HTML.

## What's where

```
index.html              hero, currency marquee, about, calculators list, stacked guide cards
loan-calculator.html    payment, total interest, extra-payment saving, amortisation table
income-calculator.html  pay conversion, budget donut, savings-goal projection
guides/                 4 long-form articles + index
about / contact / privacy / terms / disclaimer / 404
assets/                 base.css, site.js (motion), money.js + loan.js + income.js (maths)
img/                    all artwork, generated, original, no third-party assets
```

## AdSense readiness checklist

Done in this build:
- Privacy policy naming Google advertising cookies + opt-out links, terms, editorial disclaimer
- Real about + contact pages with working navigation
- 4 substantial original articles, dated, internally linked
- Two working tools that give the site a reason to exist
- sitemap.xml, robots.txt, canonicals, Article + WebSite structured data, OG images
- ads.txt placeholder

Still on you:
- A domain that's been live and indexed for a few weeks
- Real traffic from search or social — AdSense rejects sites with none
- Verify in Google Search Console and submit the sitemap
- Keep publishing: 4 articles is the floor, not the target. Add one a week.
- If you serve EU/UK visitors, add a consent-mode CMP before enabling ads.

## Notes

- All calculations run client-side. Nothing is sent anywhere, which is what the privacy policy
  claims — keep it true if you add analytics.
- Loan maths verified against the standard annuity formula: 250,000 at 5.5% over 25 years gives
  a payment of 1,535.22 and total interest of 210,566.
- Respects `prefers-reduced-motion`, keyboard focus is visible, all decorative art is
  `aria-hidden`.
