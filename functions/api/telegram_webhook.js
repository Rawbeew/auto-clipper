// Cloudflare Pages Function: /api/telegram_webhook
// Receives live incoming messages from Telegram Bot and dispatches instantly

export async function onRequestPost(context) {
  try {
    const update = await context.request.json();
    const message = update.message;

    if (!message || !message.text) {
      return new Response("OK", { status: 200 });
    }

    const chatId = message.chat.id;
    const rawText = message.text.trim();
    const textLower = rawText.toLowerCase();

    const BOT_TOKEN = context.env.TELEGRAM_BOT_TOKEN || "8896330204:AAEA7qU8xFs60slVfRwMCJ0971iRVzMV0vg";
    const GITHUB_PAT = context.env.GH_PAT || context.env.GITHUB_PAT || "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";
    const GITHUB_REPO = context.env.GITHUB_REPO || "Rawbeew/auto-clipper";

    // Helper: Reply directly to Telegram Chat
    async function replyTelegram(msgText) {
      if (BOT_TOKEN) {
        await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: chatId, text: msgText, parse_mode: 'Markdown' })
        });
      }
    }

    // 1. Natural Language Matching for "Get fresh viral ideas" / "trending"
    if (textLower.includes("fresh viral ideas") || textLower.includes("trending") || textLower.includes("ideas") || rawText.startsWith("/trending") || rawText.startswith("/ideas")) {
      await replyTelegram("🔍 *Scraping live web trends across AI, True Crime, Finance & Tech...* \n\nAnalyzing real-time signals via Groq LPU...");

      // Dispatch research mode to GitHub Actions
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
            video_url: rawText,
            mode: 'research',
            chat_id: chatId
          }
        })
      });

      return new Response("OK", { status: 200 });
    }

    // 2. Default: Treat as Stickman Video Creation / YouTube URL Clip
    await replyTelegram(`🎨 *Request Received:* "${rawText}"\n\n⚡ *Initiating pipeline:* Groq LPU Llama 3.3 scriptwriting + OpenAI voice synthesis...`);

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
          video_url: rawText,
          chat_id: chatId
        }
      })
    });

    return new Response("OK", { status: 200 });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
