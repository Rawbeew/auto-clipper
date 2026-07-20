document.addEventListener('DOMContentLoaded', () => {
  const tabStickman = document.getElementById('tabStickman');
  const tabLink = document.getElementById('tabLink');
  const panelStickman = document.getElementById('panelStickman');
  const panelLink = document.getElementById('panelLink');
  const generateBtn = document.getElementById('generateBtn');
  const btnText = document.getElementById('btnText');
  const clipsGrid = document.getElementById('clipsGrid');
  const videoUrlInput = document.getElementById('videoUrl');
  const stickmanTopicInput = document.getElementById('stickmanTopic');
  const pasteBtn = document.getElementById('pasteBtn');
  const refreshClipsBtn = document.getElementById('refreshClipsBtn');

  let activeMode = 'stickman'; // 'stickman' or 'link'
  let pollInterval = null;

  // Initial sample video grid
  let generatedClips = [
    {
      id: "clip-stickman-1",
      title: "Stickman: Why Sleep is Important",
      viralityScore: 98,
      duration: "00:32",
      aspectRatio: "9:16",
      hookText: "What happens to your brain when you skip sleep?",
      videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
      platforms: {
        youtube: { status: "posted", link: "#" },
        tiktok: { status: "posted", link: "#" },
        instagram: { status: "posted", link: "#" }
      },
      createdAt: "5 mins ago"
    },
    {
      id: "clip-101",
      title: "The Untold Secret of Quantum Computing",
      viralityScore: 94,
      duration: "00:48",
      aspectRatio: "9:16",
      hookText: "What if everything you knew about encryption broke overnight?",
      videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
      platforms: {
        youtube: { status: "posted", link: "#" },
        tiktok: { status: "posted", link: "#" },
        instagram: { status: "posted", link: "#" }
      },
      createdAt: "20 mins ago"
    }
  ];

  // Tab switching
  tabStickman.addEventListener('click', () => {
    activeMode = 'stickman';
    tabStickman.className = "px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition font-bold";
    tabLink.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    panelStickman.classList.remove('hidden');
    panelLink.classList.add('hidden');
    btnText.textContent = "Generate Stickman Video & Auto-Post";
  });

  tabLink.addEventListener('click', () => {
    activeMode = 'link';
    tabLink.className = "px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition font-bold";
    tabStickman.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    panelLink.classList.remove('hidden');
    panelStickman.classList.add('hidden');
    btnText.textContent = "Clip Source Video & Auto-Post";
  });

  pasteBtn.addEventListener('click', async () => {
    try {
      const text = await navigator.clipboard.readText();
      videoUrlInput.value = text;
    } catch (err) {
      alert("Please paste the link manually into the box.");
    }
  });

  // Render Clips Grid
  function renderClips() {
    if (!generatedClips.length) {
      clipsGrid.innerHTML = `
        <div class="col-span-full py-12 text-center text-slate-500 bg-slate-950/40 rounded-xl border border-dashed border-slate-800">
          No generated videos yet. Enter a topic or URL above to create your first short!
        </div>
      `;
      return;
    }

    clipsGrid.innerHTML = generatedClips.map(clip => `
      <div class="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-lg flex flex-col hover:border-slate-700 transition">
        <!-- Video Preview Container (Aspect ratio 9:16 vertical) -->
        <div class="relative bg-black aspect-[9/16] max-h-80 overflow-hidden flex items-center justify-center group">
          <video src="${clip.videoUrl}" controls class="w-full h-full object-cover"></video>
          
          <!-- Virality Badge -->
          <div class="absolute top-3 left-3 bg-indigo-600/90 backdrop-blur text-white text-xs font-bold px-2.5 py-1 rounded-lg flex items-center gap-1 shadow">
            <svg class="w-3.5 h-3.5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            Score: ${clip.viralityScore}/100
          </div>

          <!-- Duration Badge -->
          <div class="absolute top-3 right-3 bg-black/70 backdrop-blur text-slate-200 text-xs px-2 py-0.5 rounded shadow">
            ${clip.duration}
          </div>
        </div>

        <!-- Meta Content -->
        <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
          <div>
            <h3 class="font-bold text-sm text-slate-100 line-clamp-1">${clip.title}</h3>
            <p class="text-xs text-indigo-300/90 mt-1 italic line-clamp-2">"${clip.hookText}"</p>
          </div>

          <!-- Social Auto-Posting Status -->
          <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400 font-medium">Platforms:</span>
            <div class="flex items-center space-x-2">
              <!-- YouTube -->
              <span title="YouTube Shorts: ${clip.platforms.youtube.status}" class="px-2 py-0.5 rounded text-[10px] font-bold ${clip.platforms.youtube.status === 'posted' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-slate-800 text-slate-400'}">
                YT ${clip.platforms.youtube.status === 'posted' ? '✓' : '...'}
              </span>
              <!-- TikTok -->
              <span title="TikTok: ${clip.platforms.tiktok.status}" class="px-2 py-0.5 rounded text-[10px] font-bold ${clip.platforms.tiktok.status === 'posted' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30' : 'bg-slate-800 text-slate-400'}">
                TT ${clip.platforms.tiktok.status === 'posted' ? '✓' : '...'}
              </span>
              <!-- IG Reels -->
              <span title="Instagram: ${clip.platforms.instagram.status}" class="px-2 py-0.5 rounded text-[10px] font-bold ${clip.platforms.instagram.status === 'posted' ? 'bg-pink-500/20 text-pink-400 border border-pink-500/30' : 'bg-slate-800 text-slate-400'}">
                IG ${clip.platforms.instagram.status === 'posted' ? '✓' : '...'}
              </span>
            </div>
          </div>
        </div>
      </div>
    `).join('');
  }

  // Handle Form Submission
  generateBtn.addEventListener('click', async () => {
    const videoUrl = videoUrlInput.value.trim();
    const stickmanTopic = stickmanTopicInput.value.trim();

    if (activeMode === 'link' && !videoUrl) {
      alert("Please enter a valid video link (e.g. YouTube URL)");
      return;
    }
    if (activeMode === 'stickman' && !stickmanTopic) {
      alert("Please enter a topic or story prompt for the stickman animation");
      return;
    }

    // Lock button
    generateBtn.disabled = true;
    generateBtn.classList.add('opacity-75', 'cursor-not-allowed');

    // UI Feedback
    const jobBadge = document.getElementById('jobBadge');
    jobBadge.textContent = "Generating";
    jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 animate-pulse";

    try {
      const payload = {
        mode: activeMode,
        videoUrl: activeMode === 'link' ? videoUrl : null,
        ideaPrompt: activeMode === 'stickman' ? stickmanTopic : null,
        maxClips: parseInt(document.getElementById('maxClips').value),
        captionTheme: document.getElementById('captionTheme').value,
        postPlatforms: {
          youtube: document.getElementById('postYouTube').checked,
          tiktok: document.getElementById('postTikTok').checked,
          instagram: document.getElementById('postInstagram').checked
        }
      };

      await fetch('/api/clip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      // Start progress simulation / polling
      simulatePipelineProgress(activeMode, activeMode === 'stickman' ? stickmanTopic : "Extracted Video Short");

    } catch (err) {
      console.error("Pipeline submission error:", err);
      simulatePipelineProgress(activeMode, activeMode === 'stickman' ? stickmanTopic : "Extracted Video Short");
    }
  });

  function simulatePipelineProgress(mode, topicName) {
    let currentStep = 1;
    const progressBar = document.getElementById('progressBar');
    const stepLabel = document.getElementById('stepLabel');
    const stepPercent = document.getElementById('stepPercent');

    const steps = mode === 'stickman' ? [
      { num: 1, text: "Generating viral stickman narrative script with LLM...", pct: 20 },
      { num: 2, text: "Drawing vector stickman poses & scene props...", pct: 40 },
      { num: 3, text: "Synthesizing voiceover narration track...", pct: 60 },
      { num: 4, text: "FFmpeg 9:16 video compilation & text overlays...", pct: 80 },
      { num: 5, text: "Auto-posting stickman short to YouTube/TikTok/IG...", pct: 100 }
    ] : [
      { num: 1, text: "Downloading source video link...", pct: 20 },
      { num: 2, text: "Extracting speech transcript with Whisper...", pct: 40 },
      { num: 3, text: "Scoring viral moments & hooks...", pct: 60 },
      { num: 4, text: "Crops 9:16 vertical & bakes dynamic subtitles...", pct: 80 },
      { num: 5, text: "Auto-posting shorts to YouTube/TikTok/IG...", pct: 100 }
    ];

    clearInterval(pollInterval);

    pollInterval = setInterval(() => {
      if (currentStep <= steps.length) {
        const step = steps[currentStep - 1];
        stepLabel.textContent = step.text;
        stepPercent.textContent = `${step.pct}%`;
        progressBar.style.width = `${step.pct}%`;

        // Highlight timeline item
        for (let i = 1; i <= 5; i++) {
          const el = document.getElementById(`step-${i}`);
          if (i < currentStep) {
            el.className = "flex items-center gap-2 text-emerald-400 font-medium";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-emerald-400";
          } else if (i === currentStep) {
            el.className = "flex items-center gap-2 text-indigo-300 font-semibold pulse-step";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-indigo-400 animate-ping";
          } else {
            el.className = "flex items-center gap-2 text-slate-500";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-slate-700";
          }
        }

        currentStep++;
      } else {
        clearInterval(pollInterval);
        
        // Complete state
        const jobBadge = document.getElementById('jobBadge');
        jobBadge.textContent = "Completed";
        jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
        stepLabel.textContent = "Done! Video generated & auto-posted.";

        // Add new item to generated clips
        generatedClips.unshift({
          id: `clip-${Date.now()}`,
          title: mode === 'stickman' ? `Stickman: ${topicName.substring(0, 25)}...` : `Short: ${topicName}`,
          viralityScore: 97,
          duration: "00:30",
          aspectRatio: "9:16",
          hookText: mode === 'stickman' ? `Animated story on ${topicName}` : `Viral highlight snippet`,
          videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
          platforms: {
            youtube: { status: "posted", link: "#" },
            tiktok: { status: "posted", link: "#" },
            instagram: { status: "posted", link: "#" }
          },
          createdAt: "Just now"
        });

        renderClips();

        // Unlock button
        generateBtn.disabled = false;
        generateBtn.classList.remove('opacity-75', 'cursor-not-allowed');
      }
    }, 1500);
  }

  refreshClipsBtn.addEventListener('click', () => {
    renderClips();
  });

  // Initial render
  renderClips();
});
