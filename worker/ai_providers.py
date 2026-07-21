import os
import time
import json
import subprocess
import urllib.request

class MultiAIProvider:
    """
    Unified AI Multi-Provider Client optimized for Groq LPU, Kimi (Moonshot AI), 
    DeepSeek, Cerebras, SiliconFlow, Gemini 2.0, Anything.com, and OpenAI.
    Provides sub-second scriptwriting, speech-to-text, and vector artwork generation.
    """
    def __init__(self):
        self.providers = [
            {
                "name": "Groq LPU",
                "key": os.getenv("GROQ_API_KEY"),
                "url": "https://api.groq.com/openai/v1/chat/completions",
                "model": "llama-3.3-70b-versatile",
                "type": "openai_compatible",
                "cooldown_until": 0
            },
            {
                "name": "Kimi Moonshot AI",
                "key": os.getenv("KIMI_API_KEY"),
                "url": "https://api.moonshot.ai/v1/chat/completions",
                "model": "kimi-k2.6",
                "type": "openai_compatible",
                "cooldown_until": 0
            },
            {
                "name": "Cerebras WSE-3",
                "key": os.getenv("CEREBRAS_API_KEY"),
                "url": "https://api.cerebras.ai/v1/chat/completions",
                "model": "gemma-4-31b",
                "type": "openai_compatible",
                "cooldown_until": 0
            },
            {
                "name": "DeepSeek Native",
                "key": os.getenv("DEEPSEEK_API_KEY"),
                "url": "https://api.deepseek.com/chat/completions",
                "model": "deepseek-v4-flash",
                "type": "openai_compatible",
                "cooldown_until": 0
            },
            {
                "name": "SiliconFlow Qwen",
                "key": os.getenv("SILICONFLOW_API_KEY"),
                "url": "https://api.siliconflow.cn/v1/chat/completions",
                "model": "Qwen/Qwen2.5-72B-Instruct",
                "type": "openai_compatible",
                "cooldown_until": 0
            },
            {
                "name": "Google Gemini 2.0",
                "key": os.getenv("GEMINI_API_KEY"),
                "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                "model": "gemini-2.0-flash",
                "type": "gemini",
                "cooldown_until": 0
            },
            {
                "name": "Anything.com API",
                "key": os.getenv("ANYTHING_API_KEY"),
                "url": "https://api.anything.com/v1/chat/completions",
                "model": "default",
                "type": "openai_compatible",
                "cooldown_until": 0
            },
            {
                "name": "OpenAI API",
                "key": os.getenv("OPENAI_API_KEY"),
                "url": "https://api.openai.com/v1/chat/completions",
                "model": "gpt-4o-mini",
                "type": "openai_compatible",
                "cooldown_until": 0
            }
        ]

    def generate_json(self, prompt: str, system_prompt: str = "Respond strictly in valid JSON.") -> dict:
        now = time.time()
        for p in self.providers:
            if not p["key"]:
                continue

            if p["cooldown_until"] > now:
                print(f"⏳ Provider '{p['name']}' in rate-limit cooldown. Switching to next...")
                continue

            print(f"⚡ Attempting completion with provider: '{p['name']}'...")
            
            if p["type"] == "openai_compatible":
                res = self._call_openai_compatible(p, prompt, system_prompt)
            elif p["type"] == "gemini":
                res = self._call_gemini(p, prompt, system_prompt)
            else:
                res = None

            if res:
                print(f"✅ Success from provider: '{p['name']}'")
                return res
            else:
                p["cooldown_until"] = time.time() + 60
                print(f"⚠️ Provider '{p['name']}' failed/rate-limited. Auto-switching to next provider...")

        print("❌ All AI providers exhausted or in cooldown.")
        return None

    def _call_openai_compatible(self, provider: dict, prompt: str, system_prompt: str) -> dict:
        payload = json.dumps({
            "model": provider["model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }).encode("utf-8")

        headers = {
            "Authorization": f"Bearer {provider['key']}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipper/2.0"
        }

        try:
            req = urllib.request.Request(provider["url"], data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as e:
            print(f"Provider '{provider['name']}' call error: {e}")
            return None

    def _call_gemini(self, provider: dict, prompt: str, system_prompt: str) -> dict:
        url = f"{provider['url']}?key={provider['key']}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": f"{system_prompt}\n\nPrompt: {prompt}"}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipper/2.0"
        }

        try:
            req = urllib.request.Request(url, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
        except Exception as e:
            print(f"Gemini API call error: {e}")
            return None

    def transcribe_audio_groq(self, audio_filepath: str) -> dict:
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or not os.path.exists(audio_filepath):
            return None

        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        cmd = [
            "curl", "-s", "-X", "POST", url,
            "-H", f"Authorization: Bearer {groq_key}",
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
