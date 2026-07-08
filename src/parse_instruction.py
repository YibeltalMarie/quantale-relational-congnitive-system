import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found -- check your .env file")

client = genai.Client(api_key=api_key)


def parse_instruction(instruction, valid_actions):
    """
    Takes a plain-English instruction and a list of valid action names
    for the current domain, and returns a Python list of the required
    actions -- ready to feed directly into engine.py's run_domain().

    The prompt is DELIBERATELY constrained: we tell Gemini exactly
    which action words it's allowed to use, and ask for JSON only.
    This is the guardrail we discussed -- without it, Gemini could
    return an action name your domain doesn't know about, and the
    MeTTa engine would silently fail to score anything.
    """
    prompt = f"""You are extracting required actions from an instruction.

Valid actions (choose ONLY from this list): {valid_actions}

Instruction: "{instruction}"

Reply with ONLY a JSON array of the required actions from the valid
list above, nothing else. No explanation, no markdown, just the array.
Example valid reply: ["measure", "pour"]
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    # Gemini sometimes wraps JSON in markdown code fences even when told
    # not to -- strip those defensively before parsing.
    if raw.startswith("```"):
        raw = raw.strip("`").replace("json", "", 1).strip()

    try:
        actions = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Gemini did not return valid JSON: {raw!r}")

    # THE GUARDRAIL: reject anything Gemini returned that isn't in our
    # known action vocabulary, instead of silently passing bad data
    # into the MeTTa engine.
    invalid = [a for a in actions if a not in valid_actions]
    if invalid:
        raise ValueError(
            f"Gemini returned actions outside the valid vocabulary: {invalid}"
        )

    return actions


if __name__ == "__main__":
    
    valid_actions_domain_a = ["pour", "contain", "measure"]

    instruction = "measure 200ml of water and pour it into a bowl"
    result = parse_instruction(instruction, valid_actions_domain_a)

    print(f"Instruction: {instruction}")
    print(f"Extracted actions: {result}")