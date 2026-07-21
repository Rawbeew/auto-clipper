import os
import json
from PIL import ImageDraw, ImageFont

class CharacterManager:
    """
    Manages permanent character locking & automated niche-based mascot selection.
    Maps categories dynamically:
    - Finance / Tax / Legal -> Tax Advisor (Glasses & Tie)
    - Crime / Heists / Mystery -> Detective Noir (Fedora & Lens)
    - Science / Physics -> Lab Scientist (Lab Goggles)
    - Tech / AI / SaaS -> Tech Trader (Sunglasses)
    - History / Military / General -> Casually Explained (Classic MS Paint face)
    """
    def __init__(self, config_path="character_config.json"):
        self.config_path = config_path
        self.preset_characters = {
            "casually_explained": {
                "name": "Classic Casually Explained",
                "glasses": False,
                "hat": "none",
                "accent_color": (15, 23, 42),
                "tie": False,
                "description": "Clean MS Paint stickman with neutral deadpan expression."
            },
            "tax_advisor": {
                "name": "Prof. Tax Advisor",
                "glasses": True,
                "hat": "none",
                "accent_color": (34, 197, 94),
                "tie": True,
                "description": "Stickman with square spectacles and green executive tie."
            },
            "detective_noir": {
                "name": "Noir Detective",
                "glasses": False,
                "hat": "fedora",
                "accent_color": (225, 29, 72),
                "tie": True,
                "description": "Crimson fedora detective holding magnifying glass."
            },
            "scientist_lab": {
                "name": "Lab Scientist",
                "glasses": True,
                "hat": "lab_goggles",
                "accent_color": (56, 189, 248),
                "tie": False,
                "description": "Stickman wearing safety lab goggles and scientist coat."
            },
            "crypto_trader": {
                "name": "Wall Street Trader",
                "glasses": True,
                "hat": "sunglasses",
                "accent_color": (234, 179, 8),
                "tie": True,
                "description": "Stickman with dark sunglasses, gold chain, and cash stacks."
            }
        }

    def auto_select_mascot_by_topic(self, topic: str) -> str:
        """
        Auto-selects character mascot matching the topic's niche.
        """
        t_lower = topic.lower()
        if any(w in t_lower for w in ["tax", "finance", "money", "bank", "legal", "law", "s-corp", "income"]):
            return "tax_advisor"
        elif any(w in t_lower for w in ["crime", "heist", "fbi", "unsolved", "murder", "detective", "mystery"]):
            return "detective_noir"
        elif any(w in t_lower for w in ["quantum", "physics", "science", "brain", "dopamine", "sleep", "doctor", "lab"]):
            return "scientist_lab"
        elif any(w in t_lower for w in ["ai", "saas", "software", "tech", "crypto", "bitcoin", "startup"]):
            return "crypto_trader"
        else:
            return "casually_explained"

    def load_config(self) -> dict:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        
        default_cfg = {
            "active_character_id": "auto",
            "character_data": self.preset_characters["casually_explained"]
        }
        return default_cfg

    def save_config(self, cfg: dict):
        with open(self.config_path, "w") as f:
            json.dump(cfg, f, indent=2)

    def set_locked_character(self, character_id: str) -> dict:
        char_id = character_id.lower().strip()
        if char_id in self.preset_characters:
            cfg = {
                "active_character_id": char_id,
                "character_data": self.preset_characters[char_id]
            }
            self.save_config(cfg)
            print(f"🔒 Character permanently locked onto: '{self.preset_characters[char_id]['name']}'")
            return cfg
        return self.load_config()

    def get_character_for_topic(self, topic: str) -> dict:
        cfg = self.load_config()
        active_id = cfg.get("active_character_id", "auto")

        # If manually locked to specific mascot ID (not 'auto')
        if active_id in self.preset_characters and active_id != "auto":
            return self.preset_characters[active_id]

        # Auto-select based on topic niche
        auto_id = self.auto_select_mascot_by_topic(topic)
        return self.preset_characters[auto_id]

    def draw_locked_accessories(self, draw: ImageDraw.Draw, cx: int, head_cy: int, head_r: int, topic: str = "", stroke_color=(15, 23, 42)):
        char = self.get_character_for_topic(topic)

        # Glasses / Sunglasses / Goggles
        if char.get("hat") == "sunglasses":
            draw.rectangle([cx - 45, head_cy - 15, cx - 5, head_cy + 15], fill=stroke_color)
            draw.rectangle([cx + 5, head_cy - 15, cx + 45, head_cy + 15], fill=stroke_color)
            draw.line([cx - 5, head_cy - 5, cx + 5, head_cy - 5], fill=stroke_color, width=5)

        elif char.get("glasses") or char.get("hat") == "lab_goggles":
            g_col = (56, 189, 248) if char.get("hat") == "lab_goggles" else stroke_color
            draw.rectangle([cx - 40, head_cy - 20, cx - 5, head_cy + 15], outline=g_col, width=5)
            draw.rectangle([cx + 5, head_cy - 20, cx + 40, head_cy + 15], outline=g_col, width=5)
            draw.line([cx - 5, head_cy - 5, cx + 5, head_cy - 5], fill=g_col, width=5)

        # Fedora Hat
        if char.get("hat") == "fedora":
            fill_c = char.get("accent_color", (225, 29, 72))
            draw.polygon([
                (cx - 100, head_cy - head_r + 10),
                (cx + 100, head_cy - head_r + 10),
                (cx + 60, head_cy - head_r - 50),
                (cx - 60, head_cy - head_r - 50)
            ], fill=fill_c, outline=stroke_color)

        # Tie
        if char.get("tie"):
            tie_col = char.get("accent_color", (225, 29, 72))
            neck_y = head_cy + head_r
            draw.polygon([
                (cx - 10, neck_y + 10),
                (cx + 10, neck_y + 10),
                (cx + 18, neck_y + 90),
                (cx, neck_y + 120),
                (cx - 18, neck_y + 90)
            ], fill=tie_col, outline=stroke_color)
