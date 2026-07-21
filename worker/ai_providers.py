import os
import json
import subprocess
import urllib.request

class MultiAIProvider:
    """
    Unified AI Multi-Provider Client for Groq, Cerebras, SambaNova, SiliconFlow, 
    Anything.com, Gemini, Pollinations.ai, and OpenAI.
    Provides ultra-fast LPU inference, free FLUX image generation, and speech-to-text.
    """
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.cerebras_key = os.getenv("CEREBRAS_API_KEY")
        self.sambanova_key = os.getenv("SAMBANOVA_API_KEY")
        self.siliconflow_key = os.getenv("SILICONFLOW_API_KEY")
        self.anything_key = os.getenv("ANYTHING_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.pexels_key = os.getenv("PEXELS_API_KEY")

    # ----------------------------------------------------
    # 1. FAST SCRIPT & HIGHLIGHT LLM GENERATION
    # ----------------------------------------------------
    def generate_json(self, prompt: str, system_prompt: str = "Respond strictly in valid JSON.") -> dict:
        """
        Executes structured JSON completion across available providers in order of speed/credits:
        Cerebras -> Groq -> SambaNova -> SiliconFlow -> Gemini -> Anything.com -> OpenAI
        """
        # 1. Try Cerebras (World's Fastest Llama 3.3 70B @ 2000 tokens/sec)
        if self.cerebras_key:
            res = self._call_openai_compatible(
                url="https://api.cerebras.ai/v1/chat/completions",
                api_key=self.cerebras_key,
                model="llama3.3-70b",
                prompt=prompt,
                system_prompt=system_prompt
            )
            if res:
                return res

        # 2. Try Groq (Ultra-fast LPU Llama 3.3 / DeepSeek)
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

        # 3. Try SambaNova (DeepSeek R1 & Llama 3.3 70B)
        if self.sambanova_key:
            res = self._call_openai_compatible(
                url="https://api.sambanova.ai/v1/chat/completions",
                api_key=self.sambanova_key,
                model="Meta-Llama-3.3-70B-Instruct",
                prompt=prompt,
                system_prompt=system_prompt
            )
            if res:
                return res

        # 4. Try SiliconFlow (Qwen 2.5 / DeepSeek V3)
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

        # 5. Try Gemini (Google)
        if self.gemini_key:
            res = self._call_gemini(prompt, system_prompt)
            if res:
                return res

        # 6. Try Anything.com
        if self.anything_key:
            res = self._call_openai_compatible(
                url="https://api.anything.com/v1/chat/completions",
                api_key=self.anything_key,
                model="default",
                prompt=prompt,
                system_prompt=system_prompt
            )
            if res:
                return res

        # 7. Try OpenAI
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
        if not self.groq_key or not os.path.exists(audio_filepath):
            return None

        url = "https://api.groq.com/openai/v1/audio/transcriptions"
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
    # 3. 100% FREE IMAGE GENERATION (Pollinations.ai / SiliconFlow)
    # ----------------------------------------------------
    def generate_image_free(self, prompt: str) -> str:
        """
        Generates stickman artwork or B-roll using Pollinations.ai (100% Free, No API key needed) 
        or SiliconFlow FLUX.1.
        """
        # Pollinations.ai (100% Free zero setup)
        encoded_prompt = urllib.parse.quote(f"minimalist white vector stickman line art on dark background, {prompt}")
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&seed=42"
        return pollinations_url

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
