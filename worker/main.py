import os
import re
import time
import json
import argparse
import urllib.request
from fastapi import FastAPI, BackgroundTasks, HTTPException, Header
from pydantic import BaseModel

from downloader import VideoDownloader
from transcriber import AudioTranscriber
from highlight_detector import HighlightDetector
from video_processor import VideoProcessor
from publisher import SocialPublisher
from stickman_generator import StickmanGenerator
from trend_researcher import NicheTrendResearcher
from longform_generator import LongformNarrativeEngine
from youtube_algorithm_cracker import YouTubeAlgorithmCracker

app = FastAPI(title="AutoClipper Complete Algorithmic Media Engine", version="3.0.0")

class PipelineRequest(BaseModel):
    jobId: str
    mode: str = "stickman"
    videoUrl: str = None
    ideaPrompt: str = None
    targetMinutes: int = 15
    niche: str = "saas_tech"
    maxClips: int = 3
    aspectRatio: str = "9:16"
    captionTheme: str = "submagic"
    postPlatforms: dict = {"telegram": True, "discord": True, "youtube": True, "tiktok": True, "instagram": True}

downloader = VideoDownloader()
transcriber = AudioTranscriber()
highlight_detector = HighlightDetector()
video_processor = VideoProcessor()
publisher = SocialPublisher()
stickman_gen = StickmanGenerator()
trend_researcher = NicheTrendResearcher()
longform_engine = LongformNarrativeEngine()
algo_cracker = YouTubeAlgorithmCracker()

def send_telegram_direct_message(text: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
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

def process_pipeline_job(request: PipelineRequest):
    print(f"=== Starting Algorithmic Job: {request.jobId} (Mode: {request.mode}) ===")
    rendered_shorts = []

    # MODE A: TREND RESEARCH
    if request.mode == "research":
        niche_key = request.niche or "saas_tech"
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
    elif request.mode == "longform":
        topic = request.ideaPrompt or "The History of Artificial Intelligence"
        algo_data = algo_cracker.optimize_video_for_algorithm(topic, content_type="longform")
        ctr_title = algo_data.get("ctr_titles", [topic])[0]
        seo_hashtags = " ".join([f"#{t.replace(' ', '')}" for t in algo_data.get("youtube_seo_tags", ["Shorts", "Viral"])[:6]])

        doc_res = longform_engine.create_longform_documentary(topic, request.targetMinutes)

        longform_description = (
            f"🎯 OPTIMIZED CTR TITLE: {ctr_title}\n\n"
            f"⚡ 0-3s HOOK: {algo_data.get('pattern_interrupt_hook', '')}\n\n"
            f"📌 YOUTUBE CHAPTER TIMESTAMPS:\n{doc_res['youtube_chapters']}\n\n"
            f"🏷️ SEO TAGS:\n{seo_hashtags}"
        )

        longform_file = os.path.join(longform_engine.output_dir, f"{request.jobId}_longform.mp4")
        if not os.path.exists(longform_file):
            with open(longform_file, "wb") as f:
                f.write(b"")

        publish_results = publisher.publish_clip(
            video_path=longform_file,
            title=ctr_title,
            description=longform_description,
            platforms=request.postPlatforms,
            virality_score=99
        )

        return doc_res

    # MODE C: ANIMATED STICKMAN SHORT
    elif request.mode == "stickman" or (request.ideaPrompt and "stickman" in request.ideaPrompt.lower()):
        topic = request.ideaPrompt or "Why do central banks print money"
        algo_data = algo_cracker.optimize_video_for_algorithm(topic, content_type="short")
        ctr_title = algo_data.get("ctr_titles", [topic])[0]
        seo_hashtags = " ".join([f"#{t.replace(' ', '')}" for t in algo_data.get("youtube_seo_tags", ["Shorts", "Viral"])[:6]])

        short_file = stickman_gen.create_stickman_video(topic)

        short_description = (
            f"⚡ 0-3s Pattern Interrupt: \"{algo_data.get('pattern_interrupt_hook', '')}\"\n\n"
            f"🔄 Seamless Loop Phrase: \"{algo_data.get('seamless_loop_phrase', '')}\"\n\n"
            f"🏷️ SEO Tags: {seo_hashtags}"
        )

        publish_results = publisher.publish_clip(
            video_path=short_file,
            title=ctr_title,
            description=short_description,
            platforms=request.postPlatforms,
            virality_score=98
        )

        rendered_shorts.append({
            "clipId": f"{request.jobId}_stickman",
            "title": ctr_title,
            "hookText": algo_data.get("pattern_interrupt_hook", ""),
            "viralityScore": 98,
            "filePath": short_file,
            "publishResults": publish_results
        })

    # MODE D: LONG VIDEO CLIPPING (YouTube Link)
    else:
        topic = request.videoUrl or request.ideaPrompt
        if request.videoUrl:
            download_data = downloader.download(request.videoUrl)
            video_file = download_data["filepath"]
        else:
            video_file = stickman_gen.create_stickman_video(topic)

        transcript_data = transcriber.transcribe(video_file)
        highlights = highlight_detector.find_highlights(transcript_data, max_clips=request.maxClips)

        for i, highlight in enumerate(highlights):
            clip_id = f"{request.jobId}_clip_{i+1}"
            short_file = video_processor.render_short(
                input_video=video_file,
                start_time=highlight["start_time"],
                end_time=highlight["end_time"],
                words=transcript_data.get("words", []),
                clip_id=clip_id,
                caption_theme=request.captionTheme
            )

            publish_results = publisher.publish_clip(
                video_path=short_file,
                title=highlight["title"],
                description=highlight["hook_text"],
                platforms=request.postPlatforms,
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

    print(f"\n✅ SUCCESS: Completed Algorithmic Job {request.jobId}.")
    return rendered_shorts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoClipper CLI / GitHub Actions Runner")
    parser.add_argument("--url", type=str, help="Source long video URL")
    parser.add_argument("--topic", type=str, help="Idea prompt or topic")
    parser.add_argument("--stickman", action="store_true", help="Enable Stickman Animation mode")
    parser.add_argument("--longform", action="store_true", help="Enable 15-35 min Long-Form Documentary mode")
    parser.add_argument("--minutes", type=int, default=15, help="Target longform duration")
    parser.add_argument("--research", type=str, help="Niche name to research trends")
    parser.add_argument("--issue-text", type=str, help="Raw GitHub issue text")
    args = parser.parse_args()

    if args.research:
        req = PipelineRequest(jobId=f"gh_research_{int(time.time())}", mode="research", niche=args.research)
        process_pipeline_job(req)
    elif args.longform:
        req = PipelineRequest(
            jobId=f"gh_longform_{int(time.time())}",
            mode="longform",
            ideaPrompt=args.topic or args.issue_text or "The Untold History of AI",
            targetMinutes=args.minutes
        )
        process_pipeline_job(req)
    else:
        target_url = args.url
        if not target_url and args.issue_text:
            target_url = extract_url_from_text(args.issue_text)

        is_stickman = args.stickman or (args.topic is not None)

        req = PipelineRequest(
            jobId=f"gh_action_{int(time.time())}",
            mode="stickman" if is_stickman else "link",
            videoUrl=target_url,
            ideaPrompt=args.topic or args.issue_text or "Why central banks print money"
        )
        process_pipeline_job(req)
