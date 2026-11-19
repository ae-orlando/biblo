# FastAPI 02 — validation, representations and failure contracts

## Outcome

Define accepted input and emitted output deliberately. Prerequisite: application/HTTP plus Python errors/types. Practice: api-contract.

Pydantic models validate/convert external representations according to their configuration. Python annotations alone do not do the same. Default conversion can accept values your business contract forbids; choose strict fields where numeric strings/booleans are not valid counts. Specify lower/upper bounds, blank/whitespace handling and extra-field policy.

```python
from pydantic import BaseModel, ConfigDict, Field

class QuantityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    quantity: int = Field(strict=True, ge=1, le=100)
```

This fragment demonstrates a rule; its bounds are not automatically every lab's bounds. Check valid zero separately when a different field permits zero. JSON parsing success does not prove a valid model, and a valid model does not prove authorization or sufficient stock.

## Inputs and outputs are different contracts

Use separate request/response schemas when fields or trust differ. A response model can validate/filter output, but do not return secrets and assume one mechanism replaces all information-flow review. A create request should not freely set owner/admin/server-generated fields.

FastAPI normally reports request validation failure as 422; explicit resource conflicts can be 409, missing resources 404 and an unexpected server defect 500. State the chosen semantics. A validation failure is not the same as a network failure. Avoid asserting entire framework-generated error strings that vary across versions when stable status/field behavior suffices.

## Practice

Implement api-contract with invalid types, booleans, negatives, unknown fields and malformed JSON. Assert exact successful output so an extra internal field is caught. Extend the quote with a documented discount policy; test boundaries before changing arithmetic.

Retrieve: what is an annotation, a Pydantic schema, a domain invariant and a database constraint? Why can all four be useful without being interchangeable?

Sources: [request bodies](https://fastapi.tiangolo.com/tutorial/body/), [response models](https://fastapi.tiangolo.com/tutorial/response-model/), [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/).
