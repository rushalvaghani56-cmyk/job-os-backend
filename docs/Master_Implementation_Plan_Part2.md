# MASTER IMPLEMENTATION PLAN — Part 2: The Agentic Sprint Roadmap

> **Format:** Every task follows the Atomic Agentic Pipeline (Blueprint Rule 5)
> **TDD Mandate:** Tests are written BEFORE implementation (Blueprint Rule 6)
> **Commits:** Conventional Commits after each atomic task (Blueprint Rule 11)

---

## SPRINT 0: Foundation & Infrastructure (Week 1)

> **Goal:** Set up all repositories, tooling, CI/CD, database, and dev environment so Sprint 1 agents can write application code immediately.

---

### Task 0.1 — Initialize Backend Repository

| Field | Detail |
|-------|--------|
| **Goal** | Create backend/ repo with FastAPI project skeleton, pyproject.toml, Docker config, and all directory structure |
| **Context Files** | `Master_Implementation_Plan_Part1.md` (project tree section) |
| **Execution** | 1. `mkdir backend && cd backend` 2. Create `pyproject.toml` with ruff, mypy, pytest config. 3. Create `requirements.txt` (fastapi, uvicorn, sqlalchemy[asyncio], asyncpg, alembic, celery, redis, pydantic, python-jose, cryptography, loguru, httpx, sentry-sdk). 4. Create full directory structure per project tree. 5. Create `app/main.py` with bare FastAPI app factory. 6. Create `Dockerfile` (Python 3.12-slim). 7. Create `.env.example` with all required vars documented. |
| **Verification** | `docker build -t jobapp-backend .` succeeds. `uvicorn app.main:app --host 0.0.0.0 --port 8000` starts. `curl localhost:8000/docs` returns Swagger UI. |
| **Commit** | `feat(backend): initialize FastAPI project skeleton with Docker and config` |
| **Audit Log** | `[Sprint 0] Backend repo initialized. FastAPI skeleton running. Docker build verified.` |

---

### Task 0.2 — Initialize Frontend Repository

| Field | Detail |
|-------|--------|
| **Goal** | Create frontend/ repo with Next.js 14 App Router, shadcn/ui, Tailwind, TypeScript, and all directory structure |
| **Context Files** | `Master_Implementation_Plan_Part1.md` (project tree) |
| **Execution** | 1. `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir`. 2. Install: `shadcn-ui`, `zustand`, `@tanstack/react-query`, `@supabase/supabase-js`, `sonner`, `next-themes`, `zod`, `react-hook-form`, `@hookform/resolvers`. 3. Run `npx shadcn-ui@latest init`. 4. Create full directory structure per project tree. 5. Configure `vitest.config.ts` + `playwright.config.ts`. 6. Create `.env.example` with NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, NEXT_PUBLIC_API_URL. |
| **Verification** | `npm run dev` starts at localhost:3000. `npm run build` succeeds. `npm run lint` passes. |
| **Commit** | `feat(frontend): initialize Next.js 14 project with shadcn/ui, Tailwind, and tooling` |
| **Audit Log** | `[Sprint 0] Frontend repo initialized. Next.js 14 + shadcn/ui + Tailwind confirmed.` |

---

### Task 0.3 — Initialize Infrastructure Repository

| Field | Detail |
|-------|--------|
| **Goal** | Create infra/ repo with Docker Compose (all services), Terraform scaffolding, GitHub Actions CI/CD, and Caddy config |
| **Context Files** | `Technical_Documentation_v1.0.md` (Section 7: Infrastructure) |
| **Execution** | 1. Create `docker-compose.yml` with services: caddy, fastapi, celery-worker, celery-beat, redis, playwright. 2. Create `docker-compose.dev.yml` override (hot-reload, debug mode). 3. Create `docker/caddy/Caddyfile` for reverse proxy. 4. Create `terraform/` with main.tf, variables.tf, ec2.tf, security_groups.tf, iam.tf, ecr.tf. 5. Create GitHub Actions workflows: ci-backend.yml, ci-frontend.yml, deploy-staging.yml, deploy-production.yml, e2e-nightly.yml. 6. Create `scripts/deploy.sh` for EC2 rolling deploy. |
| **Verification** | `docker-compose -f docker-compose.dev.yml up` starts all services. `terraform validate` passes. GitHub Actions YAML lint passes. |
| **Commit** | `feat(infra): initialize Docker Compose, Terraform, CI/CD, and Caddy config` |
| **Audit Log** | `[Sprint 0] Infrastructure repo initialized. Docker Compose validated. Terraform scaffolded.` |

---

### Task 0.4 — Database Setup: SQLAlchemy Models + Alembic

| Field | Detail |
|-------|--------|
| **Goal** | Create all SQLAlchemy models per Part 1 schemas. Initialize Alembic. Generate and apply initial migration. |
| **Context Files** | `Master_Implementation_Plan_Part1.md` (Section 2: Database Schemas) |
| **Execution** | 1. Create `app/db/base.py` (Base, mixins). 2. Create `app/db/session.py` (async engine, session factory via PgBouncer). 3. Create ALL models in `app/models/` per schema spec. 4. Create `app/models/__init__.py` importing all models. 5. `alembic init alembic`. 6. Configure `alembic/env.py` to use async engine + import all models. 7. `alembic revision --autogenerate -m "initial_schema"`. 8. `alembic upgrade head`. |
| **Verification** | Connect to Supabase Postgres. `\dt` shows all tables. All indexes exist (`\di`). Alembic version table present. |
| **Commit** | `feat(db): create all SQLAlchemy models and initial Alembic migration` |
| **Audit Log** | `[Sprint 0] Database schema created. 20 tables, all indexes applied. Alembic migration v001.` |

---

### Task 0.5 — Database Seeding Script

| Field | Detail |
|-------|--------|
| **Goal** | Create seed script that populates dev database with realistic mock data using Faker |
| **Context Files** | `app/models/*.py` |
| **Execution** | 1. `pip install faker`. 2. Create `scripts/seed.py`: generates 2 users (1 admin, 1 regular), 3 profiles per user, 100 jobs, 20 applications, 50 review items, skills, experience, education. 3. Create `scripts/teardown.py`: truncates all tables respecting FK order. |
| **Verification** | `python scripts/seed.py` runs without error. Query `SELECT COUNT(*) FROM jobs` returns 100. `python scripts/teardown.py` cleans all. |
| **Commit** | `feat(db): add Faker-based seed and teardown scripts` |
| **Audit Log** | `[Sprint 0] Database seeding operational. Mock data: 2 users, 100 jobs, 20 applications.` |

---

### Task 0.6 — Core Middleware & Error Handling

| Field | Detail |
|-------|--------|
| **Goal** | Implement the middleware chain (CORS → Rate Limiter → Auth → Logging → Handler) and standardized error envelope |
| **Context Files** | `Technical_Documentation_v1.0.md` (Sections 3.5, 3.3.2) |
| **Execution** | **TDD First:** Write `tests/unit/test_error_handling.py` — test error envelope format, test all error codes return correct HTTP status. Write `tests/unit/test_rate_limiter.py` — test rate limiting with Redis mock. **Then implement:** 1. `app/core/exceptions.py` — AppError base, all error codes, exception handlers. 2. `app/core/middleware.py` — CORS, request logging (Loguru). 3. `app/core/rate_limiter.py` — Redis-based per-user limiter. 4. `app/core/security.py` — JWT verification via Supabase. 5. `app/core/logging.py` — Loguru structured JSON config. 6. Wire all in `app/main.py`. |
| **Verification** | `pytest tests/unit/test_error_handling.py -v` — all pass. `pytest tests/unit/test_rate_limiter.py -v` — all pass. Manual: `curl -H "Authorization: Bearer invalid" localhost:8000/api/v1/auth/me` returns `{"error": {"code": "AUTH_INVALID_TOKEN", ...}}`. |
| **Commit** | `feat(core): implement middleware chain, error handling, and rate limiting` |
| **Audit Log** | `[Sprint 0] Middleware chain operational: CORS → Rate Limit → Auth → Logging. Error envelope standardized. Tests: 12/12 pass.` |

---

### Task 0.7 — BYOK Encryption Module

| Field | Detail |
|-------|--------|
| **Goal** | Implement AES-256-GCM encryption with per-user HKDF key derivation for BYOK API keys |
| **Context Files** | `Technical_Documentation_v1.0.md` (Section 6.2) |
| **Execution** | **TDD First:** Write `tests/unit/test_encryption.py` — test encrypt/decrypt roundtrip, test per-user key isolation, test tamper detection. **Then implement:** `app/core/security.py` — `encrypt_api_key(user_id, plaintext_key)`, `decrypt_api_key(user_id, encrypted_data)` using `cryptography` library (HKDF + AES-256-GCM). Master key from `MASTER_ENCRYPTION_KEY` env var. |
| **Verification** | `pytest tests/unit/test_encryption.py -v` — all pass. Verify: encrypt with user_A, decrypt with user_B fails. Tampering detected. |
| **Commit** | `feat(security): implement AES-256-GCM BYOK encryption with HKDF per-user derivation` |
| **Audit Log** | `[Sprint 0] BYOK encryption operational. AES-256-GCM + HKDF. Tests: 8/8 pass. Security audit: PASS.` |

---

### Task 0.8 — Celery + Redis Setup

| Field | Detail |
|-------|--------|
| **Goal** | Configure Celery application factory, Redis broker, beat scheduler, and task communication pattern |
| **Context Files** | `Technical_Documentation_v1.0.md` (Section 3.7) |
| **Execution** | 1. Create `app/tasks/celery_app.py` — Celery app with Redis broker, result backend, serialization config. 2. Create `app/tasks/scheduled_tasks.py` — beat schedule placeholder. 3. Create `app/db/redis.py` — Redis connection pool for caching + rate limiting. 4. Wire Celery into Docker Compose (worker + beat containers). 5. Create a test task that writes to the `tasks` table. |
| **Verification** | Start worker: `celery -A app.tasks.celery_app worker --loglevel=info`. Send test task. Verify `tasks` table row updated to `completed`. Redis: `redis-cli ping` returns PONG. |
| **Commit** | `feat(tasks): configure Celery app factory, Redis broker, and beat scheduler` |
| **Audit Log** | `[Sprint 0] Celery operational. Redis broker connected. Task → DB → Realtime pipeline verified.` |

---

### Task 0.9 — Supabase Realtime Integration

| Field | Detail |
|-------|--------|
| **Goal** | Set up Supabase Realtime subscriptions on the frontend that invalidate TanStack Query caches |
| **Context Files** | `Technical_Documentation_v1.0.md` (Section 2.4), `frontend/src/lib/` |
| **Execution** | 1. Create `frontend/src/lib/supabase.ts` — browser Supabase client. 2. Create `frontend/src/lib/queryClient.ts` — TanStack QueryClient with defaults. 3. Create `frontend/src/lib/realtimeManager.ts` — subscribe to `tasks`, `jobs`, `notifications`, `review_queue` tables. On INSERT/UPDATE, call `queryClient.invalidateQueries()` with matching key. 4. Create `frontend/src/hooks/useRealtime.ts` — React hook wrapping the manager. 5. Wire into root layout provider. |
| **Verification** | Start frontend. Insert a row into `notifications` via Supabase dashboard. Frontend TanStack Query auto-refetches. Console shows invalidation log. |
| **Commit** | `feat(realtime): integrate Supabase Realtime with TanStack Query cache invalidation` |
| **Audit Log** | `[Sprint 0] Realtime operational. DB changes → WebSocket → cache invalidation → UI refresh pipeline verified.` |

---

### Task 0.10 — OpenAPI Auto-Documentation

| Field | Detail |
|-------|--------|
| **Goal** | Configure FastAPI auto-generated OpenAPI spec with proper metadata, tags, and response schemas |
| **Context Files** | `app/main.py`, `app/schemas/common.py` |
| **Execution** | 1. Configure `app/main.py` with OpenAPI metadata (title, version, description, tags). 2. Create `app/schemas/common.py` — ErrorResponse, PaginatedResponse, SuccessResponse base schemas. 3. Verify `/docs` shows Swagger UI and `/redoc` shows ReDoc. 4. Add response_model to health endpoint as first example. |
| **Verification** | `curl localhost:8000/openapi.json` returns valid OpenAPI 3.1 spec. Swagger UI renders at `/docs`. |
| **Commit** | `feat(api): configure OpenAPI auto-documentation with Swagger UI and ReDoc` |
| **Audit Log** | `[Sprint 0] API documentation operational. Swagger UI at /docs, ReDoc at /redoc.` |

---

## SPRINT 1: Authentication & User Management (Week 2)

> **Goal:** Complete auth flow (signup, login, JWT verification) + user CRUD + profile CRUD with full TDD.

---

### Task 1.1 — Auth API: Signup + Login + JWT

| Field | Detail |
|-------|--------|
| **Goal** | Implement auth endpoints using Supabase Auth with FastAPI middleware verification |
| **Context Files** | `app/core/security.py`, `app/models/user.py`, `Technical_Documentation_v1.0.md` (Section 3.4) |
| **Execution** | **TDD First:** Write `tests/integration/test_auth_api.py`: test_signup_success, test_signup_duplicate_email, test_login_success, test_login_wrong_password, test_get_me_authenticated, test_get_me_unauthenticated, test_token_refresh. **Then implement:** 1. `app/schemas/auth.py` — SignupRequest, LoginRequest, AuthResponse. 2. `app/services/auth_service.py` — create_user, authenticate, get_user_by_supabase_uid. 3. `app/api/v1/auth.py` — POST /signup, POST /login, POST /logout, POST /refresh, GET /me. 4. `app/api/deps.py` — `get_current_user` dependency. |
| **Verification** | `pytest tests/integration/test_auth_api.py -v` — all 7 tests pass. Manual: sign up via Swagger → get JWT → call /me with Bearer token. |
| **Commit** | `feat(auth): implement signup, login, JWT verification, and /me endpoint` |
| **Audit Log** | `[Sprint 1] Auth API complete. 7 integration tests pass. JWT flow verified end-to-end.` |

---

### Task 1.2 — Profile CRUD API

| Field | Detail |
|-------|--------|
| **Goal** | Implement full profile CRUD with multi-profile support, cloning, and completeness calculation |
| **Context Files** | `app/models/profile.py`, `app/schemas/profile.py`, Part 1 API Contract (4.2) |
| **Execution** | **TDD First:** Write `tests/integration/test_profiles_api.py`: test_create_profile, test_list_profiles, test_get_profile, test_update_profile, test_delete_profile (soft delete), test_clone_profile, test_activate_profile, test_completeness_calculation, test_user_isolation (user A cannot see user B's profiles). **Then implement:** 1. `app/schemas/profile.py` — ProfileCreate, ProfileUpdate, ProfileResponse. 2. `app/services/profile_service.py` — CRUD + clone + completeness calculator. 3. `app/api/v1/profiles.py` — all endpoints per contract. |
| **Verification** | `pytest tests/integration/test_profiles_api.py -v` — all 9 tests pass. Verify user isolation: create profile as user A, attempt GET as user B → 404. |
| **Commit** | `feat(profiles): implement multi-profile CRUD with cloning and completeness tracking` |
| **Audit Log** | `[Sprint 1] Profile API complete. 9 integration tests pass. User isolation verified.` |

---

### Task 1.3 — Skills, Experience, Education CRUD

| Field | Detail |
|-------|--------|
| **Goal** | Implement CRUD for skills, work experience, education, achievements, and projects |
| **Context Files** | `app/models/skill.py`, `app/models/work_experience.py`, `app/models/education.py` |
| **Execution** | **TDD First:** Write tests for each entity's CRUD. **Then implement:** Sub-resource routes under profiles (e.g., `/api/v1/profiles/:id/skills`). Batch import endpoint for skills. |
| **Verification** | All CRUD tests pass. Batch import works for 50+ skills. |
| **Commit** | `feat(profiles): add skills, experience, education, achievements, and projects CRUD` |
| **Audit Log** | `[Sprint 1] Profile sub-resources complete. Skills batch import verified.` |

---

### Task 1.4 — Frontend: Auth Pages + Zustand Store

| Field | Detail |
|-------|--------|
| **Goal** | Build login, signup, and forgot-password pages. Set up Zustand auth store. Wire to Supabase Auth. |
| **Context Files** | `frontend/src/stores/authStore.ts`, `frontend/src/lib/supabase.ts` |
| **Execution** | **TDD First:** Write `tests/unit/stores/authStore.test.ts` — test login updates state, test logout clears state, test token refresh. **Then implement:** 1. `stores/authStore.ts` — user, session, login(), signup(), logout(). 2. `app/(public)/auth/login/page.tsx` — form with RHF + Zod validation. 3. `app/(public)/auth/signup/page.tsx`. 4. Middleware: redirect authenticated users away from auth pages. 5. Middleware: redirect unauthenticated users to login from dashboard pages. |
| **Verification** | `npm run test` — store tests pass. Manual: signup → verify email → login → redirect to dashboard. |
| **Commit** | `feat(auth-ui): implement login, signup pages with Zustand auth store` |
| **Audit Log** | `[Sprint 1] Frontend auth complete. Zustand store tested. Supabase Auth integrated.` |

---

### Task 1.5 — Frontend: App Shell (Sidebar + Topbar + Layout)

| Field | Detail |
|-------|--------|
| **Goal** | Build the persistent app shell: collapsible sidebar, top bar with search/bell/profile, responsive layout |
| **Context Files** | `Technical_Documentation_v1.0.md` (Part IV: Global UX Patterns), `frontend/src/components/layout/` |
| **Execution** | 1. `components/layout/AppShell.tsx` — CSS grid/flex layout with sidebar + content + optional copilot panel. 2. `components/layout/Sidebar.tsx` — 260px collapsible, all nav items per spec (with badges). 3. `components/layout/Topbar.tsx` — global search, profile switcher, notification bell, copilot button, dark/light toggle. 4. `stores/uiStore.ts` — sidebar collapsed, theme. 5. Integrate `next-themes` for dark/light mode. 6. `app/(dashboard)/layout.tsx` — wraps all dashboard pages with AppShell. |
| **Verification** | Visual inspection at all 3 breakpoints (desktop, tablet, mobile). Sidebar collapses. Theme toggles. Nav items render with correct icons. |
| **Commit** | `feat(shell): implement app shell with responsive sidebar, topbar, and theme toggle` |
| **Audit Log** | `[Sprint 1] App shell complete. Responsive at 3 breakpoints. Dark/light mode operational.` |

---

## SPRINT 2: Job Discovery & Scoring Engine (Weeks 3-4)

> **Goal:** Implement the discovery pipeline (scraping → normalization → dedup), AI scoring engine, and Job Browser UI.

---

### Task 2.1 — Job Discovery: Scraping Tasks

| Field | Detail |
|-------|--------|
| **Goal** | Implement Celery tasks for scraping multiple job sources, normalizing data, and deduplication |
| **Context Files** | `app/models/raw_job.py`, `app/models/job.py`, `app/models/job_source.py`, `Technical_Documentation_v1.0.md` (Module F2) |
| **Execution** | **TDD First:** Write `tests/tasks/test_discovery_tasks.py`: test_normalize_job_data, test_dedup_hash_generation, test_dedup_merges_sources, test_discovery_creates_jobs. **Then implement:** 1. `app/tasks/discovery_tasks.py` — `run_discovery(profile_id)`, `normalize_raw_job(raw_data)`, `compute_dedup_hash(company, title, location)`, `merge_duplicates(raw_job_ids)`. 2. Task updates `tasks` table with progress (Supabase Realtime picks it up). |
| **Verification** | `pytest tests/tasks/test_discovery_tasks.py -v` — all pass. Mock scraping data → verify jobs table populated correctly. Verify dedup: same job from 2 sources → 1 job row + 2 job_sources rows. |
| **Commit** | `feat(discovery): implement job scraping, normalization, and deduplication pipeline` |
| **Audit Log** | `[Sprint 2] Discovery pipeline operational. Dedup verified. Tests: 8/8 pass.` |

---

### Task 2.2 — AI Scoring Engine

| Field | Detail |
|-------|--------|
| **Goal** | Implement 8-dimension scoring with configurable weights, confidence, risk, and decision routing |
| **Context Files** | `Technical_Documentation_v1.0.md` (Module F3), `app/models/job.py` (score fields) |
| **Execution** | **TDD First:** Write `tests/unit/test_scoring_engine.py`: test_skill_scoring, test_title_scoring, test_weight_normalization, test_bonus_points, test_decision_routing (≥82 → auto, ≥60 → review, <60 → skip), test_confidence_calculation, test_risk_scoring, test_dream_company_routing. **Then implement:** 1. `app/services/scoring_service.py` — `score_job(job, profile)` returns ScoreResult. 2. `app/tasks/scoring_tasks.py` — `score_job_task(job_id)`, `batch_score_jobs(job_ids)`. 3. AI proxy call for natural language analysis (via `ai_proxy_service`). |
| **Verification** | `pytest tests/unit/test_scoring_engine.py -v` — all pass. Score a job manually: verify 8-dimension breakdown, decision matches routing rules. |
| **Commit** | `feat(scoring): implement 8-dimension AI scoring engine with configurable weights` |
| **Audit Log** | `[Sprint 2] Scoring engine operational. 8 dimensions + confidence + risk. Tests: 12/12 pass.` |

---

### Task 2.3 — AI Proxy Service

| Field | Detail |
|-------|--------|
| **Goal** | Implement centralized AI provider proxy that handles BYOK key decryption, provider routing, cost tracking, and circuit breaking |
| **Context Files** | `Technical_Documentation_v1.0.md` (Section 3.6), `app/core/circuit_breaker.py`, `app/core/security.py` |
| **Execution** | **TDD First:** Write `tests/unit/test_ai_proxy.py`: test_provider_selection, test_key_decryption_before_call, test_cost_tracking, test_circuit_breaker_opens, test_fallback_to_next_provider. **Then implement:** 1. `app/services/ai_proxy_service.py` — `call_ai(user_id, task_type, prompt, model_override?)`. 2. Decrypt user's key → format request per provider → call API → track tokens/cost → handle errors → circuit break on failure. 3. `app/core/circuit_breaker.py` — Redis-based circuit breaker (5 failures in 2 min → open for 60s). |
| **Verification** | `pytest tests/unit/test_ai_proxy.py -v` — all pass. Manual: call with mock provider → verify cost logged, circuit breaker triggers on simulated failures. |
| **Commit** | `feat(ai): implement centralized AI proxy with BYOK decryption, cost tracking, and circuit breaker` |
| **Audit Log** | `[Sprint 2] AI proxy operational. BYOK decryption verified. Circuit breaker tested. Tests: 10/10 pass.` |

---

### Task 2.4 — Jobs API Endpoints

| Field | Detail |
|-------|--------|
| **Goal** | Implement all job-related REST endpoints per API contract |
| **Context Files** | Part 1 API Contract (4.3), `app/models/job.py` |
| **Execution** | **TDD First:** Write `tests/integration/test_jobs_api.py`: test_list_jobs_paginated, test_list_jobs_filtered (score, status, seniority, location), test_get_job, test_manual_add_job, test_bookmark_job, test_skip_job, test_trigger_score, test_trigger_generate, test_search_jobs, test_trigger_discovery. **Then implement:** All endpoints in `app/api/v1/jobs.py` with `app/services/job_service.py`. |
| **Verification** | `pytest tests/integration/test_jobs_api.py -v` — all pass. |
| **Commit** | `feat(jobs-api): implement all job CRUD, filtering, scoring, and discovery endpoints` |
| **Audit Log** | `[Sprint 2] Jobs API complete. 11 endpoints, 11 integration tests pass.` |

---

### Task 2.5 — Frontend: Job Browser Page

| Field | Detail |
|-------|--------|
| **Goal** | Build the Job Browser with table/card/compact views, 15+ filter sidebar, search, sort, virtualized list, and real-time score updates |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 5: Job Browser), `frontend/src/types/jobs.ts` |
| **Execution** | 1. `components/jobs/JobBrowser.tsx` — main container with view toggle + filter sidebar + content. 2. `components/jobs/JobFilterSidebar.tsx` — all filter dimensions (score slider, status, seniority, employment, location, etc.). 3. `components/jobs/JobCard.tsx` + `JobRow.tsx` — card and table row views. 4. `components/jobs/JobScoreBadge.tsx` — color-coded by score range. 5. `app/(dashboard)/jobs/page.tsx` — TanStack Query infinite scroll with cursor pagination. 6. Use `@tanstack/react-virtual` for virtualization (2000+ items). 7. Wire Supabase Realtime for live score badge updates. |
| **Verification** | Seed 500 jobs. Job Browser loads in <2s. Filter by score ≥80 shows correct subset. Virtual scroll handles full list without lag. Score badge updates when backend scores a job. |
| **Commit** | `feat(job-browser): implement Job Browser with filters, views, virtualization, and real-time updates` |
| **Audit Log** | `[Sprint 2] Job Browser complete. 15 filter dimensions. Virtual scroll verified at 500+ items.` |

---

### Task 2.6 — Frontend: Job Detail Page (7 Tabs)

| Field | Detail |
|-------|--------|
| **Goal** | Build the CRM-style Job Detail page with all 7 tabs |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 6: Job Detail) |
| **Execution** | 1. `app/(dashboard)/jobs/[jobId]/page.tsx` — fetch job + render tabbed interface. 2. Each tab as section-error-boundary-wrapped component: OverviewTab (score breakdown chart, AI summary, skills match), DocumentsTab (file list + preview), TimelineTab (chronological events), AnalyticsTab (comparisons), CompanyTab (intel display), OutreachTab (contacts + messages), CopilotTab (job-specific chat). 3. Persistent header with logo, title, company, score, status dropdown, quick actions. |
| **Verification** | Navigate to a seeded job. All 7 tabs render. Score breakdown chart shows 8 dimensions. Status dropdown updates via API. Section error boundary catches tab crash without killing page. |
| **Commit** | `feat(job-detail): implement CRM-style Job Detail page with 7 tabs` |
| **Audit Log** | `[Sprint 2] Job Detail complete. 7 tabs with section-level error boundaries.` |

---

## SPRINT 3: Content Generation & Review Queue (Weeks 5-6)

> **Goal:** AI-powered resume/CL generation, quality checking, review queue with split-panel UI, and approval workflow.

---

### Task 3.1 — Content Generation Engine (Backend)

| Field | Detail |
|-------|--------|
| **Goal** | Implement resume tailoring (2 variants), cover letter generation, QA verification, and content quality scoring |
| **Context Files** | `Technical_Documentation_v1.0.md` (Module F4), `app/services/ai_proxy_service.py` |
| **Execution** | **TDD First:** Write `tests/tasks/test_content_tasks.py`: test_resume_generation_creates_2_variants, test_cover_letter_generation, test_qa_catches_hallucination, test_quality_score_calculation, test_content_respects_ai_instructions. **Then implement:** 1. `app/services/content_service.py` — generate_resume, generate_cover_letter, run_qa_check, calculate_quality_score. 2. `app/tasks/content_tasks.py` — async Celery tasks. 3. Generated documents stored in R2, metadata in documents table. 4. Review queue items auto-created after generation. |
| **Verification** | `pytest tests/tasks/test_content_tasks.py -v` — all pass. Trigger generation → verify 2 resume variants + 1 CL in documents table. QA check flags injected hallucination. |
| **Commit** | `feat(content): implement AI resume/CL generation with QA verification and quality scoring` |
| **Audit Log** | `[Sprint 3] Content generation operational. 2 variants per job. QA pipeline verified. Tests: 8/8 pass.` |

---

### Task 3.2 — Review Queue API

| Field | Detail |
|-------|--------|
| **Goal** | Implement review queue endpoints: list, detail, approve, reject, regenerate, bulk approve |
| **Context Files** | Part 1 API Contract (4.6), `app/models/review_queue.py` |
| **Execution** | **TDD First:** Write `tests/integration/test_review_api.py`: test_list_review_queue_sorted_by_priority, test_approve_item, test_reject_with_reason, test_regenerate_with_instructions, test_bulk_approve, test_5min_undo_window. **Then implement:** `app/api/v1/review.py` + `app/services/review_service.py`. Approval triggers 5-minute undo window (stored in Redis with TTL). |
| **Verification** | `pytest tests/integration/test_review_api.py -v` — all pass. Approve → undo within 5 min succeeds. Undo after 5 min fails. |
| **Commit** | `feat(review-api): implement review queue with approval workflow and 5-minute undo` |
| **Audit Log** | `[Sprint 3] Review API complete. Priority sorting verified. 5-min undo window tested.` |

---

### Task 3.3 — Frontend: Review Queue (Split Panel)

| Field | Detail |
|-------|--------|
| **Goal** | Build the Review Queue page with left panel (queue list) and right panel (detail view with diff, variants, and actions) |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 7: Review Queue) |
| **Execution** | 1. `components/review/ReviewQueue.tsx` — split panel layout (40% list / 60% detail). 2. `ReviewQueueList.tsx` — sorted items with priority tags, type icons, quality scores. 3. `ResumeReview.tsx` — JD vs resume with diff view, 2 variant tabs, inline editing via Tiptap. 4. `CoverLetterReview.tsx`, `OutreachReview.tsx`, `AnswerReview.tsx`. 5. Action buttons: Approve & Submit, Approve, Edit & Approve, Reject, Regenerate. 6. `UndoToast.tsx` — Sonner toast with 5-min countdown and undo button. 7. Real-time queue count in sidebar badge. |
| **Verification** | Seed review items. Queue sorts by priority. Select item → right panel shows detail with diff. Approve → undo toast appears. Variant tabs switch between A and B. Tiptap inline edit works. |
| **Commit** | `feat(review-ui): implement Review Queue with split panel, diff view, and approval workflow` |
| **Audit Log** | `[Sprint 3] Review Queue UI complete. Split panel, variants, diff, undo toast verified.` |

---

## SPRINT 4: Application Tracking & File Management (Weeks 7-8)

> **Goal:** Application tracker (Kanban/Table/Calendar), file upload/download via R2, and application execution.

---

### Task 4.1 — Application Tracker API + Kanban

| Field | Detail |
|-------|--------|
| **Goal** | Implement application CRUD + status management + Kanban drag-and-drop with @dnd-kit |
| **Context Files** | Part 1 API Contract (4.5), `Technical_Documentation_v1.0.md` (Page 8) |
| **Execution** | **Backend TDD:** test_list_applications_filtered, test_update_status, test_mark_applied, test_submit_application (triggers Celery), test_undo_submission. **Frontend:** 1. `KanbanBoard.tsx` with @dnd-kit — columns per status. 2. `KanbanCard.tsx` — logo, title, company, score, days-in-stage. 3. `ApplicationTable.tsx` — sortable/filterable table view. 4. `ViewToggle.tsx` — switch between Kanban/Table/Calendar. 5. Optimistic update on drag with 30-second undo. |
| **Verification** | Drag card between columns → status updates immediately (optimistic). Undo within 30s reverts. Table view shows same data with filters. |
| **Commit** | `feat(applications): implement Application Tracker with Kanban, table views, and drag-and-drop` |
| **Audit Log** | `[Sprint 4] Application Tracker complete. Kanban drag-drop with optimistic updates. 30s undo verified.` |

---

### Task 4.2 — File Management (Presigned Upload + R2)

| Field | Detail |
|-------|--------|
| **Goal** | Implement presigned URL upload flow, file metadata CRUD, and PDF preview |
| **Context Files** | `Technical_Documentation_v1.0.md` (Section 3.8), Part 1 API Contract (4.7) |
| **Execution** | **Backend TDD:** test_presign_upload, test_confirm_upload, test_get_download_url, test_list_files, test_delete_file. **Frontend:** 1. `shared/FileUploader.tsx` — drag-and-drop upload using presigned URL. 2. `shared/PDFViewer.tsx` — react-pdf wrapper with page navigation. 3. `app/(settings)/files/page.tsx` — File Manager page. |
| **Verification** | Upload a PDF → appears in file list → preview renders inline → download URL works → delete removes. |
| **Commit** | `feat(files): implement presigned R2 upload, file management, and PDF preview` |
| **Audit Log** | `[Sprint 4] File management operational. Presigned upload → R2 → preview pipeline verified.` |

---

## SPRINT 5: AI Copilot & Notifications (Weeks 9-10)

> **Goal:** Full Copilot panel with streaming chat, slash commands, action execution. Notification system with real-time bell.

---

### Task 5.1 — Copilot Backend (Streaming Chat + Actions)

| Field | Detail |
|-------|--------|
| **Goal** | Implement Copilot chat endpoint with SSE streaming, persistent memory, context awareness, and action execution |
| **Context Files** | `Technical_Documentation_v1.0.md` (Module F24, Page 11) |
| **Execution** | **TDD:** test_copilot_chat_returns_sse_stream, test_copilot_saves_conversation, test_copilot_executes_action_with_confirmation, test_copilot_context_includes_current_page. **Implement:** `app/api/v1/copilot.py` — SSE streaming endpoint. `app/services/copilot_service.py` — context assembly, message history, action dispatch. |
| **Verification** | Stream a response via SSE. Verify conversation persisted. Execute "run discovery" action → Celery task triggered. |
| **Commit** | `feat(copilot): implement AI Copilot with SSE streaming, memory, and action execution` |
| **Audit Log** | `[Sprint 5] Copilot backend operational. SSE streaming, persistent memory, action execution verified.` |

---

### Task 5.2 — Copilot Frontend Panel

| Field | Detail |
|-------|--------|
| **Goal** | Build the resizable side panel with chat UI, slash commands, suggestion cards, and Cmd+J toggle |
| **Context Files** | `Technical_Documentation_v1.0.md` (Section 2.8), `frontend/src/components/copilot/` |
| **Execution** | 1. `CopilotPanel.tsx` — resizable, pushes main content, Zustand-managed width. 2. `CopilotChat.tsx` — message list + input. SSE consumption for streaming responses. 3. `SlashCommandInput.tsx` — /apply, /generate, /score, /discover, /stats, /compare, /mock, /negotiate, /help. 4. `CopilotSuggestionCard.tsx` — proactive insight cards. 5. Keyboard shortcut: Cmd+J toggle. 6. Mobile: full-screen overlay. |
| **Verification** | Cmd+J opens panel. Type message → streaming response renders. /discover triggers action with confirmation. Panel resizes. Mobile overlay works. |
| **Commit** | `feat(copilot-ui): implement Copilot panel with streaming chat, slash commands, and keyboard toggle` |
| **Audit Log** | `[Sprint 5] Copilot UI complete. Streaming, slash commands, responsive panel verified.` |

---

### Task 5.3 — Notification System

| Field | Detail |
|-------|--------|
| **Goal** | Implement notification CRUD, real-time bell badge, toast popups for critical events, and notification center page |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 18, Module F19) |
| **Execution** | **Backend:** `app/api/v1/notifications.py` — CRUD + read/read-all + unread count. `app/services/notification_service.py` — create_notification (called by other services). **Frontend:** 1. `shared/NotificationBell.tsx` — badge with unread count, dropdown with last 5. 2. `app/(dashboard)/notifications/page.tsx` — full notification center. 3. Sonner toast for critical notifications (bottom-right, 5s auto-dismiss). 4. Supabase Realtime subscription on notifications table → increment badge. |
| **Verification** | Create notification via backend → bell badge increments immediately → toast shows for critical. Mark read → badge decrements. |
| **Commit** | `feat(notifications): implement notification system with real-time bell and toast alerts` |
| **Audit Log** | `[Sprint 5] Notifications operational. Real-time bell, toast popups, center page verified.` |

---

## SPRINT 6: Settings, Onboarding & Dashboard (Weeks 11-12)

> **Goal:** Complete the Settings hub (9 tabs), onboarding wizard (5 steps), and Dashboard Home (command center).

---

### Task 6.1 — Settings Hub (9 Tabs)

| Field | Detail |
|-------|--------|
| **Goal** | Build all 9 settings tabs: General, AI Models, API Keys, Automation, Scoring, Sources, Schedules, Email, Feature Flags |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 16) |
| **Execution** | Each tab as a separate component with its own form (RHF + Zod). ScoringSettings includes 8 weight sliders that auto-normalize to 100% with live preview. APIKeySettings shows masked keys with validate/remove actions. |
| **Verification** | Each tab saves and persists. Scoring weights normalize correctly. API key validation calls test endpoint. |
| **Commit** | `feat(settings): implement Settings Hub with all 9 configuration tabs` |
| **Audit Log** | `[Sprint 6] Settings Hub complete. 9 tabs with form validation verified.` |

---

### Task 6.2 — Onboarding Wizard (5 Steps)

| Field | Detail |
|-------|--------|
| **Goal** | Build the 5-step onboarding flow: profile basics → import data → deep profile → master resumes → AI keys |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 3, Journey 1) |
| **Execution** | `components/onboarding/OnboardingWizard.tsx` — progress bar, back/next, step validation. Steps 1 and 5 required, rest skippable. Resume upload → AI extraction (Celery task). LinkedIn PDF import. Google Places autocomplete for locations. Min 1 valid AI key required on step 5. |
| **Verification** | Complete flow end-to-end: create profile → upload resume → AI extracts data → review → add API key → redirect to dashboard. Skip steps 2-4 → still completes. |
| **Commit** | `feat(onboarding): implement 5-step onboarding wizard with AI resume extraction` |
| **Audit Log** | `[Sprint 6] Onboarding complete. 5-step flow verified. Resume extraction pipeline working.` |

---

### Task 6.3 — Dashboard Home (Command Center)

| Field | Detail |
|-------|--------|
| **Goal** | Build the Dashboard Home with all 7 sections: Stats Row, Action Required, Copilot Preview, Discovery Status, Goal Progress, Recent Activity, Quick Actions |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 4) |
| **Execution** | Each section wrapped in SectionErrorBoundary. Stats Row: 4 cards with trend arrows. Action Required: priority-sorted items with action buttons. Quick Actions: Discover Now, Generate for Top Jobs, View Weekly Report, Open Copilot. All sections fetch data via TanStack Query + Realtime. |
| **Verification** | Dashboard loads with all 7 sections. Stats show real data from seeded DB. Quick actions trigger correctly. One section crash doesn't affect others. |
| **Commit** | `feat(dashboard): implement Dashboard Home command center with all 7 sections` |
| **Audit Log** | `[Sprint 6] Dashboard Home complete. 7 sections with error boundaries verified.` |

---

## SPRINT 7: Analytics, Market Intelligence & Admin (Weeks 13-14)

> **Goal:** Analytics dashboard (9 tabs), market intelligence, and super admin panel.

---

### Task 7.1 — Analytics Dashboard

| Field | Detail |
|-------|--------|
| **Goal** | Build analytics with Recharts (bar, line, area, pie) + D3 Sankey (funnel), exportable as CSV/PDF |
| **Context Files** | `Technical_Documentation_v1.0.md` (Page 12) |
| **Execution** | 9 tabs: Funnel (D3 Sankey), Sources, Rejections, AI Cost, Skills & Market, A/B Testing, Goals, Timing, Reports. All fed by pre-computed Redis cache (analytics Celery tasks). Export endpoint for CSV + PDF. |
| **Verification** | Funnel chart renders Sankey diagram. Each tab shows data from seeded DB. CSV export downloads valid file. |
| **Commit** | `feat(analytics): implement Analytics Dashboard with 9 tabs, Sankey funnel, and export` |
| **Audit Log** | `[Sprint 7] Analytics complete. 9 tabs, Sankey diagram, CSV/PDF export verified.` |

---

### Task 7.2 — Super Admin Panel

| Field | Detail |
|-------|--------|
| **Goal** | Build admin panel: user management, system health, feature flags, activity log viewer |
| **Context Files** | `Technical_Documentation_v1.0.md` (Module F31, Page 21) |
| **Execution** | Admin-only routes protected by role check. User list with search, impersonate (view-as), suspend. System health dashboard reading from /health endpoint. Feature flags toggle. |
| **Verification** | Regular user cannot access /admin → 403. Admin sees user list. Feature flag toggle disables module. |
| **Commit** | `feat(admin): implement Super Admin Panel with user management and feature flags` |
| **Audit Log** | `[Sprint 7] Admin panel complete. Role-based access verified. Feature flags operational.` |

---

## SPRINT 8: Polish, E2E Testing & Production Prep (Weeks 15-16)

> **Goal:** E2E test suites, performance optimization, security audit, and production deployment.

---

### Task 8.1 — E2E Test Suite (Playwright)

| Field | Detail |
|-------|--------|
| **Goal** | Write Playwright E2E tests for all critical user journeys |
| **Context Files** | `Technical_Documentation_v1.0.md` (Journey 1, 2, 3) |
| **Execution** | `signup_flow.spec.ts`, `onboarding_flow.spec.ts`, `discovery_flow.spec.ts`, `review_flow.spec.ts`, `apply_flow.spec.ts`. Each test covers the full user journey end-to-end against staging. |
| **Verification** | `npx playwright test` — all suites pass against staging environment. |
| **Commit** | `test(e2e): add Playwright E2E test suites for all critical user journeys` |
| **Audit Log** | `[Sprint 8] E2E tests complete. 5 journey suites, all passing.` |

---

### Task 8.2 — Security Audit

| Field | Detail |
|-------|--------|
| **Goal** | Run comprehensive security audit: npm audit, pip audit, env var check, input sanitization review, CORS check |
| **Context Files** | All source files |
| **Execution** | 1. `npm audit` (frontend). 2. `pip-audit` (backend). 3. Verify no secrets in codebase (`git-secrets --scan`). 4. Verify all env vars documented in `.env.example`. 5. Verify Pydantic strips HTML from plain text fields. 6. Verify bleach sanitizes Tiptap HTML output. 7. Verify CORS allows only Vercel domain. 8. Verify RLS policies active on all user tables. |
| **Verification** | No critical vulnerabilities. No exposed secrets. Sanitization confirmed. Update `Audit_Log.md` with full security report. |
| **Commit** | `chore(security): complete security audit — no critical issues found` |
| **Audit Log** | `[Sprint 8] Security audit PASS. npm audit: 0 critical. No exposed secrets. RLS verified.` |

---

### Task 8.3 — Production Deployment

| Field | Detail |
|-------|--------|
| **Goal** | Deploy to production: Vercel (frontend), EC2 (backend), run smoke tests |
| **Context Files** | `infra/` repository |
| **Execution** | 1. `terraform apply` — provision EC2, security groups, ECR. 2. Push Docker images to ECR. 3. SSH to EC2 → `docker-compose pull && docker-compose up -d`. 4. Verify health endpoint: `curl https://api.yourapp.com/api/v1/health`. 5. Deploy frontend to Vercel. 6. Run smoke tests against production. |
| **Verification** | Health endpoint returns all checks healthy. Frontend loads. Auth flow works. Job Browser renders. |
| **Commit** | `chore(deploy): production deployment — v1.0.0` |
| **Audit Log** | `[Sprint 8] Production deployed. Health: all green. Smoke tests pass. Version: 1.0.0.` |

---

> **End of Part 2.** Sprints 1-8 cover the MVP (95 features). V2 features (140 features) are planned as Sprints 9-16 following the same atomic task format.
