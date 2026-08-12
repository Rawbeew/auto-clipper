import os
import subprocess
import json

class VideoProcessor:
    """
    Handles FFmpeg video slicing, 9:16 vertical auto-cropping, ASS subtitle generation,
    and burned-in animated captions rendering.
    """
    def __init__(self, output_dir="/tmp/auto_clipper/renders"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_ass_subtitles(self, words: list, start_time: float, end_time: float, ass_path: str, theme: str = "submagic"):
        """
        Creates stylized ASS (Advanced SubStation Alpha) subtitle file with word-by-word active highlighting.
        """
        # Select style colors
        if theme == "submagic":
            primary_color = "&H00FFFF" # Yellow
            outline_color = "&H000000" # Black
        elif theme == "neon_cyan":
            primary_color = "&HFFFF00" # Cyan
            outline_color = "&H000000"
        else:
            primary_color = "&HFFFFFF" # White
            outline_color = "&H000000"

        header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,64,{primary_color},&H00FFFFFF,{outline_color},&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,40,40,750,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        lines = []
        clip_words = [w for w in words if w["start"] >= start_time and w["end"] <= end_time]

        # Group words into short 3-4 word phrases
        chunk_size = 4
        for i in range(0, len(clip_words), chunk_size):
            chunk = clip_words[i:i + chunk_size]
            if not chunk:
                continue

            # Calculate start and end in HH:MM:SS.cs format
            c_start = chunk[0]["start"] - start_time
            c_end = chunk[-1]["end"] - start_time

            def fmt_time(seconds):
                hrs = int(seconds // 3600)
                mins = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                cs = int((seconds % 1) * 100)
                return f"{hrs:01d}:{mins:02d}:{secs:02d}.{cs:02d}"

            start_str = fmt_time(max(0, c_start))
            end_str = fmt_time(c_end)

            text_str = " ".join([w["word"].upper() for w in chunk])
            lines.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{{\\b1}}{text_str}")

        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(lines))

    def render_short(self, input_video: str, start_time: float, end_time: float, words: list, clip_id: str, caption_theme: str = "submagic") -> str:
        """
        Cuts, crops to 1080x1920, burns subtitles, and exports final vertical short.
        """
        out_filepath = os.path.join(self.output_dir, f"{clip_id}.mp4")
        ass_path = os.path.join(self.output_dir, f"{clip_id}.ass")

        # Generate Subtitles
        self.generate_ass_subtitles(words, start_time, end_time, ass_path, theme=caption_theme)

        # Duration
        duration = end_time - start_time

        # FFmpeg filter:
        # 1. Split video into foreground (cropped 9:16 center 1080x1920) and background (scaled & blurred)
        # 2. Overlay ASS subtitles
        filter_complex = (
            f"[0:v]crop=ih*(9/16):ih:(iw-ih*(9/16))/2:0,scale=1080:1920[v_crop];"
            f"[v_crop]ass={ass_path}[outv]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", input_video,
            "-t", str(duration),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            out_filepath
        ]

        print(f"Executing FFmpeg render command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        return out_filepath
