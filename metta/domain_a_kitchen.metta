; ============================================================
; domain_a_kitchen.metta -- DOMAIN DATA ONLY, no engine logic here
; ============================================================
(concept Cup)
(concept Bowl)
(concept MeasuringTool)
(concept MeasuringCup)   ; facts for MeasuringCup are NOT listed here --
                          ; they are constructed by pushout.metta from
                          ; Cup + MeasuringTool. This concept is declared
                          ; so the engine knows it exists as a candidate,
                          ; but its weights come only from the pushout.

(affords Cup pour 0.80)
(affords Cup contain 0.85)
(affords Cup measure 0.20)

(affords Bowl pour 0.40)
(affords Bowl contain 0.95)
(affords Bowl measure 0.05)

(affords MeasuringTool pour 0.10)
(affords MeasuringTool contain 0.15)
(affords MeasuringTool measure 0.90)