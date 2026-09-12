---
name: accessibility-html
description: Use whenever writing, reviewing, or integrating HTML/templates/components — forms, buttons, links, images, modals, menus, tables, custom widgets — to ensure they are accessible (WCAG 2.1/2.2 AA, semantic HTML, ARIA, keyboard, focus, color contrast). Trigger on requests to "integrate" a design/mockup into HTML, build a UI component, fix accessibility issues, or review markup for a11y.
---

# HTML Accessibility Integration

Act as a web accessibility expert (WCAG 2.1/2.2 AA) when writing or reviewing HTML. Apply this systematically to every element you integrate, not just when explicitly asked for "accessibility."

## Core rule: semantics before ARIA

The first rule of ARIA is **don't use ARIA** when a native HTML element already does the job.

- Prefer `<button>`, `<a href>`, `<nav>`, `<main>`, `<header>`, `<footer>`, `<aside>`, `<section>`, `<article>`, `<ul>/<ol>`, `<table>`, `<dialog>`, `<details>/<summary>`, `<fieldset>/<legend>` over `<div>`/`<span>` + ARIA roles.
- A `<div onclick>` acting as a button is only acceptable when a real `<button>` cannot be styled to fit — and even then it needs `role="button"`, `tabindex="0"`, and both `Enter`/`Space` key handling to match native behavior. Default to fixing the styling instead.
- Only add ARIA to: expose a widget pattern with no native HTML equivalent (tabs, comboboxes, accordions not using `<details>`, live regions), or to supplement — never contradict — native semantics.

## Checklist to apply on every integration

**Structure & landmarks**
- One `<h1>` per page/view; heading levels (`h1`→`h6`) never skip a level.
- Page/region structured with landmarks (`<header>`, `<nav>`, `<main>`, `<footer>`) — one `<main>` per page.
- Reading/DOM order matches visual order (don't rely on CSS `order`/absolute positioning to fix a confusing source order).

**Images & media**
- Every `<img>` has `alt`. Decorative images get `alt=""` (empty, not omitted). Informative images describe content/function, not "image of...".
- Complex images (charts, diagrams) get a longer description nearby or via `aria-describedby`.
- `<video>`/`<audio>` have captions/transcripts when they carry meaning.

**Forms**
- Every input has a programmatically associated `<label for="id">` (or wraps the input) — placeholder is never a substitute for a label.
- Group related inputs (radios, checkboxes) in `<fieldset>` with `<legend>`.
- Required fields marked with `required`/`aria-required`, not color alone.
- Errors are announced (`aria-live` region or `aria-describedby` linking to the error text) and identified in text, not color/icon alone.
- Autocomplete attributes (`autocomplete="email"`, etc.) on common fields.

**Interactive elements & keyboard**
- Everything clickable is reachable and operable by keyboard alone (`Tab`, `Enter`/`Space`, arrow keys where the widget pattern expects them).
- Visible focus indicator is never removed (`outline: none` without a replacement is a bug) — provide a clear `:focus-visible` style if restyling.
- Logical tab order; avoid positive `tabindex` values (use `0` or `-1` only).
- Custom widgets (menus, modals, tabs, comboboxes) follow the WAI-ARIA Authoring Practices pattern for that widget (correct `role`, `aria-expanded`, `aria-controls`, `aria-activedescendant`, etc.) — check the APG before inventing a pattern.

**Modals / dialogs / dynamic content**
- Modals use `<dialog>` or `role="dialog"` + `aria-modal="true"`, trap focus while open, return focus to the trigger on close, and are dismissible with `Escape`.
- Content injected dynamically (toasts, validation, loading states) that should be announced uses `aria-live="polite"` (or `"assertive"` only for urgent/blocking messages).
- Elements toggled visible/hidden use `hidden` or `aria-hidden`/`inert` consistently — don't leave off-screen interactive content focusable.

**Links & buttons**
- Link text is meaningful out of context (avoid bare "click here" / "read more" without an accessible name via `aria-label` or visually-hidden text).
- `<a>` for navigation, `<button>` for actions — don't swap them.
- Icon-only buttons/links have an accessible name (`aria-label` or visually-hidden text), not just a tooltip/`title`.

**Color & visuals**
- Text contrast ≥ 4.5:1 (normal text) / 3:1 (large text ≥18pt or 14pt bold); UI component/graphical object contrast ≥ 3:1 against adjacent colors.
- Color is never the only means of conveying information/state (error, success, selected, required) — pair with text, icon, or pattern.
- Content reflows/works at 200% zoom and down to 320px width without loss of function.

**Tables**
- Data tables use `<th scope="col">`/`<th scope="row">` (and `<caption>`), not `<table>` for layout.

**Language & document**
- `<html lang="...">` set; language changes within content marked with `lang` on the sub-element.
- `<title>` describes the page/view meaningfully.

## When reviewing existing/integrated markup

Call out violations concretely: cite the element, the WCAG success criterion it fails (e.g. "1.1.1 Non-text Content", "2.1.1 Keyboard", "4.1.2 Name, Role, Value"), and give the corrected markup — don't just say "improve accessibility."

## Testing recommendations

Suggest automated checks (axe DevTools, Lighthouse, `eslint-plugin-jsx-a11y` if applicable) as a baseline, but note they only catch ~30-40% of issues — manual keyboard-only navigation and screen reader spot-checks (VoiceOver/NVDA) remain necessary for real coverage.
