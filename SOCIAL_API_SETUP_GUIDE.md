# 📲 Social Media Auto-Publishing API Setup Guide

This guide explains how to obtain and attach credentials for **YouTube Shorts**, **TikTok**, and **Instagram Reels** so your automated pipeline posts generated 9:16 videos and Stickman animations directly to your channels.

---

## 🚀 Shortcut Option: Upload-Post API (Easiest Method)

If you want to skip configuring 3 separate complex OAuth developer dashboards, you can use **[Upload-Post.com](https://upload-post.com)** (10 free uploads/month, zero developer app approval required):

1. Sign up for free at [upload-post.com](https://upload-post.com).
2. Connect your YouTube, TikTok, and Instagram accounts with one-click OAuth.
3. Grab your single **Upload-Post API Key**.
4. Add it to GitHub Actions as `UPLOAD_POST_API_KEY`.

*(The pipeline in `worker/publisher.py` automatically detects `UPLOAD_POST_API_KEY` and publishes to all three networks in one shot!)*

---

## 🛠️ Direct Developer API Method (Individual Platforms)

### 🔴 1. YouTube Shorts (YouTube Data API v3)

#### Step-by-Step:
1. Log in to [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Create Project** -> Name: `AutoClipper Publisher`.
3. In the search bar, search for **YouTube Data API v3** and click **Enable**.
4. Go to **OAuth Consent Screen** -> Select **External** -> Add your Google email address under **Test Users**.
5. Go to **Credentials** -> **Create Credentials** -> **OAuth Client ID** -> App type: **Desktop App**.
6. Copy your `Client ID` and `Client Secret`.
7. Obtain a Refresh Token using Google OAuth Playground ([developers.google.com/oauthplayground](https://developers.google.com/oauthplayground)):
   - Select scope: `https://www.googleapis.com/auth/youtube.upload`
   - Authorize API & exchange authorization code for tokens.
8. Save the **Refresh Token** as `YOUTUBE_OAUTH_TOKEN` in GitHub secrets.

*Note: Any video under 60 seconds with 9:16 vertical resolution uploaded via `videos.insert` is automatically processed by YouTube as a YouTube Short.*

---

### 🎵 2. TikTok Direct Auto-Posting (TikTok Content Posting API v2)

#### Step-by-Step:
1. Register a developer account at [developers.tiktok.com](https://developers.tiktok.com/).
2. Go to **My Apps** -> **Create App**.
3. Under **Products**, add **Content Posting API**.
4. Request permissions:
   - `video.upload`
   - `video.publish`
5. Click **Generate Access Token** or authorize your personal TikTok channel.
6. Save the **User Access Token** as `TIKTOK_ACCESS_TOKEN` in GitHub secrets.

---

### 📸 3. Instagram Reels (Meta Graph API)

#### Step-by-Step:
1. Ensure your Instagram account is converted to a **Professional / Creator Account** and linked to a **Facebook Page**.
2. Go to [developers.facebook.com](https://developers.facebook.com/) -> **Create App** -> Select **Other / Business**.
3. Add **Instagram Graph API** product to your app.
4. Go to **Graph API Explorer** ([developers.facebook.com/tools/explorer](https://developers.facebook.com/tools/explorer/)):
   - Select permissions: `instagram_basic`, `instagram_content_publish`, `pages_show_list`.
   - Click **Generate Access Token**.
5. Exchange short-lived token for a **Long-Lived Token** (valid for 60 days).
6. Save the token as `INSTAGRAM_ACCESS_TOKEN` in GitHub secrets.

---

## ⚡ How to Add Any Token to Your Private GitHub Secrets

Once you have your tokens, you can either:

### Method A: Paste using Python Helper Script
Run this single command in your terminal or reply to me with your tokens:
```bash
python worker/social_auth_helper.py \
  --yt "YOUR_YOUTUBE_REFRESH_TOKEN" \
  --tt "YOUR_TIKTOK_ACCESS_TOKEN" \
  --ig "YOUR_INSTAGRAM_ACCESS_TOKEN"
```

### Method B: Manual Paste in GitHub Settings
1. Go to **[github.com/Rawbeew/auto-clipper/settings/secrets/actions](https://github.com/Rawbeew/auto-clipper/settings/secrets/actions)**.
2. Click **New repository secret** and paste your token under:
   - `YOUTUBE_OAUTH_TOKEN`
   - `TIKTOK_ACCESS_TOKEN`
   - `INSTAGRAM_ACCESS_TOKEN`
