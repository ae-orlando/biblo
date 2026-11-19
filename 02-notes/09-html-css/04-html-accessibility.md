# HTML 04 — accessibility is behavior and information

## Outcome

Make a page understandable and operable without relying solely on appearance or a mouse. Prerequisites: semantics/forms. Practice: the manual parts of web-html and web-css.

Use native controls before recreating them: a real button supplies semantics, focus and keyboard behavior that a clickable div does not. ARIA can communicate relationships/state when needed; it does not add missing keyboard behavior or repair a fundamentally wrong interaction design.

## Check several channels

- Meaningful title/language, landmarks and headings help orientation.
- Programmatic labels and fieldset/legend expose relationships; visible instructions should remain available after typing.
- Keyboard order follows the DOM/interaction model; CSS visual reordering can create a confusing mismatch.
- Focus must remain visible and useful, including after validation or dynamic changes. Do not remove outlines without an adequate replacement.
- Text alternatives, error identification and status feedback convey information beyond color/position.
- Contrast, readable sizing, wrapping, target size and text enlargement support perception/operation. The lab's 44px button target is an explicit training requirement, not a claim that every WCAG criterion always requires 44px.

For ordinary text, the selected lab color pairs target at least 4.5:1 contrast. Contrast requirements depend on content/size/state; checking two opaque pairs is not a full WCAG evaluation. A checkbox that is focusable is not proof its label/instructions are understandable.

## Concrete manual evidence

Serve the dedicated lab and navigate with Tab/Shift-Tab/Enter/Space, without a pointer. Explain the current focus and where it should go next. Enlarge text/use browser zoom, inspect labels/error feedback and try an assistive technology available to you. Record unperformed checks instead of claiming universal accessibility.

The automated browser tests establish selected semantics, native validation, focus and geometry only. They cannot judge all alternative-text quality, reading order, cognitive clarity or assistive-technology combinations. A high automated audit score is useful feedback, not a certificate.

Transfer: add an error summary linked to individual invalid fields and verify keyboard/focus behavior. Later JavaScript state changes need deliberate announcements and focus management too.

Sources: [WAI tutorials](https://www.w3.org/WAI/tutorials/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [ARIA authoring practices](https://www.w3.org/WAI/ARIA/apg/).
