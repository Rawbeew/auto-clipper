import os
import re
import time
import argparse
from fastapi import FastAPI, BackgroundTasks, HTTPException, Header
from pydantic import BaseModel

from downloader import VideoDownloader
from transcriber import AudioTranscriber
from highlight_detector import HighlightDetector
from video_processor import VideoProcessor
from publisher import SocialPublisher
from stickman_generator import StickmanGenerator

app = FastAPI(title="AutoClipper Video Compute Service", version="1.0.0")

class PipelineRequest(BaseModel):
    jobId: str
    mode: str = "link" # "link", "idea", or "stickman"
    videoUrl: str = None
    ideaPrompt: str = None
    maxClips: int = 3
    aspectRatio: str = "9:16"
    captionTheme: str = "submagic"
    postPlatforms: dict = {"youtube": True, "tiktok": True, "instagram": True}

downloader = VideoDownloader()
transcriber = AudioTranscriber()
highlight_detector = HighlightDetector()
video_processor = VideoProcessor()
publisher = SocialPublisher()
stickman_gen = StickmanGenerator()

def extract_url_from_text(text: str) -> str:
    """Finds first http/https URL in issue body or text."""
    if not text:
        return None
    match = re.search(r'https?://[^\s<"]+', text)
    return match.group(0) if match else None

def process_pipeline_job(request: PipelineRequest):
    print(f"=== Starting Processing Pipeline for Job: {request.jobId} (Mode: {request.mode}) ===")
    rendered_shorts = []

    # MODE A: STICKMAN ANIMATION GENERATOR
    if request.mode == "stickman" or (request.ideaPrompt and "stickman" in request.ideaPrompt.lower()):
        print(f"Step 1: Generating Stickman Animated Video for topic: '{request.ideaPrompt or 'Curious Science'}'...")
        topic = request.ideaPrompt or "Curious Facts"
        short_file = stickman_gen.create_stickman_video(topic)

        # Auto-Publish to Platforms
        print("Step 2: Auto-publishing stickman animation short to connected social accounts...")
        publish_results = publisher.publish_clip(
            video_path=short_file,
            title=f"Stickman Story: {topic[:30]}",
            description=f"Watch this quick animated stickman video about {topic}! #Shorts #Animation",
            platforms=request.postPlatforms
        )

        rendered_shorts.append({
            "clipId": f"{request.jobId}_stickman",
            "title": f"Stickman Animation: {topic}",
            "hookText": f"Stickman animated story on {topic}",
            "viralityScore": 95,
            "filePath": short_file,
            "publishResults": publish_results
        })

    # MODE B: LONG-FORM VIDEO CLIPPING (YouTube / Video Link)
    else:
        # 1. Download source video
        if request.videoUrl:
            print(f"Step 1: Downloading video from {request.videoUrl}...")
            download_data = downloader.download(request.videoUrl)
            video_file = download_data["filepath"]
        else:
            print(f"Step 1: Falling back to stickman generation for prompt...")
            video_file = stickman_gen.create_stickman_video(request.ideaPrompt or "AI Trends")

        # 2. Transcribe Audio
        print("Step 2: Transcribing audio with word timestamps (Whisper)...")
        transcript_data = transcriber.transcribe(video_file)

        # 3. Detect Highlights
        print("Step 3: Detecting viral highlights with LLM...")
        highlights = highlight_detector.find_highlights(transcript_data, max_clips=request.maxClips)

        # 4. Process Video Cuts & Burn Captions
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

            # 5. Auto-Publish to Platforms
            print(f"Step 5: Auto-publishing clip #{i+1} to connected platforms...")
            publish_results = publisher.publish_clip(
                video_path=short_file,
                title=highlight["title"],
                description=highlight["hook_text"],
                platforms=request.postPlatforms
            )

            rendered_shorts.append({
                "clipId": clip_id,
                "title": highlight["title"],
                "hookText": highlight["hook_text"],
                "viralityScore": highlight["virality_score"],
                "filePath": short_file,
                "publishResults": publish_results
            })

    print(f"\n✅ SUCCESS: Completed Pipeline Job {request.jobId}. Created & Processed {len(rendered_shorts)} short(s).")
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
    parser.add_argument("--issue-text", type=str, help="Raw GitHub issue text containing video link or prompt")
    parser.add_argument("--clips", type=int, default=3, help="Max clips to render")
    parser.add_argument("--theme", type=str, default="submagic", help="Caption theme style")
    parser.add_argument("--no-yt", action="store_true", help="Disable YouTube Shorts posting")
    parser.add_argument("--no-tt", action="store_true", help="Disable TikTok posting")
    parser.add_argument("--no-ig", action="store_true", help="Disable Instagram Reels posting")
    args = parser.parse_args()

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
            captionTheme=args.theme,
            postPlatforms={
                "youtube": not args.no_yt,
                "tiktok": not args.no_tt,
                "instagram": not args.no_ig
            }
        )
        process_pipeline_job(req)
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
