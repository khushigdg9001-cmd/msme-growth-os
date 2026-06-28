# Backend Architecture

## Boundaries

- `domain`: pure models and repository contracts.
- `application`: use cases that coordinate domain and infrastructure.
- `infrastructure`: database, migrations, external integrations, persistence adapters.
- `ai`: LangGraph orchestration, business agents, decision engine contracts.
- `interfaces`: FastAPI routes and request/response schemas.

## MVP Agent Set

- Inventory Agent
- Finance Agent
- CRM Agent
- Compliance Agent
- Supplier Agent
- Decision Engine

The current implementation intentionally contains only stubs and graph wiring. Business logic will be added in later layer  