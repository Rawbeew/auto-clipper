import os
import time
import json
import urllib.request
import subprocess

class TelegramBotListener:
    """
    Two-Way Interactive Telegram Bot Engine.
    Allows users to text prompts, YouTube URLs, or commands like /make, /longform, and /research 
    directly in Telegram, receiving the finished MP4 videos and metadata packages back in chat!
    """
    def __init__(self, token: str = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.offset = 0

    def send_message(self, chat_id: int, text: str, parse_mode: str = "Markdown") -> bool:
        if not self.token:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }).encode("utf-8")
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return True
        except Exception as e:
            print(f"Telegram sendMessage error: {e}")
            return False

    def handle_command(self, chat_id: int, text: str):
        print(f"📩 Received Telegram command from chat_id {chat_id}: '{text}'")

        if text.startswith("/start") or text.startswith("/help"):
            welcome_msg = (
                "🤖 *Welcome to AutoClipper Interactive AI Bot!*\n\n"
                "Send me any command or text prompt to create video content instantly:\n\n"
                "• *Create Stickman Short:* `/make Why do central banks print money?`\n"
                "• *Create 15-35 Min Longform:* `/longform The Rise and Fall of Ancient Empires`\n"
                "• *Research Niche Trends:* `/research saas_tech` or `/research legal_tax`\n"
                "• *Clip Source Video:* Just paste any YouTube URL link directly in chat!\n"
            )
            self.send_message(chat_id, welcome_msg)

        elif text.startswith("/research"):
            niche = text.replace("/research", "").strip() or "saas_tech"
            self.send_message(chat_id, f"🔍 *Scraping real-time web signals and high-RPM concepts for niche:* `{niche}`...")
            
            cmd = ["python", "worker/main.py", "--research", niche]
            try:
                out = subprocess.check_output(cmd).decode("utf-8")
                self.send_message(chat_id, f"📈 *Live Trend Research Report:*\n```json\n{out[:3000]}\n```")
            except Exception as e:
                self.send_message(chat_id, f"⚠️ Research Error: {e}")

        elif text.startswith("/longform"):
            topic = text.replace("/longform", "").strip() or "The Untold History of Artificial Intelligence"
            self.send_message(chat_id, f"🎬 *Initiating 15-Minute Longform Documentary Build for:* \"{topic}\"\n\n⚡ *Status:* Groq LPU 5-chapter scriptwriting & multi-character rendering in progress...")

            cmd = ["python", "worker/main.py", "--longform", "--topic", topic, "--minutes", "15"]
            try:
                subprocess.Popen(cmd) # Background process execution
                self.send_message(chat_id, "⚙️ *Pipeline Dispatched!* The full 16:9 documentary + 3 auto-cut promo shorts will be delivered to this chat as soon as rendering completes.")
            except Exception as e:
                self.send_message(chat_id, f"⚠️ Execution Error: {e}")

        else: # Default: Treat as Stickman Short prompt or YouTube URL
            clean_prompt = text.replace("/make", "").strip()
            if not clean_prompt:
                clean_prompt = "Why do central banks print money?"

            self.send_message(chat_id, f"🎨 *Generating Animated Stickman Short for:* \"{clean_prompt}\"\n\n⚡ *Status:* Groq LPU Llama 3.3 scriptwriting + OpenAI Onyx voice synthesis...")

            if clean_prompt.startswith("http://") or clean_prompt.startswith("https://"):
                cmd = ["python", "worker/main.py", "--url", clean_prompt]
            else:
                cmd = ["python", "worker/main.py", "--stickman", "--topic", clean_prompt]

            try:
                subprocess.Popen(cmd)
                self.send_message(chat_id, "⚙️ *Short Pipeline Active!* Your video package with CTR titles, captions, and hashtags will be sent directly to this chat in ~1-2 minutes.")
            except Exception as e:
                self.send_message(chat_id, f"⚠️ Execution Error: {e}")

    def poll_updates(self):
        """
        Runs continuous long-polling loop to receive messages sent to the bot.
        """
        if not self.token:
            print("TELEGRAM_BOT_TOKEN missing. Listener idle.")
            return

        print("🤖 Telegram Two-Way Bot Listener Started! Waiting for incoming chat prompts...")
        while True:
            url = f"https://api.telegram.org/bot{self.token}/getUpdates?offset={self.offset}&timeout=20"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "AutoClipperTelegramBot/1.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    updates = data.get("result", [])
                    for update in updates:
                        self.offset = update["update_id"] + 1
                        message = update.get("message", {})
                        chat_id = message.get("chat", {}).get("id")
                        text = message.get("text", "")
                        if chat_id and text:
                            self.handle_command(chat_id, text)
            except Exception as e:
                time.sleep(5)

if __name__ == "__main__":
    listener = TelegramBotListener()
    listener.poll_updates()
