; ============================================================
; domain_a_kitchen.metta -- DOMAIN DATA ONLY, no engine logic here
; ============================================================
(concept Cup)
(concept Bowl)
(concept MeasuringTool)
(concept MeasuringCup)

(affords Cup pour 0.80)
(affords Cup contain 0.85)
(affords Cup measure 0.20)

(affords Bowl pour 0.40)
(affords Bowl contain 0.95)
(affords Bowl measure 0.05)

(affords MeasuringTool pour 0.10)
(affords MeasuringTool contain 0.15)
(affords MeasuringTool measure 0.90)

; MeasuringCup's weights = pushout of Cup and MeasuringDevice (see pushout.metta)
(affords MeasuringCup pour 0.80)
(affords MeasuringCup contain 0.85)
(affords MeasuringCup measure 0.95)