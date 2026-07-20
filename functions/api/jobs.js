// Cloudflare Pages Function: /api/jobs
export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const jobId = url.searchParams.get('id');

  if (!jobId) {
    return new Response(JSON.stringify({ error: "Job ID query parameter required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" }
    });
  }

  // Returns mock or Cloudflare KV state for job progress
  return new Response(JSON.stringify({
    jobId,
    status: "completed",
    progressPercent: 100,
    step: "publishing_completed",
    clips: [
      {
        id: `${jobId}_1`,
        title: "Extracted Highlight #1",
        viralityScore: 92,
        duration: "00:45",
        aspectRatio: "9:16",
        downloadUrl: "https://r2.yourdomain.com/clips/sample1.mp4",
        publishedUrls: {
          youtube: "https://youtube.com/shorts/sample",
          tiktok: "https://tiktok.com/@sample/video/1",
          instagram: "https://instagram.com/reel/sample"
        }
      }
    ]
  }), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}
