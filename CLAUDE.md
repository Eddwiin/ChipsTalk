# ChipsTalk

ChipsTalk is a web application for monitoring computer component
prices in near real-time and providing a real-time chat.

## Project architecture

The project is divided into:

- frontend/
- backend/
- database/
- docs/

## Frontend

The frontend is responsible for:

- user interface
- dashboards
- component price visualization
- charts
- chat interface
- WebSocket client

The frontend must NEVER access PostgreSQL directly.

## Backend

The backend is responsible for:

- REST API
- WebSocket server
- business logic
- data validation
- PostgreSQL access

## Database

PostgreSQL is the source of truth for application data.

## Agent rules

There are two development agents:

- frontend-agent
- backend-agent

frontend-agent must primarily modify:
frontend/

backend-agent must primarily modify:
backend/

Neither agent should modify the other agent's domain without
explicitly explaining why.

## Development rules

- Use TypeScript for frontend code.
- Use Python for backend code.
- Write tests for new functionality.
- Do not commit secrets.
- Do not hardcode credentials.
- Keep modules small.
- Prefer simple solutions.
- Do not introduce unnecessary dependencies.
- Read existing code before modifying it.

## Git rules

Agents work on their own branches.

Never use force push.

Never delete another agent's branch.

Always explain important architectural changes.