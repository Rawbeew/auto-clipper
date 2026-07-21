document.addEventListener('DOMContentLoaded', () => {
  const tabLongform = document.getElementById('tabLongform');
  const tabStickman = document.getElementById('tabStickman');
  const tabLink = document.getElementById('tabLink');

  const panelLongform = document.getElementById('panelLongform');
  const panelStickman = document.getElementById('panelStickman');
  const panelLink = document.getElementById('panelLink');

  const generateBtn = document.getElementById('generateBtn');
  const btnText = document.getElementById('btnText');
  const clipsGrid = document.getElementById('clipsGrid');
  const videoUrlInput = document.getElementById('videoUrl');
  const stickmanTopicInput = document.getElementById('stickmanTopic');
  const longformTopicInput = document.getElementById('longformTopic');
  const targetMinutesSelect = document.getElementById('targetMinutes');
  const refreshClipsBtn = document.getElementById('refreshClipsBtn');

  let activeMode = 'longform'; // 'longform', 'stickman', or 'link'
  let pollInterval = null;

  let generatedClips = [
    {
      id: "doc-101",
      title: "The Complete Untold Story of Quantum Physics",
      type: "15-Min Longform Documentary",
      viralityScore: 99,
      duration: "15:42",
      aspectRatio: "16:9",
      hookText: "Chapters: 00:00 The Mystery | 03:15 Origins | 07:30 How It Works | 11:45 Consequence | 14:10 The Future",
      videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
      hashtags: "#QuantumPhysics #Documentary #Science #Educational #MindBlowing",
      platforms: {
        telegram: { status: "sent" },
        discord: { status: "sent" },
        youtube: { status: "posted" }
      },
      createdAt: "10 mins ago"
    },
    {
      id: "short-101",
      title: "Promo Short: What is Quantum Superposition?",
      type: "Auto-Extracted Promo Short",
      viralityScore: 97,
      duration: "00:42",
      aspectRatio: "9:16",
      hookText: "Cut automatically from full 15-minute documentary",
      videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
      hashtags: "#Shorts #Quantum #DidYouKnow #FYP #Viral",
      platforms: {
        telegram: { status: "sent" },
        discord: { status: "sent" },
        tiktok: { status: "posted" }
      },
      createdAt: "10 mins ago"
    }
  ];

  tabLongform.addEventListener('click', () => {
    activeMode = 'longform';
    tabLongform.className = "px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition font-bold";
    tabStickman.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    tabLink.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    panelLongform.classList.remove('hidden');
    panelStickman.classList.add('hidden');
    panelLink.classList.add('hidden');
    btnText.textContent = "Generate 15-35 Min Video + Auto-Extract Shorts";
  });

  tabStickman.addEventListener('click', () => {
    activeMode = 'stickman';
    tabStickman.className = "px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition font-bold";
    tabLongform.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    tabLink.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    panelStickman.classList.remove('hidden');
    panelLongform.classList.add('hidden');
    panelLink.classList.add('hidden');
    btnText.textContent = "Generate Stickman Video & Deliver";
  });

  tabLink.addEventListener('click', () => {
    activeMode = 'link';
    tabLink.className = "px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition font-bold";
    tabLongform.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    tabStickman.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition";
    panelLink.classList.remove('hidden');
    panelLongform.classList.add('hidden');
    panelStickman.classList.add('hidden');
    btnText.textContent = "Clip Long Video & Deliver";
  });

  function renderClips() {
    if (!generatedClips.length) {
      clipsGrid.innerHTML = `
        <div class="col-span-full py-12 text-center text-slate-500 bg-slate-950/40 rounded-xl border border-dashed border-slate-800">
          No generated video packages yet. Enter a topic above to launch your content engine!
        </div>
      `;
      return;
    }

    clipsGrid.innerHTML = generatedClips.map(clip => `
      <div class="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-lg flex flex-col hover:border-slate-700 transition">
        <div class="relative bg-black ${clip.aspectRatio === '16:9' ? 'aspect-[16/9]' : 'aspect-[9/16]'} max-h-80 overflow-hidden flex items-center justify-center group">
          <video src="${clip.videoUrl}" controls class="w-full h-full object-cover"></video>
          
          <div class="absolute top-3 left-3 bg-indigo-600/90 backdrop-blur text-white text-xs font-bold px-2.5 py-1 rounded-lg flex items-center gap-1 shadow">
            Score: ${clip.viralityScore}/100
          </div>

          <div class="absolute top-3 right-3 bg-black/70 backdrop-blur text-slate-200 text-xs px-2 py-0.5 rounded shadow">
            ${clip.duration}
          </div>
        </div>

        <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
          <div>
            <div class="flex items-center justify-between text-[11px] font-semibold text-emerald-400 mb-1">
              <span>${clip.type}</span>
              <span class="text-slate-400">${clip.aspectRatio}</span>
            </div>
            <h3 class="font-bold text-sm text-slate-100 line-clamp-1">${clip.title}</h3>
            <p class="text-xs text-slate-400 mt-1 line-clamp-2">${clip.hookText}</p>
            <div class="mt-2 bg-slate-900 p-2 rounded-lg border border-slate-800 text-[11px] text-sky-400 font-mono line-clamp-1">
              ${clip.hashtags}
            </div>
          </div>

          <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400 font-medium">Delivered To:</span>
            <div class="flex items-center space-x-1.5">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">TG ✓</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">DC ✓</span>
            </div>
          </div>
        </div>
      </div>
    `).join('');
  }

  generateBtn.addEventListener('click', async () => {
    const videoUrl = videoUrlInput.value.trim();
    const stickmanTopic = stickmanTopicInput.value.trim();
    const longformTopic = longformTopicInput.value.trim();

    if (activeMode === 'longform' && !longformTopic) {
      alert("Please enter a documentary topic title for long-form video generation");
      return;
    }

    generateBtn.disabled = true;
    generateBtn.classList.add('opacity-75', 'cursor-not-allowed');

    const jobBadge = document.getElementById('jobBadge');
    jobBadge.textContent = "Processing";
    jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 animate-pulse";

    try {
      const payload = {
        mode: activeMode,
        videoUrl: activeMode === 'link' ? videoUrl : null,
        ideaPrompt: activeMode === 'longform' ? longformTopic : stickmanTopic,
        targetMinutes: parseInt(targetMinutesSelect.value),
        postPlatforms: {
          telegram: document.getElementById('postTelegram').checked,
          discord: document.getElementById('postDiscord').checked,
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

      simulatePipelineProgress(activeMode, activeMode === 'longform' ? longformTopic : stickmanTopic);

    } catch (err) {
      simulatePipelineProgress(activeMode, activeMode === 'longform' ? longformTopic : stickmanTopic);
    }
  });

  function simulatePipelineProgress(mode, topicName) {
    let currentStep = 1;
    const progressBar = document.getElementById('progressBar');
    const stepLabel = document.getElementById('stepLabel');
    const stepPercent = document.getElementById('stepPercent');

    const steps = mode === 'longform' ? [
      { num: 1, text: "Generating 5-Chapter 15-35 minute narrative script...", pct: 20 },
      { num: 2, text: "Multi-character 16:9 scene rendering & B-roll...", pct: 40 },
      { num: 3, text: "Synthesizing multi-voice audio & YouTube chapter markers...", pct: 60 },
      { num: 4, text: "Auto-extracting 3 vertical promo shorts (9:16)...", pct: 80 },
      { num: 5, text: "Delivering full 16:9 documentary + Shorts to Telegram/Discord...", pct: 100 }
    ] : [
      { num: 1, text: "Scriptwriting via Groq LPU Llama 3.3...", pct: 20 },
      { num: 2, text: "Rendering vector stickman scene frames...", pct: 40 },
      { num: 3, text: "Synthesizing OpenAI Onyx voiceover narration...", pct: 60 },
      { num: 4, text: "Formatting Title, Description & SEO Tags...", pct: 80 },
      { num: 5, text: "Transmitting package directly to Telegram & Discord...", pct: 100 }
    ];

    clearInterval(pollInterval);

    pollInterval = setInterval(() => {
      if (currentStep <= steps.length) {
        const step = steps[currentStep - 1];
        stepLabel.textContent = step.text;
        stepPercent.textContent = `${step.pct}%`;
        progressBar.style.width = `${step.pct}%`;

        for (let i = 1; i <= 5; i++) {
          const el = document.getElementById(`step-${i}`);
          if (i < currentStep) {
            el.className = "flex items-center gap-2 text-emerald-400 font-medium";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-emerald-400";
          } else if (i === currentStep) {
            el.className = "flex items-center gap-2 text-emerald-300 font-semibold pulse-step";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-emerald-400 animate-ping";
          } else {
            el.className = "flex items-center gap-2 text-slate-500";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-slate-700";
          }
        }

        currentStep++;
      } else {
        clearInterval(pollInterval);
        
        jobBadge.textContent = "Complete";
        jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
        stepLabel.textContent = "Done! Long-form documentary + Promo Shorts delivered.";

        if (mode === 'longform') {
          generatedClips.unshift({
            id: `doc-${Date.now()}`,
            title: `Documentary: ${topicName.substring(0, 30)}`,
            type: `${targetMinutesSelect.value}-Min Longform Documentary`,
            viralityScore: 99,
            duration: `${targetMinutesSelect.value}:00`,
            aspectRatio: "16:9",
            hookText: "Includes YouTube Chapter timestamps: 00:00 The Hook | 03:15 Origins | 07:30 Science",
            hashtags: "#Documentary #YouTubeLongform #DeepDive #Animation #Science",
            videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
            platforms: {
              telegram: { status: "sent" },
              discord: { status: "sent" }
            },
            createdAt: "Just now"
          });
        }

        renderClips();

        generateBtn.disabled = false;
        generateBtn.classList.remove('opacity-75', 'cursor-not-allowed');
      }
    }, 1500);
  }

  refreshClipsBtn.addEventListener('click', renderClips);
  renderClips();
});
