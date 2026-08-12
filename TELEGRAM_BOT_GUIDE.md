# ✈️ How to Receive Rendered Videos Directly on Telegram

Instead of automatically publishing videos to social media right away, you can have your pipeline send the finished **9:16 vertical short MP4 video files** directly to your **Telegram DM or private Telegram channel** so you can review, download, or share them from your phone!

---

## 🛠️ Step-by-Step Setup (2 Minutes)

### Step 1: Create a Free Telegram Bot
1. Open Telegram on your phone or desktop and search for **`@BotFather`**.
2. Start a chat with BotFather and send the command:
   ```text
   /newbot
   ```
3. Follow the instructions to give your bot a name (e.g. `My AutoClipper Bot`).
4. BotFather will generate an HTTP API token that looks like:
   ```text
   7123456789:AAFgX9_xYz1234567890abcdefghijklm
   ```
5. Copy this token — this is your `TELEGRAM_BOT_TOKEN`.

---

### Step 2: Get Your Personal Telegram Chat ID
1. Search for **`@userinfobot`** on Telegram.
2. Click **Start** or send any message.
3. The bot will respond with your Telegram numerical **`Id`** (e.g. `123456789`).
4. This numerical ID is your `TELEGRAM_CHAT_ID`.
5. Open a chat with your new bot created in Step 1 and click **Start** (so your bot has permission to message you).

---

### Step 3: Add Secrets to Your Private GitHub Actions Repo

1. Open **[github.com/Rawbeew/auto-clipper/settings/secrets/actions](https://github.com/Rawbeew/auto-clipper/settings/secrets/actions)**.
2. Add secret **`TELEGRAM_BOT_TOKEN`**: Paste your token from BotFather.
3. Add secret **`TELEGRAM_CHAT_ID`**: Paste your numerical ID from userinfobot.

---

## 🚀 How It Works in Practice

1. Whenever you generate a **Stickman Video** or **Long-Video Clip** via your web dashboard ([https://auto-clipper-32i.pages.dev](https://auto-clipper-32i.pages.dev)) or GitHub:
2. The pipeline renders the 1080x1920 9:16 vertical video with animated stickmen, voiceovers, and subtitles.
3. It immediately sends the video attachment to your Telegram chat with a summary caption:
   ```text
   🎬 New Short Generated!

   📌 Title: Stickman: Why Sleep Is Important
   💡 Hook: "What happens to your brain when you skip sleep?"
   🔥 Virality Score: 98/100

   📱 Ready to review, download, or post to YouTube, TikTok & IG Reels!
   ```
4. You can tap the video in Telegram to watch it in full HD, download it directly to your camera roll, or forward it to team members!
