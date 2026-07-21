# 🤖 Two-Way Interactive Telegram Bot Command Guide

You can run your entire video creation studio directly from **Telegram chat on your phone or desktop** without opening a web browser!

---

## 💬 Available Chat Commands

| Command | Example Usage | What the Bot Does |
| :--- | :--- | :--- |
| **`/make <prompt>`** | `/make Why do central banks print money?` | Generates a 30s stickman animation short with voiceover & Submagic captions, then sends the MP4 directly back in chat! |
| **`/longform <topic>`** | `/longform The Rise and Fall of Ancient Empires` | Generates a 15-35 min horizontal 16:9 documentary with 5 chapters + auto-extracts 3 promo shorts! |
| **`/research <niche>`** | `/research saas_tech` or `/research true_crime` | Scrapes real-time web signals and replies with the top 3 high-RPM video ideas & CPM estimates! |
| **Paste YouTube Link** | `https://www.youtube.com/watch?v=...` | Automatically downloads the long video, transcribes audio, crops to 9:16, and sends the top viral clips back to your chat! |

---

## 📦 What the Bot Sends Back to Your Telegram Chat

1. 📹 **High-Definition 1080x1920 MP4 Video File Attached** (Watch or save to camera roll with 1 tap).
2. 🎯 **Algorithmatically Optimized A/B Title**:
   `The Dark Truth About Central Bank Money Printing`
3. ⚡ **0-3s Visual Pattern Interrupt Hook**:
   `Stop scrolling! What if every dollar in your wallet was actually a hidden debt?`
4. 📝 **Ready-to-Copy Description & Caption**:
   `Have you ever wondered why central banks print billions out of thin air? Here is the truth about hidden inflation taxes.`
5. 🏷️ **SEO Hashtags**:
   `#Shorts #PersonalFinance #Banking #Wealth #Inflation #FYP #Viral`
6. 🔥 **Virality Score**: `98/100`

---

## 🛠️ How to Enable the Interactive Listener

### Method A: Automatic Telegram Webhook (Zero Setup)
When `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set in your GitHub Actions secrets, any text or issue created on GitHub triggers execution automatically and replies directly to your Telegram chat ID.

### Method B: Continuous Listener Mode
To run the bot as a continuous interactive background worker:
```bash
python worker/telegram_bot_listener.py
```
*(Runs on any free background server or Docker container to listen for incoming Telegram messages 24/7!)*
