# ChipsTalk — Frontend

Frontend of ChipsTalk: dashboards, price charts, and the chat interface.
Built with Next.js (App Router), TypeScript (strict), Tailwind CSS, React,
and Vitest.

This app talks to the ChipsTalk backend exclusively through its REST API
and WebSocket server. It never accesses PostgreSQL directly.

## Getting started

```bash
cp .env.example .env.local
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Scripts

- `npm run dev` — start the development server.
- `npm run build` — production build.
- `npm run start` — run the production build.
- `npm run lint` — ESLint.
- `npm test` — run the test suite once (Vitest).
- `npm run test:watch` — run tests in watch mode.

## Environment variables

See `.env.example`:

- `NEXT_PUBLIC_API_URL` — base URL of the backend REST API.
- `NEXT_PUBLIC_WS_URL` — base URL of the backend WebSocket server.

## Structure

```
src/
  app/         Next.js routes, layouts and pages
  components/  Reusable UI components
  hooks/       React hooks
  lib/         Utilities, API/WebSocket clients, env access
  types/       Shared TypeScript types
  test/        Test setup
```
