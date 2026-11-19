# Records — progressive hints

1. A record can be a dictionary yet still lack required fields or contain invalid types.
2. Use a set for seen IDs and a local dictionary for category accumulators. Normalizing categories is separate from the ID policy.
3. Validate before contributing to a total, create new output records and sort explicit keys. Test the same function twice with unrelated input.
