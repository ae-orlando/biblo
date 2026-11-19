# Recovery lab — progressive hints

1. Database connection, schema lookup and table reading are different privileges.
2. Default privileges affect objects created in the future by the configured creator, not every future object's creator automatically.
3. Use psql's quoted identifier syntax `:"reader"`, not string concatenation or a quoted SQL string literal. The test supplies a unique role name and cleans it up after dropping its disposable database.
