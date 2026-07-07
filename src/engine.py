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



def build_pair_list_str(metta):
    """
    Queries the bridge facts declared in profunctor.metta and turns
    them into a MeTTa list literal, e.g. ((contain store) ((measure lookup) ((pour rangeQuery) ()))).
    This means Python never hardcodes the bridge mapping -- it only
    reads whatever profunctor.metta currently declares.
    """
    result = metta.run("!(match &self (bridge $a $b) ($a $b))")
    pairs = [str(atom) for group in result for atom in group]

    pair_list = "()"
    for p in reversed(pairs):
        pair_list = f"({p} {pair_list})"
    return pair_list


def run_profunctor():
    """
    Loads both domains + pushout + profunctor bridge, constructs
    MeasuringCup first (it must exist before it can be scored),
    then scores every (Domain A concept, Domain B concept) pair
    using the bridge table as the only source of cross-domain meaning.
    """
    metta = MeTTa()
    for path in [
        "metta/engine.metta",
        "metta/domain_a_kitchen.metta",
        "metta/pushout.metta",
        "metta/domain_b_datastructures.metta",
        "metta/profunctor.metta",
    ]:
        with open(path) as f:
            metta.run(f.read())

    metta.run("!(build-pushout Cup MeasuringTool MeasuringCup)")

    pair_list = build_pair_list_str(metta)

    # Domain membership is given explicitly here, same as required_actions
    # is given explicitly per domain in DOMAINS -- it can't be derived from
    # facts alone since both domains share the plain (concept $c) tag.
    domain_a_concepts = ["Cup", "Bowl", "MeasuringTool", "MeasuringCup"]
    domain_b_concepts = ["List", "HashMap", "TreeMap"]

    print("--- Profunctor scores: Domain A concept <-> Domain B concept ---")
    for ca in domain_a_concepts:
        for cb in domain_b_concepts:
            query = f"!(profunctor-score {ca} {cb} {pair_list})"
            result = metta.run(query)
            print(f"({ca} <-> {cb})  {result}")
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

    run_profunctor()   # <-- NEW LINE