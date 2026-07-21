// Cloudflare Pages Function: /
// Enforces middleware security lock wall on root URL

export async function onRequest(context) {
  // Pass to _middleware.js which checks cookie/passcode and serves dashboard or password lock wall
  return await context.next();
}
