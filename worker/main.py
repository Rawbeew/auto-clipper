import os
import re
import time
import json
import argparse
import urllib.request

try:
    from fastapi import FastAPI, BackgroundTasks, HTTPException, Header
    from pydantic import BaseModel
    app = FastAPI(title="AutoClipper Complete Algorithmic Media Engine", version="3.0.0")
except ImportError:
    app = None
    BaseModel = object

from downloader import VideoDownloader
from transcriber import AudioTranscriber
from highlight_detector import HighlightDetector
from video_processor import VideoProcessor
from publisher import SocialPublisher
from stickman_generator import StickmanGenerator
from trend_researcher import NicheTrendResearcher
from longform_generator import LongformNarrativeEngine
from youtube_algorithm_cracker import YouTubeAlgorithmCracker
from motion_engine import MotionSkillsManimEngine

downloader = VideoDownloader()
transcriber = AudioTranscriber()
highlight_detector = HighlightDetector()
video_processor = VideoProcessor()
publisher = SocialPublisher()
stickman_gen = StickmanGenerator()
trend_researcher = NicheTrendResearcher()
longform_engine = LongformNarrativeEngine()
algo_cracker = YouTubeAlgorithmCracker()
motion_engine = MotionSkillsManimEngine()

def send_telegram_direct_message(text: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "8896330204:AAEA7qU8xFs60slVfRwMCJ0971iRVzMV0vg")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "7058639926")
    if not bot_token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            pass
    except Exception as e:
        print(f"Direct Telegram error: {e}")

def process_pipeline_job(request):
    mode = getattr(request, 'mode', 'stickman')
    jobId = getattr(request, 'jobId', 'cli_job')
    print(f"=== Starting Algorithmic Job: {jobId} (Mode: {mode}) ===")
    rendered_shorts = []

    # MODE A: TREND RESEARCH
    if mode == "research":
        niche_key = getattr(request, 'niche', 'saas_tech') or "saas_tech"
        report = trend_researcher.research_niche_trends(niche_key)
        ideas = report.get("viral_research_ideas", [])

        formatted_msg = f"🔥 *DAILY TRENDING CONTENT IDEAS FOR:* `{niche_key.upper()}`\n\n"
        for i, idea in enumerate(ideas[:3]):
            formatted_msg += (
                f"*{i+1}. {idea.get('concept_title', 'Viral Idea')}*\n"
                f"💵 *Estimated CPM:* {idea.get('estimated_cpm_range', '$15-$35 CPM')}\n"
                f"📌 *Recommended Format:* {idea.get('recommended_format', 'Short / Longform')}\n"
                f"💡 *Hook Angle:* {idea.get('hook_angle', 'Curiosity Gap')}\n"
                f"🚀 *Quick Trigger:* `/make {idea.get('concept_title', '')}`\n\n"
            )
        formatted_msg += "👉 *Copy any quick trigger line above and paste back in chat to generate the video!*"

        send_telegram_direct_message(formatted_msg)
        return report

    # MODE B: LONG-FORM DOCUMENTARY GENERATOR
    elif mode == "longform":
        topic = getattr(request, 'ideaPrompt', None) or "The History of Artificial Intelligence"
        target_minutes = getattr(request, 'targetMinutes', 15)
        algo_data = algo_cracker.optimize_video_for_algorithm(topic, content_type="longform")
        ctr_title = algo_data.get("ctr_titles", [topic])[0]
        seo_hashtags = " ".join([f"#{t.replace(' ', '')}" for t in algo_data.get("youtube_seo_tags", ["Shorts", "Viral"])[:6]])

        doc_res = longform_engine.create_longform_documentary(topic, target_minutes)

        longform_description = (
            f"🎯 OPTIMIZED CTR TITLE: {ctr_title}\n\n"
            f"⚡ 0-3s HOOK: {algo_data.get('pattern_interrupt_hook', '')}\n\n"
            f"📌 YOUTUBE CHAPTER TIMESTAMPS:\n{doc_res['youtube_chapters']}\n\n"
            f"🏷️ SEO TAGS:\n{seo_hashtags}"
        )

        longform_file = os.path.join(longform_engine.output_dir, f"{jobId}_longform.mp4")
        if not os.path.exists(longform_file):
            with open(longform_file, "wb") as f:
                f.write(b"")

        post_platforms = getattr(request, 'postPlatforms', {})
        publish_results = publisher.publish_clip(
            video_path=longform_file,
            title=ctr_title,
            description=longform_description,
            platforms=post_platforms,
            virality_score=99
        )

        return doc_res

    # MODE C: ANIMATED STICKMAN SHORT (Casually Explained + Motion-Skills Tier)
    elif mode == "stickman" or (getattr(request, 'ideaPrompt', None) and "stickman" in getattr(request, 'ideaPrompt', '').lower()):
        topic = getattr(request, 'ideaPrompt', None) or "Why do central banks print money"
        algo_data = algo_cracker.optimize_video_for_algorithm(topic, content_type="short")
        ctr_title = algo_data.get("ctr_titles", [topic])[0]
        seo_hashtags = " ".join([f"#{t.replace(' ', '')}" for t in algo_data.get("youtube_seo_tags", ["Shorts", "Viral"])[:6]])

        # Generate Manim motion graphics helper code
        motion_engine.generate_manim_script(topic)

        short_file = stickman_gen.create_stickman_video(topic)

        short_description = (
            f"⚡ 0-3s Pattern Interrupt: \"{algo_data.get('pattern_interrupt_hook', '')}\"\n\n"
            f"🔄 Seamless Loop Phrase: \"{algo_data.get('seamless_loop_phrase', '')}\"\n\n"
            f"🏷️ SEO Tags: {seo_hashtags}"
        )

        post_platforms = getattr(request, 'postPlatforms', {})
        publish_results = publisher.publish_clip(
            video_path=short_file,
            title=ctr_title,
            description=short_description,
            platforms=post_platforms,
            virality_score=98
        )

        rendered_shorts.append({
            "clipId": f"{jobId}_stickman",
            "title": ctr_title,
            "hookText": algo_data.get("pattern_interrupt_hook", ""),
            "viralityScore": 98,
            "filePath": short_file,
            "publishResults": publish_results
        })

    # MODE D: LONG VIDEO CLIPPING
    else:
        video_url = getattr(request, 'videoUrl', None)
        topic = video_url or getattr(request, 'ideaPrompt', 'AI Trends')
        if video_url:
            download_data = downloader.download(video_url)
            video_file = download_data["filepath"]
        else:
            video_file = stickman_gen.create_stickman_video(topic)

        transcript_data = transcriber.transcribe(video_file)
        max_clips = getattr(request, 'maxClips', 3)
        highlights = highlight_detector.find_highlights(transcript_data, max_clips=max_clips)

        for i, highlight in enumerate(highlights):
            clip_id = f"{jobId}_clip_{i+1}"
            short_file = video_processor.render_short(
                input_video=video_file,
                start_time=highlight["start_time"],
                end_time=highlight["end_time"],
                words=transcript_data.get("words", []),
                clip_id=clip_id,
                caption_theme=getattr(request, 'captionTheme', 'submagic')
            )

            post_platforms = getattr(request, 'postPlatforms', {})
            publish_results = publisher.publish_clip(
                video_path=short_file,
                title=highlight["title"],
                description=highlight["hook_text"],
                platforms=post_platforms,
                virality_score=highlight.get("virality_score", 95)
            )

            rendered_shorts.append({
                "clipId": clip_id,
                "title": highlight["title"],
                "hookText": highlight["hook_text"],
                "viralityScore": highlight.get("virality_score", 95),
                "filePath": short_file,
                "publishResults": publish_results
            })

    print(f"\n✅ SUCCESS: Completed Job {jobId}.")
    return rendered_shorts

class SimpleRequest:
    def __init__(self, mode="stickman", niche="saas_tech", ideaPrompt=None, videoUrl=None, jobId="job"):
        self.mode = mode
        self.niche = niche
        self.ideaPrompt = ideaPrompt
        self.videoUrl = videoUrl
        self.jobId = jobId
        self.targetMinutes = 15
        self.maxClips = 3
        self.captionTheme = "submagic"
        self.postPlatforms = {"telegram": True, "discord": True, "youtube": True, "tiktok": True, "instagram": True}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoClipper CLI Runner")
    parser.add_argument("--url", type=str, help="Source long video URL")
    parser.add_argument("--topic", type=str, help="Idea prompt or topic")
    parser.add_argument("--stickman", action="store_true", help="Enable Stickman Animation mode")
    parser.add_argument("--longform", action="store_true", help="Enable Longform mode")
    parser.add_argument("--minutes", type=int, default=15, help="Target longform duration")
    parser.add_argument("--research", type=str, help="Niche name to research trends")
    parser.add_argument("--issue-text", type=str, help="Raw GitHub issue text")
    args = parser.parse_args()

    if args.research:
        req = SimpleRequest(mode="research", niche=args.research, jobId=f"gh_research_{int(time.time())}")
        process_pipeline_job(req)
    elif args.longform:
        req = SimpleRequest(mode="longform", ideaPrompt=args.topic or "The History of AI", jobId=f"gh_longform_{int(time.time())}")
        process_pipeline_job(req)
    else:
        req = SimpleRequest(mode="stickman" if args.stickman else "link", ideaPrompt=args.topic, videoUrl=args.url, jobId=f"gh_action_{int(time.time())}")
        process_pipeline_job(req)
