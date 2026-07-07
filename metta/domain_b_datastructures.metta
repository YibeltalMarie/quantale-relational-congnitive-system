; ============================================================
; domain_b_datastructures.metta -- DOMAIN DATA ONLY
; ============================================================
(concept List)
(concept HashMap)
(concept TreeMap)

(affords List store 0.90)
(affords List lookup 0.20)
(affords List rangeQuery 0.10)

(affords HashMap store 0.90)
(affords HashMap lookup 0.95)
(affords HashMap rangeQuery 0.05)

(affords TreeMap store 0.80)
(affords TreeMap lookup 0.70)
(affords TreeMap rangeQuery 0.95)