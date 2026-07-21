import os
import re
import time
import json
import argparse
from fastapi import FastAPI, BackgroundTasks, HTTPException, Header
from pydantic import BaseModel

from downloader import VideoDownloader
from transcriber import AudioTranscriber
from highlight_detector import HighlightDetector
from video_processor import VideoProcessor
from publisher import SocialPublisher
from stickman_generator import StickmanGenerator
from trend_researcher import NicheTrendResearcher

app = FastAPI(title="AutoClipper Video Compute Service", version="1.0.0")

class PipelineRequest(BaseModel):
    jobId: str
    mode: str = "link" # "link", "stickman", or "research"
    videoUrl: str = None
    ideaPrompt: str = None
    niche: str = "science"
    maxClips: int = 3
    aspectRatio: str = "9:16"
    captionTheme: str = "submagic"
    postPlatforms: dict = {"telegram": True, "youtube": True, "tiktok": True, "instagram": True}

downloader = VideoDownloader()
transcriber = AudioTranscriber()
highlight_detector = HighlightDetector()
video_processor = VideoProcessor()
publisher = SocialPublisher()
stickman_gen = StickmanGenerator()
trend_researcher = NicheTrendResearcher()

def extract_url_from_text(text: str) -> str:
    if not text:
        return None
    match = re.search(r'https?://[^\s<"]+', text)
    return match.group(0) if match else None

def process_pipeline_job(request: PipelineRequest):
    print(f"=== Starting Processing Pipeline for Job: {request.jobId} (Mode: {request.mode}) ===")
    rendered_shorts = []

    # MODE A: TREND RESEARCH
    if request.mode == "research":
        print(f"Executing Niche & Script Research for '{request.niche}'...")
        research_results = trend_researcher.research_niche_trends(request.niche)
        print("Research Results:")
        print(json.dumps(research_results, indent=2))
        return research_results

    # MODE B: STICKMAN ANIMATION GENERATOR
    elif request.mode == "stickman" or (request.ideaPrompt and "stickman" in request.ideaPrompt.lower()):
        topic = request.ideaPrompt or "Curious Science Facts"
        print(f"Generating Stickman Animated Video for topic: '{topic}'...")
        short_file = stickman_gen.create_stickman_video(topic)

        print("Publishing stickman animation short to connected platforms & Telegram...")
        publish_results = publisher.publish_clip(
            video_path=short_file,
            title=f"Stickman: {topic[:30]}",
            description=f"Watch this quick animated stickman video about {topic}! #Shorts #Animation",
            platforms=request.postPlatforms,
            virality_score=97
        )

        rendered_shorts.append({
            "clipId": f"{request.jobId}_stickman",
            "title": f"Stickman Animation: {topic}",
            "hookText": f"Stickman animated story on {topic}",
            "viralityScore": 97,
            "filePath": short_file,
            "publishResults": publish_results
        })

    # MODE C: LONG VIDEO CLIPPING (YouTube / MP4 Link)
    else:
        if request.videoUrl:
            print(f"Step 1: Downloading video from {request.videoUrl}...")
            download_data = downloader.download(request.videoUrl)
            video_file = download_data["filepath"]
        else:
            video_file = stickman_gen.create_stickman_video(request.ideaPrompt or "AI Trends")

        print("Step 2: Transcribing audio with word timestamps (Groq / Whisper)...")
        transcript_data = transcriber.transcribe(video_file)

        print("Step 3: Detecting viral highlights with LLM...")
        highlights = highlight_detector.find_highlights(transcript_data, max_clips=request.maxClips)

        for i, highlight in enumerate(highlights):
            print(f"Step 4: Processing highlight #{i+1} ('{highlight['title']}')...")
            clip_id = f"{request.jobId}_clip_{i+1}"
            short_file = video_processor.render_short(
                input_video=video_file,
                start_time=highlight["start_time"],
                end_time=highlight["end_time"],
                words=transcript_data.get("words", []),
                clip_id=clip_id,
                caption_theme=request.captionTheme
            )

            print(f"Step 5: Publishing clip #{i+1} to platforms & Telegram...")
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

    print(f"\n✅ SUCCESS: Completed Job {request.jobId}. Processed {len(rendered_shorts)} item(s).")
    return rendered_shorts

@app.post("/process")
def handle_process(req: PipelineRequest, background_tasks: BackgroundTasks, authorization: str = Header(None)):
    secret_key = os.getenv("COMPUTE_SECRET_KEY", "demo_key")
    if authorization and authorization.replace("Bearer ", "") != secret_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    background_tasks.add_task(process_pipeline_job, req)
    return {
        "status": "queued",
        "jobId": req.jobId,
        "message": "Pipeline worker accepted request"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoClipper CLI / GitHub Actions Runner")
    parser.add_argument("--url", type=str, help="Source long video URL")
    parser.add_argument("--topic", type=str, help="Idea prompt or topic for Stickman Animation")
    parser.add_argument("--stickman", action="store_true", help="Enable Stickman Animation mode")
    parser.add_argument("--research", type=str, help="Niche name to research trends (e.g. 'tech', 'science', 'finance')")
    parser.add_argument("--issue-text", type=str, help="Raw GitHub issue text")
    parser.add_argument("--clips", type=int, default=3, help="Max clips to render")
    parser.add_argument("--theme", type=str, default="submagic", help="Caption theme style")
    args = parser.parse_args()

    if args.research:
        researcher = NicheTrendResearcher()
        res = researcher.research_niche_trends(args.research)
        print(json.dumps(res, indent=2))
    else:
        target_url = args.url
        if not target_url and args.issue_text:
            target_url = extract_url_from_text(args.issue_text)

        is_stickman = args.stickman or (args.topic is not None)

        if target_url or is_stickman or args.issue_text:
            req = PipelineRequest(
                jobId=f"gh_action_{int(time.time())}",
                mode="stickman" if is_stickman else "link",
                videoUrl=target_url,
                ideaPrompt=args.topic or args.issue_text or "Quantum Physics",
                maxClips=args.clips,
                captionTheme=args.theme
            )
            process_pipeline_job(req)
        else:
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000)
