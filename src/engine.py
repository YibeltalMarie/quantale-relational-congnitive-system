from hyperon import MeTTa


def run_domain(files, setup_queries, required_actions, label):
    """
    Generic domain runner -- works for ANY domain, including ones that
    need a construction step (like a pushout) before scoring.

    files:           list of .metta files to load, in order
                      (engine.metta always first, then domain facts,
                      then any extra files like pushout.metta)
    setup_queries:   list of MeTTa queries to run AFTER loading files
                      but BEFORE scoring -- e.g. triggering a pushout
                      construction so a concept's facts exist before
                      we try to score it. Empty list if nothing needed.
    required_actions: list of action names the task requires (AND-composed)
    label:           human-readable name for the printed output
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
# Domain configs: each domain is just DATA now, not a bespoke function.
# Adding a new domain later means adding one entry here, not writing
# new code -- that's the actual "generic engine" claim in practice.
# ----------------------------------------------------------------
DOMAINS = [
    {
        "label": "Domain A (kitchen tools)",
        "files": ["metta/engine.metta", "metta/domain_a_kitchen.metta", "metta/pushout.metta"],
        # MeasuringCup has no facts until this setup query constructs them
        "setup_queries": ["!(build-pushout Cup MeasuringTool MeasuringCup)"],
        "required_actions": ["measure", "pour"],
    },
    {
        "label": "Domain B (data structures)",
        "files": ["metta/engine.metta", "metta/domain_b_datastructures.metta"],
        "setup_queries": [],  # no construction step needed for this domain
        "required_actions": ["lookup", "rangeQuery"],
    },
]


if __name__ == "__main__":
    for domain in DOMAINS:
        run_domain(
            files=domain["files"],
            setup_queries=domain["setup_queries"],
            required_actions=domain["required_actions"],
            label=domain["label"],
        )

    # Profunctor matrix (deliverable #3)
    metta = MeTTa()
    for path in ["metta/engine.metta", "metta/domain_a_kitchen.metta", "metta/profunctor.metta"]:
        with open(path) as f:
            metta.run(f.read())
    print("--- Profunctor compatibility matrix (Cup, MeasuringTool) x (holdsLiquid, hasScale) ---")
    metta.run("!(print-matrix)")