---
name: angular-architecture
description: Use whenever writing, reviewing, or structuring Angular code — components, services, state, routing, forms — on a modern Angular (v17+) codebase. Enforces signals-based reactivity, standalone components, OnPush change detection, and the smart/dumb (container/presentational) component split. Trigger on requests to create a component, add state, wire a feature, or review Angular code for architecture/best practices.
---

# Modern Angular Architecture (Signals + Smart/Dumb Components)

Act as a senior Angular architect. Apply these conventions to every piece of Angular code you write or review — don't wait to be asked for "best practices" explicitly.

## Baseline: standalone + signals, no NgModules

- Standalone components/directives/pipes by default (`standalone: true` is implicit in v19+; explicit `standalone: true` on older v17/v18 targets). No `NgModule` unless the codebase already relies on one and migrating is out of scope.
- Dependency injection via `inject()` in field initializers, not constructor-param injection — plays better with signals and functional guards/resolvers.
- New control-flow syntax in templates: `@if`, `@for` (with `track`), `@switch` — never `*ngIf`/`*ngFor` in new code.
- `ChangeDetectionStrategy.OnPush` on every component. Signals make this free — reads through a signal in the template auto-track and trigger CD without `markForCheck`/`async` pipe gymnastics.

## Signals as the default reactivity model

- Component/service state: `signal()`. Derived state: `computed()`. Side effects tied to signal changes: `effect()` (used sparingly — prefer `computed` when the goal is a value, not a side effect).
- Component inputs: `input()` / `input.required<T>()` instead of `@Input()`. Outputs: `output<T>()` instead of `@Output() + EventEmitter`.
- Two-way binding on a component: `model<T>()` instead of a paired `@Input()`/`@Output()` pair.
- Keep RxJS for what it's actually good at — async streams (HTTP, websockets, complex event composition, debouncing/switchMap chains) — and convert to signals at the boundary with `toSignal()`. Don't reach for RxJS to hold plain synchronous UI state; that's what a signal is for. Convert the other direction with `toObservable()` only when an existing RxJS-based API needs it.
- Never mutate a signal's value in place; use `.set()` or `.update()` with immutable updates (spread/replace), especially for arrays/objects, so `computed`/template tracking stays correct.

## Smart (container) vs. dumb (presentational) components

Every feature splits into two component tiers:

**Smart/container components**
- Own state: hold the signals, call services, own the `inject()`s for data/state services.
- Own the "what happens" logic: fetch data, handle business rules, orchestrate multiple dumb components.
- Typically one per route/feature (`feature-page.component.ts`), rarely reused.
- Pass data down to dumb components via `input()`, receive events up via `(outputName)` bindings — never let a dumb component reach into a service or the router directly.

**Dumb/presentational components**
- No injected services beyond structural/UI ones (e.g. a11y helpers) — never a data/business service.
- Receive everything via `input()`/`input.required()`, communicate outward only via `output()` — no direct mutation of parent state, no side effects beyond emitting.
- Pure rendering + local, purely visual UI state (e.g. "is this dropdown open") may live in a local signal — that's fine, it's not business state.
- Highly reusable, easy to Storybook/unit-test in isolation since there's nothing to mock but inputs.

When reviewing code, flag a "dumb" component that injects an HTTP/data service, or a template that does business logic inline — that logic belongs in the smart component or a service, exposed as an already-computed input.

## State beyond a single component

- Local-to-feature state: a signal-based service (`providedIn: 'root'` or scoped to the feature's route) exposing `readonly` signals (`.asReadonly()`) plus methods to mutate — never expose a raw mutable `signal()` outside the service.
- Don't introduce NgRx/a global store by default — reach for it only when the codebase already has one or state is genuinely cross-cutting/complex (undo-redo, many independent writers). A signal store service is the default for most feature state.
- Derive, don't duplicate: if a value can be a `computed()` from existing signals, it's not its own signal.

## Component structure conventions

- File-per-responsibility: `*.component.ts` (class + `@Component` with inline or separate `template`/`styleUrl`), keep templates in a separate `.html` file once they exceed a few lines.
- Folder-per-feature (`feature/`) containing its smart container(s), its dumb components in a `components/` (or `ui/`) subfolder, and its state service — not one flat `components/` folder for the whole app.
- Functional guards/resolvers/interceptors (`CanActivateFn`, `HttpInterceptorFn`) using `inject()`, not class-based ones, unless matching an existing class-based pattern already in the repo.

## Forms

- Reactive forms (`FormBuilder`/`FormGroup`) over template-driven forms for anything beyond a trivial single field.
- Expose form validity/value to templates via signals (`toSignal(form.valueChanges)` or the newer signal-forms APIs where available) rather than manual subscriptions.

## When reviewing existing code

Call out concretely, with the fix:
- `*ngIf`/`*ngFor` → migrate to `@if`/`@for` (only when touching that template anyway — don't do a drive-by rewrite of unrelated code).
- `@Input()`/`@Output()` → `input()`/`output()`.
- Missing `ChangeDetectionStrategy.OnPush`.
- A presentational component injecting a data/HTTP service directly.
- A signal being mutated via direct property assignment instead of `.set()`/`.update()`.
- Business logic embedded in a template expression instead of a `computed()`.
