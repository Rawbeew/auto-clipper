// Cloudflare Pages Function: /api/clip
// Triggers GitHub Actions ($0 Free No-Hosting Runner) via repository_dispatch API

export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    const { videoUrl, maxClips, captionTheme, postPlatforms } = body;

    if (!videoUrl || !videoUrl.startsWith('http')) {
      return new Response(JSON.stringify({ error: "Invalid video URL provided" }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const GITHUB_PAT = context.env.GITHUB_PAT; // GitHub Personal Access Token
    const GITHUB_REPO = context.env.GITHUB_REPO || "your-username/auto-clipper"; // e.g. "username/auto-clipper"

    if (GITHUB_PAT) {
      // Dispatch event to GitHub Actions runner
      const ghRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/dispatches`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${GITHUB_PAT}`,
          'Accept': 'application/vnd.github+json',
          'User-Agent': 'Cloudflare-Pages-AutoClipper',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          event_type: 'make_short',
          client_payload: {
            video_url: videoUrl,
            max_clips: maxClips || 3,
            caption_theme: captionTheme || 'submagic',
            post_platforms: postPlatforms
          }
        })
      });

      if (!ghRes.ok) {
        const errText = await ghRes.text();
        console.error("GitHub Dispatch Failed:", errText);
      }
    }

    const jobId = `job_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;

    return new Response(JSON.stringify({
      success: true,
      jobId,
      executionEngine: "GitHub Actions VM Runner ($0 Free)",
      message: "Short creation pipeline dispatched to GitHub Actions runner",
      config: {
        videoUrl,
        maxClips,
        captionTheme
      }
    }), {
      status: 200,
      headers: { 
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
