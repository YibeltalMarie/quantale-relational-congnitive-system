"""
reasoning.py -- wraps the existing MeTTa engine so it RETURNS data
instead of only printing it. Nothing about the MeTTa logic itself
changes; this is purely an adapter layer for the web API.
"""
import os
from hyperon import MeTTa

# Compute the project root regardless of where uvicorn is launched from.
# webapp/backend/reasoning.py -> up two levels -> project root.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def _resolve(path):
    """Turn a path like 'metta/engine.metta' into an absolute path
    anchored at the project root, so it works no matter which
    directory the server process was started from."""
    return os.path.join(PROJECT_ROOT, path)

DOMAINS = {
    "kitchen": {
        "label": "Domain A (kitchen tools)",
        "files": ["metta/engine.metta", "metta/domain_a_kitchen.metta", "metta/pushout.metta"],
        "setup_queries": ["!(build-pushout Cup MeasuringTool MeasuringCup)"],
        "valid_actions": ["pour", "contain", "measure"],
        "concepts": ["Cup", "Bowl", "MeasuringTool", "MeasuringCup"],
    },
    "datastructures": {
        "label": "Domain B (data structures)",
        "files": ["metta/engine.metta", "metta/domain_b_datastructures.metta"],
        "setup_queries": [],
        "valid_actions": ["store", "lookup", "rangeQuery"],
        "concepts": ["List", "HashMap", "TreeMap"],
    },
}


def get_concept_table(domain_key):
    """
    Loads a domain and returns every concept's raw weighted relations,
    as plain Python data -- this feeds the frontend's "concepts" panel.
    """
    domain = DOMAINS[domain_key]
    metta = MeTTa()
    for path in domain["files"]:
        with open(_resolve(path)) as f:
            metta.run(f.read())
    for query in domain["setup_queries"]:
        metta.run(query)

    table = {}
    for concept in domain["concepts"]:
        result = metta.run(f"!(match &self (affords {concept} $a $w) ($a $w))")
        pairs = {}
        for group in result:
            for atom in group:
                parts = str(atom).strip("()").split()
                if len(parts) == 2:
                    pairs[parts[0]] = float(parts[1])
        table[concept] = pairs
    return table


def score_instruction(domain_key, required_actions):
    """
    Loads a domain, runs setup (pushout if needed), and scores every
    concept against required_actions. Returns a plain Python list of
    (concept, score) tuples sorted best-first -- ready for JSON.
    """
    domain = DOMAINS[domain_key]
    metta = MeTTa()
    for path in domain["files"]:
        with open(_resolve(path)) as f:
            metta.run(f.read())
    for query in domain["setup_queries"]:
        metta.run(query)

    action_list = "()"
    for a in reversed(required_actions):
        action_list = f"({a} {action_list})"

    result = metta.run(
        f"!(match &self (concept $c) ($c (score-and $c {action_list})))"
    )

    scores = []
    for group in result:
        for atom in group:
            parts = str(atom).strip("()").split()
            if len(parts) == 2:
                scores.append((parts[0], round(float(parts[1]), 4)))

    scores.sort(key=lambda pair: pair[1], reverse=True)
    return scores