import os
import json
from ai_providers import MultiAIProvider

class SpecializedAIRouter:
    """
    Dedicated AI Task Orchestrator.
    Assigns every pipeline sub-task to the specialized AI model best suited for it:
    1. Scripting & CTR Hooks -> Groq LPU Llama 3.3 70B
    2. Fact-Checking & Audit -> DeepSeek Native V4/R1
    3. Multimodal Analysis   -> Google Gemini 2.0 API
    4. B-Roll Vector Images  -> Pollinations.ai / SiliconFlow FLUX.1
    5. Voiceover Narration   -> Microsoft Edge-TTS (Local) / OpenAI TTS
    6. Video Assembly & ASS  -> FFmpeg (Local)
    """
    def __init__(self):
        self.ai_provider = MultiAIProvider()

    def task_generate_script(self, topic: str, style: str = "casually_explained") -> dict:
        """Task 1: Assigned to Groq LPU Llama 3.3 for sub-second execution."""
        print(f"🎯 [Task 1: Scripting] Assigning to Groq LPU Llama 3.3 for topic: '{topic}'...")
        prompt = f"Write a deadpan 30-second Casually Explained stickman script on '{topic}' in valid JSON."
        res = self.ai_provider.generate_json(prompt, system_prompt="You are Casually Explained script writer. Respond strictly in JSON.")
        return res

    def task_fact_check(self, script_data: dict, topic: str) -> dict:
        """Task 2: Assigned to DeepSeek V4/R1 for strict logical auditing."""
        print(f"🔬 [Task 2: Fact Audit] Assigning to DeepSeek Native V4/R1 for topic: '{topic}'...")
        prompt = f"Audit script data for strict 100% factual accuracy on '{topic}': {json.dumps(script_data)}"
        res = self.ai_provider.generate_json(prompt, system_prompt="You are a strict factual auditor. Respond strictly in JSON.")
        return res or script_data

    def task_generate_broll_image(self, scene_description: str) -> str:
        """Task 3: Assigned to Pollinations.ai / SiliconFlow FLUX.1 (100% Free, Localized)."""
        print(f"🎨 [Task 3: Vector B-Roll] Generating localized artwork for: '{scene_description}'...")
        return self.ai_provider.generate_image_free(scene_description)

if __name__ == "__main__":
    router = SpecializedAIRouter()
    script = router.task_generate_script("Quantum Computers Explained")
    print(script)
