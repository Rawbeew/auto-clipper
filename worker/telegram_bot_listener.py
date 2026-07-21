import os
import time
import json
import urllib.request
import subprocess
from trend_researcher import NicheTrendResearcher
from character_manager import CharacterManager

class TelegramBotListener:
    """
    Two-Way Interactive Telegram Bot Engine.
    Commands:
    - /character <name> : Locks onto custom mascot character (tax_advisor, detective_noir, scientist_lab, crypto_trader, casually_explained)
    - /trending [niche]  : Scrapes real-time trending content ideas.
    - /make <prompt>    : Generates 30s stickman short MP4.
    - /longform <topic> : Generates 15-35 min documentary.
    """
    def __init__(self, token: str = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.offset = 0
        self.trend_researcher = NicheTrendResearcher()
        self.char_mgr = CharacterManager()

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
                "🤖 *AutoClipper Interactive AI Studio Bot*\n\n"
                "Send me any command or text prompt to generate video packages instantly:\n\n"
                "🔒 *Lock Character Mascot:* `/character tax_advisor` (Options: `tax_advisor`, `detective_noir`, `scientist_lab`, `crypto_trader`, `casually_explained`)\n"
                "🔥 *Get Trending Ideas:* `/trending saas_tech` or `/trending true_crime`\n"
                "🎨 *Create Stickman Short:* `/make Why central banks print money`\n"
                "📹 *Create 15-35 Min Longform:* `/longform The Rise of AI Startups`\n"
                "🔗 *Clip Long Video:* Just paste any YouTube URL link directly in chat!\n"
            )
            self.send_message(chat_id, welcome_msg)

        elif text.startswith("/character"):
            char_choice = text.replace("/character", "").strip() or "tax_advisor"
            res = self.char_mgr.set_locked_character(char_choice)
            active_name = res["character_data"]["name"]
            desc = res["character_data"]["description"]
            self.send_message(chat_id, f"🔒 *MASCOT CHARACTER PERMANENTLY LOCKED!*\n\n👤 *Active Character:* `{active_name}`\n📝 *Features:* {desc}\n\n_All future videos generated will feature this exact locked character mascot!_")

        elif text.startswith("/trending") or text.startswith("/ideas"):
            parts = text.split(maxsplit=1)
            niche = parts[1].strip() if len(parts) > 1 else "saas_tech"

            self.send_message(chat_id, f"🔍 *Scraping live web trends and calculating virality metrics for:* `{niche}`...")
            
            try:
                report = self.trend_researcher.research_niche_trends(niche)
                ideas = report.get("viral_research_ideas", [])

                formatted_msg = f"🔥 *DAILY TRENDING CONTENT IDEAS FOR:* `{niche.upper()}`\n\n"
                for i, idea in enumerate(ideas[:3]):
                    formatted_msg += (
                        f"*{i+1}. {idea.get('concept_title', 'Viral Idea')}*\n"
                        f"💵 *Estimated CPM:* {idea.get('estimated_cpm_range', '$15-$35 CPM')}\n"
                        f"📌 *Format:* {idea.get('recommended_format', 'Short / Longform')}\n"
                        f"💡 *Hook Angle:* {idea.get('hook_angle', 'Curiosity Gap')}\n"
                        f"🚀 *Quick Trigger:* `/make {idea.get('concept_title', '')}`\n\n"
                    )

                formatted_msg += "👉 *Copy any quick trigger line above and reply in chat to generate the video!*"
                self.send_message(chat_id, formatted_msg)

            except Exception as e:
                self.send_message(chat_id, f"⚠️ Error fetching trend ideas: {e}")

        elif text.startswith("/longform"):
            topic = text.replace("/longform", "").strip() or "The History of Artificial Intelligence"
            self.send_message(chat_id, f"🎬 *Initiating 15-Minute Longform Documentary Build for:* \"{topic}\"\n\n⚡ *Status:* Groq LPU 5-chapter scriptwriting & multi-character rendering in progress...")

            cmd = ["python", "worker/main.py", "--longform", "--topic", topic, "--minutes", "15"]
            try:
                subprocess.Popen(cmd)
                self.send_message(chat_id, "⚙️ *Pipeline Dispatched!* The full 16:9 documentary + 3 auto-cut promo shorts will be delivered to this chat as soon as rendering completes.")
            except Exception as e:
                self.send_message(chat_id, f"⚠️ Execution Error: {e}")

        else:
            clean_prompt = text.replace("/make", "").strip()
            if not clean_prompt:
                clean_prompt = "Why do central banks print money?"

            self.send_message(chat_id, f"🎨 *Generating Animated Stickman Short for:* \"{clean_prompt}\"\n\n⚡ *Status:* Groq LPU scriptwriting + OpenAI Onyx voice synthesis...")

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
