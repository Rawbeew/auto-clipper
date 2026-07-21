// Cloudflare Pages Security Middleware: Password Gatekeeper
// Locks down https://auto-clipper-32i.pages.dev so it is NOT open to the public!

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // Allow Telegram Webhook endpoint so Telegram Bot can receive incoming updates
  if (url.pathname.startsWith('/api/telegram_webhook')) {
    return await context.next();
  }

  // Admin Passcode defined in Cloudflare environment or default
  const ADMIN_PASSCODE = env.ADMIN_PASSCODE || "rawbeew_access_2026";

  const accessKeyHeader = request.headers.get("X-Access-Key");
  const cookieHeader = request.headers.get("Cookie") || "";
  const queryKey = url.searchParams.get("key");

  const isAuthenticated = 
    (accessKeyHeader === ADMIN_PASSCODE) ||
    (queryKey === ADMIN_PASSCODE) ||
    (cookieHeader.includes(`clip_access=${ADMIN_PASSCODE}`));

  // Handle Login submission via query param ?key=...
  if (queryKey === ADMIN_PASSCODE) {
    const cleanUrl = url.pathname;
    return new Response(null, {
      status: 302,
      headers: {
        "Location": cleanUrl,
        "Set-Cookie": `clip_access=${ADMIN_PASSCODE}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=2592000`
      }
    });
  }

  // Allow authenticated users to view static assets or API endpoints
  if (isAuthenticated) {
    return await context.next();
  }

  // Lock Wall for unauthenticated public visitors
  const loginWallHTML = `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Dashboard Lock — Restricted Access</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl text-center space-y-6">
      <div class="w-16 h-16 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400 mx-auto flex items-center justify-center shadow-lg shadow-rose-500/20">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
        </svg>
      </div>
      <div>
        <h1 class="text-xl font-bold text-white">Private Media Studio</h1>
        <p class="text-xs text-slate-400 mt-1">This Cloudflare Pages site is restricted and closed to the public.</p>
      </div>
      <form method="GET" action="${url.pathname}" class="space-y-4">
        <input type="password" name="key" placeholder="Enter Admin Access Passcode" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-center text-white focus:outline-none focus:border-rose-500 shadow-inner" required />
        <button type="submit" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-semibold py-3 rounded-xl shadow transition">Unlock Private Studio</button>
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
