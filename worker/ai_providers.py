import os
import json
import subprocess
import urllib.request

class MultiAIProvider:
    """
    Unified AI Multi-Provider Client optimized for Groq LPU, SiliconFlow, 
    Cerebras, Gemini 2.0, Anything.com, and OpenAI.
    Provides sub-second scriptwriting, speech-to-text, and vector artwork generation.
    """
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.cerebras_key = os.getenv("CEREBRAS_API_KEY")
        self.sambanova_key = os.getenv("SAMBANOVA_API_KEY")
        self.siliconflow_key = os.getenv("SILICONFLOW_API_KEY")
        self.anything_key = os.getenv("ANYTHING_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

    def generate_json(self, prompt: str, system_prompt: str = "Respond strictly in valid JSON.") -> dict:
        """
        Runs completion using Groq LPU as primary provider, falling back down the stack.
        Order: Groq Llama 3.3 -> Cerebras -> SiliconFlow -> Gemini -> Anything.com -> OpenAI
        """
        # 1. Groq LPU (Ultra-fast 0.6s Llama 3.3 70B)
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

        # 2. Cerebras Cloud
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

        # 3. SiliconFlow (Qwen 2.5)
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

        # 4. Gemini 2.0
        if self.gemini_key:
            res = self._call_gemini(prompt, system_prompt)
            if res:
                return res

        # 5. Anything.com
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

        # 6. OpenAI
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

    def transcribe_audio_groq(self, audio_filepath: str) -> dict:
        """
        Transcribes audio via Groq Whisper LPU in ~2-3 seconds.
        """
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

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipper/1.0"
        }

        try:
            req = urllib.request.Request(url, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as e:
            print(f"API Provider call ({url}) failed: {e}")
            return None

    def _call_gemini(self, prompt: str, system_prompt: str) -> dict:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": f"{system_prompt}\n\nPrompt: {prompt}"}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipper/1.0"
        }

        try:
            req = urllib.request.Request(url, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
        except Exception as e:
            print(f"Gemini API failed: {e}")
            return None
