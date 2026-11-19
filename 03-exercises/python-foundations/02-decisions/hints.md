# Decisions — progressive hints

1. Separate invalid input from valid zero before deciding a fee/grade.
2. Order overlapping score thresholds from highest to lowest or use disjoint intervals explicitly.
3. Check exactly at each threshold. isinstance(True, int) is true; the contract intentionally excludes booleans.
