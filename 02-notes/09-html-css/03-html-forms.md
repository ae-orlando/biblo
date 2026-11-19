# HTML 03 — forms, labels and validation boundaries

## Outcome

Build native controls that collect and submit intentional fields without JavaScript. Prerequisite: document/URL structure. Practice: web-html.

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email" required>
```

id connects labels/other document references; name determines the submitted field name; type chooses native behavior; value is the field's submitted value. A placeholder is not a durable label. A control without the intended name may appear correctly but not submit the data you expect.

Group related radios with fieldset/legend and the same name; give options distinct values/IDs. Checkbox submission differs from a guaranteed true/false field: unchecked controls are ordinarily absent. Select options need their own actual option elements and values. Inspect the parsed DOM when malformed source changes the set of available options.

## Submission semantics

GET is appropriate for safe retrieval/search whose values can appear in a URL. POST is appropriate for the chosen state-changing/submission contract. POST does not itself encrypt anything; transport/security are separate. A button inside a form can submit by default, so declare type intentionally.

The course's POST /preview only echoes escaped fake training values and stores nothing. It is not a registration backend and does not replace server-side validation. Never enter a real password or personal data to test this demo.

required, minlength, min/max and type constraints improve feedback. Browser validation can be bypassed or differ in detail; the backend still validates format, authorization and business invariants. Client-valid email syntax does not establish deliverability or permission to use an address.

## Practice and retrieval

Complete web-html, attempt empty/invalid submission, then submit fake valid data and inspect the real POST response. Test the keyboard path, label activation, radio grouping and submitted names. Change one name attribute in a private copy and explain why the preview loses that field even though the visible label remains.

Transfer: add a date/session constraint and define both browser feedback and the corresponding server failure contract before implementing a real endpoint.

Sources: [MDN forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms), [constraint validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation), [WAI forms](https://www.w3.org/WAI/tutorials/forms/).
