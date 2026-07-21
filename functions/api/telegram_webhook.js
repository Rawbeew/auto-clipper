// Cloudflare Pages Function: /api/telegram_webhook
// Receives live incoming messages from Telegram Bot and dispatches to GitHub Actions

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

    async function replyTelegram(msgText) {
      if (BOT_TOKEN) {
        try {
          await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, text: msgText, parse_mode: 'Markdown' })
          });
        } catch (e) {
          console.error("Telegram reply failed:", e);
        }
      }
    }

    // A. Trend Research matching (/trending, /ideas, "fresh viral ideas")
    if (textLower.includes("fresh viral ideas") || textLower.includes("trending") || textLower.includes("ideas") || rawText.startsWith("/trending") || rawText.startsWith("/ideas")) {
      await replyTelegram("🔍 *Scraping live web trends across AI, True Crime, Finance & Tech...* \n\nAnalyzing real-time signals via Groq LPU...");

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

    // B. Longform Documentary matching (/longform)
    if (rawText.startsWith("/longform")) {
      const topic = rawText.replace("/longform", "").trim() || "AI Technology Secrets";
      await replyTelegram(`🎬 *Initiating 15-Minute Longform Documentary Build for:* "${topic}"\n\n⚡ *Status:* Groq LPU 5-chapter scriptwriting & multi-character rendering in progress...`);

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
            video_url: topic,
            mode: 'longform',
            chat_id: chatId
          }
        })
      });

      return new Response("OK", { status: 200 });
    }

    // C. Default: Video Generation Prompt (/make <topic>, or any topic/link text)
    const cleanPrompt = rawText.replace("/make", "").strip ? rawText.replace("/make", "").trim() : rawText;
    await replyTelegram(`🎨 *Request Received:* "${cleanPrompt}"\n\n⚡ *Initiating Video Pipeline:* Groq LPU scriptwriting + OpenAI voice synthesis + FFmpeg rendering...\n\n_Your finished MP4 video package will be delivered directly to this chat in ~1-2 minutes!_`);

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
          video_url: cleanPrompt,
          mode: 'stickman',
          chat_id: chatId
        }
      })
    });

    return new Response("OK", { status: 200 });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
