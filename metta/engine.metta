; ============================================================
; engine.metta -- GENERIC QRel_[0,1] composition engine
; Contains NO domain-specific names (no "Cup", no "HashMap").
; This file is loaded unchanged for every domain -- that's the
; functor claim: same structure-preserving machinery, any content.
; ============================================================

; Lookup a single weight for (Concept, Action)
(= (weight $concept $action)
   (match &self (affords $concept $action $w) $w))

; AND-composition over a list of required actions (multiply-together)
; Base case: no requirements -> identity element for multiplication = 1.0
(= (score-and $concept ())
   1.0)

(= (score-and $concept ($action $rest))
   (* (weight $concept $action)
      (score-and $concept $rest)))