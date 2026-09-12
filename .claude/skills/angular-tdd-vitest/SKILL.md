---
name: angular-tdd-vitest
description: Use whenever developing a new Angular feature, component, service, or bugfix test-first, or when asked to write/review tests for Angular code using Vitest. Enforces red-green-refactor TDD, Angular Testing Library over TestBed internals, and signal/service testing patterns. Trigger on requests to "TDD this", add a feature with tests, write a spec, or review test quality.
---

# TDD for Angular with Vitest

Act as a senior engineer practicing strict TDD. When asked to build something ("add feature X", "fix bug Y", "implement Z"), default to the red-green-refactor loop below rather than writing implementation first — unless the user explicitly says to skip tests or is doing a throwaway prototype.

## The loop (non-negotiable order)

1. **Red** — write one failing test that expresses the next smallest behavior, in its own edit/tool call. Run it and confirm it fails for the *expected* reason (not a typo/import error). Never write a test you haven't watched fail.
2. **Green** — write the minimum production code to pass that test. Resist adding behavior no test demands yet.
3. **Refactor** — with the test green, clean up (naming, duplication, extraction) without changing behavior. Re-run tests after every refactor step.
4. Repeat for the next behavior. Commit-sized unit: one behavior per red-green-refactor cycle, not one test file per cycle.

When reviewing/writing tests for existing code (not full TDD), still apply the test-quality rules below.

## Test what it does, not how it's built

- Prefer **Angular Testing Library** (`@testing-library/angular`) over raw `TestBed` component instance poking: `render()`, then query/interact via `screen` (`getByRole`, `getByLabelText`, `getByText`) and `fireEvent`/`userEvent`, not `fixture.debugElement.query(By.css(...))` or reaching into `componentInstance` to call methods directly.
- Assert on rendered output and emitted events (what a user/consumer observes), never on private fields/methods. If a test needs to reach a private member to pass, the behavior isn't observable yet — expose it through a public input/output/DOM state instead of reaching in.
- One logical assertion focus per test. Test names read as a spec: `it('disables the submit button while the form is invalid', ...)`, not `it('test1', ...)` or `it('works', ...)`.
- Follow **Arrange-Act-Assert**, with each phase visually separated (blank line or comment) even without labeling it.

## Testing by component tier (see [[angular-architecture]])

**Dumb/presentational components** — test in isolation via inputs/outputs only:
- Render with `input()` values via the component's `componentInputs`, assert rendered DOM.
- Trigger `output()` emissions by simulating the user interaction (click, type) and assert the emitted payload — don't call `component.someOutput.emit()` yourself, that's not what the test is meant to prove.
- No real services needed — if one sneaks in as a dependency, that's a sign the component isn't actually dumb (flag it, don't just mock around it).

**Smart/container components** — test orchestration, not the dumb children's internals:
- Mock/stub the data/business services they inject (`vi.fn()` for each method, or a lightweight fake object) via `TestBed.overrideProvider`/DI `providers` in the test — never hit a real HTTP backend.
- Assert the container calls the service correctly and passes the right data down (via the rendered DOM markers the child produces), not the child's internal rendering logic — that belongs to the child's own tests.

**Services** — test through `TestBed.inject()` when the service itself uses Angular DI (e.g. depends on `HttpClient`); plain instantiation (`new MyService(...)`) when it has no Angular dependencies, since that's simpler and faster.

**Signals**:
- Read a signal's current value directly in assertions: `expect(mySignal()).toBe(...)`. No async wrapper needed for a synchronous `computed()`.
- For `effect()`-driven behavior, run it inside `TestBed.runInInjectionContext()` and flush with `TestBed.flushEffects()` (or await a microtask tick) before asserting.

**HTTP** — mock with `provideHttpClientTesting()` + `HttpTestingController`: assert the exact request (`method`, `url`, body) was made, `flush()` a canned response, then `httpMock.verify()` at teardown to catch unexpected/missing requests.

## Vitest-specific practices

- Mock modules/functions with `vi.fn()`, `vi.spyOn()`, `vi.mock()` — reset/restore mocks between tests (`vi.restoreAllMocks()` in `afterEach`, or `restoreMocks: true` in Vitest config) so state doesn't leak across tests.
- Prefer real timers; reach for `vi.useFakeTimers()` only for genuinely time-dependent logic (debounce, polling, timeouts), and always restore real timers afterward.
- Co-locate spec files next to source (`foo.component.ts` + `foo.component.spec.ts`) so tests stay in view when editing.
- Keep tests deterministic and isolated — no shared mutable state between test cases, no reliance on execution order.

## Running tests

Check the project's `package.json` scripts first (commonly `npm test`, `npm run test:watch`, `vitest run`, `vitest --coverage`). To run a single file: `vitest run path/to/file.spec.ts`. To run by test name: `vitest run -t "test name substring"`. Use watch mode (`vitest` with no `run`) while actively cycling red-green-refactor rather than re-invoking a full run each step.

## Anti-patterns to flag in review

- Tests written after the implementation with no evidence they were ever run red (can't verify a real test-first cycle happened, but at minimum flag tests that would still pass if the production logic were deleted/stubbed — a sign they test nothing real).
- Over-mocking: mocking so much of a unit that the test only verifies the mocks were called, not real behavior.
- Snapshot tests as a substitute for meaningful assertions on markup that changes often.
- Testing Angular framework behavior itself (e.g. "does `@Input()` receive a value") instead of application logic.
