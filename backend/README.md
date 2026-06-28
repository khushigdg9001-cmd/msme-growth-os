# MSME Growth OS Backend

Production-oriented FastAPI backend skeleton for the MSME Growth OS MVP.

## Current Scope

This layer contains only architecture scaffolding:

- FastAPI application bootstrap
- Environment-based settings
- Async SQLAlchemy database setup
- Alembic migration wiring
- Domain and database model skeletons
- LangGraph agent architecture placeholders
- Decision engine interfaces
- Versioned API routing

Business logic is intentionally not implemented yet.

## Local Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn msme_growth_os.main:create_app --factory --reload
```

## Architecture

```text
src/msme_growth_os/
  core/                 App settings, logging, errors
  domain/               Pure business entities and repository contracts
  application/          Use-case interfaces and DTOs
  infrastructure/       Database, migrations, external adapters
  ai/                   LangGraph agents, orchestration, decision contracts
  interfaces/api/       FastAPI routers, dependencies, schemas
```
