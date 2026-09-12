---
name: kotlin-best-practices
description: Use whenever writing or reviewing Kotlin code — classes, functions, data modeling, null handling, coroutines, collections. Enforces idiomatic Kotlin over Java-style patterns. Trigger on requests to write/review Kotlin code, model data, handle nullability, or work with coroutines/flows.
---

# Kotlin Best Practices

Act as a senior Kotlin engineer. Apply idiomatic Kotlin, not "Java translated to Kotlin syntax," to everything you write or review.

## Immutability and null safety first

- `val` by default; `var` only when reassignment is genuinely required. Same for collections: `List`/`Map`/`Set` (read-only views) over `MutableList`/`MutableMap`/`MutableSet` unless mutation is the point.
- Model absence with nullable types (`T?`), not sentinel values (`-1`, `""`, magic constants).
- Never use `!!` to silence the compiler — it converts a compile-time safety guarantee into a runtime crash. Use safe calls (`?.`), the Elvis operator (`?:`), `requireNotNull()`/`checkNotNull()` (with a message) at a boundary where null is truly a programming error, or restructure so the type system proves non-null (smart cast after an `if (x != null)`/`require` check).
- Prefer smart casts over explicit casting: structure code (`is` checks, early returns) so the compiler can narrow the type instead of using `as`.

## Data modeling

- `data class` for anything that's a plain value/DTO — get `equals`/`hashCode`/`copy`/`toString` for free instead of hand-rolling them.
- `sealed class`/`sealed interface` to model a closed set of variants (e.g. a result type, a UI state, a domain event) so `when` becomes exhaustive and the compiler catches missing branches — prefer this over an enum + a big `if`/`when` scattered with unrelated fields, and over open class hierarchies when the set of cases is meant to be closed.
- Prefer a sealed result type (`sealed interface Result<out T> { data class Success(val value: T) : Result<T>; data class Failure(val error: DomainError) : Result<Nothing> }`) over throwing exceptions for expected/recoverable failure paths — reserve exceptions for truly exceptional, unrecoverable situations. Kotlin's built-in `Result<T>` is fine for simple cases but a custom sealed type is usually clearer when there's more than one failure shape to distinguish.
- `enum class` for a fixed set of pure constants with no per-case data/behavior beyond simple properties.
- `object` for singletons; `companion object` only for factory functions/constants tied to the class, not as a dumping ground for unrelated statics.

## Functions and control flow

- Named arguments for calls with more than 2-3 parameters, especially when several share a type (avoids transposition bugs and self-documents call sites).
- Default parameter values instead of overloaded function variants.
- Expression-bodied functions (`fun square(x: Int) = x * x`) for single-expression logic; block bodies once there's real control flow.
- `when` as an expression (assigned to a value or returned) over `when` as a statement with assignment inside each branch — and make it exhaustive (no `else` needed when covering a sealed type/enum fully; add one only for truly open types).
- Extension functions to add behavior to a type you don't own, or to keep a class focused — but don't overuse them to the point call sites need to guess where behavior lives; if it's core behavior of the type, put it as a member instead.

## Scope functions — pick the right one

- `let` — transform/act on a non-null value inline, typically after `?.` (`value?.let { ... }`), or to introduce a local scope for a nullable check.
- `apply` — configure an object and return it (builder-style init): `Foo().apply { x = 1; y = 2 }`.
- `also` — a side effect that doesn't change the object (logging, validation) while keeping the chain: `list.also { println(it.size) }`.
- `run`/`with` — compute a value from a block using `this`; `with` when you already have a non-null receiver, `run` when chaining off a nullable/expression.
- Don't nest scope functions deeply or chain several different ones together — if it hurts readability, name intermediate variables instead.

## Collections and sequences

- Prefer collection operations (`map`, `filter`, `fold`, `groupBy`, `associateBy`, `flatMap`, etc.) over manual mutable-accumulator loops — they state intent and avoid off-by-one/mutation bugs.
- Switch a chain of collection operations to a `Sequence` (`.asSequence()`) when the collection is large and multiple intermediate operations are chained, to avoid building each intermediate list eagerly. For small collections/single operations, plain collection functions are clearer and the eager evaluation cost doesn't matter.
- Use the right terminal operation for intent: `firstOrNull()`/`singleOrNull()` over `find()`/manual loops with early return, `any()`/`none()`/`all()` over manual boolean accumulation.

## Coroutines and concurrency

- Structured concurrency: launch coroutines from a scope tied to the caller's lifecycle (`coroutineScope { }`, `viewModelScope`, an injected `CoroutineScope`), never `GlobalScope` in application code.
- Suspend functions express "this does async work" in the type signature — don't wrap synchronous, non-suspending code in `suspend fun` just to call it from a coroutine.
- `withContext(Dispatchers.IO)` around blocking I/O calls inside otherwise-suspending code; don't block a coroutine's thread with `Thread.sleep`/blocking calls without switching dispatcher.
- Prefer `async`/`await` for concurrent independent work, plain sequential `suspend` calls when work is inherently sequential — don't reach for `async { }.await()` immediately, which is just a slower sequential call.
- Cancellation is cooperative: long-running loops/computations inside a coroutine should check `isActive`/call a suspending function periodically so cancellation actually takes effect.

## Visibility and API surface

- Default to the most restrictive visibility that works (`private` > `internal` > `public`); don't expose implementation details (mutable backing fields, helper functions) publicly. Common pattern: `private val _state = MutableStateFlow(...)` backing a `val state: StateFlow<T> = _state.asStateFlow()`.
- Keep constructors focused; use secondary constructors or factory functions sparingly — a top-level factory function is often clearer than a secondary constructor with divergent logic.

## Style

- Follow the official Kotlin coding conventions (4-space indent, no wildcard imports beyond a small allowlist, trailing lambda syntax when the lambda is the last parameter). Defer to the project's `ktlint`/`detekt` config when present rather than personal preference.
- String templates (`"Hello, $name"` / `"${a + b}"`) over concatenation.
