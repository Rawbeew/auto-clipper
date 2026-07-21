import json
import os
from ai_providers import MultiAIProvider

class HighlightDetector:
    """
    Uses MultiAIProvider (Groq Llama 3.3 70B, SiliconFlow Qwen 2.5, Gemini, or OpenAI)
    to score video transcripts and extract engaging, high-retention 15-60s short segments.
    """
    def __init__(self, api_key: str = None):
        self.ai_provider = MultiAIProvider()

    def find_highlights(self, transcript_data: dict, max_clips: int = 3) -> list:
        segments = transcript_data.get("segments", [])
        
        prompt = f"""
You are a viral short-form video editor for TikTok, YouTube Shorts, and Instagram Reels.
Analyze the following transcript of a long-form video with timestamps and identify up to {max_clips} viral standalone segments.

Requirements:
1. Duration of each clip must be between 15 seconds and 59 seconds.
2. Must start with a strong hook or intriguing statement.
3. Must contain a complete thought, storyline, or key takeaway.
4. Provide a virality score (0-100) and a high-converting short title & hook text.

Transcript Segments:
{json.dumps(segments, indent=2)}

Return ONLY a valid JSON array of objects with the exact structure:
[
  {{
    "title": "Short catchy title",
    "hook_text": "First punchy line overlay",
    "start_time": 12.5,
    "end_time": 48.0,
    "virality_score": 92,
    "reason": "Strong mystery hook followed by actionable takeaway."
  }}
]
"""
        res = self.ai_provider.generate_json(prompt, system_prompt="You are an expert AI video clipper and viral media engineer. Respond strictly in JSON.")
        if res:
            if isinstance(res, dict) and "highlights" in res:
                return res["highlights"][:max_clips]
            elif isinstance(res, list):
                return res[:max_clips]
            elif isinstance(res, dict) and len(res.keys()) == 1:
                key = list(res.keys())[0]
                return res[key][:max_clips]

        # Fallback default highlight if offline or templates
        total_dur = segments[-1]["end"] if segments else 60.0
        clip_dur = min(45.0, total_dur)
        return [
            {
                "title": "Top Moment from Long Form",
                "hook_text": "Watch this before it's too late...",
                "start_time": 0.0,
                "end_time": clip_dur,
                "virality_score": 88,
                "reason": "Opening highlight."
            }
        ]
