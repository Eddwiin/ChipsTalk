/**
 * Centralized access to environment variables used by the frontend.
 *
 * The frontend never hardcodes API or WebSocket URLs (see CLAUDE.md /
 * .claude/agents/frontend.md). Every value here must come from the
 * environment so it can be configured per deployment (local, staging,
 * production) without code changes. See .env.example for the full list.
 */
export const env = {
  /** Base URL of the ChipsTalk backend REST API. */
  apiUrl: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  /** Base URL of the ChipsTalk backend WebSocket server. */
  wsUrl: process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000/ws",
};
