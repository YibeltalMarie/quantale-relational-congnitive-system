; ============================================================
; DOMAIN A: Kitchen Tools -- QRel_[0,1] weighted relations
; ============================================================
; Each fact below is a MORPHISM: (affords Concept Action Weight)
; meaning "Concept supports Action with strength Weight, in [0,1]".
; This is the concrete data behind the relation table in Step 1.

(affords Cup pour 0.80)
(affords Cup contain 0.85)
(affords Cup measure 0.20)

(affords Bowl pour 0.40)
(affords Bowl contain 0.95)
(affords Bowl measure 0.05)

(affords MeasuringTool pour 0.10)
(affords MeasuringTool contain 0.15)
(affords MeasuringTool measure 0.90)

; MeasuringCup's facts come from the pushout construction (see pushout.metta),
; but we assert them here too so this file can run standalone during Day 1.
(affords MeasuringCup pour 0.80)
(affords MeasuringCup contain 0.85)
(affords MeasuringCup measure 0.95)

; ------------------------------------------------------------
; Helper: look up a single weight for (Concept, Action).
; ------------------------------------------------------------
(= (weight $concept $action)
   (match &self (affords $concept $action $w) $w))

; ------------------------------------------------------------
; AND-composition: score for a concept across a LIST of required
; actions. This implements:
;     score(concept, {a1,a2,...}) = w(concept,a1) * w(concept,a2) * ...
; Base case: empty list of actions -> neutral element for
; multiplication is 1.0 (this IS the identity morphism idea:
; "requiring nothing" shouldn't weaken the score at all).
; ------------------------------------------------------------
(= (score-and $concept ())
   1.0)

(= (score-and $concept ($action $rest))
   (* (weight $concept $action)
      (score-and $concept $rest)))

; ------------------------------------------------------------
; Rank every known concept against a required-action list, and
; report the best one. This is a small stand-in for "max over b"
; from the max-product formula, applied at the level of "max over
; candidate concepts" instead of "max over middle steps" -- both
; are the same OR-style operation: take the best available option.
; ------------------------------------------------------------
(= (rank-concepts $required)
   (let* (($cup    (score-and Cup $required))
          ($bowl   (score-and Bowl $required))
          ($mtool  (score-and MeasuringTool $required))
          ($mcup   (score-and MeasuringCup $required)))
     ( (Cup $cup) (Bowl $bowl) (MeasuringTool $mtool) (MeasuringCup $mcup) )))

; ============================================================
; REASONING TRACE (deliverable #5)
; Task: "measure 200ml of water and pour it into a bowl"
; Required actions: measure AND pour
; ============================================================
!(println! "--- Individual scores for task: measure AND pour ---")
!(println! ("Cup:" (score-and Cup (measure (pour ())))))
!(println! ("Bowl:" (score-and Bowl (measure (pour ())))))
!(println! ("MeasuringTool:" (score-and MeasuringTool (measure (pour ())))))
!(println! ("MeasuringCup:" (score-and MeasuringCup (measure (pour ())))))

!(println! "--- Full ranking ---")
!(rank-concepts (measure (pour ())))