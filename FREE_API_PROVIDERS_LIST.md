# 🎁 Ultimate List of Generous Free-Tier AI & Media APIs

You can hook all of these generous free-tier API providers directly into **ClipPulse AI** (`auto-clipper`) to generate video shorts, stickman animations, AI voiceovers, and stock footage **100% for free**!

---

## ⚡ 1. Ultra-Fast LLM Inference Providers

| Provider | Free Tier Allowance | Models Included | Signup Link | Key Name in Code |
| :--- | :--- | :--- | :--- | :--- |
| **Groq** | 30 Requests / Min (Free) | Llama 3.3 70B, DeepSeek-R1, Whisper Large v3 | [console.groq.com](https://console.groq.com) | `GROQ_API_KEY` |
| **Cerebras Cloud** | 30 RPM (World's fastest @ 2000 tokens/s!) | Llama 3.3 70B, Llama 3.1 80B | [cloud.cerebras.ai](https://cloud.cerebras.ai) | `CEREBRAS_API_KEY` |
| **SambaNova Cloud** | Generous Free Tier | DeepSeek-R1, Llama 3.3 70B Instruct | [cloud.sambanova.ai](https://cloud.sambanova.ai) | `SAMBANOVA_API_KEY` |
| **SiliconFlow** | Free sign-up credits | Qwen 2.5 72B, DeepSeek V3, FLUX.1 | [siliconflow.cn](https://siliconflow.cn) | `SILICONFLOW_API_KEY` |
| **Google Gemini API** | 15 RPM / 1M tokens/min (Free AI Studio) | Gemini 2.0 Flash, Gemini 1.5 Pro | [aistudio.google.com](https://aistudio.google.com) | `GEMINI_API_KEY` |
| **OpenRouter** | Select 100% free models | DeepSeek R1 free endpoints, Mistral, Gemma 2 | [openrouter.ai](https://openrouter.ai) | `OPENROUTER_API_KEY` |
| **Anything.com** | Workspace Free Tier | Custom models / AI assistant | [anything.com](https://anything.com) | `ANYTHING_API_KEY` |

---

## 🎙️ 2. Speech-to-Text & Voice Synthesis (TTS) APIs

| Provider | Free Tier Allowance | Function | Key Name in Code |
| :--- | :--- | :--- | :--- |
| **Groq Whisper LPU** | Free fast audio transcribing | Converts audio to word-level timestamps in ~3s | `GROQ_API_KEY` |
| **Deepgram** | **$200 Free Credits** (~200+ hours audio) | Speech-to-Text & Nova-2 transcription | `DEEPGRAM_API_KEY` |
| **AssemblyAI** | **100 Free Hours** / month | Word-level speech timestamps & chapter detection | `ASSEMBLYAI_API_KEY` |
| **ElevenLabs** | **10,000 Characters / month** | Ultra-realistic AI voice cloning & narration | `ELEVENLABS_API_KEY` |
| **Edge-TTS (Microsoft)** | **100% Free Unlimited** (Zero API Key!) | Neural voices (Onyx, Guy, Aria, Jenny) | *(Built-in)* |

---

## 🎨 3. Image & Stock Footage B-Roll APIs

| Provider | Free Tier Allowance | Purpose | Key Name in Code |
| :--- | :--- | :--- | :--- |
| **Pollinations.ai** | **100% Free Unlimited** (No key required!) | FLUX.1 & SDXL high-res artwork / stickman scenes | *(Built-in)* |
| **Pexels API** | **200 Requests / Hour** (100% Free) | HD/4K Stock footage clips for B-roll overlays | `PEXELS_API_KEY` |
| **Pixabay API** | **5,000 Requests / Hour** (100% Free) | Free stock video clips and royalty-free music | `PIXABAY_API_KEY` |
| **Fal.ai** | Free trial credits | FLUX.1 Schnell & Dev fast image rendering | `FAL_KEY` |

---

## 📲 4. Social Media Auto-Publishing APIs

| Provider | Free Tier Allowance | Supported Networks | Key Name in Code |
| :--- | :--- | :--- | :--- |
| **YouTube Data API v3** | **10,000 Quota Units / day** (~60 shorts/day!) | YouTube Shorts | `YOUTUBE_OAUTH_TOKEN` |
| **Upload-Post API** | **10 Free Uploads / month** | YouTube Shorts, TikTok, Instagram Reels | `UPLOAD_POST_API_KEY` |
| **TikTok Content Posting API** | Free native developer access | TikTok direct auto-posting | `TIKTOK_ACCESS_TOKEN` |
| **Meta Graph API** | Free native developer access | Instagram Reels & Facebook Reels | `INSTAGRAM_ACCESS_TOKEN` |

---

## 🛠️ How to Add Any Key to GitHub Actions
Simply visit **[github.com/Rawbeew/auto-clipper/settings/secrets/actions](https://github.com/Rawbeew/auto-clipper/settings/secrets/actions)** and add secret names matching the table above!
