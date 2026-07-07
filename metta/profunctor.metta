; ============================================================
; profunctor.metta -- CROSS-DOMAIN PROFUNCTOR SCORING
; A profunctor relates objects of Domain A to objects of Domain B.
; Here: the "bridge" facts declare which Domain A action corresponds
; to which Domain B action -- this table IS the profunctor. Nothing
; else in this file knows or cares what the correspondence means;
; change a line here and the scoring changes accordingly, no code edit.
; Depends on: engine.metta (for `weight`), domain_a_kitchen.metta,
; domain_b_datastructures.metta, and pushout.metta all loaded first
; (MeasuringCup must already be constructed before scoring involves it).
; ============================================================

(bridge contain store)
(bridge measure lookup)
(bridge pour rangeQuery)

; weight-pair: for ONE bridged (actionA, actionB) pair, multiply
; cA's weight on actionA by cB's weight on actionB.
(= (weight-pair $cA $cB ($a $b))
   (* (weight $cA $a) (weight $cB $b)))

; profunctor-score: fold weight-pair over a LIST of bridge pairs.
; Base case: no pairs left -> identity element for multiplication = 1.0
; (same pattern as score-and in engine.metta)
(= (profunctor-score $cA $cB ())
   1.0)

(= (profunctor-score $cA $cB ($pair $rest))
   (* (weight-pair $cA $cB $pair)
      (profunctor-score $cA $cB $rest)))