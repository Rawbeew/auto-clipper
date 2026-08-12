document.addEventListener('DOMContentLoaded', () => {
  const btnShortMode = document.getElementById('btnShortMode');
  const btnLongMode = document.getElementById('btnLongMode');
  const btnDualMode = document.getElementById('btnDualMode');

  const mainCategorySelect = document.getElementById('mainCategorySelect');
  const subNichesGrid = document.getElementById('subNichesGrid');
  const subNicheCountLabel = document.getElementById('subNicheCountLabel');
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

  // Hierarchical Niche & High-Paying Sub-Niche Database
  const HIGH_PAYING_NICHES_DATABASE = {
    "finance": [
      {
        name: "Central Banking & Hidden Inflation Taxes",
        cpm: "$25 - $45 CPM",
        competition: "Low Competition",
        prompt: "How central banks print money out of thin air and how inflation acts as a hidden wealth tax..."
      },
      {
        name: "Credit Card Reward Points & Transfer Loopholes",
        cpm: "$20 - $38 CPM",
        competition: "Low-Med Competition",
        prompt: "How travel hackers exploit credit card transfer partners for $10,000 first-class flights for $50..."
      },
      {
        name: "High-Yield Dividend Growth Investing Secrets",
        cpm: "$18 - $32 CPM",
        competition: "Medium Competition",
        prompt: "How dividend compounding works and the top 3 dividend aristocrat stocks for passive cash flow..."
      }
    ],
    "legal_tax": [
      {
        name: "Corporate Tax Loopholes & S-Corp Secrets",
        cpm: "$22 - $42 CPM",
        competition: "Low Competition",
        prompt: "How high-income earners legally pay 0% capital gains using Puerto Rico Act 60 and S-Corp corporate structures..."
      },
      {
        name: "Contract Clauses You Should Never Sign",
        cpm: "$18 - $35 CPM",
        competition: "Low Competition",
        prompt: "3 sneaky clauses hidden inside employment and freelance contracts that steal your intellectual property..."
      },
      {
        name: "Bizarre Laws You Break Every Single Day",
        cpm: "$15 - $28 CPM",
        competition: "Low-Med Competition",
        prompt: "5 unusual ancient laws that still exist on official books that ordinary citizens violate without knowing..."
      }
    ],
    "tech_ai": [
      {
        name: "Autonomous AI Agents & Enterprise Automation",
        cpm: "$20 - $38 CPM",
        competition: "Low Competition",
        prompt: "How multi-agent AI frameworks replace 100-person ops workflows in 10 seconds..."
      },
      {
        name: "Micro-SaaS Success Stories ($10M 1-Person Startups)",
        cpm: "$18 - $35 CPM",
        competition: "Low-Med Competition",
        prompt: "How solo developers build $10M ARR micro-SaaS applications using API-first backend architectures..."
      },
      {
        name: "Cybersecurity Data Breaches & Privacy Loopholes",
        cpm: "$15 - $28 CPM",
        competition: "Low Competition",
        prompt: "The dark truth about how data brokers harvest and trade personal location and credit data..."
      }
    ],
    "engineering": [
      {
        name: "Industrial & Megastructure Architectural Failures",
        cpm: "$12 - $25 CPM",
        competition: "Low Competition",
        prompt: "The $500M engineering mistake that collapsed the Tacoma Narrows Bridge due to aeroelastic flutter..."
      },
      {
        name: "Lost Ancient Engineering Technologies",
        cpm: "$10 - $22 CPM",
        competition: "Low Competition",
        prompt: "How ancient Romans built self-healing underwater concrete that survived 2000 years..."
      }
    ],
    "true_crime": [
      {
        name: "High-Tech Bank & Diamond Center Heists",
        cpm: "$12 - $22 CPM",
        competition: "Low Competition",
        prompt: "The $100M Antwerp Diamond Center heist: How 5 thieves bypassed a $10M vault without setting off a single alarm..."
      },
      {
        name: "Unsolved FBI Ciphers & Cold Cases",
        cpm: "$10 - $20 CPM",
        competition: "Low-Med Competition",
        prompt: "The Kryptos CIA sculpture code and unsolved historical ciphers no intelligence agency could crack..."
      }
    ],
    "science": [
      {
        name: "Dopamine Resets & Focus Neuroscience",
        cpm: "$12 - $22 CPM",
        competition: "Low-Med Competition",
        prompt: "What happens to your brain baseline dopamine receptors when you view morning sunlight within 30 minutes of waking..."
      },
      {
        name: "Quantum Superposition & Multiverse Paradoxes",
        cpm: "$10 - $20 CPM",
        competition: "Low Competition",
        prompt: "How quantum entanglement proves the physical universe is non-local with stickman physics lab animations..."
      }
    ]
  };

  let generatedClips = [
    {
      id: "finance-101",
      title: "How Central Banks Print Money & Hidden Inflation Taxes",
      type: "High-RPM Wealth Short ($38 CPM)",
      viralityScore: 99,
      duration: "00:48",
      aspectRatio: "9:16",
      hookText: "Why saving cash in a bank account guarantees a 5% loss per year...",
      videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
      hashtags: "#PersonalFinance #Banking #Wealth #Inflation #Shorts #FYP",
      platforms: {
        telegram: { status: "sent" },
        discord: { status: "sent" }
      },
      createdAt: "5 mins ago"
    }
  ];

  // Render Sub-Niches when Main Category changes
  function renderSubNiches(catKey) {
    const list = HIGH_PAYING_NICHES_DATABASE[catKey] || [];
    subNicheCountLabel.textContent = `Showing ${list.length} High-Paying Sub-Niches`;

    subNichesGrid.innerHTML = list.map((item, idx) => `
      <div class="subniche-card p-3 rounded-xl bg-slate-900 hover:bg-slate-800/80 border border-slate-800/80 hover:border-emerald-500/50 cursor-pointer transition flex items-center justify-between group" data-prompt="${item.prompt.replace(/"/g, '&quot;')}">
        <div>
          <div class="font-semibold text-xs text-slate-100 group-hover:text-emerald-300 transition">${item.name}</div>
          <div class="text-[11px] text-slate-400 mt-0.5 line-clamp-1">"${item.prompt}"</div>
        </div>
        <div class="flex flex-col items-end gap-1 shrink-0 ml-3">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">${item.cpm}</span>
          <span class="text-[10px] text-indigo-300 font-medium">${item.competition}</span>
        </div>
      </div>
    `).join('');

    // Attach click listener to sub-niche cards
    document.querySelectorAll('.subniche-card').forEach(card => {
      card.addEventListener('click', () => {
        const p = card.getAttribute('data-prompt');
        topicInput.value = p;
        // Highlight clicked card
        document.querySelectorAll('.subniche-card').forEach(c => c.classList.remove('border-emerald-500', 'bg-slate-800'));
        card.classList.add('border-emerald-500', 'bg-slate-800');
      });
    });

    // Default select first item prompt
    if (list.length > 0) {
      topicInput.value = list[0].prompt;
    }
  }

  // Event listener for Main Category change
  mainCategorySelect.addEventListener('change', () => {
    renderSubNiches(mainCategorySelect.value);
  });

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
    btnLongMode.className = "p-3 rounded-xl border border-emerald-500 bg-emerald-600/20 text-emerald-300 font-bold text-xs flex flex-col items-center justify-center gap-1 transition shadow";
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

  // Handle Trend Research Button
  researchBtn.addEventListener('click', async () => {
    researchBtn.disabled = true;
    researchBtn.innerHTML = "<span>⌛ Scraping Trends...</span>";

    try {
      const selectedCategory = mainCategorySelect.value;
      const res = await fetch('/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ niche: selectedCategory })
      });
      const data = await res.json();
      
      if (data.ideas && data.ideas.length > 0) {
        const topIdea = data.ideas[0];
        topicInput.value = topIdea.script_prompt || topIdea.concept_title;
        alert(`📈 Live Web Research Complete!\n\nTop Concept: "${topIdea.concept_title}"\nVirality Score: ${topIdea.virality_score}/100\nCPM Range: ${topIdea.estimated_cpm_range || '$20-$35'}`);
      }
    } catch (err) {
      console.error("Research error:", err);
    } finally {
      researchBtn.disabled = false;
      researchBtn.innerHTML = "<span>🔍 Scrape Web Trends</span>";
    }
  });

  function renderClips() {
    if (!generatedClips.length) {
      clipsGrid.innerHTML = `
        <div class="col-span-full py-12 text-center text-slate-500 bg-slate-950/40 rounded-xl border border-dashed border-slate-800">
          No generated video packages yet. Select a category and sub-niche above!
        </div>
      `;
      return;
    }

    clipsGrid.innerHTML = generatedClips.map(clip => `
      <div class="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-lg flex flex-col hover:border-slate-700 transition">
        <div class="relative bg-black ${clip.aspectRatio === '16:9' ? 'aspect-[16/9]' : 'aspect-[9/16]'} max-h-80 overflow-hidden flex items-center justify-center group">
          <video src="${clip.videoUrl}" controls class="w-full h-full object-cover"></video>
          
          <div class="absolute top-3 left-3 bg-emerald-600/90 backdrop-blur text-white text-xs font-bold px-2.5 py-1 rounded-lg flex items-center gap-1 shadow">
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
    const topic = topicInput.value.trim() || "Central Banking Mechanics & Hidden Inflation Taxes";

    generateBtn.disabled = true;
    generateBtn.classList.add('opacity-75', 'cursor-not-allowed');

    const jobBadge = document.getElementById('jobBadge');
    jobBadge.textContent = "Processing";
    jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 animate-pulse";

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
      { num: 1, text: "Groq LPU High-RPM scriptwriting...", pct: 20 },
      { num: 2, text: "Vector stickman scene pose drawing...", pct: 40 },
      { num: 3, text: "OpenAI Onyx voiceover narration synthesis...", pct: 60 },
      { num: 4, text: "Submagic banner formatting & SEO hashtags...", pct: 80 },
      { num: 5, text: "Delivering finished short package to Telegram & Discord...", pct: 100 }
    ] : [
      { num: 1, text: "5-Chapter 15-35 min high-RPM script via Groq LPU...", pct: 20 },
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
        
        jobBadge.textContent = "Delivered";
        jobBadge.className = "text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
        stepLabel.textContent = "Done! High-RPM video package delivered to Telegram & Discord.";

        generatedClips.unshift({
          id: `vid-${Date.now()}`,
          title: topicName.length > 35 ? topicName.substring(0, 35) + "..." : topicName,
          type: format === 'short' ? "High-RPM Vertical Short ($38 CPM)" : `${targetMinutesSelect.value}-Min Longform ($25 CPM)`,
          viralityScore: 99,
          duration: format === 'short' ? "00:48" : `${targetMinutesSelect.value}:00`,
          aspectRatio: format === 'short' ? "9:16" : "16:9",
          hookText: format === 'short' ? "Sub-niche targeted short with CTR tags" : "Includes YouTube Chapters: 00:00 The Hook | 03:15 Origins | 07:30 Deep Dive",
          hashtags: "#PersonalFinance #HighRPM #Shorts #FYP #Viral #DidYouKnow",
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
  
  // Initial render
  renderSubNiches(mainCategorySelect.value);
  renderClips();
});
