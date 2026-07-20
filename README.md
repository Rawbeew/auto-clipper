# 🎬 ClipPulse AI — Video Clipping & Stickman Animation Generator

> **Turn long-form videos (or text prompts) into viral 9:16 Shorts / Reels / TikToks — with built-in Stickman Animation Generation & Social Auto-Publishing.**

---

## 🎨 Stickman Story & Video Generation Module

The repository includes a dedicated **Animated Stickman Generator** (`worker/stickman_generator.py`) inspired by Casually Explained, MinutePhysics, and CGP Grey.

### How Stickman Video Generation Works:
1. **Script Generation**: An LLM (`gpt-4o-mini` / Gemini) writes a punchy 30-second narrative script broken down into timed scenes with stickman poses (`thinking`, `pointing`, `mind_blown`, `running`, `celebrating`) and props (`lightbulb`, `fire`, `question_mark`).
2. **Vector Stickman Renderer**: Draws 1080x1920 9:16 vertical vector frames using Python Pillow & SVG drawing primitives. Handles facial expressions, joints, props, and headlines.
3. **Voiceover Synthesis**: Generates clear TTS voiceover audio.
4. **FFmpeg Compilation**: Combines stickman frames, voiceover audio, dynamic animated captions, and background music into a final vertical MP4 short.
5. **Auto-Posting**: Automatically uploads the stickman video to **YouTube Shorts**, **TikTok**, and **Instagram Reels**.

---

## 🌟 GitHub Ecosystem & Repository Comparison

| Feature | `SamurAIGPT` | `auto-yt-shorts` | `OpenShorts` | **ClipPulse AI** *(This Repo)* |
| :--- | :--- | :--- | :--- | :--- |
| **Long Video Clipping** | ✅ | ✅ | ✅ | ✅ |
| **Stickman Video Generation** | ❌ | ❌ | ❌ | **✅ Built-in Vector Stickman Engine** |
| **Cloudflare Pages UI** | ❌ | ❌ | ❌ | **✅ Included Edge Web Dashboard** |
| **Zero Hosting (GitHub Actions)** | ❌ | ❌ | ❌ | **✅ Included 100% Free Runner Workflow** |
| **Auto Social Posting** | ❌ | ✅ | ✅ | **✅ YouTube Shorts, TikTok & IG Reels** |

---

## 🚀 Quickstart & Usage

### 1. Generate Stickman Videos via CLI
```bash
cd worker
pip install -r requirements.txt

# Run Stickman generator for any topic
python main.py --stickman --topic "Why do we dream?"
```

### 2. Run via GitHub Actions ($0 Free No-Hosting)
1. Push this repo to GitHub.
2. Add your secrets (`OPENAI_API_KEY`, `YOUTUBE_OAUTH_TOKEN`, `TIKTOK_ACCESS_TOKEN`, `INSTAGRAM_ACCESS_TOKEN`) in **Settings > Secrets and variables > Actions**.
3. Go to **Actions > AutoClipper Serverless Pipeline > Run workflow** and type any topic or paste a YouTube URL!

### 3. Deploy Frontend on Cloudflare Pages
```bash
wrangler pages deploy public --project-name=auto-clipper
```
Set environment variables:
- `GITHUB_PAT`: GitHub Access Token
- `GITHUB_REPO`: `YOUR_USERNAME/auto-clipper`

---

## 📁 Repository Structure

```
auto-clipper/
├── public/                # Cloudflare Pages Edge Dashboard
│   ├── index.html         # Web UI with Stickman & Video Link tabs
│   ├── app.js             # Client controller
│   └── styles.css         # Styling
├── functions/api/         # Cloudflare Edge Functions
│   ├── clip.js            # Dispatch endpoint
│   ├── jobs.js            # Status endpoint
│   └── serverless_clip.js # Serverless cloud API orchestrator
├── worker/                # Python Processing Engine
│   ├── stickman_generator.py # 🎨 Vector Stickman Renderer & Script Engine
│   ├── main.py            # CLI Runner & FastAPI Gateway
│   ├── downloader.py      # yt-dlp Video Downloader
│   ├── transcriber.py     # OpenAI Whisper Speech-to-Text
│   ├── highlight_detector.py # LLM Viral Hook Extractor
│   ├── video_processor.py # FFmpeg Vertical 9:16 Crop & Captions
│   └── publisher.py       # Social Media Auto-Publishing API Connector
└── .github/workflows/     # 100% Free Serverless Runner
    └── auto_clipper_workflow.yml # GitHub Actions Workflow
```
