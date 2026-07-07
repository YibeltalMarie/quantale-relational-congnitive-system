; ============================================================
; pushout.metta -- ALGORITHMIC PUSHOUT (COLIMIT) CONSTRUCTION
; Computes MeasuringCup's relations from Cup + MeasuringTool
; (both already exist as real domain concepts -- no invented object).
; Depends on: engine.metta (for `weight`) and domain_a_kitchen.metta
; (for Cup and MeasuringTool's facts) being loaded first.
; ============================================================

(action pour)
(action contain)
(action measure)

; max-value: MeTTa has no built-in max, so we build one from if/>.
(= (max-value $a $b)
   (if (> $a $b) $a $b))

; pushout-weight: for ONE action, take the max of the two sources'
; weights -- "the merged object inherits whichever source was stronger."
(= (pushout-weight $c1 $c2 $action)
   (max-value (weight $c1 $action) (weight $c2 $action)))

; build-pushout: for EVERY known action, compute the pushout weight
; and ADD it as a real new fact into the atomspace, so the target
; concept's numbers are genuinely derived, not typed in.
(= (build-pushout $c1 $c2 $target)
   (match &self (action $a)
      (let $w (pushout-weight $c1 $c2 $a)
        (add-atom &self (affords $target $a $w)))))