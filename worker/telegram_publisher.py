import os
import json
import subprocess
import urllib.request

class TelegramNotifier:
    """
    Delivers generated 9:16 vertical short videos and Stickman animations 
    directly to your Telegram chat or channel via Telegram Bot API.
    """
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    def send_video(self, video_filepath: str, title: str, hook_text: str, virality_score: int = 95) -> bool:
        """
        Uploads the MP4 video directly to Telegram chat with rich formatted text.
        """
        if not self.bot_token or not self.chat_id:
            print("Telegram Bot Token or Chat ID missing. Skipping Telegram notification.")
            return False

        if not os.path.exists(video_filepath):
            print(f"Video file not found for Telegram upload: {video_filepath}")
            return False

        caption = (
            f"🎬 *New Short Generated!*\n\n"
            f"📌 *Title:* {title}\n"
            f"💡 *Hook:* \"{hook_text}\"\n"
            f"🔥 *Virality Score:* {virality_score}/100\n\n"
            f"📱 Ready to post to YouTube Shorts, TikTok & Instagram Reels!"
        )

        url = f"https://api.telegram.org/bot{self.bot_token}/sendVideo"
        
        # Uses curl subprocess or multipart form upload for reliable large video transmission up to 50MB
        cmd = [
            "curl", "-s", "-X", "POST", url,
            "-F", f"chat_id={self.chat_id}",
            "-F", f"caption={caption}",
            "-F", "parse_mode=Markdown",
            "-F", f"video=@{video_filepath}"
        ]

        try:
            print(f"📤 Uploading finished video '{title}' directly to Telegram...")
            out = subprocess.check_output(cmd).decode("utf-8")
            res = json.loads(out)
            if res.get("ok"):
                print("✅ Video successfully delivered to Telegram!")
                return True
            else:
                print(f"Telegram API Error: {res}")
                return False
        except Exception as e:
            print(f"Error sending video to Telegram: {e}")
            return False

if __name__ == "__main__":
    import sys
    notifier = TelegramNotifier()
    if len(sys.argv) > 1:
        notifier.send_video(sys.argv[1], "Test Video", "Sample hook description", 96)
