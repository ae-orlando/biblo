# Count parser — progressive hints

1. Validate the original type before stripping or converting.
2. A string method's definition may include Unicode digits; enforce ASCII if that is the business policy.
3. After complete syntax validation, convert once and check the maximum. Raise the documented failure type rather than returning an unexplained fallback.
