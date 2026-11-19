# FastAPI lab: a validated quotation contract

**ID:** api-contract. Prerequisites: Python's synchronous checkpoint, HTTP basics and [[01-fastapi-application]]/[[02-fastapi-contracts]]. Export create_app() from work/app.py; return an unserved FastAPI app.

Routes: GET /health → 200 {'status':'ok'}. POST /quotes accepts exactly quantity (integer 1..1000000) and unit_price_cents (integer 0..1000000), excluding booleans/numeric strings. Return 200 with those two values and integer total_cents. Reject unknown fields, invalid ranges/shapes and malformed JSON with 422. Unknown path → 404; GET on the POST-only path → 405. Keep /openapi.json available.

```bash
python3 90-tools/practice.py start api-contract
python3 90-tools/practice.py check api-contract
```

Checks use the vault-local framework environment and in-process TestClient; no public listener/account is needed. See [[fastapi-learning-path]] if that environment is missing.

Completion: explain Python annotations versus runtime validation, response/status behavior and why zero price is valid. Add a discount policy with boundary tests. This derived quotation does not persist a resource or imply production readiness.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/api-contract/explanation.md)
