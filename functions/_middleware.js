// Cloudflare Pages Security Middleware: Password Gate & Zero Trust Access Enforcer
// Locks down https://auto-clipper-32i.pages.dev so it is NOT public!

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // Allow Telegram Webhook endpoint so Telegram Bot can still send incoming updates
  if (url.pathname.startsWith('/api/telegram_webhook')) {
    return await context.next();
  }

  // Mandatory Admin Access Passcode (Default or Custom from Cloudflare Secrets)
  const ADMIN_PASSCODE = env.ADMIN_PASSCODE || "rawbeew_access_2026";

  // Check Cookie or Custom Header or Query Param
  const authHeader = request.headers.get("Authorization");
  const accessKeyHeader = request.headers.get("X-Access-Key");
  const cookieHeader = request.headers.get("Cookie") || "";
  const queryKey = url.searchParams.get("key");

  const isAuthenticated = 
    (accessKeyHeader === ADMIN_PASSCODE) ||
    (queryKey === ADMIN_PASSCODE) ||
    (cookieHeader.includes(`clip_access=${ADMIN_PASSCODE}`)) ||
    (authHeader && authHeader === `Bearer ${ADMIN_PASSCODE}`);

  // If request contains the passcode in query param ?key=..., set cookie and redirect
  if (queryKey === ADMIN_PASSCODE) {
    const response = new Response(null, {
      status: 302,
      headers: {
        "Location": url.pathname,
        "Set-Cookie": `clip_access=${ADMIN_PASSCODE}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=2592000`
      }
    });
    return response;
  }

  // If authenticated via cookie or header, allow request to proceed
  if (isAuthenticated) {
    return await context.next();
  }

  // Otherwise, lock down with HTTP 401 Access Denied Login Wall
  const loginWallHTML = `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Dashboard Lock — Access Denied</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl text-center space-y-6">
      <div class="w-16 h-16 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400 mx-auto flex items-center justify-center">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
        </svg>
      </div>
      <div>
        <h1 class="text-xl font-bold text-white">Private Dashboard</h1>
        <p class="text-xs text-slate-400 mt-1">This Cloudflare Pages instance is private and restricted.</p>
      </div>
      <form method="GET" action="${url.pathname}" class="space-y-4">
        <input type="password" name="key" placeholder="Enter Admin Access Passcode" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-center text-white focus:outline-none focus:border-rose-500 shadow-inner" required />
        <button type="submit" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-semibold py-3 rounded-xl shadow transition">Unlock Dashboard</button>
      </form>
    </div>
  </body>
  </html>
  `;

  return new Response(loginWallHTML, {
    status: 401,
    headers: { "Content-Type": "text/html" }
  });
}
