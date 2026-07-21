// Cloudflare Pages Function: /api/telegram_webhook
// Receives live incoming text messages from Telegram Bot and dispatches to GitHub Actions runner

export async function onRequestPost(context) {
  try {
    const update = await context.request.json();
    const message = update.message;

    if (!message || !message.text) {
      return new Response("OK", { status: 200 });
    }

    const chatId = message.chat.id;
    const text = message.text.trim();

    const GITHUB_PAT = context.env.GH_PAT || context.env.GITHUB_PAT;
    const GITHUB_REPO = context.env.GITHUB_REPO || "Rawbeew/auto-clipper";

    if (GITHUB_PAT) {
      // Dispatch incoming command to GitHub Actions serverless runner
      await fetch(`https://api.github.com/repos/${GITHUB_REPO}/dispatches`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${GITHUB_PAT}`,
          'Accept': 'application/vnd.github+json',
          'User-Agent': 'Cloudflare-Pages-TelegramHook',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          event_type: 'make_short',
          client_payload: {
            video_url: text,
            chat_id: chatId
          }
        })
      });
    }

    return new Response("OK", { status: 200 });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
