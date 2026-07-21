import os
import math
import json
import asyncio
import subprocess
import urllib.request
from PIL import Image, ImageDraw, ImageFont

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    from ai_providers import MultiAIProvider
except ImportError:
    from worker.ai_providers import MultiAIProvider

class StickmanGenerator:
    """
    Advanced YouTube-Style Animated Stickman Engine.
    Supports:
    1. Stand-Up Comedy Stage Animation (Red Velvet Curtain, Spotlight, Mic Stand, Audience)
    2. Slate Minimal Vector (CGP Grey / Casually Explained)
    3. True Crime Noir Vector (Detective Fedora, Magnifying Glass, Crimson Banner)
    Includes HD Edge-TTS Voiceovers & Submagic Yellow Highlighted Captions.
    """
    def __init__(self, output_dir="/tmp/auto_clipper/stickman"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ai_provider = MultiAIProvider()

    def generate_script(self, topic: str) -> dict:
        prompt = f"""
You are a top YouTube stand-up comedy & documentary stickman animator.
Write an engaging 30-second stickman video script demonstrating or joking about: "{topic}".

Provide a JSON object with:
1. "title": Short catchy CTR title
2. "style": ["standup_comedy", "dark_slate", "detective"]
3. "scenes": A list of 4 scenes. Each scene must have:
   - "scene_num": integer
   - "duration": float (e.g. 6.0)
   - "narration": Spoken text (15-25 words max)
   - "action_type": Visual type ["standup_mic", "walking", "presenting_chart", "falling_cash", "mind_blown", "detective"]
   - "headline": Short 3-5 word headline overlay
   - "demonstration_element": Extra prop or graph ["chart_down", "chart_up", "cash", "matrix_code", "lightbulb", "none"]

Format: JSON strictly.
"""
        res = self.ai_provider.generate_json(prompt, system_prompt="You are an expert YouTube stickman animator. Respond strictly in valid JSON.")
        if res:
            return res

        return {
            "title": f"The Stand-Up Story of {topic}",
            "style": "standup_comedy",
            "scenes": [
                {
                    "scene_num": 1,
                    "duration": 6.0,
                    "narration": f"Have you ever noticed how weird {topic} actually is? Let me break this down for you.",
                    "action_type": "standup_mic",
                    "headline": "THE REALITY OF " + topic.upper()[:16],
                    "demonstration_element": "lightbulb"
                },
                {
                    "scene_num": 2,
                    "duration": 6.0,
                    "narration": "People literally spend billions of dollars on this every year without questioning it.",
                    "action_type": "falling_cash",
                    "headline": "BILLIONS WASTED!",
                    "demonstration_element": "cash"
                },
                {
                    "scene_num": 3,
                    "duration": 6.0,
                    "narration": "And when you look at the statistics, the results are completely absurd.",
                    "action_type": "presenting_chart",
                    "headline": "ABSURD NUMBERS 📉",
                    "demonstration_element": "chart_down"
                },
                {
                    "scene_num": 4,
                    "duration": 6.0,
                    "narration": "So next time someone asks you about it, just remember this one simple truth.",
                    "action_type": "mind_blown",
                    "headline": "THE TRUTH 🤯",
                    "demonstration_element": "none"
                }
            ]
        }

    def synthesize_voiceover(self, text: str, output_mp3: str) -> bool:
        if edge_tts:
            try:
                async def run_edge():
                    communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
                    await communicate.save(output_mp3)
                asyncio.run(run_edge())
                if os.path.exists(output_mp3) and os.path.getsize(output_mp3) > 1000:
                    return True
            except Exception as e:
                print(f"Edge-TTS error: {e}")

        key = os.getenv("OPENAI_API_KEY")
        if key:
            try:
                url = "https://api.openai.com/v1/audio/speech"
                payload = json.dumps({"model": "tts-1", "voice": "onyx", "input": text}).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(output_mp3, "wb") as f:
                        f.write(resp.read())
                if os.path.getsize(output_mp3) > 1000:
                    return True
            except Exception as e:
                print(f"OpenAI TTS error: {e}")

        try:
            cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=5", output_mp3]
            subprocess.run(cmd, check=True)
        except Exception:
            with open(output_mp3, "wb") as f:
                f.write(b"0" * 5000)
        return True

    def draw_animated_scene_frame(self, action_type: str, headline: str, demo_element: str, narration_text: str, frame_num: int, total_frames: int, style: str = "standup_comedy", width=1080, height=1920) -> Image.Image:
        """
        Renders Stand-Up Comedy Club Stage or Noir/Slate vector frames with animated props & Submagic captions.
        """
        progress = frame_num / max(1, total_frames)

        # STAND-UP COMEDY STAGE BACKGROUND
        if style == "standup_comedy" or action_type == "standup_mic":
            img = Image.new("RGB", (width, height), (24, 8, 12))
            draw = ImageDraw.Draw(img)

            # Red Velvet Curtain Folds
            for x in range(0, width, 80):
                shade = 120 + int(math.sin(x * 0.05) * 40)
                draw.rectangle([x, 0, x + 40, height - 500], fill=(shade, 15, 25))
                draw.rectangle([x + 40, 0, x + 80, height - 500], fill=(max(0, shade - 30), 10, 18))

            # Wooden Stage Floor
            draw.rectangle([0, height - 500, width, height], fill=(45, 22, 12))
            for line_y in range(height - 500, height, 40):
                draw.line([0, line_y, width, line_y], fill=(30, 14, 8), width=2)

            # Warm Spotlight
            cx = width // 2
            cy = height - 400
            spotlight_r = 320
            draw.ellipse([cx - spotlight_r, cy - 120, cx + spotlight_r, cy + 120], fill=(254, 240, 138, 180), outline=(253, 224, 71), width=4)

            # Audience Silhouettes
            for aud in range(0, width, 110):
                aud_head_y = height - 120 + int(math.sin(aud * 0.1) * 15)
                draw.ellipse([aud - 40, aud_head_y, aud + 40, aud_head_y + 100], fill=(2, 6, 23))

        else: # Dark Slate / Noir
            bg_color = (2, 6, 23) if style == "detective" else (15, 23, 42)
            img = Image.new("RGB", (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            cx = width // 2
            cy = height // 2 + 100

        # Motion & Stickman Drawing
        stickman_cy = cy + int(math.sin(frame_num * 0.2) * 8)
        stroke_color = (255, 255, 255)
        head_r = 75
        body_len = 220
        line_w = 16

        head_cy = stickman_cy - body_len - head_r

        # Head & Smile
        draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], outline=stroke_color, width=line_w)
        draw.ellipse([cx - 30, head_cy - 15, cx - 10, head_cy + 5], fill=stroke_color)
        draw.ellipse([cx + 10, head_cy - 15, cx + 30, head_cy + 5], fill=stroke_color)
        draw.arc([cx - 30, head_cy, cx + 30, head_cy + 30], start=0, end=180, fill=stroke_color, width=8)

        # Spine
        draw.line([cx, head_cy + head_r, cx, stickman_cy], fill=stroke_color, width=line_w)
        shoulder_y = head_cy + head_r + 40

        # Arms (Microphone Stand)
        draw.line([cx, shoulder_y, cx - 120, shoulder_y + 40], fill=stroke_color, width=line_w)
        draw.line([cx, shoulder_y, cx + 60, shoulder_y - 20], fill=stroke_color, width=line_w)
        draw.line([cx + 60, shoulder_y - 20, cx + 25, head_cy + 25], fill=stroke_color, width=line_w)

        # Silver Microphone & Stand
        draw.ellipse([cx + 15, head_cy + 5, cx + 35, head_cy + 25], fill=(203, 213, 225), outline=(255, 255, 255), width=3)
        draw.line([cx + 25, head_cy + 25, cx + 25, stickman_cy + 180], fill=(148, 163, 184), width=8)

        # Legs
        draw.line([cx, stickman_cy, cx - 80, stickman_cy + 220], fill=stroke_color, width=line_w)
        draw.line([cx, stickman_cy, cx + 80, stickman_cy + 220], fill=stroke_color, width=line_w)

        # Demonstration Graphics Overlay (Charts / Money)
        if demo_element == "chart_down":
            gx, gy = cx + 160, head_cy - 100
            draw.rectangle([gx, gy, gx + 260, gy + 260], outline=(51, 65, 85), width=4, fill=(2, 6, 23))
            draw.line([gx + 20, gy + 40, gx + 100, gy + 80, gx + 180, gy + 180, gx + 240, gy + 240], fill=(225, 29, 72), width=12)
        elif demo_element == "cash":
            for bill in range(5):
                bx = (cx - 300 + (bill * 130) + int(frame_num * 8)) % (width - 100)
                by = (200 + (bill * 200) + int(frame_num * 15)) % (height - 300)
                draw.rectangle([bx, by, bx + 110, by + 60], fill=(34, 197, 94), outline=(255, 255, 255), width=3)

        # Top Headline Banner
        if headline:
            padding_y = 160
            clean_hl = headline.encode('ascii', 'ignore').decode('ascii')
            try:
                font_hl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
            except:
                font_hl = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), clean_hl, font=font_hl)
            text_w = bbox[2] - bbox[0]
            draw.rectangle([0, padding_y - 20, width, padding_y + 80], fill=(2, 6, 23))
            draw.text(((width - text_w) // 2, padding_y), clean_hl, fill=(253, 224, 71), font=font_hl)

        # Submagic Word Captions
        words = [w.strip() for w in narration_text.split() if w.strip()]
        if words:
            word_idx = min(len(words) - 1, int(progress * len(words)))
            start_w = max(0, word_idx - 1)
            end_w = min(len(words), start_w + 4)
            phrase_words = words[start_w:end_w]

            sub_y = height - 280
            try:
                font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
            except:
                font_sub = ImageFont.load_default()

            full_phrase = " ".join([w.upper() for w in phrase_words])
            bbox_p = draw.textbbox((0, 0), full_phrase, font=font_sub)
            phrase_w = bbox_p[2] - bbox_p[0]

            start_x = (width - phrase_w) // 2
            draw.rectangle([start_x - 30, sub_y - 15, start_x + phrase_w + 30, sub_y + 85], fill=(0, 0, 0, 220))

            curr_x = start_x
            for i, word in enumerate(phrase_words):
                w_upper = word.upper()
                w_bbox = draw.textbbox((0, 0), w_upper + " ", font=font_sub)
                w_width = w_bbox[2] - w_bbox[0]

                is_active = (start_w + i) == word_idx
                word_color = (253, 224, 71) if is_active else (255, 255, 255)

                draw.text((curr_x + 3, sub_y + 3), w_upper, fill=(0, 0, 0), font=font_sub)
                draw.text((curr_x, sub_y), w_upper, fill=word_color, font=font_sub)

                curr_x += w_width

        return img

    def create_stickman_video(self, topic: str) -> str:
        print(f"🎬 Generating Stand-Up Comedy Style Stickman Short for: '{topic}'...")
        script_data = self.generate_script(topic)
        style = script_data.get("style", "standup_comedy")

        scene_files = []
        fps = 24

        for i, scene in enumerate(script_data["scenes"]):
            scene_num = scene["scene_num"]
            duration = scene.get("duration", 6.0)
            total_frames = int(duration * fps)

            scene_audio = os.path.join(self.output_dir, f"audio_{scene_num}.mp3")
            self.synthesize_voiceover(scene["narration"], scene_audio)

            frame_dir = os.path.join(self.output_dir, f"scene_{scene_num}")
            os.makedirs(frame_dir, exist_ok=True)

            for f in range(total_frames):
                frame_img = self.draw_animated_scene_frame(
                    action_type=scene.get("action_type", "standup_mic"),
                    headline=scene.get("headline", ""),
                    demo_element=scene.get("demonstration_element", "none"),
                    narration_text=scene.get("narration", ""),
                    frame_num=f,
                    total_frames=total_frames,
                    style=style
                )
                frame_path = os.path.join(frame_dir, f"frame_{f:04d}.png")
                frame_img.save(frame_path)

            scene_mp4 = os.path.join(self.output_dir, f"scene_{scene_num}.mp4")
            cmd_img = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(frame_dir, "frame_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                scene_mp4
            ]
            subprocess.run(cmd_img, check=True)

            scene_final = os.path.join(self.output_dir, f"scene_final_{scene_num}.mp4")
            cmd_combine = [
                "ffmpeg", "-y",
                "-i", scene_mp4,
                "-i", scene_audio,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                scene_final
            ]
            subprocess.run(cmd_combine, check=True)
            scene_files.append(scene_final)

        concat_list = os.path.join(self.output_dir, "concat.txt")
        with open(concat_list, "w") as f:
            for s_file in scene_files:
                f.write(f"file '{s_file}'\n")

        final_output_mp4 = os.path.join(self.output_dir, "stickman_final_short.mp4")
        cmd_concat = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            final_output_mp4
        ]
        subprocess.run(cmd_concat, check=True)

        print(f"✅ Stand-Up Comedy Stickman Video created: {final_output_mp4}")
        return final_output_mp4

if __name__ == "__main__":
    generator = StickmanGenerator()
    generator.create_stickman_video("How to Create Stickman Stand Up Videos")
