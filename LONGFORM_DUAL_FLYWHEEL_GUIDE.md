# 📽️ 15–35 Minute Long-Form Narrative Engine & Dual Monetization Strategy

By incorporating **15 to 35-minute horizontal 16:9 documentary-style videos**, your channel taps into the highest monetization tier on YouTube (8+ minute videos unlock **mid-roll ad placements**), while automatically producing vertical 9:16 Shorts to drive viral subscriber acquisition across TikTok, Instagram Reels, and YouTube Shorts!

---

## 💡 The Dual Monetization Flywheel Architecture

```
                      [Topic Prompt / Trend Scraper Signal]
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │   15 to 35-Minute Long-Form Scriptwriter  │
                  │ (5-Chapter Structure + Multi-Characters)  │
                  └─────────────────────┬─────────────────────┘
                                        │
                   ┌────────────────────┴────────────────────┐
                   ▼                                         ▼
   [16:9 Horizontal Master Video]            [Auto-Extracted 9:16 Promo Shorts]
   - Multi-Character Stickmen                 - Highest CTR 30-45s moments
   - YouTube Chapter Markers                  - Submagic Animated Captions
   - Mid-Roll Ad Placements                   - Funnel traffic to Long-Form video
                   │                                         │
                   ▼                                         ▼
 [Delivered to Telegram/Discord/YT]        [Delivered to Telegram/Discord/TikTok/Reels]
```

---

## 🎬 How Long-Form Video Generation Works

1. **5-Chapter Narrative Script Structure (`worker/longform_generator.py`)**:
   - **Chapter 1 (00:00 - 03:15)**: The Irresistible Hook & Core Mystery
   - **Chapter 2 (03:15 - 07:30)**: Historical Origins & Context
   - **Chapter 3 (07:30 - 11:45)**: Technical, Scientific, or Economic Deep Dive
   - **Chapter 4 (11:45 - 14:10)**: Hidden Case Studies & Unintended Consequences
   - **Chapter 5 (14:10 - 15:00+)**: The Future & Mind-Blowing Conclusion

2. **Multi-Character Interaction & Positioning**:
   - Supports **Narrator Stickman**, **Expert Guest**, **Inquisitive Host**, and **Skeptic** with dynamic speech bubbles and pose changes.
   - Generates 1920x1080 horizontal HD frames with character badges and chapter titles.

3. **YouTube Chapter Timestamps**:
   Every generated long-form video produces formatted YouTube Chapter timestamps ready to paste into your YouTube video description:
   ```text
   📌 CHAPTER TIMESTAMPS:
   00:00 - The Mystery
   03:15 - The Hidden History
   07:30 - How It Actually Works
   11:45 - Unintended Consequences
   14:10 - The Mind-Blowing Future
   ```

4. **Automatic Promo Short Extraction**:
   For every long-form documentary created, the pipeline automatically extracts **3 vertical 9:16 promo shorts** to post on TikTok, Instagram Reels, and YouTube Shorts with a call to action:
   > *"Watch the full 15-minute documentary on our main channel!"*

---

## 🚀 How to Generate Long-Form Videos

### Option A: From the Web Dashboard
1. Open **[https://auto-clipper-32i.pages.dev](https://auto-clipper-32i.pages.dev)**
2. Select the **📹 15-35 Min Long-Form** tab.
3. Select target duration (15, 25, or 35 minutes).
4. Click **Generate 15-35 Min Video + Auto-Extract Shorts**.

### Option B: From Terminal / GitHub Runner
```bash
# Generate a 25-minute documentary with automatic shorts extraction
python worker/main.py --longform --topic "How the Roman Empire Truly Collapsed" --minutes 25
```
