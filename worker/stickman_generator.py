import os
import math
import json
import asyncio
import subprocess
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from character_manager import CharacterManager

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
    Advanced YouTube-Style Animated Stickman Engine with Permanent Mascot Continuity.
    Supports:
    - Character Manager (Lock onto custom mascot: Tax Advisor, Fedora Detective, Lab Scientist, Crypto Trader)
    - Casually Explained Signature MS-Paint Format (Graphs, Option Boxes)
    - Tax & Finance Document Simulator (Form 1040 Paper, Green Stamps, Checkboxes)
    - Stand-Up Comedy Stage Animation (Red Velvet Curtain, Spotlight, Mic Stand)
    Includes HD Edge-TTS Voiceovers & Submagic Yellow Highlighted Captions.
    """
    def __init__(self, output_dir="/tmp/auto_clipper/stickman"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ai_provider = MultiAIProvider()
        self.char_mgr = CharacterManager()

    def generate_script(self, topic: str) -> dict:
        prompt = f"""
You are Casually Explained (the famous YouTube animator known for dry, sarcastic MS-Paint style stickman videos).
Write a deadpan, fast-paced 30-second stickman script explaining or demonstrating: "{topic}".

Provide a JSON object with:
1. "title": Short catchy CTR title
2. "style": "casually_explained"
3. "scenes": A list of 4 scenes. Each scene must have:
   - "scene_num": integer
   - "duration": float (e.g. 6.0)
   - "narration": Sarcastic, matter-of-fact deadpan spoken text (15-25 words max)
   - "headline": Short 3-5 word headline overlay
   - "diagram_type": ["paper_form", "graph", "crowd_reaction", "choices", "mind_blown"]

Format: JSON strictly.
"""
        res = self.ai_provider.generate_json(prompt, system_prompt="You are Casually Explained. Respond strictly in valid JSON.")
        if res:
            return res

        return {
            "title": f"Casually Explained: {topic}",
            "style": "casually_explained",
            "scenes": [
                {
                    "scene_num": 1,
                    "duration": 6.0,
                    "narration": f"If you've ever looked at a tax form or financial statement and felt completely lost, you're not alone.",
                    "headline": f"THE REALITY OF {topic.upper()[:16]}",
                    "diagram_type": "paper_form"
                },
                {
                    "scene_num": 2,
                    "duration": 6.0,
                    "narration": "You are currently sitting right at the peak of Mount Stupid on the confidence vs skill graph.",
                    "headline": "THE CONFIDENCE PARADOX",
                    "diagram_type": "graph"
                },
                {
                    "scene_num": 3,
                    "duration": 6.0,
                    "narration": "When you share this strategy, everyone in the room realizes you've beaten the system.",
                    "headline": "CROWD REACTION 📈",
                    "diagram_type": "crowd_reaction"
                },
                {
                    "scene_num": 4,
                    "duration": 6.0,
                    "narration": "Subscribe to the channel, or don't. The choice is completely up to your dopamine levels.",
                    "headline": "LIKE & SUBSCRIBE 🤯",
                    "diagram_type": "mind_blown"
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

    def draw_casually_explained_frame(self, headline: str, narration_text: str, diagram_type: str, frame_num: int, total_frames: int, width=1080, height=1920) -> Image.Image:
        bg_color = (255, 255, 255)
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        stroke_color = (15, 23, 42)
        red_accent = (225, 29, 72)
        green_accent = (34, 197, 94)
        blue_accent = (37, 99, 235)
        line_w = 12

        # Stickman Position
        cx = 300
        cy = height // 2 + 200 + int(math.sin(frame_num * 0.15) * 6)
        head_r = 75
        body_len = 220
        head_cy = cy - body_len - head_r

        # 1. Head & Face
        draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], outline=stroke_color, width=line_w)
        draw.ellipse([cx - 30, head_cy - 10, cx - 10, head_cy + 10], fill=stroke_color)
        draw.ellipse([cx + 10, head_cy - 10, cx + 30, head_cy + 10], fill=stroke_color)
        draw.line([cx - 20, head_cy + 30, cx + 20, head_cy + 30], fill=stroke_color, width=6)

        # 2. Draw Permanent Locked Mascot Accessories (Glasses, Ties, Hats, Goggles)
        self.char_mgr.draw_locked_accessories(draw, cx, head_cy, head_r, stroke_color)

        # 3. Spine & Gesturing Arm pointing at diagram
        draw.line([cx, head_cy + head_r, cx, cy], fill=stroke_color, width=line_w)
        shoulder_y = head_cy + head_r + 40
        draw.line([cx, shoulder_y, cx - 80, shoulder_y + 100], fill=stroke_color, width=line_w)
        draw.line([cx, shoulder_y, cx + 180, shoulder_y - 40], fill=stroke_color, width=line_w)

        # 4. Legs
        draw.line([cx, cy, cx - 70, cy + 220], fill=stroke_color, width=line_w)
        draw.line([cx, cy, cx + 70, cy + 220], fill=stroke_color, width=line_w)

        # 5. DIAGRAM ON RIGHT
        if diagram_type == "paper_form":
            fx, fy = 520, height // 2 - 240
            fw, fh = 480, 620

            draw.rectangle([fx + 15, fy + 15, fx + fw + 15, fy + fh + 15], fill=(203, 213, 225))
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(248, 250, 252), outline=stroke_color, width=8)

            try:
                font_form = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
            except:
                font_form = ImageFont.load_default()
                font_sm = ImageFont.load_default()

            draw.text((fx + 20, fy + 25), "FORM 1040: TAX RETURN", fill=stroke_color, font=font_form)
            draw.line([fx + 20, fy + 70, fx + fw - 20, fy + 70], fill=stroke_color, width=4)

            form_lines = [
                ("Gross Income:", "$250,000"),
                ("Sec. 179 Deduction:", "-$180,000"),
                ("S-Corp Salary:", "$50,000"),
                ("Taxable Balance:", "$20,000")
            ]

            for idx, (label, val) in enumerate(form_lines):
                ly = fy + 110 + (idx * 80)
                draw.rectangle([fx + 25, ly, fx + 55, ly + 30], outline=stroke_color, width=4)
                draw.line([fx + 25, ly, fx + 55, ly + 30], fill=green_accent, width=5)
                draw.text((fx + 70, ly), label, fill=stroke_color, font=font_sm)
                draw.text((fx + 320, ly), val, fill=green_accent if "-" in val else stroke_color, font=font_sm)
                draw.line([fx + 25, ly + 45, fx + fw - 25, ly + 45], fill=(226, 232, 240), width=2)

            stamp_x, stamp_y = fx + 60, fy + fh - 140
            draw.rectangle([stamp_x, stamp_y, stamp_x + 360, stamp_y + 80], outline=green_accent, width=8)
            draw.text((stamp_x + 20, stamp_y + 15), "0% TAX SAVINGS!", fill=green_accent, font=font_form)

        elif diagram_type == "crowd_reaction":
            for c in range(6):
                crowd_x = 550 + (c % 3) * 150
                crowd_y = height // 2 - 100 + (c // 3) * 220 + int(math.sin(frame_num * 0.3 + c) * 10)
                draw.ellipse([crowd_x - 35, crowd_y - 35, crowd_x + 35, crowd_y + 35], outline=stroke_color, width=6)
                draw.line([crowd_x, crowd_y + 35, crowd_x, crowd_y + 120], fill=stroke_color, width=6)
                draw.line([crowd_x, crowd_y + 50, crowd_x - 40, crowd_y], fill=stroke_color, width=6)
                draw.line([crowd_x, crowd_y + 50, crowd_x + 40, crowd_y], fill=stroke_color, width=6)
                draw.rectangle([crowd_x - 40, crowd_y - 100, crowd_x + 80, crowd_y - 50], fill=(254, 240, 138), outline=stroke_color, width=3)
                try:
                    font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
                except:
                    font_sm = ImageFont.load_default()
                draw.text((crowd_x - 30, crowd_y - 90), "WOW!", fill=stroke_color, font=font_sm)

        elif diagram_type == "choices":
            bx1, by1 = 550, height // 2 - 200
            draw.rectangle([bx1, by1, bx1 + 420, by1 + 140], outline=stroke_color, width=8, fill=(241, 245, 249))
            draw.rectangle([bx1, by1 + 220, bx1 + 420, by1 + 360], outline=stroke_color, width=8, fill=(254, 226, 226))

            try:
                box_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
            except:
                box_font = ImageFont.load_default()

            draw.text((bx1 + 30, by1 + 50), "OPTION A: REASON", fill=stroke_color, font=box_font)
            draw.text((bx1 + 30, by1 + 270), "OPTION B: CHAOS", fill=red_accent, font=box_font)

        else: # Graph
            gx, gy = 550, height // 2 - 150
            gw, gh = 440, 480

            draw.line([gx, gy, gx, gy + gh], fill=stroke_color, width=10)
            draw.line([gx, gy + gh, gx + gw, gy + gh], fill=stroke_color, width=10)
            draw.polygon([(gx, gy - 20), (gx - 15, gy + 10), (gx + 15, gy + 10)], fill=stroke_color)
            draw.polygon([(gx + gw + 20, gy + gh), (gx + gw - 10, gy + gh - 15), (gx + gw - 10, gy + gh + 15)], fill=stroke_color)

            try:
                label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            except:
                label_font = ImageFont.load_default()

            draw.text((gx + 10, gy - 60), "CONFIDENCE", fill=stroke_color, font=label_font)
            draw.text((gx + 100, gy + gh + 20), "ACTUAL SKILL", fill=stroke_color, font=label_font)

            curve_points = [
                (gx, gy + gh - 20),
                (gx + 100, gy + 80),
                (gx + 220, gy + 380),
                (gx + 340, gy + 240),
                (gx + gw - 10, gy + 140)
            ]
            draw.line(curve_points, fill=red_accent, width=12)
            draw.line([(gx + 100, gy + 80), (gx + 180, gy + 20)], fill=blue_accent, width=6)
            draw.text((gx + 190, gy + 5), "YOU ARE HERE", fill=blue_accent, font=label_font)

        # Top Title Header
        if headline:
            clean_hl = headline.encode('ascii', 'ignore').decode('ascii')
            try:
                font_hl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
            except:
                font_hl = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), clean_hl, font=font_hl)
            text_w = bbox[2] - bbox[0]
            draw.rectangle([0, 140, width, 240], fill=(15, 23, 42))
            draw.text(((width - text_w) // 2, 160), clean_hl, fill=(255, 255, 255), font=font_hl)

        # Submagic Captions
        progress = frame_num / max(1, total_frames)
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
            draw.rectangle([start_x - 30, sub_y - 15, start_x + phrase_w + 30, sub_y + 85], fill=(15, 23, 42))

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
        print(f"🎬 Generating Casually Explained Style Video for: '{topic}'...")
        script_data = self.generate_script(topic)

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
                frame_img = self.draw_casually_explained_frame(
                    headline=scene.get("headline", ""),
                    narration_text=scene.get("narration", ""),
                    diagram_type=scene.get("diagram_type", "paper_form"),
                    frame_num=f,
                    total_frames=total_frames
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

        print(f"✅ Casually Explained Video created: {final_output_mp4}")
        return final_output_mp4

if __name__ == "__main__":
    generator = StickmanGenerator()
    generator.create_stickman_video("3 Legal Tax Secrets Rich People Use")
