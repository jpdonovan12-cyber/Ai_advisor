from model_profiles import PROFILES

class PromptEngine:
    def __init__(self, config: dict):
        self.config = config
        self.default_model = config.get("default_model", "gemini_4_argon")

    def get_profile(self, model_key: str = None):
        key = model_key or self.default_model
        if key not in PROFILES:
            raise ValueError(f"Unknown model profile '{key}'. Available: {list(PROFILES.keys())}")
        return PROFILES[key]

    def build_payload(self, user_prompt: str, model_key: str = None, context: str = None) -> dict:
        profile = self.get_profile(model_key)
        system_instructions = profile.instructions.strip()
        
        full_prompt = user_prompt.strip()
        if context:
            full_prompt = f"[Context]\n{context.strip()}\n\n[Request]\n{full_prompt}"

        return {
            "model_name": profile.name,
            "model_version": profile.version,
            "traits": profile.traits,
            "system_instruction": system_instructions,
            "user_prompt": full_prompt,
            "parameters": {
                "temperature": self.config.get("temperature", 0.2),
                "max_tokens": self.config.get("max_tokens", 4096),
                "top_p": self.config.get("top_p", 0.95)
            }
        }
