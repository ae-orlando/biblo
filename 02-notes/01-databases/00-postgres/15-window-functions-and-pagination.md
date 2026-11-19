# Window functions, deterministic ordering and pagination

## Outcome

After [[08-filtering-sorting-aggregates]] and [[12-subqueries-ctes-views]], rank rows without collapsing them and choose a stable traversal strategy. Practice: `pg-queries` and the `pg-plans` extension.

## Grouping versus windows

GROUP BY collapses rows into groups. A window calculates across related rows while retaining individual rows. `PARTITION BY` chooses the related set; window ORDER BY chooses sequence within it, not the final output ordering.

```sql
SELECT id, user_id, occurred_at,
       row_number() OVER (
         PARTITION BY user_id ORDER BY occurred_at DESC, id DESC
       ) AS position
FROM logins;
```

Equal timestamps need a tie-breaker if you require one deterministic winner. Filter a window result in a surrounding query or CTE. `rank` leaves gaps after ties; `dense_rank` does not; `row_number` assigns a distinct position. These answer different business questions.

For running aggregates, state the frame. With ordering, the default frame includes peers and can surprise you. `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` makes a row-by-row running sum explicit when the order is uniquely determined.

## Pagination is an ordering and consistency decision

OFFSET is simple but scanning/discarding large offsets becomes expensive. Inserts/deletes between requests can shift pages even with ORDER BY. A unique order is necessary, not a cross-request snapshot guarantee.

For descending `(created_at,id)`, a later keyset page can use:

```sql
SELECT id, created_at FROM events
WHERE user_id = $1 AND kind = 'login'
  AND (created_at, id) < ($2, $3)
ORDER BY created_at DESC, id DESC LIMIT $4;
```

This is a driver-parameterized query fragment; `$1` etc. are not values to paste into ordinary psql. Define timestamp nullability, cursor encoding/validation and behavior when sort keys change. Stable historical exports may need an explicit snapshot strategy.

## Practice

In `pg-queries`, introduce tied events and explain your latest-row selection. In `pg-plans`, add a cursor query and compare plans. Retrieval: why does a window ORDER BY not guarantee final output order? Why can stable ORDER BY still yield duplicate/missing items with OFFSET across requests?

Sources: [Window tutorial](https://www.postgresql.org/docs/18/tutorial-window.html), [window functions](https://www.postgresql.org/docs/18/functions-window.html), [LIMIT/OFFSET](https://www.postgresql.org/docs/18/queries-limit.html).
