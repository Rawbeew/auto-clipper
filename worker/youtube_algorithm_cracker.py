import os
import json
from ai_providers import MultiAIProvider

class YouTubeAlgorithmCracker:
    """
    Reverse-engineers YouTube's recommendation neural network (CTR + AVD + Looping Retention).
    Generates high-CTR A/B title variants, 0-3s visual pattern interrupts, and seamless loop hooks.
    """
    def __init__(self):
        self.ai_provider = MultiAIProvider()

    def optimize_video_for_algorithm(self, topic: str, content_type: str = "short") -> dict:
        """
        Passes topic through the Algorithmic Retention Framework.
        Outputs:
        - 3 A/B Testable High-CTR Titles
        - 0-3 Second Visual Pattern Interrupt Hook
        - Infinite Looping Phrase (for Shorts >100% retention)
        - Suggested Video Tags & Co-Watch Competitor Embeddings
        """
        print(f"🧬 Cracking YouTube Algorithm metrics for topic: '{topic}' ({content_type})...")

        prompt = f"""
You are the chief YouTube Algorithm & Virality Data Scientist.
Analyze the topic: "{topic}" and optimize it for YouTube's recommendation engine algorithms.

Requirements:
1. "ctr_titles": Generate 3 A/B titles following high-CTR psychology (Curiosity Gap, High Stakes, Negative Angle). Must be under 50 characters.
2. "pattern_interrupt_hook": The exact 0-3 second visual/text hook to prevent drop-off in the first 3 seconds.
3. "seamless_loop_phrase": A sentence for the end of the video that seamlessly connects to the first word of the video for infinite looping (>100% retention rate).
4. "retention_triggers": List 3 moments in the script where visual pattern interrupts must occur (every 4-7 seconds).
5. "youtube_seo_tags": Array of 10 high-search-volume tags for YouTube Suggested Video sidebar placement.

Respond strictly in valid JSON format.
"""
        res = self.ai_provider.generate_json(prompt, system_prompt="You are an elite YouTube Virality & Algorithm Scientist. Respond strictly in JSON.")
        if res:
            return res

        # Fallback algorithmic optimization payload
        return {
            "ctr_titles": [
                f"The Dark Truth About {topic[:20]}",
                f"Why 99% Get {topic[:20]} Wrong",
                f"What Nobody Tells You About {topic[:20]}"
            ],
            "pattern_interrupt_hook": "Stop scrolling! What if everything you knew was a lie?",
            "seamless_loop_phrase": "...and that is exactly why...",
            "retention_triggers": [
                "03s: Sound effect woosh + text color shift",
                "09s: Zoom-in transition + character pose change",
                "18s: Background color flip + dramatic pause"
            ],
            "youtube_seo_tags": [
                topic, f"{topic} explained", "educational animation", "facts", 
                "trending shorts", "mind blowing", "viral documentary"
            ]
        }

if __name__ == "__main__":
    cracker = YouTubeAlgorithmCracker()
    res = cracker.optimize_video_for_algorithm("Why Central Banks Print Money", "short")
    print(json.dumps(res, indent=2))
