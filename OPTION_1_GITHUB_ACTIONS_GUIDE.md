# 🚀 Option 1 Setup Guide: 100% Serverless GitHub Actions Video Pipeline

This setup runs your video clipping, 9:16 vertical cropping, dynamic captioning, and social auto-posting **completely free with zero hosted servers**, utilizing **GitHub Actions** virtual machines (2,000 free runner minutes per month).

---

## 🛠️ Complete Setup Guide (5 Minutes)

### Step 1: Push Project to a GitHub Repository
1. Initialize git and push this project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of AutoClipper pipeline"
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/auto-clipper.git
   git push -u origin main
   ```

---

### Step 2: Configure API Secrets in GitHub
Go to your GitHub repository in your web browser:
1. Click **Settings** (top navigation tab of your repository).
2. On the left sidebar, click **Secrets and variables** -> **Actions**.
3. Click **New repository secret** for each of the following keys:

| Secret Name | Purpose | How to Get It |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | Audio transcription (Whisper) & viral hook identification (GPT-4o-mini). | Get from [platform.openai.com](https://platform.openai.com/api-keys). |
| `YOUTUBE_OAUTH_TOKEN` | Auto-posts 9:16 shorts to YouTube. | Google Cloud Console -> YouTube Data API v3 OAuth. |
| `TIKTOK_ACCESS_TOKEN` | Auto-posts videos directly to TikTok. | TikTok Developer Portal -> Content Posting API v2. |
| `INSTAGRAM_ACCESS_TOKEN` | Auto-posts Reels to Instagram. | Meta for Developers -> Instagram Graph API. |

---

### Step 3: Connect Cloudflare Pages Frontend (Optional but Recommended)
Deploy the frontend UI on Cloudflare Pages so you can submit video links from a web browser or mobile phone:

1. Deploy `public/` to Cloudflare Pages:
   ```bash
   wrangler pages deploy public --project-name=auto-clipper
   ```
2. In the Cloudflare Pages Dashboard, go to **Settings > Environment variables > Add Variable**:
   - `GITHUB_PAT`: A GitHub Personal Access Token with scope `repo` or `workflow` (generated at [github.com/settings/tokens](https://github.com/settings/tokens)).
   - `GITHUB_REPO`: `YOUR_GITHUB_USERNAME/auto-clipper`
3. Now, whenever you paste a URL in your Cloudflare Pages dashboard, it triggers the GitHub Actions workflow instantly!

---

## 📱 How to Trigger Video Clipping & Auto-Posting

You have **3 convenient ways** to process videos without running any servers:

### Method A: Via your Cloudflare Pages Web Dashboard
1. Open your live Cloudflare Pages URL (e.g. `https://auto-clipper.pages.dev`).
2. Paste any YouTube link (e.g. podcast, interview, vlog) into the URL field.
3. Select max clips (e.g., 3 shorts) and caption style.
4. Click **Run AI Pipeline & Auto-Post**.
5. The Cloudflare Edge Function dispatches the event to GitHub Actions, which renders the videos and auto-posts them!

### Method B: Directly from GitHub Actions Tab
1. Open your repository on GitHub.
2. Click the **Actions** tab.
3. Select **AutoClipper Serverless Pipeline** on the left menu.
4. Click **Run workflow**, paste your video URL, and click the green **Run workflow** button.

### Method C: By Opening a GitHub Issue (Mobile friendly!)
1. Open a new **Issue** on your GitHub repository from your phone or desktop.
2. Paste the YouTube URL anywhere in the issue text or title.
3. Add the label `make-short`.
4. GitHub Actions will process the link, render the shorts, auto-post to YouTube/TikTok/IG, and post a confirmation comment on the issue!

---

## ⚙️ How the Pipeline Executes on GitHub Runners

```
[User Input (Cloudflare / GitHub Issue / Actions UI)]
                      │
                      ▼
[GitHub Actions Ubuntu Runner Virtual Machine Provisions]
                      │
                      ├─ 1. yt-dlp fetches raw video audio/video
                      ├─ 2. OpenAI Whisper extracts word-level timestamps
                      ├─ 3. GPT-4o-mini identifies viral hooks & punchlines
                      ├─ 4. FFmpeg crops 16:9 to vertical 9:16 & bakes dynamic subtitles
                      └─ 5. Uploads to YouTube Shorts, TikTok & IG Reels
                      │
                      ▼
[Runner VM Shuts Down & Terminates (0 Server Cost)]
```
