import argparse
import subprocess
import sys
from prompt_engine import PromptEngine

def copy_to_clipboard(text: str):
    try:
        subprocess.run("clip", input=text.encode("utf-8"), check=True, shell=True)
        return True
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="AI Advisor: Custom behavioral prompt generator.")
    parser.add_argument("task", help="The task or question you want Gemini to perform.")
    parser.add_argument("-b", "--behavior", required=True, help="How you want Gemini to behave (e.g. 'Be extremely concise, no fluff, use bullet points')")
    parser.add_argument("-c", "--context", help="Optional background context.")

    args = parser.parse_args()
    engine = PromptEngine({})

    final_prompt = engine.build_behavioral_prompt(args.task, behavior=args.behavior, context=args.context)
    copied = copy_to_clipboard(final_prompt)

    print("\n" + "="*55)
    print(" CUSTOM GENERATED PROMPT" + (" (COPIED TO CLIPBOARD!)" if copied else ""))
    print("="*55 + "\n")
    print(final_prompt)
    print("\n" + "="*55)

if __name__ == "__main__":
    main()
