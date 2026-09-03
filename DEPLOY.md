# Deploy — GitHub then Vercel

The folder is already a git repo with one commit made. Nothing to initialise.

## 1. GitHub

Create an empty repo at https://github.com/new — name it `moneta`, leave "Add a README",
`.gitignore` and licence all **unchecked** (the repo already has files; adding any would
force you to merge).

Then, in the unzipped folder:

```bash
git remote add origin https://github.com/YOUR-USERNAME/moneta.git
git push -u origin main
```

If you have the GitHub CLI installed, both steps collapse into one:

```bash
gh repo create moneta --public --source=. --push
```

## 2. Vercel

Two ways. Pick one.

**A — link the repo (recommended).** Go to https://vercel.com/new, pick the `moneta` repo,
and press Deploy. Framework preset: **Other**. Build command: **leave empty**. Output
directory: **leave empty**. It is plain static HTML — there is nothing to build. Every future
`git push` then redeploys automatically.

**B — deploy straight from the folder, no GitHub needed:**

```bash
npx vercel --prod
```

Answer the prompts with the defaults. Same result, but no automatic redeploys on push.

## 3. After the first deploy

1. Note the live URL Vercel gives you (`moneta-something.vercel.app`).
2. Open `build.py`, set `SITE` to that URL (or your custom domain), run `python3 build.py`,
   commit and push. This fixes every canonical tag, OG image URL and the sitemap.
3. Add your domain in Vercel under Project → Settings → Domains. At Namecheap point the
   A record to `76.76.21.21` and the `www` CNAME to `cname.vercel-dns.com`.
4. Verify the domain in Google Search Console and submit `/sitemap.xml`.

Do the AdSense steps in `README.md` only after the site has been live and indexed for a while.
