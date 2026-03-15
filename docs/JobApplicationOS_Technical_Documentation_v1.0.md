# JOB APPLICATION OS — Technical Documentation

> **Version:** 1.0 | **Date:** March 13, 2026 | **Status:** APPROVED — Ready for Implementation
>
> **Product Spec Version:** v2.3 COMBINED FINAL | **Total Modules:** 31 | **Total Features:** 285+
>
> **Technical Decisions:** 78 | **Product Decisions:** 24 | **Total:** 102
>
> This is the SINGLE DEFINITIVE TECHNICAL DOCUMENT. It combines the product feature specification with all architectural and infrastructure decisions. Intended for developers, DevOps engineers, and technical stakeholders involved in implementation.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Frontend Architecture](#2-frontend-architecture)
3. [Backend Architecture](#3-backend-architecture)
4. [Database & Data Layer](#4-database--data-layer)
5. [Error Handling & Resiliency](#5-error-handling--resiliency)
6. [Security & Compliance](#6-security--compliance)
7. [Infrastructure & DevOps](#7-infrastructure--devops)
8. [Observability & Monitoring](#8-observability--monitoring)
9. [Testing & Quality Assurance](#9-testing--quality-assurance)
10. [Complete Architecture Decision Registry](#10-complete-architecture-decision-registry)
11. [Appendix: Product Architecture Decisions](#11-appendix-product-architecture-decisions)
12. [Document Control](#12-document-control)

---

## 1. Executive Summary

Job Application OS is an AI-powered job search command center that automates the entire application lifecycle: from job discovery and scoring, through resume tailoring and application submission, to interview preparation and offer negotiation. The platform is designed as a multi-user, multi-profile SaaS application with a BYOK (Bring Your Own Key) AI model supporting Anthropic, OpenAI, and Google providers.

This document serves as the single definitive technical specification, combining the product feature specification (285+ features across 31 modules) with all architectural and infrastructure decisions (78 total). It is intended for developers, DevOps engineers, and technical stakeholders involved in implementation.

### 1.1 System Overview

| Dimension | Specification |
|-----------|---------------|
| Total Modules | 31 |
| Total Features | 285+ (95 MVP, 140 V2, 50 V3) |
| Total Pages/Views | 21 dashboard pages |
| Architecture Decisions | 24 (product spec) + 78 (technical) = 102 |
| Target Users | Individual job seekers (no social/team features) |
| AI Providers | Anthropic + OpenAI + Google (BYOK) |
| Deployment Model | Vercel (frontend) + AWS EC2 Docker (backend) + Supabase (DB/Auth/Realtime) |

### 1.2 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend Framework | Next.js 14 (App Router) | SSR/CSR hybrid rendering, Server Components |
| UI Library | shadcn/ui + Tailwind CSS | Component library with utility-first styling |
| State Management | Zustand | Lightweight global client state |
| Data Fetching | TanStack Query (React Query) | Server-state caching, dedup, background refetch |
| Real-Time | Supabase Realtime (WebSocket) | Live UI updates, invalidates TanStack cache |
| Backend Framework | Python FastAPI | Async REST API server |
| Task Queue | Celery + Redis | Background job orchestration |
| Database | Supabase (PostgreSQL) | Primary data store with RLS |
| ORM | SQLAlchemy (async) | Database queries, model definitions |
| Migrations | Alembic | Version-controlled schema migrations |
| File Storage | Cloudflare R2 (S3-compatible) | Documents, resumes, screenshots |
| Authentication | Supabase Auth | Email + Google OAuth, JWT tokens |
| Browser Automation | Playwright | ATS auto-fill, E2E testing |
| Hosting (Frontend) | Vercel | Edge deployment, analytics |
| Hosting (Backend) | AWS EC2 + Docker Compose | Containerized backend services |
| CI/CD | GitHub Actions | Build, test, deploy pipelines |
| Monitoring | Sentry + Vercel Analytics | Error tracking, APM, web vitals |
| IaC | Terraform | Infrastructure as code for AWS resources |

---

## 2. Frontend Architecture

### 2.1 Rendering Strategy

The application uses a hybrid rendering approach: Server-Side Rendering (SSR) for initial page loads to optimize Largest Contentful Paint (LCP) and SEO for public pages, with Client-Side Rendering (CSR) for subsequent in-app navigation. The Next.js App Router with Server Components enables this pattern natively, where server components handle data fetching and initial rendering while client components manage interactive state.

### 2.2 Application Router & Route Organization

The application uses the Next.js App Router (app/ directory) with Server Components as the default. Routes are organized by domain using route groups for clean separation:

| Route Group | Pages | Purpose |
|-------------|-------|---------|
| (public) | Landing, Auth, Status | Public-facing pages, no auth required |
| (onboarding) | Onboarding Wizard (5 steps) | First-time user setup flow |
| (dashboard) | Home, Jobs, Review Queue, Applications | Core application pages |
| (outreach) | Outreach Hub, Email Hub | Communication management |
| (analytics) | Analytics, Market Intelligence | Data and reporting |
| (interviews) | Interview Calendar | Interview management |
| (settings) | Settings, Profiles, Files, Activity Log | User configuration |
| (admin) | Super Admin Panel | Platform management (owner only) |

### 2.3 State Management Architecture

State is managed across three layers, each with a distinct responsibility:

**Zustand (Global Client State):** Manages authentication state, active profile selection, Copilot panel state (open/closed, width), UI preferences (theme, sidebar collapsed), and transient UI state that must persist across route navigation.

**TanStack Query (Server State):** Manages all data fetched from the FastAPI backend — job listings, review queue items, application records, analytics data, profile details. Handles caching, deduplication, background refetch, optimistic updates, and cache invalidation.

**React Hook Form + Zod (Form State):** Manages form-specific state for all input-heavy pages (onboarding wizard, profile editor, settings tabs, review queue inline editing). Zod schemas are shared between frontend and backend for consistent validation.

### 2.4 Real-Time Data Integration

Supabase Realtime subscriptions push live updates to the frontend via WebSocket. When a Realtime event fires (e.g., job score updated, Kanban status changed, new notification), it triggers TanStack Query cache invalidation via `queryClient.invalidateQueries()`, causing automatic refetch of the affected data. This ensures the UI stays in sync without manual polling while leveraging TanStack Query's caching layer for performance.

**Fallback behavior:** If the Supabase Realtime connection drops (detected via heartbeat), the system falls back to TanStack Query's `refetchInterval` as a polling backup until the WebSocket reconnects.

### 2.5 Key Frontend Libraries

| Library | Purpose | Usage Context |
|---------|---------|---------------|
| @dnd-kit | Drag-and-drop | Kanban board, scoring weight sliders |
| next-themes | Dark/light theming | OS preference detection + manual toggle |
| Recharts | Charts (primary) | Bar, line, area, pie, histogram, radar charts |
| D3 (Sankey module) | Sankey diagrams | Analytics funnel visualization only |
| react-pdf | PDF rendering | Document preview in Review Queue, File Manager |
| Tiptap | Rich text editor | Inline resume/CL editing in Review Queue |
| Sonner | Toast notifications | Bottom-right alerts, undo actions, async feedback |
| @tanstack/react-virtual | List virtualization | Job Browser (2000+ items), Activity Log |

### 2.6 Code Splitting Strategy

Two-layer code splitting optimizes bundle size. Route-based splitting is automatic via Next.js App Router (each route group loads independently). On top of that, heavy client-only components use `next/dynamic` with `ssr: false`, ensuring libraries like Tiptap, react-pdf, Recharts, D3, and @dnd-kit only load when the component actually renders. Users see a fast skeleton/loading state, then the heavy component hydrates.

### 2.7 Optimistic Updates Strategy

Common, reversible actions use optimistic updates via TanStack Query's `onMutate` callback with automatic rollback on error. This includes: approving review items, bookmarking jobs, dragging Kanban cards, marking notifications as read, and skipping jobs.

Destructive or irreversible actions wait for server confirmation before updating the UI: submitting applications, deleting profiles, sending outreach emails, confirming offers, and account deletion.

### 2.8 Copilot Panel Architecture

The AI Copilot renders as a resizable side panel that pushes the main content area narrower (similar to VS Code's sidebar). Panel width is stored in Zustand and the main content area uses CSS flexbox to reflow responsively. On tablet (768–1279px) and mobile (<768px), the Copilot becomes a full-screen overlay. The panel is toggled via Cmd+J, the floating button, or the navigation item. It supports persistent conversation memory across sessions and is separately configurable to use a different AI model from other tasks.

### 2.9 Accessibility

The application targets WCAG 2.1 AA compliance. shadcn/ui components (built on Radix primitives) provide accessible foundations including keyboard navigation, focus management, and ARIA labels. All interactive elements support keyboard operation, color contrast meets 4.5:1 ratio for text, form errors are announced to screen readers, and the full keyboard shortcut system (Cmd+K command palette, Cmd+J Copilot, etc.) has ARIA-compatible implementations.

### 2.10 Responsive Design

| Breakpoint | Layout Behavior |
|------------|----------------|
| Desktop (1280px+) | Full layout: left sidebar (260px) + main content + optional Copilot side panel |
| Tablet (768–1279px) | Sidebar collapses to icons, split panels stack vertically, Copilot becomes full overlay |
| Mobile (<768px) | Bottom nav or hamburger menu, full-screen card views, Copilot as full overlay |

---

## 3. Backend Architecture

### 3.1 Service Architecture: Modular Monolith

The backend is organized as a modular monolith: a single FastAPI application deployed in one Docker container, with clearly separated internal modules per domain. Each module has its own router, service layer, Pydantic models, and SQLAlchemy models. This provides the organizational benefits of domain separation without the deployment complexity of microservices. If a module later needs independent scaling (e.g., the AI proxy under heavy load), it can be extracted into a separate service without rewriting — the module boundaries are already clean.

### 3.2 Module Structure

| Module | Responsibility | Key Endpoints |
|--------|---------------|---------------|
| auth | JWT verification, user management, Google OAuth | /api/v1/auth/* |
| profiles | CRUD for candidate profiles, multi-profile switching | /api/v1/profiles/* |
| jobs | Job CRUD, discovery triggers, scoring, browser queries | /api/v1/jobs/* |
| content | Resume/CL generation, QA, variants, templates | /api/v1/content/* |
| applications | Application tracking, status management, Kanban | /api/v1/applications/* |
| review | Review queue management, approval workflow | /api/v1/review/* |
| outreach | Recruiter contacts, messages, follow-ups | /api/v1/outreach/* |
| email | Gmail OAuth, detection, sending, templates | /api/v1/email/* |
| interviews | Calendar, scheduling, prep packs, logging | /api/v1/interviews/* |
| analytics | Funnel, sources, rejections, goals, reports | /api/v1/analytics/* |
| market | Trending skills, hot companies, salary trends | /api/v1/market/* |
| ai | AI provider proxy, BYOK key management, cost tracking | /api/v1/ai/* |
| files | Presigned URLs, file metadata, storage management | /api/v1/files/* |
| copilot | Chat interface, action execution, context management | /api/v1/copilot/* |
| notifications | CRUD, delivery, custom alert rules | /api/v1/notifications/* |
| admin | User management, feature flags, system health | /api/v1/admin/* |
| health | Dependency health checks, service status | /api/v1/health |

### 3.3 API Design

#### 3.3.1 REST Conventions

All endpoints are versioned under `/api/v1/` from day one. Standard REST verbs apply: GET for reads, POST for creates, PUT/PATCH for updates, DELETE for removals. All responses follow a consistent envelope format. Successful responses return the resource directly. Error responses use a standardized error envelope with machine-readable error codes.

#### 3.3.2 Standardized Error Envelope

Every error from the API — validation, auth, business logic, rate limit, or server error — returns the same JSON shape with a typed `code` field the frontend can programmatically switch on:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "salary_min", "message": "Must be greater than 0" },
      { "field": "target_role", "message": "Required field" }
    ]
  }
}
```

| Error Code | HTTP Status | Description |
|-----------|-------------|-------------|
| VALIDATION_ERROR | 422 | Invalid input with field-level details array |
| AUTH_TOKEN_EXPIRED | 401 | JWT token has expired, client should refresh |
| AUTH_INVALID_TOKEN | 401 | JWT signature invalid or malformed |
| AUTH_INSUFFICIENT_ROLE | 403 | User role lacks permission for this action |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests, includes retry_after field |
| AI_PROVIDER_TIMEOUT | 504 | AI provider did not respond within timeout |
| AI_PROVIDER_QUOTA_EXCEEDED | 502 | User's AI API key has hit its quota |
| AI_KEY_INVALID | 400 | User's AI API key failed validation |
| ATS_CAPTCHA_DETECTED | 409 | CAPTCHA encountered during auto-apply |
| ATS_SUBMISSION_FAILED | 502 | ATS form submission failed |
| RESOURCE_NOT_FOUND | 404 | Requested entity does not exist |
| RESOURCE_ALREADY_EXISTS | 409 | Duplicate resource creation attempt |
| TASK_FAILED | 500 | Celery task failed after max retries |

#### 3.3.3 Pagination

All list endpoints use cursor-based (keyset) pagination with configurable page sizes per endpoint. Response format:

```json
{
  "data": [...],
  "next_cursor": "abc123",
  "has_more": true
}
```

Default page sizes: 50 for jobs, 100 for activity log, 20 for review queue, 25 for notifications.

### 3.4 Authentication & Authorization

#### 3.4.1 Auth Flow

Supabase Auth handles user registration and login (email + password, Google OAuth). On successful authentication, Supabase issues a JWT. The frontend includes this token as an `Authorization: Bearer` header on every API request. A FastAPI middleware dependency (`get_current_user`) decodes and verifies the JWT using Supabase's JWT secret, extracts the `user_id` from token claims, and injects it into every route handler.

#### 3.4.2 Authorization Model

RBAC with two roles (`user`, `super_admin`) plus row-level ownership enforcement. Middleware checks role for admin-only routes. Every data query includes `WHERE user_id = :current_user_id` as a mandatory filter. Supabase Row Level Security (RLS) policies act as a database-level safety net — even if application code misses a filter, RLS prevents cross-user data access.

### 3.5 Middleware Chain

FastAPI processes middleware in this exact order for every incoming request:

| Order | Middleware | Purpose |
|-------|-----------|---------|
| 1 | CORS | Answer preflight OPTIONS requests; reject disallowed origins |
| 2 | Rate Limiter | Per-user rate limiting via Redis; reject abusive traffic before auth |
| 3 | Auth (JWT Verify) | Decode Supabase JWT, extract user_id; reject expired/invalid tokens |
| 4 | Request Logging | Log request with user_id, endpoint, timestamp via Loguru |
| 5 | Route Handler | Execute business logic |

Public routes (landing page, health check, auth endpoints) skip Auth middleware via FastAPI dependency injection.

### 3.6 AI Provider Proxy

All AI provider calls route through a centralized backend proxy module. User BYOK API keys are decrypted from the database (AES-256-GCM, see Security section), and the proxy handles:

- Provider selection based on task-model mapping
- Request formatting per provider API
- Streaming response proxying for Copilot chat (via SSE)
- Token counting and cost tracking per call
- Circuit breaker logic per provider
- Automatic fallback to alternative providers when circuits open

Keys never leave the server.

### 3.7 Background Task Architecture

#### 3.7.1 Task Split

| Task Type | Handler | Examples |
|-----------|---------|----------|
| Light (<5 seconds) | FastAPI BackgroundTasks | Activity log writes, notification inserts, email open tracking, webhook acks |
| Heavy (>5 seconds) | Celery | Discovery scraping, AI scoring, content generation, auto-apply, email sending |

#### 3.7.2 Celery Task Communication

Celery workers update a `tasks` table in Postgres (status: `pending` → `running` → `completed`, plus `progress_pct` and result metadata). The frontend subscribes to this table via Supabase Realtime, and TanStack Query auto-refetches relevant data when status hits `completed`. This reuses existing Realtime infrastructure with no additional SSE endpoints or polling.

### 3.8 File Upload Flow

File uploads use presigned URLs for direct client-to-R2 upload:

1. Client requests a presigned PUT URL from FastAPI, specifying filename and content type.
2. FastAPI generates a short-lived presigned URL via the R2/S3 SDK and returns it.
3. Client uploads the file directly to R2 using the presigned URL.
4. On upload completion, client notifies FastAPI with the file key.
5. FastAPI records file metadata in the database (filename, size, content type, R2 key, user_id, job_id).

This keeps file bytes off the backend entirely, eliminating memory pressure and bandwidth costs on the VPS.

### 3.9 API Rate Limiting

Dual-layer protection:

- **Vercel edge middleware** catches volumetric abuse (bot floods, DDoS) before requests hit the backend.
- **FastAPI middleware** enforces per-user limits via Redis (100 requests/minute default), using keys like `rate:{user_id}:{endpoint_group}` with TTL expiry.

This is separate from business-logic daily limits (applications/day, outreach/day) which are enforced at the service layer.

### 3.10 API Documentation

FastAPI auto-generates an OpenAPI specification from route definitions and Pydantic models. Interactive Swagger UI and ReDoc are published at `/docs` and `/redoc` respectively. The OpenAPI spec is a first-class deliverable, versioned alongside the codebase, and serves as the contract between frontend and backend teams.

---

## 4. Database & Data Layer

### 4.1 Database Engine & ORM

Supabase provides a managed PostgreSQL instance. SQLAlchemy (full ORM) with async support via the `asyncio` extension handles all database interactions. Alembic manages version-controlled schema migrations with auto-generated diff scripts. The ORM connects through Supabase's built-in PgBouncer connection pooler for efficient connection multiplexing.

### 4.2 Schema Design Principles

| Principle | Implementation |
|-----------|---------------|
| Primary Keys | UUIDs (`uuid_generate_v4()`) for all tables — globally unique, URL-safe, no sequential guessing |
| Soft Delete | User-facing entities get `is_deleted` + `deleted_at` columns; transient data (logs, task records) uses hard delete |
| Timestamps | All tables include `created_at` and `updated_at` (auto-managed by SQLAlchemy event listeners) |
| User Isolation | Every user-owned table includes `user_id` foreign key with mandatory WHERE filtering |
| JSONB Strategy | Hybrid: normalized columns/tables for queryable data; JSONB for metadata blobs (score breakdowns, company intel, custom fields, config objects) |
| Multi-Profile | `profile_id` foreign key on jobs, applications, documents; `user_id` for top-level ownership |

### 4.3 Core Schema Overview

| Table | Key Columns | Relationships |
|-------|------------|---------------|
| users | id (UUID), email, role, settings (JSONB) | Has many profiles |
| profiles | id, user_id, name, target_role, config (JSONB) | Has many jobs, applications |
| skills | id, user_id, name, category, proficiency, years_used | Belongs to user, linked to profiles |
| work_experience | id, user_id, company, title, start/end dates | Belongs to user |
| education | id, user_id, institution, degree, field, dates | Belongs to user |
| raw_jobs | id, source, url, raw_data (JSONB), dedup_hash | Linked to jobs via job_sources |
| jobs | id, user_id, profile_id, title, company, score, status | Has many applications, documents |
| job_sources | job_id, raw_job_id, source, scraped_at | Junction: jobs ↔ raw_jobs |
| applications | id, job_id, user_id, status, submitted_at | Belongs to job, has many documents |
| documents | id, job_id, user_id, type, r2_key, quality_score | Belongs to job/application |
| review_queue | id, user_id, item_type, item_id, priority, status | References documents/outreach |
| outreach_contacts | id, user_id, job_id, name, channel, warmth | Has many outreach_messages |
| outreach_messages | id, contact_id, content, status, sent_at | Belongs to contact |
| interviews | id, application_id, round_type, scheduled_at | Belongs to application |
| notifications | id, user_id, type, priority, title, read | Belongs to user |
| activity_log | id, user_id, action, actor, entity_type, entity_id | Belongs to user |
| tasks | id, user_id, task_name, status, progress_pct, result | Celery task tracking |
| failed_tasks | id, task_name, args, error, failed_at | Dead letter queue |
| api_keys | id, user_id, provider, encrypted_key, status | Belongs to user |
| copilot_conversations | id, user_id, messages (JSONB), context | Belongs to user |

### 4.4 Job Deduplication Model

Discovery scrapes multiple sources, producing duplicate entries for the same job. The dedup pipeline uses a three-table model:

- **raw_jobs** stores every scraped entry exactly as found (one row per source per job).
- A `dedup_hash` computed from normalized (company + title + location) identifies matches.
- The dedup pipeline merges matching raw entries into a single **jobs** row, picking the best data from each source (e.g., salary from LinkedIn, full description from company page).
- A **job_sources** junction table preserves provenance, enabling source health analytics and re-runnable dedup.

### 4.5 Indexing Strategy

Indexes are defined upfront for critical query paths, with reactive additions guided by `EXPLAIN ANALYZE` on slow query logs:

| Table | Index | Purpose |
|-------|-------|---------|
| jobs | (user_id, is_deleted, score DESC) | Job Browser default sort |
| jobs | (user_id, status) | Application Tracker filtering |
| jobs | (user_id, created_at DESC) | Date-based sorting |
| jobs | GIN on search_vector (tsvector) | Full-text search across title, company, description, skills |
| review_queue | (user_id, priority, created_at) | Sorted queue display |
| applications | (user_id, status, updated_at) | Kanban column filtering |
| activity_log | (user_id, created_at DESC) | Chronological browse |
| activity_log | (user_id, action_type) | Filtered views |
| raw_jobs | (dedup_hash) | Deduplication lookups |

### 4.6 Full-Text Search

Postgres `tsvector` with GIN indexing powers all text search. A generated `search_vector` column on the jobs table combines title, company, description, and skills. The Command Palette (Cmd+K) queries a lightweight `search_index` table with `(entity_type, entity_id, search_vector, display_text)` for cross-entity search. No external search engine (Elasticsearch) is required at this scale.

### 4.7 Connection Pooling

Supabase's built-in PgBouncer (transaction mode, port 6543) multiplexes database connections. SQLAlchemy's async engine connects through PgBouncer with `pool_size=10` and `max_overflow=20`. Celery workers use a separate connection string with their own pool. This two-layer approach prevents connection exhaustion under high concurrency.

### 4.8 Caching Layer

Redis caches only expensive computed data: analytics aggregations (funnel conversion rates), dashboard stats (counts with trend comparisons), market intelligence (skill demand tiers), and AI cost rollups. These are computed by Celery on a schedule, cached with TTLs, and served instantly. Hot read paths (job list, profile data) rely on Postgres query performance with proper indexing, supplemented by TanStack Query client-side caching.

### 4.9 Backup Strategy

Supabase provides daily automated backups with point-in-time recovery up to 7 days. Additionally, a weekly `pg_dump` cron writes a full database backup to Cloudflare R2 as an independent offsite backup, surviving even Supabase outages.

---

## 5. Error Handling & Resiliency

### 5.1 Celery Task Retry Strategy

All Celery tasks use exponential backoff via Celery's built-in `autoretry_for` mechanism with a default of 3 maximum retries. Individual tasks can override (e.g., discovery sets `max_retries=5` for flaky scraping). After max retries are exhausted, the task is written to a `failed_tasks` dead letter queue table in Postgres. This feeds into:

- The Activity Log (user sees the failure)
- Notifications (high-priority alert)
- The admin panel (system health dashboard shows failure rates)

No silent failures.

### 5.2 Circuit Breaker Pattern

External service calls (AI providers, ATS sites, Gmail API) are protected by circuit breakers implemented via Redis. Failures are tracked per provider in a sliding window (`circuit:{provider}:failures`). After 5 failures in 2 minutes, the circuit opens and all requests to that provider fail fast for 60 seconds.

During open circuit, if the user has multiple AI keys configured, the system falls back to the next provider in their preference order. The Copilot proactively warns users about provider issues. Circuit state is checked before every external call.

### 5.3 Graceful Degradation

Subsystems are independent — a Gmail API outage does not prevent job browsing. A service health registry in Redis (updated every 30 seconds by health check pings) tracks each subsystem's status. When a service is degraded, the frontend shows a persistent dismissable banner identifying impacted features.

| Subsystem Down | Behavior |
|---------------|----------|
| AI Providers | Scoring queued, generation paused, Copilot shows unavailable, manual tracking works |
| Discovery/Scraping | Existing jobs fully functional, "Next discovery delayed" notice displayed |
| Gmail API | Email detection paused, manual status updates work, outreach queued for later |
| Supabase Realtime | Falls back to TanStack Query refetchInterval polling as backup |
| Cloudflare R2 | File uploads queued, Supabase storage fallback activated (per spec Decision #4) |

### 5.4 Frontend Error Boundaries

Two levels of React Error Boundaries prevent cascading UI failures:

- **Route-level boundaries** wrap each route group — if a page crashes, it shows a "Something went wrong — reload page" fallback without affecting other pages.
- **Section-level boundaries** wrap independent widgets on critical pages: Dashboard Home (each of the 7 sections wrapped independently), Job Detail (each of the 7 tabs), and Analytics (each chart). If one chart crashes, the rest of the page remains functional.

### 5.5 Timeout Strategy

| Service | Timeout | Rationale |
|---------|---------|-----------|
| Internal API (Postgres, Redis) | 5 seconds | Local network, should be near-instant |
| Gmail API | 10 seconds | Google's API is generally fast |
| Scraping/Discovery (Playwright) | 15 seconds per page | Job board pages vary in load time |
| R2 File Operations | 30 seconds | Large file uploads may be slow |
| ATS Auto-Fill (Playwright) | 60 seconds | Multi-step forms with dynamic loading |
| AI Providers (non-streaming) | 90 seconds | Claude Opus with large context can take 30–60s |
| AI Providers (streaming/Copilot) | 120 seconds (15s first-token) | Long generation with streaming; abort if no tokens in 15s |

All timeouts are configurable via environment variables.

---

## 6. Security & Compliance

### 6.1 Secret Management

For MVP, application secrets (Supabase connection string, Redis URL, JWT secret, R2 credentials, master encryption key) are stored in Docker environment variables (backend) and Vercel environment variables (frontend), both encrypted at rest by their respective platforms. All secrets are accessed via a centralized `settings.py` module using `os.environ`, enabling a clean migration path to a dedicated secret manager (Vault, Doppler) in V2 without code changes.

### 6.2 BYOK API Key Encryption

User API keys for Anthropic, OpenAI, and Google are encrypted using AES-256-GCM with per-user derived encryption keys:

1. A **master encryption key** (stored as an environment variable, never in the database) serves as the root secret.
2. The master key is combined with each user's UUID via **HKDF** (HMAC-based Key Derivation Function) to produce a unique encryption key per user.
3. Each API key is encrypted with the user's derived key using **AES-256-GCM**, providing both confidentiality and integrity/tamper detection.

This means: if the database leaks, encrypted keys are useless without the master key. If the master key leaks, an attacker still needs the database. Per-user derivation means compromising one user's key material doesn't help decrypt another's. The AI proxy module decrypts on every AI call — AES-256-GCM decryption takes microseconds, so there is no performance impact.

### 6.3 CORS Policy

Strict CORS for MVP: only the exact Vercel frontend domain(s) are allowed. No wildcards, no localhost in production. Development environment uses a separate `.env` with `localhost:3000` added. The policy will expand to a configurable allowlist when the Chrome extension and public API ship in V3.

### 6.4 Input Sanitization

Defense-in-depth across two input categories:

- **Plain text fields** (profile fields, AI instructions, notes, Copilot chat, custom fields): Pydantic validation strips or rejects HTML tags entirely — no HTML allowed.
- **Rich text fields** (Tiptap editor output in Review Queue): DOMPurify sanitizes on the frontend before sending, and `bleach` whitelist-sanitizes on the backend before storing (allowing only safe tags: `<p>`, `<strong>`, `<em>`, `<ul>`, `<li>`, `<h1>`–`<h3>`, `<a>` with `rel=noopener`).

SQLAlchemy's parameterized queries prevent SQL injection by default.

### 6.5 Content Security Policy

Moderate CSP for MVP with known CDN allowlists for Google Places, fonts, and charting libraries. CSP reporting (`report-to` directive) is enabled to identify violations over the first weeks, and the policy is tightened iteratively based on real violation data.

### 6.6 Privacy Compliance (GDPR)

GDPR-ready from day one. The application handles deeply personal data (work history, salary expectations, visa status, career aspirations, Gmail content). Implementation includes:

- **Consent tracking:** Timestamped, revocable records of user consent for Gmail scanning and data processing.
- **Data export:** Full JSON export of all user data (spec Q7), available within 72 hours.
- **Right to deletion:** Account deletion triggers soft delete with hard purge cron after 30 days (spec Q6).
- **Privacy policy page:** Clear explanation of data collection, usage, and retention periods.
- **Data isolation:** RLS + application-level filtering ensures complete user data separation.

### 6.7 Data Isolation (Multi-Tenant)

Defense-in-depth isolation:

- **Application-level** `WHERE user_id = :uid` is the primary mechanism in every query.
- **Supabase Row Level Security (RLS)** policies act as a database-level safety net — even if application code misses a filter, RLS prevents cross-user data access.
- Super admin routes include an RLS bypass clause.

---

## 7. Infrastructure & DevOps

### 7.1 Deployment Topology

| Component | Platform | Details |
|-----------|----------|---------|
| Frontend | Vercel | Next.js App Router, edge deployment, automatic HTTPS, preview deploys per PR |
| Backend API | AWS EC2 (Docker) | FastAPI container, Caddy reverse proxy with auto-HTTPS |
| Task Workers | AWS EC2 (Docker) | Celery worker + beat containers, same Docker Compose stack |
| Browser Automation | AWS EC2 (Docker) | Playwright container (isolated, resource-limited) |
| Cache / Broker | AWS EC2 (Docker) | Redis container for Celery broker, rate limiting, circuit breakers, computed cache |
| Database | Supabase | Managed PostgreSQL with PgBouncer, RLS, Realtime |
| File Storage | Cloudflare R2 | S3-compatible object storage for documents, resumes, screenshots |
| Container Registry | Amazon ECR | Built images stored here, pulled by EC2 on deploy |
| DNS / SSL | Vercel (frontend) / Caddy (API) | Automatic HTTPS via Let's Encrypt for API domain |

### 7.2 Docker Compose Services

| Service | Image | Ports | Resource Notes |
|---------|-------|-------|---------------|
| caddy | Official Caddy image | 80, 443 (public) | Reverse proxy + auto HTTPS, ~50MB RAM |
| fastapi | Custom (Python 3.12 slim) | 8000 (internal) | API server, uvicorn, ~256MB RAM |
| celery-worker | Same codebase, different entrypoint | None | Scalable via --concurrency, ~512MB RAM |
| celery-beat | Same codebase, beat entrypoint | None | Single instance only, ~128MB RAM |
| redis | Official Redis 7 image | 6379 (internal) | Broker + cache, ~128MB RAM |
| playwright | Custom (Chromium + Python) | None | Isolated, memory-capped, ~1GB RAM |

**Recommended EC2 instances:** t3.xlarge (4 vCPU, 16GB RAM) for production. t3.medium (2 vCPU, 4GB RAM) for staging.

### 7.3 CI/CD Pipeline

GitHub Actions handles all build, test, and deployment workflows:

| Stage | Trigger | Actions |
|-------|---------|---------|
| Lint + Type Check | Every PR | ruff (Python), mypy, eslint, tsc --noEmit |
| Unit Tests | Every PR | pytest (backend) + vitest (frontend), coverage threshold check |
| Build + Push | Merge to main | Build Docker images, push to ECR, build Next.js on Vercel |
| Deploy Staging | Merge to main | SSH to staging EC2, pull new images, rolling restart |
| E2E Tests | Nightly + pre-release | Playwright tests against staging environment |
| Deploy Production | Manual trigger or release tag | SSH to production EC2, rolling deploy, smoke test |

### 7.4 Deployment Strategy

Rolling deploy for zero-downtime updates. Docker Compose containers are restarted one by one: Celery workers drain their current tasks before restarting, FastAPI uses graceful shutdown (in-flight requests complete before the new container takes over), and Caddy routes traffic to the healthy container throughout.

Migration path to ECS Fargate is preserved — each Docker Compose service maps directly to a Fargate task definition.

### 7.5 Environment Strategy

| Environment | Infrastructure | Purpose |
|-------------|---------------|---------|
| Development | Local (Docker Compose + Supabase local) | Developer workstation, hot reload, debug mode |
| Staging | AWS EC2 t3.medium + Supabase project (separate) | Pre-production testing, E2E test target, PR previews |
| Production | AWS EC2 t3.xlarge + Supabase project (separate) | Live application, real users |

### 7.6 Infrastructure as Code

Terraform manages all AWS resources: EC2 instances, security groups, IAM roles, ECR repositories, and associated networking. Terraform state is stored in an S3 backend with DynamoDB locking. Infrastructure changes go through the same PR review process as application code in the dedicated infra repository.

### 7.7 Repository Structure

| Repository | Contents | Deploy Target |
|------------|----------|--------------|
| frontend | Next.js app, React components, Tailwind config, Zod schemas | Vercel (auto-deploy on push to main) |
| backend | FastAPI app, Celery tasks, SQLAlchemy models, Alembic migrations, Dockerfiles | AWS EC2 via GitHub Actions |
| infra | Terraform configs, Docker Compose files, Caddy config, CI/CD workflows | AWS (Terraform apply) |

---

## 8. Observability & Monitoring

### 8.1 Observability Stack

| Tool | Scope | Purpose |
|------|-------|---------|
| Sentry | Backend + Frontend | Error tracking with stack traces, performance monitoring (APM), release tracking |
| Vercel Analytics | Frontend | Real-user Core Web Vitals (LCP, FID, CLS, TTFB) per page, device, geography |
| Loguru (structured JSON) | Backend | Structured logging to stdout, captured by Docker, forwarded to CloudWatch |
| AWS CloudWatch Logs | Backend | Searchable log aggregation for all Docker container output |
| UptimeRobot | External | 5-minute interval ping on /health endpoint, downtime alerts |

### 8.2 Logging Strategy

Loguru replaces Python's standard logging module across all backend services. Configured at startup to output structured JSON to stdout. Each log entry includes: timestamp, level, module, function, message, and custom context fields (`user_id`, `request_id`, `task_id`). A FastAPI middleware injects a unique `request_id` into every log entry for request tracing. Celery tasks bind `task_id` automatically. Docker captures stdout and forwards to AWS CloudWatch Logs.

### 8.3 Health Check Endpoint

A comprehensive `/api/v1/health` endpoint checks every dependency and returns structured status:

```json
{
  "status": "healthy",
  "checks": {
    "postgres": { "status": "healthy", "latency_ms": 4 },
    "redis": { "status": "healthy", "latency_ms": 1 },
    "r2": { "status": "healthy" },
    "celery": { "status": "healthy", "queued_tasks": 3 },
    "gmail": { "status": "degraded", "error": "token refresh needed" }
  },
  "version": "1.2.0",
  "uptime_seconds": 86400
}
```

This endpoint powers the public Status Page (Page 21) and is polled by UptimeRobot for external uptime monitoring.

### 8.4 Alerting

| Alert Source | Triggers | Delivery |
|-------------|----------|----------|
| Sentry | Error rate spikes, performance degradation (p95 > threshold) | Email + Slack #alerts |
| UptimeRobot | Health endpoint unreachable for 2+ consecutive checks | Email + Slack #alerts |
| Custom Celery Health | Queue depth > threshold, DLQ entries, circuit breaker opens, Redis memory > 80% | Slack #alerts only |

Critical alerts (downtime, error spikes) go to both email and Slack. Low-priority alerts (queue depth warnings, performance advisories) go to Slack only to avoid email fatigue.

---

## 9. Testing & Quality Assurance

### 9.1 Testing Frameworks

| Layer | Framework | Scope |
|-------|-----------|-------|
| Backend Unit | pytest (+ pytest-asyncio, pytest-cov, pytest-mock) | FastAPI routes, Celery tasks, scoring engine, dedup logic, AI proxy |
| Frontend Unit/Component | Vitest + React Testing Library | React components, form validation, conditional rendering, Zustand stores |
| End-to-End | Playwright | Full-stack user flows: signup → onboarding → discovery → review → apply |
| Load Testing (V2) | k6 | API throughput, concurrent user simulation, database query performance |

### 9.2 CI Quality Gates

| Gate | When | Blocking? |
|------|------|-----------|
| ruff (Python linter) | Every PR | Yes — must pass to merge |
| mypy (Python type check) | Every PR | Yes |
| eslint (JS/TS linter) | Every PR | Yes |
| tsc --noEmit (TypeScript) | Every PR | Yes |
| pytest (backend units) | Every PR | Yes |
| vitest (frontend units) | Every PR | Yes |
| Coverage threshold (60% MVP, 80% V2) | Every PR | Yes — no PR may drop overall coverage |
| Playwright E2E | Nightly + pre-release branch | No for nightly (creates issue on failure). Yes for release. |

### 9.3 Test Organization

Backend tests are organized as:

- `tests/unit/` — Pure logic: scoring algorithm, dedup hashing, content generation rules
- `tests/integration/` — API endpoints with a test database
- `tests/tasks/` — Celery tasks with mocked external services

Frontend tests mirror the component directory structure. E2E tests are organized by user journey (`signup_flow.spec.ts`, `discovery_flow.spec.ts`, `review_flow.spec.ts`, `apply_flow.spec.ts`).

---

## 10. Complete Architecture Decision Registry

This section consolidates all 78 technical architecture decisions made during the technical design phase. Each decision is final and locked.

### 10.1 Frontend Architecture & UX (18 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| F-01 | Rendering Strategy | Hybrid: SSR initial load, CSR navigation |
| F-02 | Router | App Router (app/ directory, Server Components) |
| F-03 | Global State | Zustand |
| F-04 | Data Fetching | TanStack Query (React Query) |
| F-05 | Real-Time Integration | Supabase Realtime → invalidates TanStack Query cache |
| F-06 | Route Organization | Grouped by domain: (jobs), (outreach), (settings), etc. |
| F-07 | Drag-and-Drop | @dnd-kit |
| F-08 | Theming | next-themes (OS preference + manual toggle) |
| F-09 | Charting | Recharts primary + D3 Sankey module |
| F-10 | Forms & Validation | React Hook Form + Zod (shared client/server schemas) |
| F-11 | Accessibility | WCAG 2.1 AA |
| F-12 | List Virtualization | @tanstack/react-virtual for Job Browser + Activity Log |
| F-13 | PDF Preview | react-pdf |
| F-14 | Rich Text Editing | Tiptap (formatted fields); plain textarea for simple fields |
| F-15 | Toasts | Sonner |
| F-16 | Code Splitting | Route-based (auto) + next/dynamic ssr:false for heavy components |
| F-17 | Optimistic Updates | Optimistic for common actions; wait for destructive actions |
| F-18 | Copilot Panel | Resizable side panel, pushes main content (full overlay on mobile) |

### 10.2 Backend & API Design (15 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| B-01 | Backend Framework | Python (FastAPI) |
| B-02 | API Paradigm | REST with versioned endpoints (/api/v1/) |
| B-03 | Service Architecture | Modular monolith (domain-separated internal modules) |
| B-04 | Auth Flow | Supabase JWT verification in FastAPI middleware |
| B-05 | Authorization Model | RBAC (user/super_admin) + row-level ownership checks |
| B-06 | Pagination | Cursor-based (keyset), configurable page size per endpoint |
| B-07 | Validation | Pydantic + custom error formatter (standardized error envelope) |
| B-08 | API Documentation | Auto-generated OpenAPI spec, published interactive docs |
| B-09 | API Versioning | /api/v1/ prefix from day 1 |
| B-10 | Task Communication | Supabase Realtime (Celery updates DB → frontend subscribes) |
| B-11 | File Upload | Presigned R2 URLs (client uploads direct to R2) |
| B-12 | Rate Limiting | Dual-layer: Vercel edge (DDoS) + FastAPI per-user via Redis |
| B-13 | AI Provider Proxy | All AI calls through backend proxy (keys never leave server) |
| B-14 | Background Tasks | FastAPI BackgroundTasks (<5s) + Celery (heavy/long-running) |
| B-15 | Middleware Order | CORS → Rate limiter → Auth → Logging → Handler |

### 10.3 Database & Data Layer (12 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| D-01 | ORM / Query Layer | SQLAlchemy (full ORM) with async support |
| D-02 | Migrations | Alembic (auto-generated, version-controlled) |
| D-03 | Server-Side Cache | Redis for expensive computed data only |
| D-04 | Primary Keys | UUIDs for all tables |
| D-05 | Deletion Strategy | Soft delete (user-facing) + hard delete (transient) |
| D-06 | Job Dedup Storage | Separate raw_jobs + jobs tables with job_sources junction |
| D-07 | JSONB Strategy | Hybrid: normalized for queryable, JSONB for metadata |
| D-08 | Data Isolation | RLS safety net + application-level user_id filtering |
| D-09 | Backups | Supabase daily + weekly pg_dump to R2 |
| D-10 | Indexing | Upfront for critical paths + reactive for rest |
| D-11 | Connection Pooling | Supabase PgBouncer + SQLAlchemy async pool |
| D-12 | Full-Text Search | Postgres tsvector + GIN index |

### 10.4 Error Handling & Resiliency (6 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| E-01 | Error Format | Standardized envelope + machine-readable error codes |
| E-02 | Celery Retry | Exponential backoff (3 retries default) + dead letter queue |
| E-03 | Circuit Breaker | Per external service via Redis + provider fallback |
| E-04 | Graceful Degradation | Feature-level degradation + banner for impacted features |
| E-05 | Error Boundaries | Route-level + section-level on critical pages |
| E-06 | Timeouts | Tiered per service (5s internal to 120s AI streaming) |

### 10.5 Security & Compliance (6 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| S-01 | Secret Management | Environment variables for MVP, dedicated manager in V2 |
| S-02 | BYOK Encryption | AES-256-GCM with per-user keys via HKDF |
| S-03 | CORS | Strict (Vercel domain only) for MVP |
| S-04 | Input Sanitization | DOMPurify (frontend) + bleach (backend) + Pydantic |
| S-05 | CSP | Moderate with CDN allowlist, tighten via reporting |
| S-06 | Privacy Compliance | GDPR-ready from day 1 |

### 10.6 Infrastructure & DevOps (9 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| I-01 | VPS Provider | AWS EC2 (MVP), migrate to ECS Fargate when needed |
| I-02 | Container Strategy | Docker Compose: fastapi, celery-worker, celery-beat, redis, playwright |
| I-03 | CI/CD | GitHub Actions |
| I-04 | Deployment | Rolling deploy (zero-downtime container restarts) |
| I-05 | IaC | Terraform |
| I-06 | Environments | 3: local dev, staging (small EC2), production (main EC2) |
| I-07 | Repos | Separate: frontend, backend, infra |
| I-08 | Reverse Proxy | Caddy (automatic HTTPS via Let's Encrypt) |
| I-09 | Container Registry | Amazon ECR |

### 10.7 Observability & Monitoring (6 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| O-01 | Observability Platform | Sentry (errors + APM) + CloudWatch Logs |
| O-02 | Logging | Loguru structured JSON to stdout |
| O-03 | Health Checks | Custom /health endpoint + UptimeRobot |
| O-04 | Alerting | Sentry + UptimeRobot + custom Celery health alerts |
| O-05 | Alert Delivery | Email (critical) + Slack #alerts (all) |
| O-06 | Performance Metrics | Sentry Performance (backend) + Vercel Analytics (frontend) |

### 10.8 Testing & QA (6 Decisions)

| ID | Decision | Choice |
|----|----------|--------|
| T-01 | Backend Testing | pytest (+ pytest-asyncio, pytest-cov, pytest-mock) |
| T-02 | Frontend Testing | Vitest + React Testing Library |
| T-03 | E2E Testing | Playwright (reused from ATS automation) |
| T-04 | Coverage Target | 60% MVP, increase to 80% by V2 |
| T-05 | CI Quality Gates | Lint + type + unit per PR; E2E nightly + pre-release |
| T-06 | Load Testing | Defer to V2, use k6 against staging weekly |

---

## 11. Appendix: Product Architecture Decisions

These 24 decisions were locked in the product specification (v2.3) and are included here for completeness. They are the foundation upon which all technical decisions were made.

| # | Decision | Choice |
|---|----------|--------|
| 1 | Frontend | Next.js 14 + shadcn/ui + Tailwind |
| 2 | Auth | Supabase Auth (email + Google OAuth) |
| 3 | Multi-user | Multi-user from day 1 |
| 4 | Storage | Cloudflare R2 primary + Supabase fallback |
| 5 | Notifications | In-app only |
| 6 | Multi-profile | Independent identities + shared data |
| 7 | AI Providers | Anthropic + OpenAI + Google (BYOK) |
| 8 | Deployment | Vercel (frontend) + Docker VPS (backend) |
| 9 | Real-time | Supabase Realtime (WebSocket) |
| 10 | Orchestrator | Celery + Redis |
| 11 | Job Detail UX | CRM-style 7 tabs |
| 12 | Approval Flow | Dedicated Review Queue page |
| 13 | AI Assistant | Full Copilot: chat + proactive + execute actions |
| 14 | Profile Depth | Every detail + custom fields |
| 15 | Beyond Applying | Interview scheduling + calendar integration |
| 16 | Social | No — purely individual tool |
| 17 | Email Integration | All 4: rejection detect, interview detect, send outreach, templates |
| 18 | Mobile | Responsive web |
| 19 | Data Import | LinkedIn PDF + resume parsing |
| 20 | Document Types | Resume, cover letter, thank-you, referral, cold email, withdrawal |
| 21 | Market Intelligence | Full: trends + reports + hiring velocity + competitor analysis |
| 22 | Slack/Sheets | Removed permanently |
| 23 | n8n | Removed permanently |
| 24 | API Keys | BYOK (users bring own keys) |

---

## 12. Document Control

| Field | Value |
|-------|-------|
| Document Title | Job Application OS — Technical Documentation |
| Version | 1.0 |
| Date | March 13, 2026 |
| Status | APPROVED — Ready for Implementation |
| Product Spec Version | v2.3 COMBINED FINAL |
| Total Technical Decisions | 78 |
| Total Product Decisions | 24 |
| Total Modules | 31 |
| Total Features | 285+ |
| Classification | Confidential |

---

> **31 modules. 285+ features. 78 technical decisions. 24 product decisions. 102 total. Zero ambiguity. Ready for implementation.**
