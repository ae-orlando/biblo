# Aggregation — progressive hints

1. Separate record validation from deciding whether its value contributes to a total.
2. A Set can detect duplicate IDs; a Map avoids inherited-property surprises when grouping user strings.
3. Build new aggregate records and sort a new output array. Check the summed value, not only each input amount, for safe integer overflow.
