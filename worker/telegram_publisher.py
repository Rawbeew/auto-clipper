import os
import json
import subprocess

class TelegramNotifier:
    """
    Delivers rendered 9:16 MP4 video files directly to your Telegram chat or channel
    along with complete copy-paste posting packages (Titles, Captions, and SEO Hashtags).
    """
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    def generate_tags(self, title: str) -> str:
        words = [w.strip("#,.!?").capitalize() for w in title.split() if len(w) > 3]
        base_tags = ["#Shorts", "#Viral", "#FYP", "#Trending", "#Animation"]
        custom_tags = [f"#{w}" for w in words[:5]]
        return " ".join(list(dict.fromkeys(base_tags + custom_tags)))

    def send_video(self, video_filepath: str, title: str, description: str, virality_score: int = 98) -> bool:
        if not self.bot_token or not self.chat_id:
            print("Telegram credentials missing. Skipping Telegram dispatch.")
            return False

        if not os.path.exists(video_filepath):
            print(f"Video file not found: {video_filepath}")
            return False

        hashtags = self.generate_tags(title)

        caption = (
            f"🎬 *READY TO POST: NEW SHORT GENERATED!*\n\n"
            f"📌 *TITLE (CTR Optimized):*\n{title}\n\n"
            f"📝 *CAPTION & DESCRIPTION:*\n{description}\n\n"
            f"🏷️ *HASHTAGS & TAGS:*\n`{hashtags}`\n\n"
            f"🔥 *VIRALITY SCORE:* {virality_score}/100\n\n"
            f"📱 _Download video attachment below and paste title/caption directly to YouTube Shorts, TikTok & Instagram Reels!_"
        )

        url = f"https://api.telegram.org/bot{self.bot_token}/sendVideo"
        
        cmd = [
            "curl", "-s", "-X", "POST", url,
            "-F", f"chat_id={self.chat_id}",
            "-F", f"caption={caption}",
            "-F", "parse_mode=Markdown",
            "-F", f"video=@{video_filepath}"
        ]

        try:
            print(f"📤 Transmitting finished MP4 short & metadata package to Telegram...")
            out = subprocess.check_output(cmd).decode("utf-8")
            res = json.loads(out)
            if res.get("ok"):
                print("✅ Video package successfully delivered to Telegram!")
                return True
            else:
                print(f"Telegram API Error: {res}")
                return False
        except Exception as e:
            print(f"Error delivering to Telegram: {e}")
            return False
