; ============================================================
; profunctor.metta -- GRADED COMPATIBILITY MATRIX
; A profunctor is a "fuzzy bridge" between two categories that
; don't map onto each other exactly. Here: physical CONCEPTS
; (Cup, MeasuringTool) vs abstract FEATURES (holdsLiquid, hasScale).
; Each fact is one cell of the matrix -- not a strict yes/no
; mapping, but a graded compatibility score in [0,1].
; ============================================================

(feature holdsLiquid)
(feature hasScale)

; Cup: good vessel shape (holds liquid well), no markings (low hasScale)
(compat Cup holdsLiquid 0.90)
(compat Cup hasScale 0.05)

; MeasuringTool: precise markings (high hasScale), not built to hold
; liquid on its own (low holdsLiquid) -- this is WHY it's a valid
; pushout partner for Cup: their strengths don't overlap, so gluing
; them together (pushout.metta) produces something strong at both.
(compat MeasuringTool holdsLiquid 0.10)
(compat MeasuringTool hasScale 0.95)

; ------------------------------------------------------------
; print-matrix: walks every (concept, feature) pair generically
; using the SAME declared-facts pattern as engine.metta (concept)
; and this file's (feature ...) facts -- no hardcoded names.
; ------------------------------------------------------------
(= (print-matrix)
   (match &self (concept $c)
      (match &self (feature $f)
         (let $w (match &self (compat $c $f $w2) $w2)
            (println! ($c $f $w))))))