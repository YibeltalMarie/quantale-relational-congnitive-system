"""
app.py -- the actual web server. Exposes reasoning.py's functions as
HTTP endpoints the frontend can call with fetch().

Run with: uvicorn app:app --reload --port 8000
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from reasoning import DOMAINS, get_concept_table, score_instruction
from parse_instruction_adapter import parse_instruction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReasonRequest(BaseModel):
    domain: str
    instruction: str


@app.get("/api/domains")
def list_domains():
    return {
        key: {"label": d["label"], "concepts": d["concepts"], "valid_actions": d["valid_actions"]}
        for key, d in DOMAINS.items()
    }


@app.get("/api/concepts/{domain_key}")
def concepts(domain_key: str):
    if domain_key not in DOMAINS:
        raise HTTPException(status_code=404, detail="Unknown domain")
    return get_concept_table(domain_key)


@app.post("/api/reason")
def reason(req: ReasonRequest):
    if req.domain not in DOMAINS:
        raise HTTPException(status_code=404, detail="Unknown domain")

    valid_actions = DOMAINS[req.domain]["valid_actions"]

    try:
        actions = parse_instruction(req.instruction, valid_actions)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    scores = score_instruction(req.domain, actions)

    return {
        "instruction": req.instruction,
        "extracted_actions": actions,
        "scores": [{"concept": c, "score": s} for c, s in scores],
        "winner": scores[0][0] if scores else None,
    }