import os
import json
import urllib.request

class MultiAIProvider:
    """
    Unified AI Multi-Provider Client for Groq, SiliconFlow, Anything.ai, Gemini, and OpenAI.
    Allows ultra-fast LPU inference, FLUX image generation, and speech-to-text.
    """
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.siliconflow_key = os.getenv("SILICONFLOW_API_KEY")
        self.anything_key = os.getenv("ANYTHING_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

    # ----------------------------------------------------
    # 1. FAST SCRIPT & HIGHLIGHT LLM GENERATION
    # ----------------------------------------------------
    def generate_json(self, prompt: str, system_prompt: str = "Respond strictly in valid JSON.") -> dict:
        """
        Executes structured JSON completion across available providers in order of speed/credits:
        Groq -> SiliconFlow -> Gemini -> Anything.ai -> OpenAI -> Fallback None
        """
        # 1. Try Groq (Ultra-fast LPU Llama 3.3 / DeepSeek)
        if self.groq_key:
            res = self._call_openai_compatible(
                url="https://api.groq.com/openai/v1/chat/completions",
                api_key=self.groq_key,
                model="llama-3.3-70b-versatile",
                prompt=prompt,
                system_prompt=system_prompt
            )
            if res:
                return res

        # 2. Try SiliconFlow (Qwen 2.5 / DeepSeek V3)
        if self.siliconflow_key:
            res = self._call_openai_compatible(
                url="https://api.siliconflow.cn/v1/chat/completions",
                api_key=self.siliconflow_key,
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt=prompt,
                system_prompt=system_prompt
            )
            if res:
                return res

        # 3. Try Gemini (Google)
        if self.gemini_key:
            res = self._call_gemini(prompt, system_prompt)
            if res:
                return res

        # 4. Try OpenAI
        if self.openai_key:
            res = self._call_openai_compatible(
                url="https://api.openai.com/v1/chat/completions",
                api_key=self.openai_key,
                model="gpt-4o-mini",
                prompt=prompt,
                system_prompt=system_prompt
            )
            if res:
                return res

        return None

    # ----------------------------------------------------
    # 2. ULTRA-FAST AUDIO TRANSCRIPTION (Groq Whisper LPU)
    # ----------------------------------------------------
    def transcribe_audio_groq(self, audio_filepath: str) -> dict:
        """
        Transcribes audio in milliseconds using Groq's Whisper Large V3 LPU.
        """
        if not self.groq_key or not os.path.exists(audio_filepath):
            return None

        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        
        # Multipart form data upload or curl subprocess
        cmd = [
            "curl", "-s", "-X", "POST", url,
            "-H", f"Authorization: Bearer {self.groq_key}",
            "-F", f"file=@{audio_filepath}",
            "-F", "model=whisper-large-v3-turbo",
            "-F", "response_format=verbose_json",
            "-F", "timestamp_granularities[]=word"
        ]
        try:
            out = subprocess.check_output(cmd).decode("utf-8")
            return json.loads(out)
        except Exception as e:
            print(f"Groq Whisper transcription skipped: {e}")
            return None

    # ----------------------------------------------------
    # 3. SILICONFLOW FLUX / SDXL IMAGE GENERATION
    # ----------------------------------------------------
    def generate_image_siliconflow(self, prompt: str) -> str:
        """
        Generates stickman / B-roll images using SiliconFlow's FLUX.1 Schnell model.
        """
        if not self.siliconflow_key:
            return None

        url = "https://api.siliconflow.cn/v1/images/generations"
        payload = json.dumps({
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": f"Minimalist white vector stickman line art on dark background, {prompt}",
            "image_size": "1024x1024"
        }).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=payload, headers={
                "Authorization": f"Bearer {self.siliconflow_key}",
                "Content-Type": "application/json"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["images"][0]["url"]
        except Exception as e:
            print(f"SiliconFlow FLUX image generation skipped: {e}")
            return None

    # Helper methods for REST calls
    def _call_openai_compatible(self, url: str, api_key: str, model: str, prompt: str, system_prompt: str) -> dict:
        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=payload, headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as e:
            print(f"API provider ({url}) skipped: {e}")
            return None

    def _call_gemini(self, prompt: str, system_prompt: str) -> dict:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": f"{system_prompt}\n\nPrompt: {prompt}"}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
        except Exception as e:
            print(f"Gemini API skipped: {e}")
            return None
