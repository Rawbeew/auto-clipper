import os
import json
import subprocess

class DiscordNotifier:
    """
    Delivers rendered MP4 videos directly to your Discord server channel via Webhooks
    with complete titles, descriptions, and hashtags formatted in Markdown codeblocks.
    """
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

    def generate_tags(self, title: str) -> str:
        words = [w.strip("#,.!?").capitalize() for w in title.split() if len(w) > 3]
        base_tags = ["#Shorts", "#Viral", "#FYP", "#Trending", "#Animation"]
        custom_tags = [f"#{w}" for w in words[:5]]
        return " ".join(list(dict.fromkeys(base_tags + custom_tags)))

    def send_video(self, video_filepath: str, title: str, description: str, virality_score: int = 98) -> bool:
        if not self.webhook_url:
            print("Discord Webhook URL missing. Skipping Discord dispatch.")
            return False

        if not os.path.exists(video_filepath):
            print(f"Video file not found: {video_filepath}")
            return False

        hashtags = self.generate_tags(title)

        content = (
            f"🎬 **NEW SHORT READY FOR POSTING!**\n\n"
            f"📌 **TITLE:**\n`{title}`\n\n"
            f"📝 **CAPTION / DESCRIPTION:**\n```{description}```\n\n"
            f"🏷️ **HASHTAGS & TAGS:**\n`{hashtags}`\n\n"
            f"🔥 **VIRALITY SCORE:** {virality_score}/100"
        )

        cmd = [
            "curl", "-s", "-X", "POST", self.webhook_url,
            "-F", f"content={content}",
            "-F", f"file=@{video_filepath}"
        ]

        try:
            print(f"📤 Transmitting finished MP4 short & metadata package to Discord...")
            subprocess.run(cmd, check=True)
            print("✅ Video package successfully delivered to Discord!")
            return True
        except Exception as e:
            print(f"Error delivering to Discord: {e}")
            return False
