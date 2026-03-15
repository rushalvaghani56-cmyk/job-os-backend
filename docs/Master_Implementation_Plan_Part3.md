# MASTER IMPLEMENTATION PLAN — Part 3: MCP, Infrastructure & Agentic Blueprint (15 Modules)

> **This document defines all 15 Blueprint Modules** that govern how AI agents operate throughout the project lifecycle.

---

## MODULE A: System & Architecture Initialization

---

### Module 1: Cursor Agent Rules

#### `.cursorrules` (Root — applies to all repos)

```
# ════════════════════════════════════════════
# JOB APPLICATION OS — CURSOR AGENT RULES
# ════════════════════════════════════════════

## STACK CONSTRAINTS
- Frontend: Next.js 14 App Router + TypeScript (strict) + shadcn/ui + Tailwind CSS
- Backend: Python 3.12 + FastAPI + SQLAlchemy (async) + Pydantic v2
- Database: PostgreSQL (Supabase) — always use parameterized queries via SQLAlchemy
- State: Zustand (global client state), TanStack Query (server state), React Hook Form + Zod (forms)
- Task Queue: Celery + Redis
- Testing: pytest (backend), Vitest (frontend unit), Playwright (E2E)

## MANDATORY BEHAVIORS
1. ALWAYS read existing files before modifying them — never assume content
2. ALWAYS write failing tests BEFORE implementation code (TDD mandate)
3. ALWAYS use TypeScript strict mode — no `any` types, no `@ts-ignore`
4. ALWAYS use Pydantic models for all API request/response validation
5. ALWAYS include `user_id` filter in every database query (security isolation)
6. NEVER hardcode secrets, API keys, or database URIs — use environment variables
7. ALWAYS update .env.example when adding new environment variables
8. ALWAYS use semantic commit messages: feat|fix|test|chore|docs(scope): description
9. ALWAYS wrap page sections in ErrorBoundary components on critical pages

## TRACKER FILES (update after every completed task)
- Implementation_Tracker.md — current phase, decisions, implementation details
- Audit_Log.md — security scans, bug fixes, test coverage metrics

## CODE PATTERNS
- Backend services: thin controller (router) → service layer → repository (SQLAlchemy)
- Frontend data: TanStack Query for server state, Zustand for client-only state
- Forms: React Hook Form + Zod schemas (shared with backend Pydantic via schema parity)
- Errors: standardized error envelope { error: { code, message, details? } }
- Pagination: cursor-based { data, next_cursor, has_more }

## FILE NAMING
- Backend: snake_case for all Python files
- Frontend: PascalCase for components, camelCase for hooks/utils/stores
- Tests: test_*.py (backend), *.test.ts (frontend unit), *.spec.ts (E2E)

## FORBIDDEN
- No `console.log` in committed code (use proper logging)
- No `print()` in Python (use Loguru)
- No inline styles (use Tailwind classes)
- No direct Supabase client calls from backend (use SQLAlchemy)
- No localStorage/sessionStorage (use Zustand persist middleware if needed)
```

#### `.cursor/rules/backend-agent.md`

```markdown
# Backend Agent Rules

## Before writing any code:
1. Read the relevant SQLAlchemy model in app/models/
2. Read the Pydantic schema in app/schemas/
3. Read the existing service in app/services/ (if exists)
4. Read the test file (if exists) to understand expected behavior

## Implementation order:
1. Write/update Pydantic schemas (request + response)
2. Write failing test (pytest)
3. Implement service logic
4. Implement API route
5. Run test — must pass
6. Run `ruff check .` and `mypy .`
7. Update OpenAPI docs if new endpoint

## Database queries:
- ALWAYS filter by user_id
- ALWAYS use async session
- ALWAYS handle soft-deleted records (WHERE is_deleted = false)
- Use selectin/joinedload for relationships, never lazy load in async
```

#### `.cursor/rules/frontend-agent.md`

```markdown
# Frontend Agent Rules

## Before writing any component:
1. Read the relevant types in src/types/
2. Read the relevant Zod validators in src/lib/validators/
3. Check if a shadcn/ui primitive exists before building custom

## Component patterns:
- Use React Server Components by default, add "use client" only when needed
- All client components that fetch data: use TanStack Query hooks
- All forms: React Hook Form + Zod + shadcn/ui Form components
- Error boundaries: route-level for pages, section-level for Dashboard/JobDetail/Analytics
- Loading states: Suspense boundaries with skeleton components

## State rules:
- Server data → TanStack Query (never Zustand)
- Auth/profile/UI → Zustand
- Form data → React Hook Form (never Zustand or useState for forms)
- URL state → Next.js searchParams (filters, pagination cursors)
```

---

### Module 2: MCP Architecture Map

#### Pre-Built MCP Servers Required

| MCP Server | Purpose | Configuration |
|-----------|---------|---------------|
| **PostgreSQL MCP** (`@modelcontextprotocol/server-postgres`) | Direct database querying for debugging and data inspection | Connection string: `SUPABASE_DB_URL` |
| **GitHub MCP** (`@modelcontextprotocol/server-github`) | PR creation, issue management, branch operations | Token: `GITHUB_TOKEN`, repos: frontend, backend, infra |
| **Filesystem MCP** (`@modelcontextprotocol/server-filesystem`) | Read/write project files across all 3 repos | Allowed paths: `/frontend`, `/backend`, `/infra` |
| **Redis MCP** (custom or CLI wrapper) | Inspect cache, circuit breaker states, rate limit counters | Connection: `REDIS_URL` |

#### Custom MCP Tools to Build

```yaml
# Custom MCP Server: jobapp-dev-tools

tools:
  - name: run_backend_tests
    description: "Run pytest with optional path filter"
    input: { test_path: string (optional) }
    execution: "cd backend && pytest {test_path} -v --tb=short"

  - name: run_frontend_tests
    description: "Run Vitest with optional filter"
    input: { test_filter: string (optional) }
    execution: "cd frontend && npx vitest run {test_filter}"

  - name: run_linting
    description: "Run all linters (ruff + mypy + eslint + tsc)"
    input: { repo: "backend" | "frontend" }
    execution: |
      if backend: "cd backend && ruff check . && mypy ."
      if frontend: "cd frontend && npx eslint . && npx tsc --noEmit"

  - name: check_migration_status
    description: "Check Alembic migration status"
    execution: "cd backend && alembic current && alembic heads"

  - name: generate_migration
    description: "Auto-generate Alembic migration"
    input: { message: string }
    execution: "cd backend && alembic revision --autogenerate -m '{message}'"

  - name: seed_database
    description: "Run seed script"
    execution: "cd backend && python scripts/seed.py"

  - name: check_coverage
    description: "Get current test coverage"
    input: { repo: "backend" | "frontend" }
    execution: |
      if backend: "cd backend && pytest --cov=app --cov-report=term-missing"
      if frontend: "cd frontend && npx vitest run --coverage"

  - name: health_check
    description: "Check all service health"
    execution: "curl -s http://localhost:8000/api/v1/health | python -m json.tool"

resources:
  - name: implementation_tracker
    uri: "file://Implementation_Tracker.md"
    description: "Current project state and decisions"

  - name: audit_log
    uri: "file://Audit_Log.md"
    description: "Security scans, bugs, and coverage metrics"

  - name: api_contract
    uri: "file://Master_Implementation_Plan_Part1.md#4-the-api-contract"
    description: "Complete API endpoint specification"
```

---

### Module 3: Agent Roles & Skill Definitions

#### Backend Engineer Agent
```
Skills:
- Run pytest (unit, integration, tasks)
- Execute Alembic migrations (generate, upgrade, downgrade)
- Run ruff linter + mypy type checker
- Manage Celery tasks (start worker, inspect active tasks)
- Query database via SQLAlchemy (read models, write queries)
- Manage Redis (inspect cache, flush, check circuit breakers)
- Run seed/teardown scripts
- Generate OpenAPI spec
```

#### Frontend Agent
```
Skills:
- Run Next.js dev server (npm run dev)
- Run Vitest (npm run test)
- Run Playwright E2E (npx playwright test)
- Run ESLint + TypeScript check (npm run lint, npx tsc --noEmit)
- Install shadcn/ui components (npx shadcn-ui@latest add [component])
- Build production bundle (npm run build)
- Inspect bundle size (npx next build --analyze)
```

#### Infrastructure/DevOps Agent
```
Skills:
- Docker Compose operations (up, down, build, logs, exec)
- Terraform (init, plan, apply, destroy)
- GitHub Actions workflow authoring
- SSH to EC2 for deployment
- Caddy configuration
- SSL certificate management (automatic via Caddy)
- ECR image push/pull
- pg_dump backup execution
```

---

### Module 4: Claude Code CLI Initialization Runbook

#### Step 1: Initialize Workspace
```bash
# Clone all repos
git clone git@github.com:yourorg/jobapp-frontend.git frontend
git clone git@github.com:yourorg/jobapp-backend.git backend
git clone git@github.com:yourorg/jobapp-infra.git infra

# Pin context files
claude --context \
  Implementation_Tracker.md \
  Audit_Log.md \
  Master_Implementation_Plan_Part1.md \
  Master_Implementation_Plan_Part2.md \
  Master_Implementation_Plan_Part3.md \
  backend/.cursorrules \
  frontend/.cursorrules
```

#### Step 2: Initial Prompt for Phase 1
```
You are the principal architect for Job Application OS. Your context includes the complete 
Implementation Plan (3 parts), the Implementation Tracker, and the Audit Log.

We are starting Sprint 0. Execute tasks 0.1 through 0.10 in sequence. For each task:
1. Read the task specification from Part 2
2. Read any context files mentioned
3. Write failing tests FIRST (TDD mandate)
4. Implement the solution
5. Verify all tests pass
6. Commit with semantic message
7. Update Implementation_Tracker.md and Audit_Log.md

Begin with Task 0.1: Initialize Backend Repository.
```

---

### Module 5: Atomic Agentic Pipeline

Every task follows this exact pipeline:

```
┌─────────────────┐
│ 1. READ CONTEXT  │  Read task spec + context files + existing code
└────────┬────────┘
         │
┌────────▼────────┐
│ 2. WRITE TEST    │  Write failing test (pytest/vitest) — TDD mandate
└────────┬────────┘
         │
┌────────▼────────┐
│ 3. RUN TEST      │  Verify test fails (red phase)
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. IMPLEMENT     │  Write minimal code to pass the test
└────────┬────────┘
         │
┌────────▼────────┐
│ 5. RUN TEST      │  Verify test passes (green phase)
└────────┬────────┘
         │
┌────────▼────────┐
│ 6. LINT & TYPE   │  ruff + mypy (backend) OR eslint + tsc (frontend)
└────────┬────────┘
         │
┌────────▼────────┐
│ 7. VERIFY        │  Run the task-specific verification step
└────────┬────────┘
         │
┌────────▼────────┐
│ 8. COMMIT        │  Semantic commit message (feat|fix|test|chore)
└────────┬────────┘
         │
┌────────▼────────┐
│ 9. UPDATE DOCS   │  Update Implementation_Tracker.md + Audit_Log.md
└─────────────────┘
```

---

## MODULE B: Continuous Quality & Self-Healing Pipeline

---

### Module 6: TDD Mandate

```
RULE: The agent MUST write failing tests BEFORE writing implementation code.

Testing Sequence:
1. Read the task requirements
2. Write test file with all test cases (each testing one behavior)
3. Run tests — ALL must fail (confirms tests are meaningful)
4. Write implementation code
5. Run tests — ALL must pass
6. Refactor if needed (tests still pass)

Frameworks:
- Backend Unit:       pytest + pytest-asyncio + pytest-mock
- Backend Integration: pytest + httpx.AsyncClient (FastAPI TestClient)
- Backend Tasks:      pytest + celery.contrib.pytest (mocked broker)
- Frontend Unit:      Vitest + React Testing Library
- Frontend E2E:       Playwright

Coverage Thresholds:
- Sprint 0-4 (MVP core):   60% minimum
- Sprint 5-8 (MVP full):   70% minimum
- V2 sprints:              80% minimum
- Critical paths (auth, scoring, encryption, payment): 90% minimum

Enforcement: pytest --cov-fail-under=60 (backend), vitest --coverage.thresholds.lines=60 (frontend)
```

---

### Module 7: Auto-Fixing & Debugging Loop

```
WHEN a test fails or compilation error occurs:

Step 1: READ the full error output (stack trace, assertion failure, type error)
Step 2: IDENTIFY the root cause category:
  - Type error → check Pydantic schema / TypeScript interface mismatch
  - Import error → check module paths, __init__.py, barrel exports
  - Database error → check model definition, migration status, connection
  - Test assertion → check expected vs actual, verify test logic
  - Runtime error → check null handling, async/await, dependency injection

Step 3: IMPLEMENT a targeted fix (not a shotgun approach)
Step 4: RE-RUN the failing test only
Step 5: If still failing, repeat from Step 1

INFINITE LOOP BREAKER:
If the agent fails to fix a bug after 3 consecutive attempts:
1. STOP all implementation
2. Create Bug_Reports/BUG_{timestamp}_{description}.md with:
   - Error message and full stack trace
   - All 3 attempted fixes and why they failed
   - Hypothesis for root cause
   - Suggested next steps for human review
3. PROMPT the human user: "I've been unable to resolve this issue after 3 attempts.
   Please review Bug_Reports/BUG_xxx.md and provide guidance."
4. DO NOT continue to the next task until the bug is resolved
```

---

### Module 8: Automated Security & Code Audits

```
RUN AFTER: Every sprint completion (or after 5+ tasks if mid-sprint)

Security Checklist:
□ pip-audit (backend) — no critical/high vulnerabilities
□ npm audit (frontend) — no critical/high vulnerabilities
□ git-secrets --scan — no secrets in codebase
□ .env.example is up-to-date with all required variables
□ Pydantic strips HTML from all plain text input fields
□ bleach sanitizes all rich text (Tiptap) fields
□ All database queries include user_id filter
□ CORS allows only configured frontend domain(s)
□ Rate limiting is active on all authenticated endpoints
□ AES-256-GCM encryption is used for all stored API keys
□ RLS policies are active on all user-scoped tables

Code Quality:
□ ruff check . — 0 errors (backend)
□ mypy . — 0 errors (backend)
□ eslint . — 0 errors (frontend)
□ tsc --noEmit — 0 errors (frontend)
□ No TODO/FIXME/HACK comments without linked issue

Performance:
□ No N+1 queries (use selectinload/joinedload)
□ All list endpoints use cursor pagination (never offset)
□ Heavy components use next/dynamic with ssr:false
□ Job Browser uses @tanstack/react-virtual
□ Redis cache hit rate for analytics endpoints > 80%

Output: Update Audit_Log.md with complete results.
```

---

### Module 9: Audit_Log.md Template

```markdown
# Audit Log — Job Application OS

## Format
Each entry: `[DATE] [SPRINT] [TYPE] Description`
Types: SECURITY, BUG_FIX, COVERAGE, PERFORMANCE, DEPLOYMENT

---

## Log Entries

### Sprint 0
- [2026-03-14] [Sprint 0] [SECURITY] Initial security setup: AES-256-GCM encryption, 
  CORS strict mode, rate limiting configured. pip-audit: 0 critical.
- [2026-03-14] [Sprint 0] [COVERAGE] Backend: 45% (core + middleware only). Frontend: 0%.
- [2026-03-14] [Sprint 0] [PERFORMANCE] Health endpoint: <50ms. Docker build: 45s.

### Sprint 1
- [2026-03-21] [Sprint 1] [SECURITY] Auth audit: JWT verification working, no token leakage, 
  password never stored (delegated to Supabase). npm audit: 0 critical.
- [2026-03-21] [Sprint 1] [COVERAGE] Backend: 62%. Frontend: 35%.
- [2026-03-21] [Sprint 1] [BUG_FIX] Fixed: Supabase JWT clock skew causing intermittent 401s. 
  Root cause: server timezone not UTC. Fix: force UTC in container.

(continues per sprint...)
```

---

### Module 10: Functionality Verification (End-to-End Check)

```
BEFORE closing any task, verify against the Technical Documentation:

Checklist Template:
□ Does the implementation match the spec exactly? (check field names, types, behaviors)
□ Does the API response match the contract in Part 1 Section 4?
□ Are all error codes returned correctly per the error code table?
□ Does the UI match the page description in the spec?
□ Does real-time update work? (change in DB → Realtime → UI updates)
□ Does the user flow work end-to-end? (e.g., signup → JWT → protected route)
□ Are edge cases handled? (empty state, error state, loading state)
□ Is the Audit_Log.md updated?
□ Is the Implementation_Tracker.md updated?

Critical User Flow Verifications (per sprint):
- Sprint 1: User registers → JWT generated → DB row created → Frontend redirects to onboarding
- Sprint 2: Discovery runs → Jobs appear → Scores display → Filter works
- Sprint 3: Content generates → 2 variants appear → Review queue populated → Approve works → Undo works
- Sprint 4: Application tracks → Kanban drag works → Status updates → Files upload/preview
- Sprint 5: Copilot responds → Actions execute → Notifications appear in real-time
- Sprint 6: Onboarding completes → Dashboard shows data → Settings persist
- Sprint 7: Analytics render → Charts show data → Export downloads → Admin panel works
- Sprint 8: E2E tests pass → Security audit clean → Production deploys → Health check green
```

---

## MODULE C: Production & Lifecycle Management

---

### Module 11: Git & Version Control Protocol

```
BRANCHING STRATEGY:
- main          → production-ready code only
- develop       → integration branch
- feature/*     → new features (e.g., feature/auth-api, feature/job-browser)
- bugfix/*      → bug fixes (e.g., bugfix/jwt-clock-skew)
- test/*        → test additions (e.g., test/auth-integration)
- chore/*       → non-code changes (e.g., chore/docker-config)

WORKFLOW:
1. Create branch: git checkout -b feature/{task-name}
2. Implement task (following Atomic Pipeline)
3. Commit with semantic message
4. Push branch
5. Create PR (via GitHub MCP or manually)
6. After review/merge: delete branch

COMMIT FORMAT (Conventional Commits):
feat(scope): description      — new feature
fix(scope): description       — bug fix
test(scope): description      — test addition/modification
chore(scope): description     — tooling, deps, config
docs(scope): description      — documentation update
refactor(scope): description  — code restructuring
perf(scope): description      — performance improvement

SCOPES: auth, profiles, jobs, scoring, content, review, applications, files, 
        copilot, notifications, analytics, market, admin, settings, onboarding, 
        shell, realtime, db, security, infra, ci

RULES:
- NEVER push directly to main
- NEVER batch multiple features in one commit
- ALWAYS commit after each successful atomic task
- Commit message body should reference the task (e.g., "Task 1.1 — Sprint 1")
```

---

### Module 12: Context & Memory Management

```
MILESTONE SUMMARIZATION:
After completing each Sprint, generate a Phase Summary:

Template:
---
## Phase Summary: Sprint {N}
**Completed:** {date}
**Tasks Completed:** {count}/{total}
**Test Coverage:** Backend {X}%, Frontend {Y}%

### What Was Built:
- {bullet list of implemented features}

### Current State:
- Database: {N} tables, {M} migrations applied
- API: {N} endpoints active
- Frontend: {N} pages implemented
- Active branches: {list}

### Key Decisions Made:
- {any deviations from the plan with reasoning}

### Known Issues:
- {open bugs, if any, with Bug_Report references}

### Next Sprint Focus:
- {Sprint N+1 goals}
---

CONTEXT FLUSHING:
When to start a fresh session:
1. After completing a full Sprint
2. When context window is approaching limit (>80% capacity)
3. After resolving a complex bug that required extensive debugging

Fresh session baseline files:
- Implementation_Tracker.md (latest)
- Audit_Log.md (latest)
- Phase Summary for the completed Sprint
- .cursorrules
- The next Sprint's task list from Part 2
```

---

### Module 13: Secrets & Environment Management

```
ABSOLUTE RULE: No secrets in source code. Ever.

Backend .env.example:
```
# ═══ Database ═══
SUPABASE_DB_URL=postgresql+asyncpg://user:pass@host:6543/dbname  # PgBouncer port
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret

# ═══ Redis ═══
REDIS_URL=redis://localhost:6379/0

# ═══ File Storage ═══
R2_ACCOUNT_ID=your-cloudflare-account-id
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=jobapp-files
R2_ENDPOINT_URL=https://{account_id}.r2.cloudflarestorage.com

# ═══ Encryption ═══
MASTER_ENCRYPTION_KEY=your-256-bit-hex-key  # For BYOK API key encryption

# ═══ Monitoring ═══
SENTRY_DSN=https://key@sentry.io/project

# ═══ Application ═══
ENVIRONMENT=development  # development | staging | production
CORS_ORIGINS=http://localhost:3000
API_VERSION=v1
LOG_LEVEL=DEBUG
```

Frontend .env.example:
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SENTRY_DSN=https://key@sentry.io/project
```

RULE: Whenever a new environment variable is added:
1. Add it to .env.example with a description comment
2. Add it to app/config.py (backend) with type + default + validation
3. Document it in Implementation_Tracker.md
```

---

### Module 14: Database Seeding & Mock Data

```python
# backend/scripts/seed.py

"""
Database seed script using Faker for realistic mock data.
Run: python scripts/seed.py
"""

from faker import Faker
import asyncio
from app.db.session import async_session
from app.models import *

fake = Faker()

async def seed():
    async with async_session() as session:
        # ─── Users ───
        admin = User(
            email="admin@jobapp.test",
            role=UserRole.SUPER_ADMIN,
            full_name="Admin User",
            supabase_uid="test-admin-uid",
        )
        user = User(
            email="user@jobapp.test",
            role=UserRole.USER,
            full_name="Test User",
            supabase_uid="test-user-uid",
        )
        session.add_all([admin, user])
        await session.flush()

        # ─── Profiles (3 per user) ───
        profiles = []
        for u in [user]:
            for role in ["Backend Engineer", "ML Engineer", "Platform Engineer"]:
                p = Profile(
                    user_id=u.id,
                    name=f"{role} Search",
                    target_role=role,
                    target_seniority="Senior (6-10 YOE)",
                    years_of_experience=fake.random_int(5, 10),
                    salary_min=fake.random_int(150000, 200000),
                    salary_max=fake.random_int(200000, 300000),
                    completeness_pct=fake.random_int(60, 95),
                )
                profiles.append(p)
        session.add_all(profiles)
        await session.flush()

        # ─── Skills (20 per user) ───
        skill_names = ["Python", "TypeScript", "Go", "Rust", "React", "Next.js", 
                       "FastAPI", "Django", "PostgreSQL", "Redis", "Docker", "K8s",
                       "AWS", "GCP", "Terraform", "GraphQL", "gRPC", "Kafka",
                       "PyTorch", "TensorFlow"]
        for name in skill_names:
            session.add(Skill(
                user_id=user.id,
                name=name,
                category="language" if name in ["Python", "TypeScript", "Go", "Rust"] else "framework",
                proficiency=fake.random_int(2, 5),
                years_used=fake.random_int(1, 8),
            ))

        # ─── Jobs (100) ───
        companies = ["Google", "Stripe", "Meta", "Netflix", "Airbnb", "Uber",
                     "Databricks", "Figma", "Vercel", "Supabase", "Linear",
                     "Anthropic", "OpenAI", "Datadog", "Cloudflare"]
        for _ in range(100):
            session.add(Job(
                user_id=user.id,
                profile_id=profiles[0].id,
                title=fake.job(),
                company=fake.random_element(companies),
                location=fake.city(),
                location_type=fake.random_element(["remote", "hybrid_flex", "onsite"]),
                seniority="Senior",
                employment_type="Full-time",
                score=round(fake.random.uniform(30, 98), 1),
                confidence=round(fake.random.uniform(0.5, 0.99), 2),
                status=fake.random_element(["new", "scored", "content_ready", "applied"]),
                salary_min=fake.random_int(150000, 200000),
                salary_max=fake.random_int(200000, 350000),
                salary_currency="USD",
            ))

        # ─── Applications (20) ───
        # ─── Notifications (30) ───
        # ─── Review Queue Items (15) ───
        # (similar pattern — create realistic mock data)

        await session.commit()
        print("✅ Seed complete: 2 users, 3 profiles, 20 skills, 100 jobs")


# Teardown
async def teardown():
    async with async_session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
        print("🧹 Teardown complete: all tables truncated")
```

---

### Module 15: Automated API Documentation

```
RULE: Every API endpoint must be documented in the OpenAPI spec before the task is closed.

Implementation:
- FastAPI auto-generates OpenAPI spec from route definitions + Pydantic models
- Every route MUST include:
  - response_model (Pydantic schema)
  - summary (short description)
  - tags (module name)
  - responses (error codes with schemas)

Example:
```python
@router.post(
    "/signup",
    response_model=AuthResponse,
    summary="Register a new user",
    tags=["auth"],
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        409: {"model": ErrorResponse, "description": "Email already registered"},
    },
)
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    ...
```

Verification:
- After implementing any endpoint: curl localhost:8000/openapi.json | python -m json.tool
- Verify the endpoint appears in Swagger UI at /docs
- Verify request/response schemas are correctly documented
- Verify error responses are listed

Maintenance:
- OpenAPI spec is auto-generated — no manual YAML/JSON files to maintain
- Pydantic schemas ARE the documentation (single source of truth)
```

---

## MCP & INFRASTRUCTURE PREPARATION (Sprint 0 Prerequisite)

### Before Any Application Code:

| Step | Action | Verification |
|------|--------|-------------|
| 1 | Create Supabase project (production + staging) | Dashboard accessible, connection string works |
| 2 | Create Cloudflare R2 bucket | `aws s3 ls --endpoint-url $R2_ENDPOINT` succeeds |
| 3 | Create AWS EC2 instances (prod + staging) | SSH access confirmed |
| 4 | Set up Amazon ECR repository | `docker push` to ECR succeeds |
| 5 | Configure GitHub repos (frontend, backend, infra) | Clone + push works, branch protection on main |
| 6 | Set up Sentry projects (backend + frontend) | DSN available, test error appears |
| 7 | Configure UptimeRobot monitor | Pointing to staging health endpoint |
| 8 | Install MCP servers (postgres, github, filesystem) | `mcp list-tools` shows all tools |
| 9 | Generate all .env files from .env.example | `docker-compose up` starts without env errors |
| 10 | Verify Docker Compose stack | All 6 containers running: caddy, fastapi, celery-worker, celery-beat, redis, playwright |

### Environment Variable Checklist

| Variable | Required By | How to Obtain |
|----------|------------|---------------|
| `SUPABASE_DB_URL` | Backend | Supabase Dashboard → Settings → Database → Connection String (port 6543 for PgBouncer) |
| `SUPABASE_URL` | Backend + Frontend | Supabase Dashboard → Settings → API → URL |
| `SUPABASE_ANON_KEY` | Frontend | Supabase Dashboard → Settings → API → anon/public |
| `SUPABASE_SERVICE_ROLE_KEY` | Backend | Supabase Dashboard → Settings → API → service_role |
| `SUPABASE_JWT_SECRET` | Backend | Supabase Dashboard → Settings → API → JWT Secret |
| `REDIS_URL` | Backend | `redis://localhost:6379/0` (Docker) or managed Redis URL |
| `R2_ACCOUNT_ID` | Backend | Cloudflare Dashboard → R2 → Account ID |
| `R2_ACCESS_KEY_ID` | Backend | Cloudflare Dashboard → R2 → API Tokens |
| `R2_SECRET_ACCESS_KEY` | Backend | Cloudflare Dashboard → R2 → API Tokens |
| `R2_BUCKET_NAME` | Backend | Name chosen during R2 bucket creation |
| `MASTER_ENCRYPTION_KEY` | Backend | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `SENTRY_DSN` | Backend + Frontend | Sentry Dashboard → Settings → Client Keys |
| `GITHUB_TOKEN` | CI/CD | GitHub → Settings → Developer Settings → Personal Access Tokens |

---

> **End of Part 3.** All 15 Blueprint Modules defined. All infrastructure prerequisites documented. Ready for Sprint 0 execution.
