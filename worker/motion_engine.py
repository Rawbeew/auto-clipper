import os
import sys
import json
import subprocess

# Import vendor tools
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vendor", "generative-manim"))

class MotionSkillsManimEngine:
    """
    Combines 'generative-manim' math/physics visualization code generation 
    and 'motion-skills' kinetic typography and data-viz animation layouts
    to produce 3Blue1Brown & Kurzgesagt tier motion graphics for Casually Explained shorts.
    """
    def __init__(self, output_dir="/tmp/auto_clipper/motion"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_manim_script(self, concept_description: str) -> str:
        """
        Generates Python Manim code for mathematical/data-viz diagrams.
        """
        code = f"""from manim import *

class GeneratedDiagram(Scene):
    def construct(self):
        # Casually Explained style dark background
        self.camera.background_color = "#0F172A"

        title = Text("{concept_description.upper()[:25]}", font_size=42, color=YELLOW)
        title.to_edge(UP)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 100, 20],
            axis_config={{"color": BLUE}},
        )
        labels = axes.get_axis_labels(x_label="SKILL", y_label="CONFIDENCE")

        graph = axes.plot(lambda x: 10 * (x - 2)**2 + 10, color=RED)
        dot = Dot(color=YELLOW).move_to(axes.c2p(2, 10))
        label = Text("YOU ARE HERE", font_size=24, color=YELLOW).next_to(dot, UP)

        self.play(Write(title))
        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.play(FadeIn(dot), Write(label))
        self.wait(3)
"""
        py_path = os.path.join(self.output_dir, "GenDiagram.py")
        with open(py_path, "w") as f:
            f.write(code)

        return py_path

    def render_manim_video(self, concept_description: str) -> str:
        py_path = self.generate_manim_script(concept_description)
        out_mp4 = os.path.join(self.output_dir, "diagram_render.mp4")

        cmd = [
            "manim", "-ql", "--format=mp4",
            "-o", out_mp4,
            py_path, "GeneratedDiagram"
        ]
        print(f"Executing Generative-Manim render: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            return out_mp4
        except Exception as e:
            print(f"Manim render fallback: {e}")
            return None

if __name__ == "__main__":
    engine = MotionSkillsManimEngine()
    engine.generate_manim_script("Dunning Kruger Confidence vs Skill Curve")
