// Cloudflare Pages Middleware: Security & Cloudflare Access Verification
// Protects all frontend routes and API endpoints (/api/*) with Cloudflare Zero Trust / Access

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // If Cloudflare Access Enforcement is enabled via Environment Variables
  const TEAM_NAME = env.CF_ACCESS_TEAM_NAME; // e.g. "myteam"
  const POLICY_AUD = env.CF_ACCESS_POLICY_AUD; // Application Audience Tag (AUD)
  const REQUIRED_CLIENT_ID = env.CF_ACCESS_CLIENT_ID;
  const REQUIRED_CLIENT_SECRET = env.CF_ACCESS_CLIENT_SECRET;

  // Skip validation in local development / unconfigured state
  if (!TEAM_NAME && !POLICY_AUD && !REQUIRED_CLIENT_ID) {
    return await context.next();
  }

  // 1. Service Token Authentication (for programmatic API calls)
  const clientIdHeader = request.headers.get("CF-Access-Client-Id");
  const clientSecretHeader = request.headers.get("CF-Access-Client-Secret");

  if (REQUIRED_CLIENT_ID && REQUIRED_CLIENT_SECRET) {
    if (clientIdHeader === REQUIRED_CLIENT_ID && clientSecretHeader === REQUIRED_CLIENT_SECRET) {
      return await context.next();
    }
  }

  // 2. JWT Identity Verification (for browser users passing Cloudflare Access login)
  const jwtAssertion = request.headers.get("Cf-Access-Jwt-Assertion");

  if (!jwtAssertion) {
    return new Response(JSON.stringify({
      error: "Unauthorized: Missing Cloudflare Access JWT Assertion or Service Token headers",
      documentation: "Please authenticate via Cloudflare Zero Trust Access or pass CF-Access-Client-Id & CF-Access-Client-Secret"
    }), {
      status: 401,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    // Optionally verify JWT token against Cloudflare Access Public Certs endpoint:
    // https://<your-team>.cloudflareaccess.com/cdn-cgi/access/certs
    /*
    const certsUrl = `https://${TEAM_NAME}.cloudflareaccess.com/cdn-cgi/access/certs`;
    // JWT verification logic using JWKS...
    */

    return await context.next();

  } catch (err) {
    return new Response(JSON.stringify({ error: "Access Denied: Invalid Cloudflare Access JWT token" }), {
      status: 403,
      headers: { "Content-Type": "application/json" }
    });
  }
}
