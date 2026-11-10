import argparse
import json
import os
import sys
from prompt_engine import PromptEngine
from model_profiles import PROFILES

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {
            "default_model": "gemini_4_argon",
            "temperature": 0.2,
            "max_tokens": 4096,
            "top_p": 0.95,
            "api_key": "YOUR_API_KEY_HERE"
        }
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="AI Advisor: Model-specific prompt orchestration CLI.")
    parser.add_argument("prompt", nargs="?", help="The user prompt to optimize and package.")
    parser.add_argument("-m", "--model", choices=list(PROFILES.keys()), help="Target model profile key.")
    parser.add_argument("-c", "--context", help="Optional context string to prepend.")
    parser.add_argument("-l", "--list", action="store_true", help="List available model profiles.")
    parser.add_argument("--json", action="store_true", help="Output raw JSON payload.")

    args = parser.parse_args()
    config = load_config()
    engine = PromptEngine(config)

    if args.list:
        for key, prof in PROFILES.items():
            print(f"- {key}: {prof.name} (v{prof.version}) | Traits: {', '.join(prof.traits)}")
        sys.exit(0)

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    payload = engine.build_payload(args.prompt, model_key=args.model, context=args.context)

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"=== Target: {payload['model_name']} ({payload['model_version']}) ===")
        print(f"Traits: {', '.join(payload['traits'])}")
        print(f"Params: temp={payload['parameters']['temperature']}, max_tokens={payload['parameters']['max_tokens']}")
        print("\n--- System Instruction ---")
        print(payload["system_instruction"])
        print("\n--- Optimized User Prompt ---")
        print(payload["user_prompt"])

if __name__ == "__main__":
    main()