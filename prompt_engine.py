class PromptEngine:
    def __init__(self, config: dict):
        self.config = config

    def build_behavioral_prompt(self, task: str, behavior: str, context: str = None) -> str:
        parts = [
            "[SYSTEM / BEHAVIORAL DIRECTIVE]",
            behavior.strip()
        ]
        if context:
            parts.append(f"\n[BACKGROUND CONTEXT]\n{context.strip()}")
            
        parts.append(f"\n[TASK / REQUEST]\n{task.strip()}")
        return "\n".join(parts)
