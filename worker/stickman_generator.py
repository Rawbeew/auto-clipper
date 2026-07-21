import os
import math
import json
import subprocess
import urllib.request
from PIL import Image, ImageDraw, ImageFont

try:
    from ai_providers import MultiAIProvider
except ImportError:
    from worker.ai_providers import MultiAIProvider

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class StickmanGenerator:
    """
    Generates AI animated stickman short videos from text prompts/topics.
    Utilizes MultiAIProvider (Groq, SiliconFlow, Gemini, OpenAI) for scriptwriting
    and OpenAI TTS / Edge-TTS for HD voiceover narration.
    """
    def __init__(self, output_dir="/tmp/auto_clipper/stickman"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ai_provider = MultiAIProvider()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_key) if (OpenAI and self.openai_key) else None

    def generate_script(self, topic: str) -> dict:
        prompt = f"""
You are a viral YouTube Shorts and TikTok stickman animator (like Casually Explained / CGP Grey).
Write a captivating, fast-paced 30-second stickman video script about: "{topic}".

Provide a JSON object with:
1. "title": Short catchy video title.
2. "scenes": A list of 4 to 6 scenes. Each scene must have:
   - "scene_num": integer
   - "duration": float (duration in seconds, e.g. 5.0)
   - "narration": Short text spoken in voiceover
   - "pose": Stickman pose choice. Choose from: ["thinking", "pointing", "mind_blown", "happy", "running", "working_laptop", "confused", "celebrating"]
   - "text_overlay": Big punchy headline text displayed on screen (3-6 words max)
   - "prop": Optional prop icon or emoji ["lightbulb", "money", "space", "computer", "fire", "question_mark", "none"]

Format: JSON strictly.
"""
        res = self.ai_provider.generate_json(prompt, system_prompt="You are an expert viral stickman animator scriptwriter. Respond strictly in valid JSON.")
        if res:
            return res

        return {
            "title": f"The Truth About {topic}",
            "scenes": [
                {
                    "scene_num": 1,
                    "duration": 5.0,
                    "narration": f"Have you ever wondered about {topic}? Most people get it completely wrong.",
                    "pose": "confused",
                    "text_overlay": f"THE TRUTH ABOUT {topic.upper()[:18]}",
                    "prop": "question_mark"
                },
                {
                    "scene_num": 2,
                    "duration": 6.0,
                    "narration": "Scientists discovered something incredible that changes everything.",
                    "pose": "thinking",
                    "text_overlay": "NEW DISCOVERY!",
                    "prop": "lightbulb"
                },
                {
                    "scene_num": 3,
                    "duration": 6.0,
                    "narration": "When you look at the data, the result is absolutely mind blowing.",
                    "pose": "mind_blown",
                    "text_overlay": "MIND BLOWN!",
                    "prop": "fire"
                },
                {
                    "scene_num": 4,
                    "duration": 5.0,
                    "narration": "Share this with a friend who needs to know this today!",
                    "pose": "celebrating",
                    "text_overlay": "SHARE & FOLLOW!",
                    "prop": "none"
                }
            ]
        }

    def draw_stickman_frame(self, pose: str, text_overlay: str, prop: str, frame_num: int, width=1080, height=1920) -> Image.Image:
        bg_color = (15, 23, 42)
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        cx = width // 2
        cy = height // 2 + 100

        bounce = int(math.sin(frame_num * 0.2) * 12)
        cy += bounce

        stroke_color = (255, 255, 255)
        accent_color = (99, 102, 241)
        head_r = 75
        body_len = 220
        line_w = 16

        head_cy = cy - body_len - head_r

        # 1. Head
        draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], outline=stroke_color, width=line_w)

        # Facial Expression
        if pose == "confused":
            draw.line([cx - 30, head_cy - 20, cx - 10, head_cy], fill=stroke_color, width=8)
            draw.line([cx - 10, head_cy - 20, cx - 30, head_cy], fill=stroke_color, width=8)
            draw.ellipse([cx + 10, head_cy - 20, cx + 30, head_cy], fill=stroke_color, width=8)
        elif pose == "mind_blown":
            draw.ellipse([cx - 35, head_cy - 25, cx - 15, head_cy - 5], fill=accent_color, outline=stroke_color, width=6)
            draw.ellipse([cx + 15, head_cy - 25, cx + 35, head_cy - 5], fill=accent_color, outline=stroke_color, width=6)
            draw.ellipse([cx - 20, head_cy + 10, cx + 20, head_cy + 40], fill=stroke_color)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x1 = cx + int(math.cos(rad) * (head_r + 20))
                y1 = head_cy + int(math.sin(rad) * (head_r + 20))
                x2 = cx + int(math.cos(rad) * (head_r + 60))
                y2 = head_cy + int(math.sin(rad) * (head_r + 60))
                draw.line([x1, y1, x2, y2], fill=(244, 63, 94), width=10)
        else:
            draw.ellipse([cx - 30, head_cy - 15, cx - 10, head_cy + 5], fill=stroke_color)
            draw.ellipse([cx + 10, head_cy - 15, cx + 30, head_cy + 5], fill=stroke_color)
            draw.arc([cx - 25, head_cy + 5, cx + 25, head_cy + 35], start=0, end=180, fill=stroke_color, width=8)

        # 2. Body Spine
        spine_bottom = (cx, cy)
        spine_top = (cx, head_cy + head_r)
        draw.line([spine_top[0], spine_top[1], spine_bottom[0], spine_bottom[1]], fill=stroke_color, width=line_w)

        shoulder_y = spine_top[1] + 40

        # 3. Arms & Legs
        if pose == "pointing":
            draw.line([cx, shoulder_y, cx - 100, shoulder_y + 120], fill=stroke_color, width=line_w)
            draw.line([cx, shoulder_y, cx + 180, shoulder_y - 80], fill=stroke_color, width=line_w)
        elif pose == "thinking":
            draw.line([cx, shoulder_y, cx - 100, shoulder_y + 120], fill=stroke_color, width=line_w)
            draw.line([cx, shoulder_y, cx + 80, shoulder_y + 20], fill=stroke_color, width=line_w)
            draw.line([cx + 80, shoulder_y + 20, cx + 20, head_cy + 20], fill=stroke_color, width=line_w)
        elif pose == "celebrating":
            draw.line([cx, shoulder_y, cx - 140, shoulder_y - 120], fill=stroke_color, width=line_w)
            draw.line([cx, shoulder_y, cx + 140, shoulder_y - 120], fill=stroke_color, width=line_w)
        elif pose == "mind_blown":
            draw.line([cx, shoulder_y, cx - 100, head_cy], fill=stroke_color, width=line_w)
            draw.line([cx, shoulder_y, cx + 100, head_cy], fill=stroke_color, width=line_w)
        else:
            draw.line([cx, shoulder_y, cx - 120, shoulder_y + 120], fill=stroke_color, width=line_w)
            draw.line([cx, shoulder_y, cx + 120, shoulder_y + 120], fill=stroke_color, width=line_w)

        if pose == "running":
            draw.line([cx, cy, cx - 120, cy + 180], fill=stroke_color, width=line_w)
            draw.line([cx, cy, cx + 140, cy + 140], fill=stroke_color, width=line_w)
            draw.line([cx + 140, cy + 140, cx + 80, cy + 240], fill=stroke_color, width=line_w)
        else:
            draw.line([cx, cy, cx - 90, cy + 220], fill=stroke_color, width=line_w)
            draw.line([cx, cy, cx + 90, cy + 220], fill=stroke_color, width=line_w)

        # 4. Props
        if prop == "lightbulb":
            lb_x, lb_y = cx + 180, head_cy - 120
            draw.ellipse([lb_x - 35, lb_y - 35, lb_x + 35, lb_y + 35], fill=(253, 224, 71), outline=(234, 179, 8), width=6)
            draw.rectangle([lb_x - 15, lb_y + 35, lb_x + 15, lb_y + 55], fill=(148, 163, 184))
        elif prop == "question_mark":
            qm_x, qm_y = cx - 180, head_cy - 100
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
            except:
                font = ImageFont.load_default()
            draw.text((qm_x, qm_y), "?", fill=(56, 189, 248), font=font)

        # 5. Text Overlay
        if text_overlay:
            padding_y = 180
            try:
                font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
            except:
                font_title = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text_overlay, font=font_title)
            text_w = bbox[2] - bbox[0]
            draw.rectangle([0, padding_y - 20, width, padding_y + 80], fill=(2, 6, 23))
            draw.text(((width - text_w) // 2, padding_y), text_overlay, fill=(253, 224, 71), font=font_title)

        return img

    def synthesize_narration(self, text: str, output_mp3: str) -> bool:
        key = self.openai_key or os.getenv("OPENAI_API_KEY")
        if key:
            try:
                url = "https://api.openai.com/v1/audio/speech"
                payload = json.dumps({
                    "model": "tts-1",
                    "voice": "onyx",
                    "input": text
                }).encode("utf-8")

                req = urllib.request.Request(url, data=payload, headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                })
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(output_mp3, "wb") as f:
                        f.write(resp.read())
                return True
            except Exception as e:
                print(f"OpenAI TTS API error: {e}")

        # Fallback silent track
        try:
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", "anullsrc=r=44100:cl=mono",
                "-t", "5.0", output_mp3
            ]
            subprocess.run(cmd, check=True)
        except Exception:
            with open(output_mp3, "wb") as f:
                f.write(b"") # Empty placeholder
        return True

    def create_stickman_video(self, topic: str) -> str:
        print(f"Generating Stickman Animation Video for topic: '{topic}'...")
        script_data = self.generate_script(topic)

        scene_files = []
        fps = 24

        for i, scene in enumerate(script_data["scenes"]):
            scene_num = scene["scene_num"]
            duration = scene.get("duration", 5.0)
            total_frames = int(duration * fps)

            frame_dir = os.path.join(self.output_dir, f"scene_{scene_num}")
            os.makedirs(frame_dir, exist_ok=True)

            for f in range(total_frames):
                frame_img = self.draw_stickman_frame(
                    pose=scene.get("pose", "standing"),
                    text_overlay=scene.get("text_overlay", ""),
                    prop=scene.get("prop", "none"),
                    frame_num=f
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

            scene_audio = os.path.join(self.output_dir, f"audio_{scene_num}.mp3")
            self.synthesize_narration(scene["narration"], scene_audio)

            scene_final = os.path.join(self.output_dir, f"scene_final_{scene_num}.mp4")
            cmd_combine = [
                "ffmpeg", "-y",
                "-i", scene_mp4,
                "-i", scene_audio,
                "-c:v", "copy",
                "-c:a", "aac",
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

        print(f"✅ Stickman Animation Video successfully generated: {final_output_mp4}")
        return final_output_mp4

if __name__ == "__main__":
    generator = StickmanGenerator()
    generator.create_stickman_video("Quantum Computers Explained")
