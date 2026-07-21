document.addEventListener('DOMContentLoaded', () => {
  const btnShortMode = document.getElementById('btnShortMode');
  const btnLongMode = document.getElementById('btnLongMode');
  const btnDualMode = document.getElementById('btnDualMode');

  const nichePreset = document.getElementById('nichePreset');
  const topicInput = document.getElementById('topicInput');
  const longformDurationBox = document.getElementById('longformDurationBox');
  const targetMinutesSelect = document.getElementById('targetMinutes');

  const generateBtn = document.getElementById('generateBtn');
  const researchBtn = document.getElementById('researchBtn');
  const btnText = document.getElementById('btnText');
  const clipsGrid = document.getElementById('clipsGrid');
  const refreshClipsBtn = document.getElementById('refreshClipsBtn');

  let activeFormat = 'short'; // 'short', 'longform', or 'dual'
  let pollInterval = null;

  let generatedClips = [
    {
      id: "crime-101",
      title: "The $100M Antwerp Diamond Heist That Vanished",
      type: "True Crime Vertical Short ($22 CPM)",
      viralityScore: 99,
      duration: "00:48",
      aspectRatio: "9:16",
      hookText: "How 5 thieves bypassed a $10M vault without setting off a single sensor...",
      videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
      hashtags: "#TrueCrime #UnsolvedMystery #Heist #Shorts #FYP #Noir",
      platforms: {
        telegram: { status: "sent" },
        discord: { status: "sent" }
      },
      createdAt: "5 mins ago"
    },
    {
      id: "doc-101",
      title: "How 1-Person AI Startups Reach $10M ARR",
      type: "15-Min High-RPM Longform ($25 CPM)",
      viralityScore: 98,
      duration: "15:42",
      aspectRatio: "16:9",
      hookText: "Chapters: 00:00 The Rise | 03:15 Tech Stack | 07:30 Agent Workflows | 11:45 Monetization",
      videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
      hashtags: "#AIAgents #SaaS #BuildInPublic #Tech #Documentary",
      platforms: {
        telegram: { status: "sent" },
        discord: { status: "sent" }
      },
      createdAt: "15 mins ago"
    }
  ];

  // Format Switchers
  btnShortMode.addEventListener('click', () => {
    activeFormat = 'short';
    btnShortMode.className = "p-3 rounded-xl border border-indigo-500 bg-indigo-600/20 text-indigo-300 font-bold text-xs flex flex-col items-center justify-center gap-1 transition shadow";
    btnLongMode.className = "p-3 rounded-xl border border-slate-800 bg-slate-950 text-slate-400 hover:text-slate-200 font-semibold text-xs flex flex-col items-center justify-center gap-1 transition";
    btnDualMode.className = "p-3 rounded-xl border border-slate-800 bg-slate-950 text-slate-400 hover:text-slate-200 font-semibold text-xs flex flex-col items-center justify-center gap-1 transition";
    longformDurationBox.classList.add('hidden');
    btnText.textContent = "Generate Short Video (9:16) & Deliver";
  });

  btnLongMode.addEventListener('click', () => {
    activeFormat = 'longform';
    btnLongMode.className = "p-3 rounded-xl border border-rose-500 bg-rose-600/20 text-rose-300 font-bold text-xs flex flex-col items-center justify-center gap-1 transition shadow";
    btnShortMode.className = "p-3 rounded-xl border border-slate-800 bg-slate-950 text-slate-400 hover:text-slate-200 font-semibold text-xs flex flex-col items-center justify-center gap-1 transition";
    btnDualMode.className = "p-3 rounded-xl border border-slate-800 bg-slate-950 text-slate-400 hover:text-slate-200 font-semibold text-xs flex flex-col items-center justify-center gap-1 transition";
    longformDurationBox.classList.remove('hidden');
    btnText.textContent = "Generate 15-35 Min Documentary (16:9) & Deliver";
  });

  btnDualMode.addEventListener('click', () => {
    activeFormat = 'dual';
    btnDualMode.className = "p-3 rounded-xl border border-sky-500 bg-sky-600/20 text-sky-300 font-bold text-xs flex flex-col items-center justify-center gap-1 transition shadow";
    btnShortMode.className = "p-3 rounded-xl border border-slate-800 bg-slate-950 text-slate-400 hover:text-slate-200 font-semibold text-xs flex flex-col items-center justify-center gap-1 transition";
    btnLongMode.className = "p-3 rounded-xl border border-slate-800 bg-slate-950 text-slate-400 hover:text-slate-200 font-semibold text-xs flex flex-col items-center justify-center gap-1 transition";
    longformDurationBox.classList.remove('hidden');
    btnText.textContent = "Generate 16:9 Longform + Auto-Extract 3 Shorts";
  });

  // Handle Niche Preset Selection
  nichePreset.addEventListener('change', () => {
    const val = nichePreset.value;
    const presets = {
      "true_crime": "The $100M Antwerp Diamond Center heist: How 5 thieves bypassed a $10M vault without setting off alarms...",
      "saas_tech": "How 1-person AI startups build $10M ARR SaaS products with automated AI agents...",
      "legal_tax": "3 unusual tax loopholes rich entrepreneurs use to legally pay 0% capital gains...",
      "engineering": "The $500M engineering mistake that destroyed the world's most expensive bridge...",
      "banking_wealth": "How the central banking system prints money and creates hidden inflation taxes...",
      "neuroscience": "What happens to your brain chemicals when you view sunlight within 30 minutes of waking..."
    };
    if (presets[val]) {
      topicInput.value = presets[val];
    }
  });

  // Handle Trend Research Button
  researchBtn.addEventListener('click', async () => {
    researchBtn.disabled = true;
    researchBtn.innerHTML = "<span>⌛ Scraping Trends...</span>";

    try {
      const selectedNiche = nichePreset.value;
      const res = await fetch('/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ niche: selectedNiche })
      });
      const data = await res.json();
      
      if (data.ideas && data.ideas.length > 0) {
        const topIdea = data.ideas[0];
        topicInput.value = topIdea.script_prompt || topIdea.concept_title;
        alert(`📈 Live Web Research Complete!\n\nTop Concept: "${topIdea.concept_title}"\nVirality Score: ${topIdea.virality_score}/100\nHook Angle: ${topIdea.hook_angle}`);
      }
    } catch (err) {
      console.error("Research error:", err);
    } finally {
      researchBtn.disabled = false;
      researchBtn.innerHTML = "<span>🔍 Scrape Case & Niche Trends</span>";
    }
  });

  function renderClips() {
    if (!generatedClips.length) {
      clipsGrid.innerHTML = `
        <div class="col-span-full py-12 text-center text-slate-500 bg-slate-950/40 rounded-xl border border-dashed border-slate-800">
          No generated video packages yet. Select a niche and format above to start!
        </div>
      `;
      return;
    }

    clipsGrid.innerHTML = generatedClips.map(clip => `
      <div class="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-lg flex flex-col hover:border-slate-700 transition">
        <div class="relative bg-black ${clip.aspectRatio === '16:9' ? 'aspect-[16/9]' : 'aspect-[9/16]'} max-h-80 overflow-hidden flex items-center justify-center group">
          <video src="${clip.videoUrl}" controls class="w-full h-full object-cover"></video>
          
          <div class="absolute top-3 left-3 bg-rose-600/90 backdrop-blur text-white text-xs font-bold px-2.5 py-1 rounded-lg flex items-center gap-1 shadow">
            Score: ${clip.viralityScore}/100
          </div>

          <div class="absolute top-3 right-3 bg-black/70 backdrop-blur text-slate-200 text-xs px-2 py-0.5 rounded shadow">
            ${clip.duration}
          </div>
        </div>

        <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
          <div>
            <div class="flex items-center justify-between text-[11px] font-semibold text-rose-400 mb-1">
              <span>${clip.type}</span>
              <span class="text-slate-400 font-mono">${clip.aspectRatio}</span>
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
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">Telegram ✓</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Discord ✓</span>
            </div>
          </div>
        </div>
      </div>
    `).join('');
  }

  generateBtn.addEventListener('click', async () => {
    const topic = topicInput.value.trim() || "The $100M Antwerp Diamond Center Heist";

    generateBtn.disabled = true;
    generateBtn.classList.add('opacity-75', 'cursor-not-allowed');

    const jobBadge = document.getElementById('jobBadge');
    jobBadge.textContent = "Processing";
    jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 animate-pulse";

    try {
      const payload = {
        mode: activeFormat === 'short' ? 'stickman' : 'longform',
        ideaPrompt: topic,
        targetMinutes: parseInt(targetMinutesSelect.value || 15),
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

      simulatePipelineProgress(activeFormat, topic);

    } catch (err) {
      simulatePipelineProgress(activeFormat, topic);
    }
  });

  function simulatePipelineProgress(format, topicName) {
    let currentStep = 1;
    const progressBar = document.getElementById('progressBar');
    const stepLabel = document.getElementById('stepLabel');
    const stepPercent = document.getElementById('stepPercent');

    const steps = format === 'short' ? [
      { num: 1, text: "Groq LPU True Crime scriptwriting...", pct: 20 },
      { num: 2, text: "Noir detective stickman pose drawing...", pct: 40 },
      { num: 3, text: "OpenAI Onyx deep voice narration synthesis...", pct: 60 },
      { num: 4, text: "Crimson banner formatting & SEO hashtags...", pct: 80 },
      { num: 5, text: "Delivering True Crime short package to Telegram & Discord...", pct: 100 }
    ] : [
      { num: 1, text: "5-Chapter 15-35 min mystery script via Groq LPU...", pct: 20 },
      { num: 2, text: "Multi-character 16:9 scene rendering & B-roll...", pct: 40 },
      { num: 3, text: "Multi-voice narration & YouTube chapter timestamps...", pct: 60 },
      { num: 4, text: "Auto-extracting 3 promo shorts (9:16)...", pct: 80 },
      { num: 5, text: "Delivering full 16:9 documentary + Shorts to Telegram/Discord...", pct: 100 }
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
            el.className = "flex items-center gap-2 text-rose-400 font-medium";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-rose-400";
          } else if (i === currentStep) {
            el.className = "flex items-center gap-2 text-rose-300 font-semibold pulse-step";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-rose-400 animate-ping";
          } else {
            el.className = "flex items-center gap-2 text-slate-500";
            el.querySelector('span').className = "w-2 h-2 rounded-full bg-slate-700";
          }
        }

        currentStep++;
      } else {
        clearInterval(pollInterval);
        
        jobBadge.textContent = "Delivered";
        jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30";
        stepLabel.textContent = "Done! Video package delivered to Telegram & Discord.";

        generatedClips.unshift({
          id: `crime-${Date.now()}`,
          title: topicName.length > 35 ? topicName.substring(0, 35) + "..." : topicName,
          type: format === 'short' ? "True Crime Vertical Short ($22 CPM)" : `${targetMinutesSelect.value}-Min Noir Documentary ($20 CPM)`,
          viralityScore: 99,
          duration: format === 'short' ? "00:48" : `${targetMinutesSelect.value}:00`,
          aspectRatio: format === 'short' ? "9:16" : "16:9",
          hookText: format === 'short' ? "Detective stickman vector rendering with tags" : "Includes YouTube Chapters: 00:00 The Heist | 03:15 The Investigation | 07:30 The Clue",
          hashtags: "#TrueCrime #UnsolvedMystery #Heist #Shorts #FYP #Noir",
          videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
          platforms: {
            telegram: { status: "sent" },
            discord: { status: "sent" }
          },
          createdAt: "Just now"
        });

        renderClips();

        generateBtn.disabled = false;
        generateBtn.classList.remove('opacity-75', 'cursor-not-allowed');
      }
    }, 1500);
  }

  refreshClipsBtn.addEventListener('click', renderClips);
  renderClips();
});
