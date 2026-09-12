---
name: spring-boot-best-practices
description: Use whenever writing or reviewing Spring Boot code — controllers, services, repositories, configuration, exception handling, testing. Enforces layered architecture, constructor injection, DTO/entity separation, and proper test slicing. Trigger on requests to add an endpoint, a service, a repository, wire configuration, or review Spring Boot code for architecture/best practices.
---

# Spring Boot Best Practices

Act as a senior Spring Boot engineer (Spring Boot 3.x / Java or Kotlin — see [[kotlin-best-practices]] when the codebase is Kotlin). Apply these conventions to everything you write or review, not just when explicitly asked for "best practices."

## Layered architecture, strict responsibilities

- **Controller** (`@RestController`) — HTTP concerns only: request mapping, input binding/validation, calling exactly one service method, mapping the result to a response DTO/status code. No business logic, no direct repository access.
- **Service** (`@Service`) — business logic and orchestration lives here. Transaction boundaries (`@Transactional`) belong on service methods, not controllers or repositories.
- **Repository** (`@Repository`/Spring Data interface) — persistence only. No business rules embedded in queries beyond the query itself.
- A controller calling a repository directly, or business logic sitting in a controller method, is an architecture violation to flag even if functionally correct.

## Dependency injection

- Constructor injection only — never `@Autowired` on a field. It makes dependencies explicit, enables `final` fields, and lets the class be instantiated in a plain unit test without Spring.
- With a single constructor, `@Autowired` on it is redundant (Spring infers it) — omit it.
- In Kotlin, constructor injection reads naturally with a primary constructor + `val` properties; keep the class itself as small as its actual dependencies (a bloated constructor parameter list is a signal the class has too many responsibilities).

## DTOs vs. entities

- Never expose a JPA `@Entity` directly as an API request/response body — it leaks persistence details (lazy-loaded associations, internal fields) and couples the API contract to the schema. Map to/from dedicated request/response DTOs (Java `record`s or Kotlin `data class`es) at the controller boundary.
- Keep mapping explicit and visible (a small mapper function/class, or MapStruct if the project already uses it) rather than scattering ad hoc field copying across controllers.
- Request DTOs validate with Bean Validation annotations (`@NotNull`, `@Size`, `@Valid` on the controller parameter); don't re-validate the same rules manually in the service unless the rule depends on business state the annotation can't express.

## Configuration

- Externalize configuration via `@ConfigurationProperties` classes (bound, type-safe, IDE-completable) over scattered `@Value("${...}")` injections, especially once more than a couple of related properties exist.
- Use Spring profiles (`application-{profile}.yml`) for environment-specific config; don't branch on environment inside application code.
- Secrets never hardcoded or committed — sourced from environment variables/a secrets manager, referenced by property placeholder.

## Error handling

- Centralize exception-to-HTTP-response mapping in a `@RestControllerAdvice`/`@ExceptionHandler` class — don't catch-and-translate exceptions ad hoc inside individual controller methods.
- Return a consistent error response shape (problem-detail style: status, message, error code, timestamp) across all endpoints, using Spring's built-in `ProblemDetail`/RFC 7807 support where the project targets Boot 3.x.
- Distinguish client errors (4xx — validation, not found, conflict) from server errors (5xx) precisely; don't let an unmapped exception fall through to a generic 500 when it's actually a 400/404/409 case.

## REST API design

- Use HTTP methods/status codes correctly: `POST` → 201 with `Location` header for creation, `PUT`/`PATCH` for updates (idempotent `PUT` = full replace, `PATCH` = partial), `DELETE` → 204, `GET` never mutates state.
- Version or evolve the API deliberately (URL/header versioning per the project's existing convention) rather than making breaking changes to an existing endpoint's contract.
- Paginate collection endpoints that can grow unbounded (`Pageable`/`Page<T>`) instead of returning an unbounded list.

## Testing strategy — slice tests over `@SpringBootTest` everywhere

- Prefer the narrowest Spring test slice that exercises the thing under test, since full-context tests are slow and reach past the current specification (see [[angular-tdd-vitest]] for the same red-green-refactor discipline on the frontend side):
  - `@WebMvcTest(Controller.class)` for controller/HTTP-layer behavior (request mapping, validation, status codes), with service dependencies mocked (`@MockBean`/`@MockitoBean`).
  - `@DataJpaTest` for repository/query behavior against a real (typically embedded/Testcontainers) database.
  - Plain unit tests (no Spring context at all) for service-layer business logic — constructor-inject mocks, no `@SpringBootTest` needed since the service has no framework dependency beyond its own injected collaborators.
- Reserve `@SpringBootTest` for genuine end-to-end/integration tests that need the full context wired — not as the default for every test.
- Prefer Testcontainers over H2/in-memory substitutes for integration tests against a real database engine when the project already uses Postgres/MySQL/etc. in production — an in-memory substitute can pass while the real engine would reject the same SQL/constraint.

## Observability and cross-cutting concerns

- Structured logging (not `System.out.println`) via the standard logger, with meaningful context (correlation/request IDs where the project has them) — avoid logging sensitive data (credentials, PII) at any level.
- Expose health/readiness via Spring Boot Actuator rather than hand-rolled health endpoints when the project already depends on it.
- Keep cross-cutting concerns (logging, auth checks, metrics) out of business logic via AOP/filters/interceptors rather than duplicating them into every service method.

## When reviewing existing code

Call out concretely, with the fix:
- Field injection (`@Autowired` on a field) → constructor injection.
- An entity returned/accepted directly on a controller method → introduce a DTO.
- Business logic in a controller → move to the service layer.
- A broad `catch (Exception e)` swallowing/rethrowing generically inside a controller → move to a `@RestControllerAdvice` handler for that specific exception type.
- A test annotated `@SpringBootTest` for what's actually pure business logic with mockable dependencies → drop to a plain unit test or the appropriate slice.
