from hyperon import MeTTa
from parse_instruction import parse_instruction


def run_domain(files, setup_queries, required_actions, label):
    """
    Generic domain runner -- works for ANY domain, including ones that
    need a construction step (like a pushout) before scoring.
    """
    metta = MeTTa()

    for path in files:
        with open(path) as f:
            metta.run(f.read())

    for query in setup_queries:
        result = metta.run(query)
        print(f"[setup] {query}  ->  {result}")

    action_list = "()"
    for a in reversed(required_actions):
        action_list = f"({a} {action_list})"

    print(f"--- {label}: required = {required_actions} ---")
    query = f"!(match &self (concept $c) (println! ($c (score-and $c {action_list}))))"
    metta.run(query)
    print()


# ----------------------------------------------------------------
# Domain configs. Added: "valid_actions" (the full action vocabulary
# the LLM is allowed to choose from) and "instruction" (the plain
# English sentence a real user would type -- replaces the hardcoded
# required_actions list from before).
# ----------------------------------------------------------------
DOMAINS = [
    {
        "label": "Domain A (kitchen tools)",
        "files": ["metta/engine.metta", "metta/domain_a_kitchen.metta", "metta/pushout.metta"],
        "setup_queries": ["!(build-pushout Cup MeasuringTool MeasuringCup)"],
        "valid_actions": ["pour", "contain", "measure"],
        "instruction": "measure 200ml of water and pour it into a bowl",
    },
    {
        "label": "Domain B (data structures)",
        "files": ["metta/engine.metta", "metta/domain_b_datastructures.metta"],
        "setup_queries": [],
        "valid_actions": ["store", "lookup", "rangeQuery"],
        "instruction": "look up a value by key and also fetch a range of entries in order",
    },
]


if __name__ == "__main__":
    for domain in DOMAINS:
        print(f"=== NLP front-end: parsing instruction for {domain['label']} ===")
        print(f"Instruction: \"{domain['instruction']}\"")

        # This is the new step: instead of a hardcoded action list,
        # we ask Gemini to extract the required actions from plain
        # English, constrained to this domain's known vocabulary.
        required_actions = parse_instruction(domain["instruction"], domain["valid_actions"])
        print(f"Extracted actions: {required_actions}")
        print()

        # Everything from here on is UNCHANGED from before -- the
        # engine doesn't know or care that its input came from an LLM
        # instead of a Python list you typed by hand.
        run_domain(
            files=domain["files"],
            setup_queries=domain["setup_queries"],
            required_actions=required_actions,
            label=domain["label"],
        )