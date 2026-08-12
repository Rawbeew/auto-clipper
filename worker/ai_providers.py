import os
import time
import json
import subprocess
import urllib.request

class MultiAIProvider:
    """
    Unified AI Multi-Provider Client optimized for Anthropic Claude 3.5 Sonnet (#1),
    Kimi Moonshot AI (#2), DeepSeek Native (#3), Groq LPU (#4), Cerebras (#5), 
    SiliconFlow (#6), Gemini 2.0 (#7), Anything.com (#8), and OpenAI (#9).
    Provides sub-second scriptwriting, speech-to-text, and vector artwork generation.
    """
    def __init__(self):
            self.providers = [
                # PRIORITY 1: Fireworks via our Cloudflare relay (key injected server-side)
                {
                    "name": "Fireworks Relay",
                    "key": os.getenv("FIREWORKS_API_KEY") or "relay",
                    "url": "https://groq-relay.rahbiew.workers.dev/inference/v1/chat/completions",
                    "model": "accounts/fireworks/models/deepseek-v4-flash",
                    "type": "openai_compatible",
                    "cooldown_until": 0,
                    "thinking_disabled": True
                },
                # PRIORITY 2: Groq via relay (bypasses Cloudflare 1010 datacenter ban)
                {
                    "name": "Groq Relay",
                    "key": os.getenv("GROQ_API_KEY") or "relay",
                    "url": "https://groq-relay.rahbiew.workers.dev/v1/chat/completions",
                    "model": "llama-3.3-70b-versatile",
                    "type": "openai_compatible",
                    "cooldown_until": 0
                },
                # PRIORITY 3: SambaNova (direct, proven container-reachable)
                {
                    "name": "SambaNova",
                    "key": os.getenv("SAMBA_API_KEY"),
                    "url": "https://api.sambanova.ai/v1/chat/completions",
                    "model": "Meta-Llama-3.3-70B-Instruct",
                    "type": "openai_compatible",
                    "cooldown_until": 0
                },
                # PRIORITY 4: NVIDIA NIM (direct)
                {
                    "name": "NVIDIA NIM",
                    "key": os.getenv("NVIDIA_API_KEY"),
                    "url": "https://integrate.api.nvidia.com/v1/chat/completions",
                    "model": "deepseek-ai/deepseek-v4-flash-0731",
                    "type": "openai_compatible",
                    "cooldown_until": 0
                },
                # Legacy providers kept as referral failsafes (most have stale keys).
                # PRIORITY 5: Anthropic Claude
                {
                    "name": "Anthropic Claude",
                    "key": os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY"),
                    "url": "https://api.anthropic.com/v1/messages",
                    "model": "claude-3-5-sonnet-20241022",
                    "type": "anthropic",
                    "cooldown_until": 0
                },
                # PRIORITY 6: OpenAI
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
            
            if p["type"] == "anthropic":
                res = self._call_anthropic(p, prompt, system_prompt)
            elif p["type"] == "openai_compatible":
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

    def _call_anthropic(self, provider: dict, prompt: str, system_prompt: str) -> dict:
        payload = json.dumps({
            "model": provider["model"],
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": f"{prompt}\n\nRespond strictly in valid JSON format."}
            ]
        }).encode("utf-8")

        headers = {
            "x-api-key": provider["key"],
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipper/3.0"
        }

        try:
            req = urllib.request.Request(provider["url"], data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["content"][0]["text"]
                return json.loads(text)
        except Exception as e:
            print(f"Anthropic Claude API call error: {e}")
            return None

    def _call_openai_compatible(self, provider: dict, prompt: str, system_prompt: str) -> dict:
            payload = {
                "model": provider["model"],
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.7
            }
            # Fireworks models think by default; disable to get the raw answer,
            # same as the knife-agency failover chain.
            if provider.get("thinking_disabled"):
                payload["thinking"] = {"type": "disabled"}

            headers = {
                "Authorization": f"Bearer {provider['key']}",
                "Content-Type": "application/json",
                # Our Cloudflare relay returns 1010 for python-urllib's default UA.
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipper/3.0"
            }

            try:
                req = urllib.request.Request(provider["url"], data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=20) as resp:
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipper/3.0"
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
