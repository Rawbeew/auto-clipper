import os
import math
import json
from PIL import Image, ImageDraw

class SVGStickmanRenderer:
    """
    SVG Stickman Vector Renderer with Joint Keyframe Interpolation.
    Inspired by madeindjs/stickman and davepagurek/Axis keyframing engines.
    """
    def __init__(self, output_dir="/tmp/auto_clipper/svg_frames"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_svg_stickman(self, pose_name: str = "pointing", joint_angle_deg: float = 0.0) -> str:
        """
        Outputs clean SVG vector XML for stickman figure with variable joint angles.
        """
        rad = math.radians(joint_angle_deg)
        arm_x = int(math.cos(rad) * 120)
        arm_y = int(math.sin(rad) * 120)

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0F172A"/>
  <g stroke="#FFFFFF" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- Head -->
    <circle cx="540" cy="700" r="75" fill="none" />
    <circle cx="510" cy="690" r="10" fill="#FFFFFF" />
    <circle cx="570" cy="690" r="10" fill="#FFFFFF" />
    <!-- Spine -->
    <line x1="540" y1="775" x2="540" y2="1050" />
    <!-- Left Arm -->
    <line x1="540" y1="820" x2="{540 - 120}" y2="920" />
    <!-- Right Arm (Animated) -->
    <line x1="540" y1="820" x2="{540 + arm_x}" y2="{820 + arm_y}" />
    <!-- Legs -->
    <line x1="540" y1="1050" x2="450" y2="1270" />
    <line x1="540" y1="1050" x2="630" y2="1270" />
  </g>
</svg>"""
        svg_path = os.path.join(self.output_dir, f"stickman_{pose_name}.svg")
        with open(svg_path, "w") as f:
            f.write(svg_content)

        return svg_path

    def interpolate_keyframes(self, start_angle: float, end_angle: float, steps: int = 24) -> list:
        """
        Smooth ease-in-out joint interpolation across frames.
        """
        angles = []
        for step in range(steps):
            t = step / max(1, steps - 1)
            # Ease-in-out cubic formula
            ease_t = 3 * t**2 - 2 * t**3
            curr_angle = start_angle + (end_angle - start_angle) * ease_t
            angles.append(curr_angle)
        return angles

if __name__ == "__main__":
    renderer = SVGStickmanRenderer()
    svg_path = renderer.generate_svg_stickman("waving", -45.0)
    print(f"Generated SVG stickman file: {svg_path}")
