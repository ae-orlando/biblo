# Query lab — progressive hints

1. Begin with all users; inner joins cannot preserve users with no events.
2. Count a non-null event key. For absence, consider a correlated `NOT EXISTS`, not `NOT IN` over nullable IDs.
3. Rank events within each user using timestamp descending, then ID descending. Filter rank in an outer query; window results are not available in the same query's `WHERE`.
