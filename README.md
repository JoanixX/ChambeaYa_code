# ChambeaYa Backend — FastAPI service matching students to company challenges

The backend for a platform that connects university students with companies posting real
project challenges. It owns the relational domain — students, companies, job offers,
skills, interests, experience, matches and agreements — over async SQLAlchemy and
PostgreSQL, and delegates candidate/offer ranking to a separate AI service over HTTP.
The code is laid out as ports and adapters: 15 domain entities, 8 use cases with explicit
port interfaces, and FastAPI confined to the input adapter.

**Interactive API docs:** `/docs` (Swagger) · `/redoc` · **License:** MIT

## Results

There are no tests, no benchmarks and no evaluation of the matching in this repository —
the CI workflow builds and deploys but runs no test step. What is verifiable is the API
surface and the layering, so that is what this table reports.

| Property | Value | Evidence |
|---|---|---|
| HTTP endpoints exposed | 8, all under `/api` | `app/main.py` router registration |
| Domain entities | 15 | `app/domain/entities/` |
| Use cases with explicit ports | 8 | `app/application/use_cases/`, `app/application/ports/` |
| Domain repository interfaces | 6 | `app/domain/repositories/` |
| Domain services (framework-free) | 5 | `app/domain/services/` |
| Database access | async SQLAlchemy + asyncpg | `app/infraestructure/database/connection.py` |
| Production server | gunicorn, 4 uvicorn workers | `startup.sh` |
| Automated tests | **none** | — |
| CI test stage | **none** — build and deploy only | `.github/workflows/s5_api-backend-cy.yml` |

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/register/user` | Create an application user |
| POST | `/api/login` | Authenticate, returns a JWT |
| POST | `/api/register/student` | Register a student profile |
| POST | `/api/register/company` | Register a company |
| POST | `/api/filter/student/preprocess_all_student` | Embed all student profiles (proxied to the AI service) |
| POST | `/api/filter/job_offer/preprocess_all_job_offer` | Embed all job offers (proxied to the AI service) |
| POST | `/api/aimodel/student/best_job_offers/{student_id}` | Rank offers for one student |
| POST | `/api/aimodel/job_offer/matching_offers` | Score a student against an offer |

Reproduce: `uvicorn app.main:app --reload`, then open `http://localhost:8000/docs`.

## How it works

- **Ranking lives in a separate service, not in this codebase.**
  `app/infraestructure/ai_client/ai_connection.py` posts to an AI API (default
  `http://localhost:8001`) for both embedding and matching. The backend owns the database
  and the authorization decision; the model service stays stateless and independently
  deployable, at the cost of a network hop per ranking request.
- **Every use case declares a port.** `app/application/ports/` holds one interface per
  use case, so the FastAPI route depends on an abstraction rather than on a concrete
  repository — the domain can be exercised without a running database.
- **Domain services are framework-free** (`agreement_policy_checker`,
  `student_profile_evaluator`, `company_needs_analyzer`, `filter_match_service`,
  `match_job_student_service`), keeping the eligibility and evaluation rules readable
  without FastAPI or SQLAlchemy in scope.
- **Database access is async end to end** — `create_async_engine` with asyncpg and an
  `AsyncSession` dependency — so a request awaiting Postgres does not occupy the event
  loop while the AI service call is also in flight.
- **Passwords are hashed with bcrypt via passlib**, and sessions are HS256 JWTs with a
  60-minute default expiry (`app/adapters/input/fastapi/routes/jwt_utils.py`).
- **Secrets and the connection string come from the environment and have no in-code
  fallback.** A missing `DATABASE_URL` or `JWT_SECRET_KEY` raises at import with a message
  naming the variable, because a default signing key that silently works in production is
  worse than a service that refuses to boot.
- **CORS is an explicit allowlist**, not a wildcard: only the two local frontend origins
  are permitted.

## Quick start

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # fill in DATABASE_URL and JWT_SECRET_KEY
uvicorn app.main:app --reload
```

`DATABASE_URL` and `JWT_SECRET_KEY` are required — the app refuses to start without them,
rather than falling back to a default secret. `ACCESS_TOKEN_EXPIRE_MINUTES` (default 60),
`SQL_ECHO` (default `false`) and `IA_API_URL` are optional; see `.env.example`.

API docs at `http://localhost:8000/docs` (Swagger) and `/redoc`.

Ranking endpoints additionally require the AI service running on port 8001; set
`IA_API_URL` if it lives elsewhere. In production the service is started with
`./startup.sh` (gunicorn, 4 uvicorn workers, port 8000) and deployed to Azure App Service
by the workflow in `.github/workflows/`.

## Data & provenance

No datasets are committed. All records — student profiles, companies, offers, skills,
matches, agreements — are created at runtime through the API and persisted to PostgreSQL.
Embeddings and match scores are derived by the external AI service and are not stored in
this repository.

## Limitations

- **The old credentials are still in git history and must be rotated.** The database
  password and JWT signing key were previously literals in source; they now come from the
  environment, but removing them from the working tree does not remove them from earlier
  commits. Until the Postgres password is changed and a new signing key is issued, anyone
  with read access to this repository's history holds working database credentials and can
  forge tokens.
- **No tests and no CI test stage.** The deploy workflow installs dependencies, zips the
  tree and ships it; nothing verifies that the application imports, that a route responds,
  or that a use case behaves. The workflow's own comment marks the test step as still
  optional and unfilled.
- **The ports layer is declared but not enforced.** Interfaces exist for all 8 use cases,
  yet the routes construct their dependencies directly rather than receiving them through
  injection, so the abstraction does not currently buy testability.
- **There is no database migration tooling.** The schema is whatever the entity
  definitions produced against the live database; there is no versioned, replayable path
  to recreate it.
- **No rate limiting, no refresh tokens, no token revocation.** A leaked 60-minute JWT is
  valid until it expires.

## License

MIT
