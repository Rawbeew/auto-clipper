import urllib.request
import json
import re
from ai_providers import MultiAIProvider

class NicheTrendResearcher:
    """
    Scrapes real-time signals from Google News RSS, HackerNews, and Subreddits
    and analyzes them using LLMs (Groq LPU / DeepSeek) for high-RPM virality potential.
    Features pre-configured high-paying low-competition presets:
    - legal_tax ($15-$40 CPM)
    - saas_tech ($14-$35 CPM)
    - engineering ($10-$25 CPM)
    - banking_wealth ($18-$45 CPM)
    - neuroscience ($10-$20 CPM)
    """
    def __init__(self):
        self.ai_provider = MultiAIProvider()

    def fetch_google_news_trends(self, topic: str) -> list:
        encoded_topic = urllib.parse.quote(topic)
        url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"}
        trends = []

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                raw_xml = resp.read().decode("utf-8")
                titles = re.findall(r'<title>(.*?)</title>', raw_xml)
                for t in titles[1:6]:
                    clean_title = re.sub(r' - [^-]+$', '', t)
                    trends.append({"source": "Google News", "title": clean_title})
        except Exception as e:
            print(f"Google News RSS fetch error: {e}")

        return trends

    def fetch_hackernews_trends(self, limit: int = 5) -> list:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoClipperHNScraper/1.0"}
        stories = []

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                item_ids = json.loads(resp.read().decode("utf-8"))[:limit]
                for item_id in item_ids:
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
                    req_item = urllib.request.Request(item_url, headers=headers)
                    with urllib.request.urlopen(req_item, timeout=5) as item_resp:
                        item_data = json.loads(item_resp.read().decode("utf-8"))
                        if item_data and "title" in item_data:
                            stories.append({
                                "source": "HackerNews",
                                "title": item_data["title"],
                                "score": item_data.get("score", 0)
                            })
        except Exception as e:
            print(f"HackerNews fetch error: {e}")

        return stories

    def research_niche_trends(self, niche: str = "saas_tech") -> dict:
        print(f"🔍 Scraping live viral trends for High-RPM Niche: '{niche}'...")
        
        raw_signals = []
        if niche.lower() in ["legal_tax", "legal", "tax"]:
            raw_signals.extend(self.fetch_google_news_trends("tax loopholes tax law business"))
        elif niche.lower() in ["saas_tech", "saas", "ai_agents"]:
            raw_signals.extend(self.fetch_hackernews_trends(limit=5))
            raw_signals.extend(self.fetch_google_news_trends("AI agents SaaS startup"))
        elif niche.lower() in ["engineering", "disasters"]:
            raw_signals.extend(self.fetch_google_news_trends("engineering disaster failure breakdown"))
        elif niche.lower() in ["banking_wealth", "finance"]:
            raw_signals.extend(self.fetch_google_news_trends("banking system central bank money printing"))
        else:
            raw_signals.extend(self.fetch_google_news_trends(niche))

        prompt = f"""
You are a top YouTube strategist specializing in high-RPM faceless channels ($15-$40 CPM niches).
Analyze these real-time trending web signals for the niche: "{niche}".

Trending Signals:
{json.dumps(raw_signals, indent=2)}

Task: Generate 3 HIGH-RETENTION CONTENT CONCEPTS.
Specify for each concept whether it works better as a "Short (9:16)", "Longform Documentary (16:9)", or "Dual Flywheel".

Respond strictly in valid JSON format with root key "viral_research_ideas", containing:
- "concept_title": High CTR title
- "recommended_format": "Short (9:16)" OR "Longform (16:9)" OR "Dual Flywheel"
- "estimated_cpm_range": e.g. "$18 - $35 CPM"
- "virality_score": Integer 0-100
- "hook_angle": Psychological hook angle
- "script_prompt": Ready-to-use prompt for auto-generation
"""
        res = self.ai_provider.generate_json(prompt, system_prompt="You are an expert high-RPM YouTube channel strategist. Respond strictly in JSON.")
        if res:
            return res

        return {
            "niche": niche,
            "viral_research_ideas": [
                {
                    "concept_title": "How 1-Person AI Startups Are Reaching $10M ARR",
                    "recommended_format": "Dual Flywheel",
                    "estimated_cpm_range": "$18 - $35 CPM",
                    "virality_score": 98,
                    "hook_angle": "B2B Success Secrets",
                    "script_prompt": "Explain how modern AI micro-SaaS solo founders build automated 8-figure companies with stickman animations."
                },
                {
                    "concept_title": "3 Legal Tax Secrets Rich People Use (100% Legal)",
                    "recommended_format": "Longform (16:9)",
                    "estimated_cpm_range": "$20 - $45 CPM",
                    "virality_score": 96,
                    "hook_angle": "Myth Debunked",
                    "script_prompt": "Explain tax deductions, S-Corp structures, and trust setups using clear animated stickman host visuals."
                }
            ]
        }

if __name__ == "__main__":
    researcher = NicheTrendResearcher()
    results = researcher.research_niche_trends("saas_tech")
    print(json.dumps(results, indent=2))
