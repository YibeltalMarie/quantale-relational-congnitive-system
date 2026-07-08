# Quantale Relational Cognitive System (QRel_[0,1])

A category-theory-based reasoning system built in MeTTa, developed for
the iCog Labs category theory training assignment. Given a task
requiring one or more actions, the system selects the best-fitting
concept from a domain by composing weighted relations using the
QRel_[0,1] quantale (values in [0,1], combined by multiplication and
max).

## What this project demonstrates

- A working implementation of objects, morphisms, and composition in
  MeTTa (not just diagrams describing them)
- Max-product composition: `(R;S)(a,c) = max_b [ R(a,b) x S(b,c) ]`
- A pushout (colimit) that is **computed**, not hand-typed: `MeasuringCup`'s
  relations are derived from `Cup` and `MeasuringTool` at runtime
- A profunctor: a graded compatibility matrix between concepts and
  physical features
- A functor demonstration: the exact same composition engine, unmodified,
  correctly reasons about a second, unrelated domain (data structures)
- A CASL-style formal specification of the entire system

## Environment setup

Requires Python 3.8-3.12 (hyperon has no wheel for 3.13+ at time of writing).

```bash
pyenv local 3.10.6          # or any installed 3.8-3.12 version
python -m venv .venv
source .venv/bin/activate
pip install hyperon
```

## How to run

```bash
source .venv/bin/activate
python3 src/engine.py
```

This runs, in order:
1. The pushout construction (builds `MeasuringCup` from `Cup` + `MeasuringTool`)
2. Domain A scoring (kitchen tools, task = measure AND pour)
3. Domain B scoring (data structures, task = lookup AND rangeQuery) --
   using the identical engine code as Domain A
4. The profunctor compatibility matrix

## Project structure

category_theory/
├── metta/
│   ├── engine.metta                    generic composition engine
│   │                                    (weight lookup + AND-composition;
│   │                                    contains no domain-specific names)
│   ├── domain_a_kitchen.metta          Domain A facts: Cup, Bowl,
│   │                                    MeasuringTool, MeasuringCup
│   │                                    (MeasuringCup has no facts here --
│   │                                    see pushout.metta)
│   ├── domain_b_datastructures.metta   Domain B facts: List, HashMap,
│   │                                    TreeMap -- proves the engine
│   │                                    generalizes (the functor claim)
│   ├── pushout.metta                   algorithmic pushout: derives
│   │                                    MeasuringCup's relations from
│   │                                    Cup + MeasuringTool via add-atom
│   └── profunctor.metta                graded compatibility matrix:
│                                        (Cup, MeasuringTool) x
│                                        (holdsLiquid, hasScale)
├── src/
│   └── engine.py                       Python runner, config-driven:
│                                        each domain is a data entry, not
│                                        a bespoke function
├── spec/
│   └── casl_spec.txt                   formal CASL-style specification
│                                        of the quantale, domain data,
│                                        composition, and pushout
├── diagrams/
│   ├── pushout_diagram.svg             VolumeObject -> Cup, MeasuringTool
│   │                                    -> MeasuringCup (pushout square)
│   └── reasoning_trace.svg             composite score comparison,
│                                        MeasuringCup winning at 0.72
├── project_plan.txt                    full worked plan: domain data,
│                                        composition rules, pushout,
│                                        profunctor matrix, with reasoning
└── README.md                           this file


## Core concepts, briefly

- **Object** -- a "thing" in the system (a concept like `Cup`, or an
  action like `pour`)
- **Morphism** -- a weighted relation between two objects, e.g.
  `Cup --0.80--> pour` means "Cup supports pour with strength 0.80"
- **Composition (AND)** -- when multiple actions are required together,
  multiply their weights: `score = w1 x w2 x ...`. A weak link drags
  down the whole result, matching real-world "only as strong as your
  weakest requirement" reasoning
- **Composition (max-product, OR)** -- when choosing between
  alternative routes, take the strongest one:
  `(R;S)(a,c) = max_b [ R(a,b) x S(b,c) ]`
- **Pushout (colimit)** -- gluing two objects together through a shared
  object, taking the max of their relations per action. Proves
  `MeasuringCup` is a principled combination of `Cup` and
  `MeasuringTool`, not an arbitrarily invented object
- **Profunctor** -- a graded ("fuzzy") bridge between two different
  kinds of objects (here: concepts and physical features) that doesn't
  require an exact structural mapping
- **Functor** -- a structure-preserving map between two categories.
  Demonstrated here by running the identical `engine.metta` code,
  unmodified, on two unrelated domains

## Results

**Domain A (kitchen tools), task = measure AND pour:**

| Concept | Composite score |
|---|---|
| MeasuringCup | 0.72 (winner) |
| Cup | 0.16 |
| MeasuringTool | 0.09 |
| Bowl | 0.02 |

`MeasuringCup` wins because it is the pushout of `Cup` (strong at
pouring, weak at measuring) and `MeasuringTool` (strong at measuring,
weak at pouring) -- the pushout inherits the best of both, so it has
no glaring weak point for the AND-composition to expose.

**Domain B (data structures), task = lookup AND rangeQuery** (same
engine code, different domain):

| Concept | Composite score |
|---|---|
| TreeMap | 0.665 (winner) |
| HashMap | 0.0475 |
| List | 0.02 |

`TreeMap` wins because it's the only structure strong at both ordered
range queries and lookups, despite `HashMap` being nominally faster at
plain lookups alone.

## Formal specification

See `spec/casl_spec.txt` for the full CASL-style specification,
covering:
1. The base quantale [0,1] (identity, associativity, absorbing zero)
2. Domain data (concepts, actions, the `affords` relation)
3. Composition rules (AND and max-product)
4. The pushout as a formal derivation (not an assumption)
5. The profunctor compatibility matrix

## Status / next steps

- [x] Core engine, both domains, functor demonstration
- [x] Algorithmic pushout construction
- [x] Profunctor matrix
- [x] CASL-style formal specification
- [x] Pushout and reasoning-trace diagrams
- [ ] Stretch: NLP front-end (parse a plain-language instruction into
      required actions, feed directly into the engine) -- to be added
      if time permits


