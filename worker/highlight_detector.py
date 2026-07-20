import json
import os
from openai import OpenAI

class HighlightDetector:
    """
    Uses LLMs (GPT-4o-mini / Gemini) to score video transcripts and extract
    engaging, high-retention 15-60s short segments with hooks and headlines.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

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
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert AI video clipper and viral media engineer. Respond strictly in JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                res_content = response.choices[0].message.content
                parsed = json.loads(res_content)
                if isinstance(parsed, dict) and "highlights" in parsed:
                    return parsed["highlights"][:max_clips]
                elif isinstance(parsed, list):
                    return parsed[:max_clips]
                elif isinstance(parsed, dict) and len(parsed.keys()) == 1:
                    key = list(parsed.keys())[0]
                    return parsed[key][:max_clips]
            except Exception as e:
                print(f"Highlight detection error: {e}")

        # Fallback default highlight if LLM unavailable or fails
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
