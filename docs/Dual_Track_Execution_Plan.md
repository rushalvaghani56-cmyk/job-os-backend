# DUAL-TRACK EXECUTION PLAN — Operational Playbook

> **Version:** 1.0 | **Date:** March 13, 2026 | **Status:** READY FOR EXECUTION
>
> **Participants:** Human (Tech Lead / DevOps / Reviewer) + AI Agents (Cursor Composer + Claude CLI)
>
> **Source Documents:** Technical Documentation v1.0, Master Implementation Plan (Parts 1-3), Product Spec v2.3

---

## 1. THE HUMAN WORKFLOW (Tech Lead & Infrastructure)

---

### 1.1 Sprint 0 — Pre-Flight: Environment Setup (Human Only)

These steps MUST be completed before any AI agent writes a single line of application code. No exceptions. The AI cannot do these because they require account creation, billing credentials, and access to cloud dashboards that exist outside any CLI or MCP context.

#### Phase A: Account & Service Provisioning (Day 1 Morning)

| Step | Action | Output Artifact | How to Verify |
|------|--------|----------------|---------------|
| H-01 | **Create Supabase project** (production). Go to supabase.com → New Project. Region: closest to your users. Name: `jobapp-prod`. Save the generated password. | `SUPABASE_DB_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET` | Dashboard loads. Settings → API shows all keys. Settings → Database shows connection strings (use port 6543 for PgBouncer). |
| H-02 | **Create Supabase project** (staging). Same process. Name: `jobapp-staging`. | Same 5 variables for staging env | Separate dashboard from production. |
| H-03 | **Create Cloudflare R2 bucket.** Cloudflare Dashboard → R2 → Create Bucket → `jobapp-files`. Create an API token with read+write on this bucket. | `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_ENDPOINT_URL` | `aws s3 ls --endpoint-url https://<account_id>.r2.cloudflarestorage.com` returns empty bucket. |
| H-04 | **Provision AWS EC2 instances.** Via AWS Console or Terraform (if you prefer). Production: `t3.xlarge` (4 vCPU, 16GB). Staging: `t3.medium` (2 vCPU, 4GB). Both running Ubuntu 24.04. Install Docker + Docker Compose on each. | EC2 public IPs, SSH key pair `.pem` file | `ssh -i key.pem ubuntu@<ip>` connects. `docker --version` returns 24+. |
| H-05 | **Create Amazon ECR repository.** AWS Console → ECR → Create repo: `jobapp-backend`. | ECR repository URI | `aws ecr describe-repositories` shows `jobapp-backend`. |
| H-06 | **Create Sentry projects.** sentry.io → Create Project → `jobapp-backend` (Python/FastAPI). Create another → `jobapp-frontend` (Next.js). | `SENTRY_DSN` for backend, `NEXT_PUBLIC_SENTRY_DSN` for frontend | Sentry dashboard shows both projects with DSN strings. |
| H-07 | **Set up UptimeRobot.** uptimerobot.com → New Monitor → HTTP(s) → `https://api.yourdomain.com/api/v1/health` → 5-min interval. Add alert contact (email + Slack webhook). | UptimeRobot monitor ID | Dashboard shows monitor in "paused" state (will activate after first deployment). |
| H-08 | **Generate the master encryption key.** Run locally: `python3 -c "import secrets; print(secrets.token_hex(32))"`. Store the output securely (password manager). This key NEVER goes into any repo. | `MASTER_ENCRYPTION_KEY` (64 hex chars) | The string is 64 characters of hex (256 bits). |
| H-09 | **Configure your domain DNS.** Point `api.yourdomain.com` → production EC2 public IP (A record). Point `staging-api.yourdomain.com` → staging EC2 IP. Frontend domain is managed by Vercel automatically. | DNS A records | `dig api.yourdomain.com` resolves to EC2 IP. |

#### Phase B: Repository & Tooling Initialization (Day 1 Afternoon)

| Step | Action | Output Artifact | How to Verify |
|------|--------|----------------|---------------|
| H-10 | **Create 3 GitHub repositories.** `yourorg/jobapp-frontend`, `yourorg/jobapp-backend`, `yourorg/jobapp-infra`. All private. Enable branch protection on `main`: require PR reviews, require status checks to pass, no direct pushes. | 3 empty repos with branch protection | GitHub Settings → Branches shows protection rules on each repo. |
| H-11 | **Clone repos locally.** `git clone` all 3 into a workspace directory. Create root-level files: `Implementation_Tracker.md`, `Audit_Log.md`, `Bug_Reports/` directory. | Local workspace: `workspace/frontend/`, `workspace/backend/`, `workspace/infra/` | `ls workspace/` shows all 3 dirs + tracker files. |
| H-12 | **Install MCP servers.** Install globally: `npm install -g @modelcontextprotocol/server-postgres @modelcontextprotocol/server-github @modelcontextprotocol/server-filesystem`. Configure in Cursor settings: Postgres MCP → point to your Supabase staging DB URL. GitHub MCP → provide `GITHUB_TOKEN` (create a PAT with repo scope). Filesystem MCP → allow paths to your workspace. | MCP servers running in Cursor | Cursor → MCP panel shows 3 connected servers. Test: ask Cursor to "list tables in the database" → it should reply "no tables yet" (empty DB). |
| H-13 | **Create the `.env` files (REAL secrets).** Using `.env.example` from Part 3 Module 13 as template, fill in actual values from steps H-01 through H-08. Create `backend/.env` and `frontend/.env.local`. These are `.gitignore`d and NEVER committed. | `backend/.env`, `frontend/.env.local` | `cat backend/.env` shows all variables populated. `grep -r "sk-" backend/app/` returns zero matches (no hardcoded secrets). |
| H-14 | **Place `.cursorrules` files.** Copy the `.cursorrules` content from Part 3 Module 1 into each repo root. Create `.cursor/rules/backend-agent.md` and `.cursor/rules/frontend-agent.md` per the spec. | `.cursorrules` in each repo root, agent rules in `.cursor/rules/` | Open any file in Cursor → the agent rules appear in Cursor's context sidebar. |
| H-15 | **Create GitHub Actions secrets.** In each repo's Settings → Secrets, add: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `ECR_REGISTRY`, `STAGING_EC2_HOST`, `STAGING_SSH_KEY`, `PROD_EC2_HOST`, `PROD_SSH_KEY`, `SUPABASE_DB_URL_STAGING`, `SENTRY_DSN`. | GitHub Secrets configured | Settings → Secrets → Actions shows all variables (values masked). |
| H-16 | **Set up Slack #alerts channel.** Create a Slack channel. Configure incoming webhook URL. Add to Sentry alert rules + UptimeRobot alert contacts. | Slack webhook URL | Send test message to webhook URL → appears in #alerts channel. |

#### Phase C: Verify the Foundation (Day 1 End)

Run this checklist before handoff to AI:

```
□ Supabase project (staging) accessible — connection string works
□ Supabase project (production) accessible — connection string works
□ R2 bucket exists — AWS CLI can list it
□ EC2 instances SSH-accessible — Docker installed
□ ECR repository exists
□ Sentry projects exist — DSN strings available
□ All 3 GitHub repos created with branch protection
□ MCP servers connected in Cursor (Postgres, GitHub, Filesystem)
□ .env files created with real secrets (git-ignored)
□ .cursorrules placed in all repos
□ GitHub Actions secrets configured
□ Master encryption key generated and stored securely
□ DNS records pointing to EC2 instances
```

If any item fails, resolve it before proceeding. The AI agents assume all infrastructure exists.

---

### 1.2 The Handoff Protocol (How to Prompt the AI at Each Sprint Start)

#### The Universal Sprint Handoff Template

When starting a new sprint with Cursor Composer or Claude CLI, use this exact structure:

```
SYSTEM CONTEXT:
You are the principal developer for Job Application OS. 
Your stack: Next.js 14 (App Router) + FastAPI + Supabase (PostgreSQL) + SQLAlchemy + Celery + Redis.

PIN THESE FILES (always in context):
1. Implementation_Tracker.md (current project state)
2. Audit_Log.md (security and quality tracking)
3. .cursorrules (coding standards)

SPRINT CONTEXT:
We are executing Sprint {N}: {Sprint Title}.
Read Master_Implementation_Plan_Part2.md, section "SPRINT {N}" for the full task list.

CURRENT STATE:
{Paste the "Latest Changes" section from Implementation_Tracker.md}

YOUR ASSIGNMENT:
Execute Task {N.X}: {Task Name}
Follow the Atomic Agentic Pipeline (9 steps) for this task.
Begin by reading the Context Files listed in the task specification.
Write failing tests FIRST per the TDD mandate.
```

#### Sprint-Specific Handoff Details

| Sprint | Files to Pin (Beyond Universal 3) | Pre-Handoff Human Check |
|--------|----------------------------------|------------------------|
| Sprint 0, Tasks 0.1-0.3 | `Master_Implementation_Plan_Part1.md` (project tree section) | All cloud accounts provisioned, .env files created |
| Sprint 0, Tasks 0.4-0.5 | `Master_Implementation_Plan_Part1.md` (Section 2: DB Schemas) | Supabase staging DB accessible from local machine |
| Sprint 0, Tasks 0.6-0.7 | `Technical_Documentation_v1.0.md` (Sections 3.5, 6.2) | Redis running locally (`redis-cli ping` → PONG) |
| Sprint 0, Tasks 0.8-0.10 | `Technical_Documentation_v1.0.md` (Sections 3.7, 2.4) | Docker Compose starts all containers |
| Sprint 1, Tasks 1.1-1.3 | `Master_Implementation_Plan_Part1.md` (Section 4: API Contract, 4.1-4.2) + `backend/app/models/user.py` + `backend/app/models/profile.py` | Alembic migration applied, tables exist in staging DB |
| Sprint 1, Tasks 1.4-1.5 | `frontend/src/types/database.ts` + `frontend/src/lib/supabase.ts` | Backend auth endpoints running and testable via curl |
| Sprint 2, Tasks 2.1-2.3 | `Technical_Documentation_v1.0.md` (Modules F2, F3) + `backend/app/services/ai_proxy_service.py` | At least 1 valid AI provider key in .env for testing |
| Sprint 2, Tasks 2.4-2.6 | `Master_Implementation_Plan_Part1.md` (Section 4.3) + `frontend/src/types/jobs.ts` | Backend job endpoints running, seed data present |

---

### 1.3 The Review Gate (Human Code Review Checklist)

After the AI completes a task or group of tasks and pushes a branch, you MUST review before merging. Never blindly merge.

#### The 4-Layer Review

**Layer 1 — Automated Checks (must all be green before you even look)**
```
□ GitHub Actions CI passes (lint + type check + unit tests)
□ Test coverage has not dropped below threshold (60% MVP)
□ No new npm/pip audit vulnerabilities (critical or high)
```

**Layer 2 — Functional Correctness (does it work?)**
```
□ Pull the branch locally and run the application
□ Execute the task's verification step manually (from Part 2 task spec)
□ Test the happy path end-to-end (e.g., create a profile → verify in DB)
□ Test 2 edge cases (e.g., duplicate email signup, empty required field)
□ Test the error case (e.g., unauthorized access → correct error code)
□ If the task involves real-time: trigger a DB change → verify UI updates
```

**Layer 3 — Security & Architecture (does it follow the rules?)**
```
□ No secrets in code (grep for API keys, passwords, connection strings)
□ Every DB query includes user_id filter (no cross-tenant data leakage)
□ Pydantic schemas validate all inputs (no raw request.json() access)
□ Error responses use the standardized envelope (no raw exceptions)
□ New environment variables are documented in .env.example
□ Soft delete is used for user-facing entities (not hard delete)
□ No N+1 queries (check for selectinload/joinedload usage)
```

**Layer 4 — Quality & Consistency (does it match the standards?)**
```
□ Code follows the patterns in .cursorrules
□ File naming matches convention (snake_case backend, PascalCase components)
□ New components use shadcn/ui primitives where applicable
□ Commit messages are semantic (feat|fix|test|chore(scope): description)
□ Implementation_Tracker.md and Audit_Log.md are updated
□ OpenAPI docs include the new endpoint (check /docs)
```

**Merge Decision:**
- All 4 layers pass → **Merge to `develop`** (or `main` for Sprint 0)
- Layer 1 fails → **Block.** AI must fix CI before re-review.
- Layer 2 fails → **Block.** AI must fix the specific failing case.
- Layer 3 fails → **Block.** This is a security issue. Fix immediately.
- Layer 4 fails → **Soft block.** Can merge with follow-up ticket for cleanup.

---

### 1.4 Tasks Reserved Strictly for the Human

These tasks MUST NOT be delegated to AI agents, ever:

| Task | Reason |
|------|--------|
| Creating cloud accounts (Supabase, AWS, Cloudflare, Sentry) | Requires billing credentials and identity verification |
| Populating `.env` files with real secrets | AI must never see production credentials in chat context |
| Running `terraform apply` on production | Infrastructure mutation requires human confirmation |
| Running `alembic upgrade head` on production database | Schema changes to production require human verification |
| Merging to `main` branch | Code review gate is a human responsibility |
| Setting GitHub branch protection rules | Access control decisions are human-only |
| Approving and deploying to production | Final deployment decision is always human |
| Monitoring production health after deployment | AI can generate dashboards but humans watch them |
| Rotating secrets and encryption keys | Key management requires secure human handling |
| Responding to Sentry alerts in production | Incident response requires human judgment |
| Managing DNS records | Domain management affects availability |
| Configuring OAuth redirect URIs in Supabase | Affects auth flow for all users |

---

## 2. THE AI AGENT WORKFLOW (The Micro-Step Execution Loop)

---

This is the exhaustive, step-by-step loop the AI MUST follow for **every single task**. There is zero ambiguity. The AI agent reads this section as gospel.

### The 7-Step Execution Loop

---

#### STEP A: Context Ingestion (MANDATORY — Never Skip)

```
BEFORE writing any code, the AI MUST read these files IN THIS ORDER:

1. Implementation_Tracker.md
   → Understand: What sprint are we in? What was built last? What is the current state?
   
2. The task specification from Master_Implementation_Plan_Part2.md
   → Understand: What exactly needs to be built? What are the context files?

3. Each Context File listed in the task spec:
   → For backend tasks: the relevant SQLAlchemy model, Pydantic schema, existing service
   → For frontend tasks: the relevant TypeScript types, Zod validators, existing components
   → For both: the API Contract section in Part 1

4. The .cursorrules file
   → Understand: What patterns, conventions, and prohibitions apply?

5. Any existing test file for the module being modified
   → Understand: What tests already exist? What patterns do they use?

RULE: If the AI cannot find a Context File (e.g., the model doesn't exist yet), 
it must check if the file should be created as part of this task or a previous task. 
If a previous task was skipped, STOP and flag to the human.

OUTPUT OF THIS STEP: The AI should state:
"I've read [list of files]. Current state: [summary]. 
I'm now implementing Task X.Y: [name]. My plan is: [brief plan]."
```

---

#### STEP B: The TDD Mandate (Tests First — Always)

```
SEQUENCE:
1. Create or open the test file for this module
   → Backend: tests/unit/test_{module}.py or tests/integration/test_{module}_api.py
   → Frontend: tests/unit/{module}.test.ts

2. Write ALL test cases for the feature being built:
   → Happy path (the expected success case)
   → Validation failures (missing fields, wrong types, out-of-range values)
   → Authorization failures (wrong user, no token, expired token)
   → Edge cases (empty list, max pagination, duplicate creation)
   
   TEST NAMING CONVENTION:
   → Python: def test_{action}_{expected_outcome}():
   → TypeScript: it('should {action} when {condition}', () => {...})

3. RUN the tests and CONFIRM they FAIL:
   → Backend: pytest tests/unit/test_{module}.py -v --tb=short
   → Frontend: npx vitest run tests/unit/{module}.test.ts
   
   EXPECTED OUTPUT: All tests should show FAILED status.
   
   If ANY test passes BEFORE implementation, the test is wrong:
   → It's testing existing functionality (not the new feature)
   → It has no assertions (always passes)
   → It's importing from the wrong module
   → FIX THE TEST before proceeding.

4. DECLARE: "Written {N} tests. All {N} fail as expected. Proceeding to implementation."
```

---

#### STEP C: Implementation (Write Minimum Code to Pass Tests)

```
BACKEND IMPLEMENTATION ORDER:
1. Pydantic schemas (app/schemas/{module}.py)
   → Request models, Response models, validation rules
   
2. Service layer (app/services/{module}_service.py)
   → Business logic, database queries, external service calls
   → EVERY query MUST include: where(Model.user_id == current_user_id)
   → EVERY query MUST include: where(Model.is_deleted == False) for soft-deletable entities
   
3. API router (app/api/v1/{module}.py)
   → Thin controller: parse request → call service → return response
   → EVERY route MUST include response_model, summary, tags, responses
   → EVERY authenticated route MUST depend on get_current_user
   
4. Wire the router into app/api/v1/router.py

FRONTEND IMPLEMENTATION ORDER:
1. Types (src/types/{module}.ts) — if not already existing
2. Validators (src/lib/validators/{module}.ts) — Zod schemas
3. API hooks (custom hook or inline TanStack Query in component)
4. Component implementation
5. Page integration

CRITICAL RULES DURING IMPLEMENTATION:
→ Write the MINIMUM code to pass the tests. Do not over-engineer.
→ Do not add features not specified in the task.
→ Do not refactor unrelated code in the same task.
→ Do not modify any file not listed in the task's context files 
  (unless it's a barrel export or router aggregation).
```

---

#### STEP D: The Auto-Fixing & Debugging Loop

```
AFTER writing implementation code, RUN ALL TESTS:
→ Backend: pytest tests/ -v --tb=short (run ALL tests, not just new ones)
→ Frontend: npx vitest run (run ALL tests)

IF ALL TESTS PASS → Proceed to Step E.

IF ANY TEST FAILS → Enter the Debug Loop:

┌─────────────────────────────────────────────────────────┐
│                    DEBUG ITERATION 1                      │
├─────────────────────────────────────────────────────────┤
│ 1. READ the complete error output:                       │
│    → Full stack trace                                    │
│    → Assertion failure details (expected vs actual)      │
│    → File path and line number                           │
│                                                          │
│ 2. CATEGORIZE the error:                                 │
│    → ImportError: Check module path, __init__.py          │
│    → TypeError: Check Pydantic schema, TS interface      │
│    → AssertionError: Check test logic, mock data         │
│    → DatabaseError: Check model, migration, connection   │
│    → ValidationError: Check Pydantic/Zod schema          │
│    → 401/403: Check auth middleware, test auth headers   │
│    → 404: Check route registration, URL path             │
│    → 422: Check request payload matches schema           │
│                                                          │
│ 3. CROSS-REFERENCE with codebase:                        │
│    → Open the file at the error location                 │
│    → Read 20 lines above and below the error             │
│    → Check if the function signature matches the caller  │
│                                                          │
│ 4. IMPLEMENT a targeted fix (ONE change, not a rewrite)  │
│                                                          │
│ 5. RE-RUN the specific failing test only:                │
│    → pytest tests/unit/test_{module}.py::test_{name} -v  │
└─────────────────────────────────────────────────────────┘

IF STILL FAILING → Debug Iteration 2 (same process, different hypothesis)

IF STILL FAILING → Debug Iteration 3 (same process, last chance)

IF STILL FAILING AFTER 3 ITERATIONS → INVOKE THE 3-STRIKE RULE:

┌─────────────────────────────────────────────────────────┐
│               ⛔ 3-STRIKE RULE TRIGGERED                 │
├─────────────────────────────────────────────────────────┤
│ 1. STOP all implementation work immediately              │
│                                                          │
│ 2. CREATE file: Bug_Reports/BUG_{YYYY-MM-DD}_{desc}.md  │
│    Contents:                                             │
│    - ## Bug Description                                  │
│    - ## Task Context (Sprint, Task number, Goal)         │
│    - ## Error Output (full stack trace)                  │
│    - ## Attempt 1: What I tried + Why it failed          │
│    - ## Attempt 2: What I tried + Why it failed          │
│    - ## Attempt 3: What I tried + Why it failed          │
│    - ## Root Cause Hypothesis                            │
│    - ## Suggested Next Steps for Human                   │
│    - ## Files Modified (so human can review/revert)      │
│                                                          │
│ 3. UPDATE Audit_Log.md:                                  │
│    "[Date] [Sprint N] [BUG] Task N.X blocked.            │
│     See Bug_Reports/BUG_xxx.md. Awaiting human review."  │
│                                                          │
│ 4. OUTPUT to human:                                      │
│    "⛔ I've been unable to resolve this issue after 3     │
│    attempts. I've documented the bug in                   │
│    Bug_Reports/BUG_xxx.md with all details.              │
│    Please review and provide guidance before I continue." │
│                                                          │
│ 5. DO NOT proceed to the next task.                      │
│    DO NOT attempt a 4th fix.                             │
│    WAIT for human intervention.                          │
└─────────────────────────────────────────────────────────┘
```

---

#### STEP E: Security & Linting Audit

```
RUN THESE CHECKS IN ORDER. ALL must pass before committing.

BACKEND:
1. Linting:     ruff check . --fix
   → If any unfixable errors, resolve manually
   
2. Type check:  mypy . --ignore-missing-imports
   → Zero errors required
   
3. Security:    pip-audit
   → Zero critical or high vulnerabilities
   → If found: check if it's in a dev dependency. If prod: fix immediately.
   
4. Secrets:     grep -rn "sk-\|api_key.*=.*['\"]" app/ --include="*.py"
   → MUST return zero matches (no hardcoded secrets)
   
5. User isolation: grep -rn "\.query\|\.filter\|select(" app/services/ --include="*.py" 
   → Every query result should be near a user_id filter. Spot-check 3 queries.

FRONTEND:
1. Linting:     npx eslint . --fix
   → Zero errors required
   
2. Type check:  npx tsc --noEmit
   → Zero errors required
   
3. Security:    npm audit
   → Zero critical or high vulnerabilities
   
4. Secrets:     grep -rn "sk-\|api_key\|secret" src/ --include="*.ts" --include="*.tsx"
   → MUST return zero matches
   
5. Build test:  npm run build
   → Must succeed (catches SSR-breaking issues that lint/tsc miss)

IF ANY CHECK FAILS:
→ Fix the issue
→ Re-run the specific check
→ Do not proceed to Step F until all checks pass
```

---

#### STEP F: Documentation Sync

```
UPDATE BOTH tracker files. This is not optional.

1. Implementation_Tracker.md
   → Update "Current Project Phase" section
   → Add entry under "Latest Changes" with:
     - Task completed (e.g., "Task 1.1 — Auth API")
     - What was built (1-2 sentences)
     - Test count and pass rate
     - Any deviations from the plan

2. Audit_Log.md
   → Add entry in format:
     [YYYY-MM-DD] [Sprint N] [TYPE] Description
   → Types: SECURITY (for audits), COVERAGE (for test metrics),
     BUG_FIX (for bugs caught and fixed), PERFORMANCE (for perf checks)
   → Include current test coverage numbers:
     "Backend: XX% (Y/Z tests pass). Frontend: XX% (Y/Z tests pass)."
```

---

#### STEP G: Atomic Commit

```
STAGE only the files modified for THIS task. Never batch multiple tasks.

1. Review staged files:
   git status
   git diff --staged --stat
   
   → Verify: only files related to this task are staged
   → If unrelated files are modified: unstage them (git reset HEAD <file>)

2. Commit with semantic message:
   git commit -m "{type}({scope}): {description}

   Task {N.X} — Sprint {N}
   
   - {bullet 1: what was built}
   - {bullet 2: test results}
   - {bullet 3: any notable decisions}"

   TYPES: feat | fix | test | chore | docs | refactor | perf
   SCOPES: auth | profiles | jobs | scoring | content | review | applications |
           files | copilot | notifications | analytics | market | admin |
           settings | onboarding | shell | realtime | db | security | infra | ci

3. Push branch:
   git push origin feature/{task-name}

4. Announce to human:
   "✅ Task {N.X} complete. Branch: feature/{task-name}.
    Tests: {pass}/{total}. Coverage: {X}%.
    Ready for review."
```

---

## 3. THE STEP-BY-STEP SYNC MATRIX (First 3 Phases)

---

### PHASE 1: Foundation (Sprint 0) — Week 1

```
┌──────────────────────────────────────────────────────────────────────┐
│                         SPRINT 0 TIMELINE                             │
├────────┬─────────────────────────────────────────────────────────────┤
│  TRACK │  ACTIONS                                                     │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  H-01 through H-16: Provision all cloud services,           │
│ DAY 1  │  create repos, configure MCP servers, create .env files,     │
│ (solo) │  place .cursorrules. Run pre-flight checklist.              │
│        │                                                              │
│        │  OUTPUT: All 16 infrastructure items verified ✓               │
│        │  SIGNAL TO AI: "Infrastructure ready. Begin Sprint 0."       │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│   AI   │  Task 0.1: Initialize Backend Repository                     │
│ DAY 2  │  → Step A: Read project tree from Part 1                     │
│ (auto) │  → Step C: Create directory structure, pyproject.toml,       │
│        │    requirements.txt, Dockerfile, main.py, .env.example       │
│        │  → Step E: ruff check + docker build                        │
│        │  → Step G: commit "feat(backend): initialize project"        │
│        │                                                              │
│   AI   │  Task 0.2: Initialize Frontend Repository                    │
│        │  → Same loop: create-next-app, install deps, directory       │
│        │    structure, vitest + playwright configs                    │
│        │  → Step G: commit "feat(frontend): initialize project"       │
│        │                                                              │
│   AI   │  Task 0.3: Initialize Infrastructure Repository              │
│        │  → docker-compose.yml, Caddyfile, terraform scaffold,       │
│        │    GitHub Actions workflows, deploy scripts                  │
│        │  → Step G: commit "feat(infra): initialize config"           │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  REVIEW GATE #1:                                             │
│ DAY 2  │  □ Pull all 3 branches locally                               │
│ (sync) │  □ docker-compose -f docker-compose.dev.yml up → all         │
│        │    containers start                                          │
│        │  □ curl localhost:8000/docs → Swagger UI loads                │
│        │  □ npm run dev (frontend) → Next.js starts                   │
│        │  □ terraform validate → passes                               │
│        │  □ Merge all 3 to main                                       │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│   AI   │  Task 0.4: Database Setup (Models + Alembic)                 │
│ DAY 3  │  → Step A: Read ALL model specs from Part 1 Section 2        │
│ (auto) │  → Step C: Create 20 SQLAlchemy models + base mixins         │
│        │  → Step C: alembic init + configure + autogenerate migration │
│        │  → Step E: ruff check + mypy                                │
│        │  → Step G: commit "feat(db): create models and migration"    │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  SYNC POINT:                                                 │
│ DAY 3  │  □ Review the migration SQL (alembic/versions/*.py)          │
│ (sync) │  □ Verify all 20 tables + indexes in migration               │
│        │  □ Apply migration to staging: alembic upgrade head          │
│        │  □ Connect to staging DB: \dt → verify tables                │
│        │  □ Merge to main                                             │
│        │  SIGNAL: "Schema applied to staging. Continue."              │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│   AI   │  Task 0.5: Seed Script                                       │
│ DAY 3  │  → Create scripts/seed.py + scripts/teardown.py              │
│ (auto) │  → Run seed → verify data → run teardown → verify clean      │
│        │                                                              │
│   AI   │  Task 0.6: Core Middleware + Error Handling                   │
│ DAY 4  │  → Step B: Write 12+ tests (error envelope, rate limiter)   │
│ (auto) │  → Step B: Confirm all fail                                  │
│        │  → Step C: Implement exceptions, middleware, rate limiter    │
│        │  → Step D: Run tests → debug if needed                      │
│        │  → Step G: commit "feat(core): middleware + error handling"   │
│        │                                                              │
│   AI   │  Task 0.7: BYOK Encryption Module                            │
│        │  → Step B: Write 8 encryption tests                          │
│        │  → Step C: AES-256-GCM + HKDF implementation                │
│        │  → Step G: commit "feat(security): BYOK encryption"          │
│        │                                                              │
│   AI   │  Task 0.8: Celery + Redis Setup                              │
│ DAY 4  │  → Celery app factory, Redis pool, test task                 │
│ (auto) │  → Step G: commit "feat(tasks): Celery + Redis config"       │
│        │                                                              │
│   AI   │  Task 0.9: Supabase Realtime Integration                     │
│        │  → Frontend: supabase client, queryClient, realtimeManager   │
│        │  → Step G: commit "feat(realtime): Supabase Realtime setup"  │
│        │                                                              │
│   AI   │  Task 0.10: OpenAPI Auto-Documentation                       │
│        │  → Configure FastAPI metadata, tags, base schemas            │
│        │  → Step G: commit "feat(api): OpenAPI documentation"         │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  REVIEW GATE #2 (Sprint 0 Final):                            │
│ DAY 5  │  □ Run ALL tests: pytest tests/ -v → all pass                │
│ (sync) │  □ docker-compose up → all 6 containers healthy             │
│        │  □ curl localhost:8000/api/v1/health → all checks green      │
│        │  □ Seed database → verify with Postgres MCP                  │
│        │  □ Frontend connects to Supabase Realtime                    │
│        │  □ Check Audit_Log.md has entries for all tasks              │
│        │  □ Check Implementation_Tracker.md is current                │
│        │  □ Security spot-check: grep for hardcoded secrets           │
│        │  □ Merge all Sprint 0 work to main                          │
│        │  □ Tag: git tag v0.1.0-foundation                            │
│        │                                                              │
│        │  GENERATE Phase Summary (per Module 12):                     │
│        │  "Sprint 0 complete. 10 tasks. Foundation operational.       │
│        │   20 tables, 6 containers, middleware chain, encryption,     │
│        │   Realtime, OpenAPI. Test coverage: Backend 45%."            │
│        │                                                              │
│        │  FLUSH CONTEXT (if session is getting long):                 │
│        │  Start fresh session. Pin only:                              │
│        │  Implementation_Tracker.md, Audit_Log.md, .cursorrules,     │
│        │  Phase Summary for Sprint 0.                                 │
│        │                                                              │
└────────┴─────────────────────────────────────────────────────────────┘
```

---

### PHASE 2: Authentication & User Management (Sprint 1) — Week 2

```
┌──────────────────────────────────────────────────────────────────────┐
│                         SPRINT 1 TIMELINE                             │
├────────┬─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  PRE-SPRINT TASKS:                                           │
│ DAY 6  │  □ Configure Supabase Auth: enable email + Google OAuth     │
│ (solo) │  □ Set up Google OAuth credentials (console.cloud.google)   │
│        │  □ Add OAuth redirect URIs in Supabase dashboard:           │
│        │    - http://localhost:3000/auth/callback (dev)               │
│        │    - https://yourdomain.com/auth/callback (prod)            │
│        │  □ Verify: Supabase Auth → can create test user via API     │
│        │  □ Add GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET to .env       │
│        │                                                              │
│        │  HANDOFF: Use Sprint Handoff Template with Sprint 1 context │
│        │  Pin: Implementation_Tracker, Audit_Log, .cursorrules,      │
│        │  Part 1 API Contract (Sections 4.1, 4.2),                   │
│        │  backend/app/models/user.py, backend/app/models/profile.py  │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│   AI   │  Task 1.1: Auth API (Signup + Login + JWT)                   │
│ DAY 6  │  → Step A: Read user model, auth schema, API contract 4.1   │
│ (auto) │  → Step B: Write 7 integration tests (test_auth_api.py):    │
│        │    - test_signup_success                                     │
│        │    - test_signup_duplicate_email → 409                       │
│        │    - test_login_success                                      │
│        │    - test_login_wrong_password → 401                         │
│        │    - test_get_me_authenticated                               │
│        │    - test_get_me_unauthenticated → 401                       │
│        │    - test_token_refresh                                      │
│        │  → Step B: Run tests → all 7 fail ✓                         │
│        │  → Step C: Implement schemas, service, router               │
│        │  → Step D: Run tests → debug if needed                      │
│        │  → Step E: ruff + mypy + pip-audit + secrets check          │
│        │  → Step F: Update trackers                                   │
│        │  → Step G: commit "feat(auth): signup, login, JWT"           │
│        │                                                              │
│   AI   │  Task 1.2: Profile CRUD API                                  │
│ DAY 7  │  → Step B: Write 9 integration tests:                       │
│ (auto) │    - test_create_profile                                     │
│        │    - test_list_profiles (returns only user's profiles)       │
│        │    - test_get_profile                                        │
│        │    - test_update_profile                                     │
│        │    - test_delete_profile (soft delete)                       │
│        │    - test_clone_profile                                      │
│        │    - test_activate_profile                                   │
│        │    - test_completeness_calculation                           │
│        │    - test_user_isolation (user A ≠ user B)                   │
│        │  → Full loop (Steps A through G)                            │
│        │                                                              │
│   AI   │  Task 1.3: Skills, Experience, Education CRUD                │
│ DAY 7  │  → Sub-resource routes under /profiles/:id/                  │
│ (auto) │  → Batch import endpoint for skills                         │
│        │  → Full loop (Steps A through G)                            │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  MID-SPRINT REVIEW GATE:                                     │
│ DAY 7  │  □ Pull backend branch                                       │
│ (sync) │  □ pytest tests/ -v → all pass                               │
│        │  □ Test auth manually:                                       │
│        │    curl -X POST localhost:8000/api/v1/auth/signup ...        │
│        │    → Verify user in Supabase dashboard                      │
│        │    curl -H "Authorization: Bearer <jwt>" .../api/v1/auth/me │
│        │    → Returns user data                                       │
│        │  □ Test profile isolation:                                   │
│        │    Create profile as user A → GET as user B → 404            │
│        │  □ Check OpenAPI: /docs shows all new endpoints              │
│        │  □ Merge backend work to develop                             │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│   AI   │  Task 1.4: Frontend Auth Pages + Zustand Store               │
│ DAY 8  │  → Step B: Write Vitest tests for authStore                  │
│ (auto) │  → Step C: Zustand store, login/signup pages,               │
│        │    auth middleware (redirect logic)                          │
│        │  → Full loop (Steps A through G)                            │
│        │                                                              │
│   AI   │  Task 1.5: App Shell (Sidebar + Topbar + Layout)             │
│ DAY 9  │  → Step C: AppShell, Sidebar, Topbar, ProfileSwitcher,      │
│ (auto) │    MobileNav, next-themes integration                       │
│        │  → Full loop (Steps A through G)                            │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  SPRINT 1 FINAL REVIEW GATE:                                 │
│ DAY 10 │  □ Run ALL backend tests → pass                              │
│ (sync) │  □ Run ALL frontend tests → pass                             │
│        │  □ Full E2E manual test:                                     │
│        │    Signup → Email verify → Login → See dashboard shell       │
│        │    → Sidebar renders → Profile switcher works                │
│        │    → Dark/light mode toggles → Responsive at 3 breakpoints  │
│        │  □ Security: no secrets, user isolation verified             │
│        │  □ Merge all Sprint 1 to main                               │
│        │  □ Tag: git tag v0.2.0-auth                                  │
│        │                                                              │
│        │  GENERATE Phase Summary. FLUSH context if needed.            │
│        │                                                              │
└────────┴─────────────────────────────────────────────────────────────┘
```

---

### PHASE 3: Job Discovery & Scoring (Sprint 2) — Weeks 3-4

```
┌──────────────────────────────────────────────────────────────────────┐
│                         SPRINT 2 TIMELINE                             │
├────────┬─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  PRE-SPRINT TASKS:                                           │
│ DAY 11 │  □ Ensure at least 1 real AI provider key in .env            │
│ (solo) │    (Anthropic recommended — for testing scoring + content)   │
│        │  □ Verify Celery worker is running (docker-compose logs      │
│        │    celery-worker → shows "ready")                            │
│        │  □ Verify Redis is accessible (redis-cli ping → PONG)       │
│        │  □ Run seed script to populate 100 test jobs                 │
│        │  □ Verify Supabase Realtime is connected (check frontend     │
│        │    console for "Realtime connected" log)                    │
│        │                                                              │
│        │  HANDOFF: Pin Part 1 API Contract (Section 4.3),             │
│        │  Technical Documentation Modules F2 + F3,                    │
│        │  backend/app/models/job.py, backend/app/models/raw_job.py,  │
│        │  backend/app/services/ai_proxy_service.py (if exists)       │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│   AI   │  Task 2.1: Discovery Pipeline (Scraping + Dedup)             │
│ DAY 11 │  → Step B: Write 8 tests:                                    │
│ (auto) │    - test_normalize_job_data                                 │
│        │    - test_dedup_hash_generation (same job = same hash)       │
│        │    - test_dedup_merges_sources                               │
│        │    - test_discovery_creates_jobs                              │
│        │    - test_discovery_updates_progress (tasks table)           │
│        │    - test_duplicate_job_from_2_sources_creates_1_job         │
│        │    - test_job_sources_junction_populated                     │
│        │    - test_raw_jobs_preserved_after_merge                     │
│        │  → Full loop (Steps A through G)                            │
│        │                                                              │
│   AI   │  Task 2.2: Scoring Engine (8 Dimensions)                     │
│ DAY 12 │  → Step B: Write 12 tests for scoring logic                  │
│ (auto) │  → Step C: Implement scoring_service.py                     │
│        │  → Step G: commit "feat(scoring): 8-dimension scoring"       │
│        │                                                              │
│   AI   │  Task 2.3: AI Proxy Service                                  │
│ DAY 13 │  → Step B: Write 10 tests (provider selection, circuit      │
│ (auto) │    breaker, fallback, cost tracking)                         │
│        │  → Step C: Implement ai_proxy_service.py +                  │
│        │    circuit_breaker.py                                        │
│        │  → This task may trigger the 3-Strike Rule if AI provider   │
│        │    API mocking is complex — THAT'S OK, follow the protocol  │
│        │  → Step G: commit "feat(ai): AI proxy with circuit breaker"  │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  MID-SPRINT REVIEW GATE:                                     │
│ DAY 13 │  □ Run ALL backend tests → pass                              │
│ (sync) │  □ Manual: trigger scoring on a seeded job → verify score    │
│        │    breakdown has 8 dimensions in DB                          │
│        │  □ Manual: trigger discovery → verify raw_jobs + jobs +     │
│        │    job_sources populated correctly                           │
│        │  □ Test circuit breaker: simulate provider failure →         │
│        │    verify circuit opens after 5 failures                    │
│        │  □ Review Bug_Reports/ — any 3-Strike reports?              │
│        │  □ Merge backend to develop                                  │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│   AI   │  Task 2.4: Jobs API Endpoints                                │
│ DAY 14 │  → Step B: Write 11 integration tests                       │
│ (auto) │  → Step C: Implement all endpoints from API contract 4.3    │
│        │  → Step G: commit "feat(jobs-api): all job endpoints"        │
│        │                                                              │
│   AI   │  Task 2.5: Job Browser UI                                    │
│ DAY 15 │  → Virtualized list, 15 filter dimensions, card/table views │
│ (auto) │  → TanStack Query with cursor pagination                    │
│        │  → Real-time score badge updates                            │
│        │  → Step G: commit "feat(job-browser): Job Browser UI"        │
│        │                                                              │
│   AI   │  Task 2.6: Job Detail Page (7 Tabs)                          │
│ DAY 17 │  → CRM-style tabbed view with error boundaries              │
│ (auto) │  → Step G: commit "feat(job-detail): 7-tab Job Detail"       │
│        │                                                              │
├────────┼─────────────────────────────────────────────────────────────┤
│        │                                                              │
│ HUMAN  │  SPRINT 2 FINAL REVIEW GATE:                                 │
│ DAY 18 │  □ Run ALL tests (backend + frontend) → pass                 │
│ (sync) │  □ Full E2E manual test:                                     │
│        │    Login → Trigger discovery → Jobs appear in browser →     │
│        │    Filter by score ≥80 → Shows correct subset →             │
│        │    Click job → 7 tabs render → Score breakdown chart shows  │
│        │    → Change status → Kanban updates                         │
│        │  □ Performance: Job Browser loads 500 seeded jobs in <2s     │
│        │  □ Real-time: score a job from backend → badge updates      │
│        │    in browser without page refresh                          │
│        │  □ Coverage check: Backend ≥60%, Frontend ≥40%               │
│        │  □ Security audit (Module 8 checklist)                      │
│        │  □ Merge all Sprint 2 to main                               │
│        │  □ Tag: git tag v0.3.0-discovery-scoring                     │
│        │                                                              │
│        │  GENERATE Phase Summary. FLUSH context.                      │
│        │  Deploy to staging: docker-compose pull && up -d             │
│        │  Run health check against staging.                          │
│        │                                                              │
└────────┴─────────────────────────────────────────────────────────────┘
```

---

## APPENDIX: Quick Reference Cards

### Human Quick Reference: "What Do I Do Right Now?"

```
IF starting a new sprint:
  → Complete the PRE-SPRINT human tasks for that sprint
  → Use the Handoff Template to prompt the AI
  → Pin the correct context files

IF AI is working autonomously:
  → Monitor for 3-Strike Bug Reports in Bug_Reports/
  → Check Audit_Log.md periodically for anomalies
  → Be available for questions (AI will ask via bug reports)

IF AI signals task completion:
  → Pull the branch
  → Run the 4-Layer Review Gate
  → Merge or block with specific feedback

IF AI hits a 3-Strike:
  → Read the Bug_Report.md
  → Diagnose the root cause
  → Provide guidance (paste into next prompt)
  → AI resumes from where it stopped

IF a sprint is complete:
  → Run full test suite
  → Run security audit
  → Merge to main + tag
  → Generate Phase Summary
  → Deploy to staging
  → Run health check
  → Flush context for next sprint
```

### AI Quick Reference: "What Do I Do Right Now?"

```
FOR EVERY TASK:
  A → Read: Tracker + Task Spec + Context Files + .cursorrules
  B → Test: Write ALL tests FIRST → Run → Confirm they FAIL
  C → Code: Write MINIMUM code to pass tests
  D → Fix:  If tests fail → Debug Loop (max 3 strikes)
  E → Lint: ruff/mypy/eslint/tsc/audit/secrets check
  F → Docs: Update Implementation_Tracker.md + Audit_Log.md
  G → Git:  Stage → Commit (semantic) → Push → Announce

NEVER:
  → Skip Step A (context reading)
  → Skip Step B (writing tests first)
  → Batch multiple tasks in one commit
  → Hardcode secrets
  → Push directly to main
  → Continue past a 3-Strike without human input
  → Modify files outside the task scope
```

---

> **This playbook is now the operating manual.** Both tracks (Human and AI) reference this document at every step. No improvisation. No shortcuts. Execute the plan.
