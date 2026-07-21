import os
import sys
import json

# Vendor integration paths
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vendor", "agnes-video-generator"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vendor", "OpenMontage"))

class OpenMontageAgnesStudioBridge:
    """
    Unified Production Bridge combining:
    1. 'calesthio/OpenMontage' Agentic Storyboard & Montage Composer
    2. 'lcy362/agnes-video-generator' Digital Anchor & Scene Pipeline
    3. 'Wan2.2' / 'LTX-2' / 'CogVideoX' Open Diffusion Models
    """
    def __init__(self, output_dir="/tmp/auto_clipper/open_montage"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def assemble_montage_storyboard(self, script_data: dict) -> dict:
        """
        Converts AutoClipper JSON scripts into OpenMontage / Agnes multi-scene timeline objects.
        """
        print("🎬 [OpenMontage Bridge] Structuring multi-scene storyboard montage timeline...")
        scenes = script_data.get("scenes", [])
        timeline_cuts = []

        for s in scenes:
            timeline_cuts.append({
                "scene_id": s.get("scene_num", 1),
                "duration_sec": s.get("duration", 6.0),
                "visual_prompt": f"Minimalist vector stickman line art, {s.get('headline', '')}, 4k clean composition",
                "audio_script": s.get("narration", ""),
                "transition": "cut"
            })

        montage_blueprint = {
            "title": script_data.get("title", "Generated Montage"),
            "aspect_ratio": "9:16",
            "fps": 24,
            "timeline": timeline_cuts
        }

        out_path = os.path.join(self.output_dir, "montage_timeline.json")
        with open(out_path, "w") as f:
            json.dump(montage_blueprint, f, indent=2)

        print(f"✅ OpenMontage storyboard assembled: {out_path}")
        return montage_blueprint

if __name__ == "__main__":
    bridge = OpenMontageAgnesStudioBridge()
    sample_script = {
        "title": "Quantum Physics Demystified",
        "scenes": [
            {"scene_num": 1, "duration": 6.0, "narration": "Quantum particles exist in all states at once.", "headline": "SUPERPOSITION"}
        ]
    }
    bridge.assemble_montage_storyboard(sample_script)
