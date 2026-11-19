# Semantic HTML — progressive hints

1. A label's for points to an ID; the control's name determines submission. A placeholder is not a substitute for a label.
2. Group radios with the same name and a fieldset/legend, but give them distinct IDs/values. required is a browser feedback rule, not server security.
3. Inspect actual parsed option elements if selection fails. Malformed closing markup can remove an intended option even when its text appears in source. Submit only fake data to the restricted local preview.
