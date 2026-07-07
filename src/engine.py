from hyperon import MeTTa

def run_domain(engine_path, domain_path, required_actions, label):
    """
    Load the generic engine + one domain's facts, then score every
    concept declared in that domain against the required actions.
    Same engine code runs for ANY domain -- this is the functor proof.
    """
    metta = MeTTa()

    with open(engine_path) as f:
        metta.run(f.read())

    with open(domain_path) as f:
        metta.run(f.read())

    # Build the MeTTa list literal for required actions, e.g. (measure (pour ()))
    action_list = "()"
    for a in reversed(required_actions):
        action_list = f"({a} {action_list})"

    print(f"--- {label}: required = {required_actions} ---")
    query = f"!(match &self (concept $c) (println! ($c (score-and $c {action_list}))))"
    metta.run(query)
    print()


if __name__ == "__main__":
    run_domain("metta/engine.metta", "metta/domain_a_kitchen.metta",
               ["measure", "pour"], "Domain A (kitchen tools)")

    run_domain("metta/engine.metta", "metta/domain_b_datastructures.metta",
               ["lookup", "rangeQuery"], "Domain B (data structures)")