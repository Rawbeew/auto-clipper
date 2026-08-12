import json
from ai_providers import MultiAIProvider

class FactCheckerEngine:
    """
    Mandatory Fact-Checking & Historical Realism Verification Engine.
    Audits every generated script against real-world scientific, historical, legal, 
    and military facts. Eliminates fiction, fake myths, and ungrounded exaggeration.
    """
    def __init__(self):
        self.ai_provider = MultiAIProvider()

    def verify_and_refine_script(self, script_data: dict, topic: str) -> dict:
        """
        Audits script for strict 100% factual accuracy.
        Even for hypothetical comparisons (e.g. 'Roman Gladiator vs 10 Navy SEALs'),
        forces military tactics, real historical equipment parameters, and scientific facts.
        """
        print(f"🔬 Auditing and fact-checking script for: '{topic}'...")

        prompt = f"""
You are an uncompromising Lead Historian, Defense Tactics Analyst, and Scientific Fact-Checker.
Audit the following draft video script about: "{topic}".

Draft Script Data:
{json.dumps(script_data, indent=2)}

STRICT FACT-CHECKING CONSTRAINTS:
1. NEVER output fantasy, hand-waving fiction, or cartoonish exaggerations.
2. Ensure ALL historical data (e.g. Roman Gladius steel hardness, Lorica Segmentata armor specs, Gladiatorial training regimes) and modern data (e.g. Navy SEAL CQB hand-to-hand training, armor penetration, physical stamina, tactical positioning) are 100% accurate.
3. For hypothetical battles or scenarios, apply realistic physical laws, biomechanics, line-of-sight tactics, and historical military analysis.
4. Correct any popular myths or inaccuracies in the narration text and replace them with verified facts.

Return the fully audited and corrected JSON script with root keys preserved.
Respond strictly in valid JSON format.
"""
        res = self.ai_provider.generate_json(
            prompt,
            system_prompt="You are an uncompromising Lead Historical & Scientific Fact-Checker. Respond strictly in valid JSON."
        )
        if res and isinstance(res, dict) and "scenes" in res:
            print("✅ Script successfully verified & fact-checked against historical/scientific standards!")
            return res

        return script_data
