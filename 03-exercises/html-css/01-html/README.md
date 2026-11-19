# HTML lab: a semantic form that really submits locally

**ID:** web-html. Read [[01-html-document]] through [[04-html-accessibility]]. Build work/index.html; the supplied schedule.svg is local decoration, not required external content.

Contract: an English complete document/title, one main and clear h1, a first-focusable skip link to #main, unique IDs, a schedule data table with caption/scoped headers, and at least one image with an intentional alt attribute. Build a native POST /preview form with these accessible labels/submitted fields:

| Label | Control / submitted field |
| --- | --- |
| Full name | required text, name=name |
| Email | required email, name=email |
| Track | required select name=track with python/web choices |
| Morning / Evening | radio group name=session, values morning/evening, fieldset/legend |
| I agree to the training terms | required checkbox name=terms, value=agreed |
| Register | submit button |

```bash
python3 90-tools/practice.py start web-html
python3 90-tools/practice.py check web-html
python3 90-tools/serve-web.py web-html
```

Real Chromium checks inspect semantics/labels, native invalid-email/required behavior, keyboard entry and an actual loopback POST. Preview stores nothing and escapes submitted fake data; never enter real personal information/credentials.

Manual completion: inspect source versus DOM, keyboard/label behavior, meaningful headings/alternatives and assistive-technology behavior where available. Record unperformed checks. Extend with another validated field and explain the server validation still required for a real application.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/web-html/explanation.md)
