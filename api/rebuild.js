export default async function handler(req, res) {
  const hookUrl = process.env.SANITY_DEPLOY_HOOK_URL;
  if (!hookUrl) {
    res.status(500).json({ error: "SANITY_DEPLOY_HOOK_URL not configured" });
    return;
  }
  const r = await fetch(hookUrl, { method: "POST" });
  const body = await r.json();
  res.status(200).json({ triggered: true, deployHook: body });
}
