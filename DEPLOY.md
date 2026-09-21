# Deploy — Moneta

Live at **https://monetaa.online**, deployed via the `monetaa` Vercel project
(team `digitalsupplycoo-svgs-projects`), git repo
`github.com/digitalsupplycoo-svg/monetaa`.

## Project settings (already configured)

The site is a static build, but it now has a real build step because the blog
pulls content from Sanity at build time. Vercel project settings:

- **Framework preset:** Other
- **Build command:** `python3 build.py`
- **Output directory:** `.` (repo root — `build.py` writes files there directly)
- **Install command:** default (no root `package.json`, nothing to install)

If these ever get reset to "Auto", set them again with:

```bash
vercel project update monetaa --build-command "python3 build.py" --output-directory "."
```

## Regular deploy

```bash
python3 build.py      # regenerate every page, including /blog/ from Sanity
git add -A && git commit -m "..." && git push
vercel --prod          # or let the git push trigger it if auto-deploy is on
```

## The blog (Sanity)

- **Studio (where you write posts):** https://monetaa.sanity.studio — sign in
  with the Google account `digitalsupplycoo@gmail.com`. Whatever you publish
  there becomes a `post` document.
- **How it gets on the site:** `build.py` calls `fetch_blog_posts()` at build
  time (stdlib `urllib`, no dependency), converts the Portable Text body to
  HTML, and writes `/blog/index.html` + `/blog/<slug>.html` using the same
  template functions as the rest of the site. There is no live database query
  at request time — publishing only takes effect on the next build.
- **Project:** Sanity project `auge2q4g`, dataset `production`, provisioned
  via the Vercel Marketplace integration (`vercel integration add
  sanity/project`). Env vars (`SANITY_API_PROJECT_ID`, `SANITY_API_DATASET`,
  `SANITY_API_READ_TOKEN`, `SANITY_API_WRITE_TOKEN`) are already set on the
  Vercel project for Production/Preview/Development — pull them locally with
  `vercel env pull`.
- **Studio source:** `studio/` (its own small Node project, the only place
  npm is used in this repo — completely separate from the main static
  build). To change the post schema, edit `studio/schemaTypes/post.ts` then
  redeploy the studio: `cd studio && npx sanity deploy --url monetaa`.

### Triggering a rebuild when you publish

Two mechanisms are wired up so a new post goes live without anyone running
`vercel --prod` by hand:

1. **Sanity webhook** (`Vercel deploy on publish`, dataset `production`,
   filtered to `_type == "post"`) — should call the Vercel Deploy Hook
   immediately on publish. **As of this writing this has not reliably fired
   in testing** (the hook is created successfully via Sanity's API but
   delivery attempts show empty, most likely because the Sanity project was
   provisioned as a Vercel Marketplace "sandbox" resource with the webhooks
   feature not fully activated). Worth re-testing after publishing a real
   post from the Studio UI — it may behave differently than API-created test
   documents.
2. **Daily cron fallback** (`api/rebuild.js` + `vercel.json` `crons`, `0 3
   * * *` UTC) — hits the same Vercel Deploy Hook once a day regardless, so
   even if the webhook never fires, a published post is live within 24
   hours at worst. Vercel's Hobby plan caps cron frequency at once/day; a
   Pro plan would allow a much tighter schedule (e.g. every 15 minutes).

If you publish something and want it live **right now**, the reliable path
today is: ask for a manual rebuild, or run `python3 build.py && vercel
--prod` yourself. The Deploy Hook itself can also be triggered directly:

```bash
curl -X POST https://api.vercel.com/v1/integrations/deploy/prj_8yZDWQu0lNpdKpDUrdpGaN7caXf5/nC1wXrVcZ9
```

### Known limitation

`build.py` never deletes stale generated blog pages — if a post is removed
from Sanity, its old `/blog/<slug>.html` file stays on disk until someone
deletes it manually before the next build/commit.

## Search

`build.py` also emits `/search-index.json` (every calculator, guide, legal
page and blog post) and `assets/search.js` is a small vanilla-JS overlay that
searches it client-side. No backend involved.

## Domain / DNS

`monetaa.online` → A record `76.76.21.21`, `www` CNAME →
`cname.vercel-dns.com`. Already configured.

## AdSense

See `README.md`.
