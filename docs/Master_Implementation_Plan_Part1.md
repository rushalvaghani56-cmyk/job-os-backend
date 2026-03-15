# MASTER IMPLEMENTATION PLAN — Part 1: Core Architecture & Data Contracts

> **Version:** 1.0 | **Date:** March 13, 2026 | **Status:** APPROVED
>
> **Source Documents:** Technical Documentation v1.0 + Product Spec v2.3 COMBINED FINAL
>
> **Stack Alignment Note:** This plan aligns with the LOCKED technical decisions: Next.js 14 (App Router) + Python FastAPI + Supabase (PostgreSQL) + SQLAlchemy + Celery + Redis. All Blueprint references to "MERN" have been translated to the actual stack.

---

## 1. THE MASTER PROJECT TREE

```
jobapp-os/
├── README.md
├── Implementation_Tracker.md
├── Audit_Log.md
├── Bug_Reports/
│   └── .gitkeep
│
├── ──────────────────────────────────────────
│   FRONTEND REPOSITORY (frontend/)
│   ──────────────────────────────────────────
├── frontend/
│   ├── .cursorrules
│   ├── .cursor/
│   │   └── rules/
│   │       ├── frontend-agent.md
│   │       └── component-patterns.md
│   ├── .env.example
│   ├── .env.local                          # git-ignored
│   ├── .eslintrc.json
│   ├── .prettierrc
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── vitest.config.ts
│   ├── playwright.config.ts
│   ├── package.json
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── assets/
│   │       └── images/
│   │
│   ├── src/
│   │   ├── app/                            # Next.js App Router
│   │   │   ├── layout.tsx                  # Root layout (providers, theme, sidebar)
│   │   │   ├── loading.tsx                 # Global loading skeleton
│   │   │   ├── error.tsx                   # Root error boundary
│   │   │   ├── not-found.tsx
│   │   │   │
│   │   │   ├── (public)/                   # Public route group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx                # Landing page
│   │   │   │   ├── auth/
│   │   │   │   │   ├── login/page.tsx
│   │   │   │   │   ├── signup/page.tsx
│   │   │   │   │   ├── forgot-password/page.tsx
│   │   │   │   │   └── verify-email/page.tsx
│   │   │   │   └── status/page.tsx         # Public status page
│   │   │   │
│   │   │   ├── (onboarding)/               # Onboarding route group
│   │   │   │   ├── layout.tsx
│   │   │   │   └── onboarding/
│   │   │   │       ├── page.tsx            # Redirects to step-1
│   │   │   │       ├── step-1/page.tsx     # Profile basics
│   │   │   │       ├── step-2/page.tsx     # Import data
│   │   │   │       ├── step-3/page.tsx     # Deep profile
│   │   │   │       ├── step-4/page.tsx     # Master resumes
│   │   │   │       └── step-5/page.tsx     # AI keys
│   │   │   │
│   │   │   ├── (dashboard)/                # Core app route group
│   │   │   │   ├── layout.tsx              # App shell: sidebar + topbar + content
│   │   │   │   ├── home/page.tsx           # Dashboard Home (Command Center)
│   │   │   │   ├── jobs/
│   │   │   │   │   ├── page.tsx            # Job Browser
│   │   │   │   │   └── [jobId]/
│   │   │   │   │       ├── page.tsx        # Job Detail (7 tabs)
│   │   │   │   │       └── loading.tsx
│   │   │   │   ├── review/page.tsx         # Review Queue
│   │   │   │   ├── applications/page.tsx   # Application Tracker (Kanban/Table/Calendar)
│   │   │   │   ├── notifications/page.tsx  # Notification Center
│   │   │   │   └── changelog/page.tsx      # What's New
│   │   │   │
│   │   │   ├── (outreach)/                 # Outreach route group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── outreach/page.tsx       # Outreach Hub
│   │   │   │   └── email/page.tsx          # Email Intelligence Hub
│   │   │   │
│   │   │   ├── (analytics)/                # Analytics route group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── analytics/page.tsx      # Analytics Dashboard (9 tabs)
│   │   │   │   └── market/page.tsx         # Market Intelligence Dashboard
│   │   │   │
│   │   │   ├── (interviews)/               # Interviews route group
│   │   │   │   ├── layout.tsx
│   │   │   │   └── interviews/page.tsx     # Interview Calendar
│   │   │   │
│   │   │   ├── (settings)/                 # Settings route group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── settings/
│   │   │   │   │   ├── page.tsx            # Settings Hub (9 tabs)
│   │   │   │   │   └── [tab]/page.tsx      # Dynamic tab routing
│   │   │   │   ├── profiles/page.tsx       # Profile Manager
│   │   │   │   ├── files/page.tsx          # File Manager
│   │   │   │   └── activity/page.tsx       # Activity Log
│   │   │   │
│   │   │   └── (admin)/                    # Admin route group
│   │   │       ├── layout.tsx
│   │   │       └── admin/page.tsx          # Super Admin Panel
│   │   │
│   │   ├── components/
│   │   │   ├── ui/                         # shadcn/ui components (auto-generated)
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── dropdown-menu.tsx
│   │   │   │   ├── command.tsx             # Command Palette base
│   │   │   │   ├── toast.tsx               # Sonner wrapper
│   │   │   │   └── ...                     # All shadcn primitives
│   │   │   │
│   │   │   ├── layout/
│   │   │   │   ├── AppShell.tsx            # Main layout: sidebar + topbar + content
│   │   │   │   ├── Sidebar.tsx             # Left sidebar (260px, collapsible)
│   │   │   │   ├── SidebarItem.tsx         # Nav item with badge
│   │   │   │   ├── Topbar.tsx              # Global search + profile + bell + copilot btn
│   │   │   │   ├── ProfileSwitcher.tsx     # Top-bar profile dropdown
│   │   │   │   └── MobileNav.tsx           # Bottom nav for mobile
│   │   │   │
│   │   │   ├── copilot/
│   │   │   │   ├── CopilotPanel.tsx        # Resizable side panel
│   │   │   │   ├── CopilotChat.tsx         # Chat interface
│   │   │   │   ├── CopilotMessage.tsx      # Single message bubble
│   │   │   │   ├── CopilotSuggestionCard.tsx
│   │   │   │   └── SlashCommandInput.tsx   # Slash command handler
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── StatsRow.tsx            # 4 stat cards
│   │   │   │   ├── ActionRequiredPanel.tsx
│   │   │   │   ├── CopilotPreview.tsx      # Mini widget
│   │   │   │   ├── DiscoveryStatus.tsx
│   │   │   │   ├── GoalProgress.tsx
│   │   │   │   ├── RecentActivity.tsx
│   │   │   │   └── QuickActions.tsx
│   │   │   │
│   │   │   ├── jobs/
│   │   │   │   ├── JobBrowser.tsx          # Main browser component
│   │   │   │   ├── JobCard.tsx             # Card view item
│   │   │   │   ├── JobRow.tsx              # Table view item
│   │   │   │   ├── JobFilterSidebar.tsx    # 15+ filter dimensions
│   │   │   │   ├── JobScoreBadge.tsx       # Color-coded score
│   │   │   │   ├── JobDetail/
│   │   │   │   │   ├── JobDetailHeader.tsx
│   │   │   │   │   ├── OverviewTab.tsx
│   │   │   │   │   ├── DocumentsTab.tsx
│   │   │   │   │   ├── TimelineTab.tsx
│   │   │   │   │   ├── AnalyticsTab.tsx
│   │   │   │   │   ├── CompanyTab.tsx
│   │   │   │   │   ├── OutreachTab.tsx
│   │   │   │   │   └── CopilotTab.tsx
│   │   │   │   └── SavedSearches.tsx
│   │   │   │
│   │   │   ├── review/
│   │   │   │   ├── ReviewQueue.tsx         # Split panel
│   │   │   │   ├── ReviewQueueList.tsx     # Left 40%
│   │   │   │   ├── ReviewQueueItem.tsx
│   │   │   │   ├── ResumeReview.tsx        # Right 60% - resume detail
│   │   │   │   ├── CoverLetterReview.tsx
│   │   │   │   ├── OutreachReview.tsx
│   │   │   │   ├── AnswerReview.tsx
│   │   │   │   ├── VariantTabs.tsx         # 2-variant switcher
│   │   │   │   ├── ContentQualityScore.tsx
│   │   │   │   └── DiffViewer.tsx          # Green/yellow diff highlights
│   │   │   │
│   │   │   ├── applications/
│   │   │   │   ├── KanbanBoard.tsx         # @dnd-kit drag-and-drop
│   │   │   │   ├── KanbanColumn.tsx
│   │   │   │   ├── KanbanCard.tsx
│   │   │   │   ├── ApplicationTable.tsx    # Table view
│   │   │   │   ├── ApplicationCalendar.tsx # Calendar view
│   │   │   │   └── ViewToggle.tsx
│   │   │   │
│   │   │   ├── analytics/
│   │   │   │   ├── FunnelChart.tsx         # D3 Sankey
│   │   │   │   ├── SourcesChart.tsx        # Recharts bar
│   │   │   │   ├── RejectionsHeatmap.tsx
│   │   │   │   ├── AICostChart.tsx
│   │   │   │   ├── SkillsDemandChart.tsx
│   │   │   │   ├── ABTestResults.tsx
│   │   │   │   ├── GoalsTracker.tsx
│   │   │   │   ├── TimingChart.tsx
│   │   │   │   └── WeeklyReport.tsx
│   │   │   │
│   │   │   ├── profiles/
│   │   │   │   ├── ProfileCard.tsx
│   │   │   │   ├── ProfileEditor.tsx       # Full 65+ field editor
│   │   │   │   ├── CompletenessRing.tsx
│   │   │   │   └── ProfileComparison.tsx
│   │   │   │
│   │   │   ├── settings/
│   │   │   │   ├── GeneralSettings.tsx
│   │   │   │   ├── AIModelSettings.tsx
│   │   │   │   ├── APIKeySettings.tsx
│   │   │   │   ├── AutomationSettings.tsx
│   │   │   │   ├── ScoringSettings.tsx
│   │   │   │   ├── SourceSettings.tsx
│   │   │   │   ├── ScheduleSettings.tsx
│   │   │   │   ├── EmailSettings.tsx
│   │   │   │   └── FeatureFlagSettings.tsx
│   │   │   │
│   │   │   ├── onboarding/
│   │   │   │   ├── OnboardingWizard.tsx
│   │   │   │   ├── ProfileBasicsStep.tsx
│   │   │   │   ├── ImportDataStep.tsx
│   │   │   │   ├── DeepProfileStep.tsx
│   │   │   │   ├── MasterResumeStep.tsx
│   │   │   │   └── AIKeysStep.tsx
│   │   │   │
│   │   │   └── shared/
│   │   │       ├── ErrorBoundary.tsx       # Route-level + section-level
│   │   │       ├── SectionErrorBoundary.tsx
│   │   │       ├── LoadingSkeleton.tsx
│   │   │       ├── EmptyState.tsx
│   │   │       ├── ConfirmDialog.tsx
│   │   │       ├── UndoToast.tsx           # 5-min / 30-sec undo
│   │   │       ├── CommandPalette.tsx       # Cmd+K
│   │   │       ├── KeyboardShortcuts.tsx
│   │   │       ├── NotificationBell.tsx
│   │   │       ├── FileUploader.tsx         # Presigned URL upload
│   │   │       └── PDFViewer.tsx            # react-pdf wrapper
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts                  # Supabase auth hook
│   │   │   ├── useProfile.ts               # Active profile context
│   │   │   ├── useRealtime.ts              # Supabase Realtime subscription
│   │   │   ├── useCopilot.ts               # Copilot panel state + actions
│   │   │   ├── useKeyboardShortcuts.ts
│   │   │   ├── useOptimisticMutation.ts    # TanStack optimistic wrapper
│   │   │   ├── useDebounce.ts
│   │   │   ├── useMediaQuery.ts            # Responsive breakpoints
│   │   │   └── useFileUpload.ts            # Presigned URL flow
│   │   │
│   │   ├── stores/
│   │   │   ├── authStore.ts                # Zustand: auth state
│   │   │   ├── profileStore.ts             # Zustand: active profile
│   │   │   ├── copilotStore.ts             # Zustand: panel open/width
│   │   │   ├── uiStore.ts                  # Zustand: theme, sidebar, transient UI
│   │   │   └── commandPaletteStore.ts
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts                      # Axios/fetch instance with auth headers
│   │   │   ├── supabase.ts                 # Supabase client (browser)
│   │   │   ├── supabase-server.ts          # Supabase client (server component)
│   │   │   ├── queryClient.ts              # TanStack Query client config
│   │   │   ├── queryKeys.ts                # Centralized query key factory
│   │   │   ├── realtimeManager.ts          # Supabase Realtime → invalidate queries
│   │   │   ├── validators/                 # Shared Zod schemas
│   │   │   │   ├── auth.ts
│   │   │   │   ├── profile.ts
│   │   │   │   ├── job.ts
│   │   │   │   ├── application.ts
│   │   │   │   ├── review.ts
│   │   │   │   ├── settings.ts
│   │   │   │   └── index.ts
│   │   │   ├── utils.ts                    # General utilities
│   │   │   ├── constants.ts                # App-wide constants
│   │   │   └── cn.ts                       # Tailwind class merge utility
│   │   │
│   │   ├── types/
│   │   │   ├── api.ts                      # API response/request types
│   │   │   ├── database.ts                 # Database entity types
│   │   │   ├── jobs.ts
│   │   │   ├── profiles.ts
│   │   │   ├── applications.ts
│   │   │   ├── review.ts
│   │   │   ├── outreach.ts
│   │   │   ├── analytics.ts
│   │   │   ├── copilot.ts
│   │   │   ├── notifications.ts
│   │   │   ├── settings.ts
│   │   │   └── index.ts                    # Barrel export
│   │   │
│   │   └── styles/
│   │       └── globals.css                 # Tailwind base + custom CSS vars
│   │
│   └── tests/
│       ├── unit/                           # Vitest unit tests
│       │   ├── components/
│       │   ├── hooks/
│       │   └── stores/
│       ├── integration/                    # API integration tests
│       └── e2e/                            # Playwright E2E tests
│           ├── signup.spec.ts
│           ├── onboarding.spec.ts
│           ├── discovery.spec.ts
│           ├── review.spec.ts
│           └── apply.spec.ts
│
├── ──────────────────────────────────────────
│   BACKEND REPOSITORY (backend/)
│   ──────────────────────────────────────────
├── backend/
│   ├── .cursorrules
│   ├── .cursor/
│   │   └── rules/
│   │       ├── backend-agent.md
│   │       └── api-patterns.md
│   ├── .env.example
│   ├── .env                                # git-ignored
│   ├── pyproject.toml                      # Python project config (ruff, mypy, pytest)
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── alembic.ini
│   │
│   ├── alembic/                            # Database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── .gitkeep
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                         # FastAPI app factory + middleware
│   │   ├── config.py                       # Settings from environment
│   │   ├── dependencies.py                 # Shared FastAPI dependencies
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py                 # JWT verification, BYOK encryption (AES-256-GCM)
│   │   │   ├── middleware.py               # CORS, rate limiter, auth, logging
│   │   │   ├── exceptions.py               # Standardized error envelope + codes
│   │   │   ├── rate_limiter.py             # Redis-based per-user rate limiting
│   │   │   ├── circuit_breaker.py          # Per-service circuit breaker via Redis
│   │   │   └── logging.py                  # Loguru structured JSON setup
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py                  # SQLAlchemy async engine + session factory
│   │   │   ├── base.py                     # Declarative base + common mixins
│   │   │   └── redis.py                    # Redis connection pool
│   │   │
│   │   ├── models/                         # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── profile.py
│   │   │   ├── skill.py
│   │   │   ├── work_experience.py
│   │   │   ├── education.py
│   │   │   ├── achievement.py
│   │   │   ├── project.py
│   │   │   ├── raw_job.py
│   │   │   ├── job.py
│   │   │   ├── job_source.py
│   │   │   ├── application.py
│   │   │   ├── document.py
│   │   │   ├── review_queue.py
│   │   │   ├── outreach_contact.py
│   │   │   ├── outreach_message.py
│   │   │   ├── interview.py
│   │   │   ├── notification.py
│   │   │   ├── activity_log.py
│   │   │   ├── task.py
│   │   │   ├── failed_task.py
│   │   │   ├── api_key.py
│   │   │   └── copilot_conversation.py
│   │   │
│   │   ├── schemas/                        # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── common.py                   # Pagination, error envelope, base schemas
│   │   │   ├── auth.py
│   │   │   ├── profile.py
│   │   │   ├── job.py
│   │   │   ├── application.py
│   │   │   ├── review.py
│   │   │   ├── outreach.py
│   │   │   ├── email.py
│   │   │   ├── interview.py
│   │   │   ├── analytics.py
│   │   │   ├── market.py
│   │   │   ├── ai.py
│   │   │   ├── file.py
│   │   │   ├── copilot.py
│   │   │   ├── notification.py
│   │   │   └── admin.py
│   │   │
│   │   ├── api/                            # FastAPI routers (one per module)
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py               # Aggregates all v1 routers
│   │   │   │   ├── auth.py
│   │   │   │   ├── profiles.py
│   │   │   │   ├── jobs.py
│   │   │   │   ├── content.py
│   │   │   │   ├── applications.py
│   │   │   │   ├── review.py
│   │   │   │   ├── outreach.py
│   │   │   │   ├── email.py
│   │   │   │   ├── interviews.py
│   │   │   │   ├── analytics.py
│   │   │   │   ├── market.py
│   │   │   │   ├── ai.py
│   │   │   │   ├── files.py
│   │   │   │   ├── copilot.py
│   │   │   │   ├── notifications.py
│   │   │   │   ├── admin.py
│   │   │   │   └── health.py
│   │   │   └── deps.py                     # Route-level dependencies (get_current_user, etc.)
│   │   │
│   │   ├── services/                       # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── profile_service.py
│   │   │   ├── job_service.py
│   │   │   ├── scoring_service.py
│   │   │   ├── content_service.py
│   │   │   ├── application_service.py
│   │   │   ├── review_service.py
│   │   │   ├── outreach_service.py
│   │   │   ├── email_service.py
│   │   │   ├── interview_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── market_service.py
│   │   │   ├── ai_proxy_service.py
│   │   │   ├── file_service.py
│   │   │   ├── copilot_service.py
│   │   │   ├── notification_service.py
│   │   │   └── admin_service.py
│   │   │
│   │   └── tasks/                          # Celery task definitions
│   │       ├── __init__.py
│   │       ├── celery_app.py               # Celery application factory
│   │       ├── discovery_tasks.py          # Job scraping + normalization + dedup
│   │       ├── scoring_tasks.py            # AI scoring (8 dimensions)
│   │       ├── content_tasks.py            # Resume/CL generation + QA
│   │       ├── application_tasks.py        # ATS auto-fill via Playwright
│   │       ├── outreach_tasks.py           # Recruiter discovery + messaging
│   │       ├── email_tasks.py              # Gmail scan + send
│   │       ├── analytics_tasks.py          # Compute aggregations → Redis cache
│   │       ├── market_tasks.py             # Market intelligence computation
│   │       └── scheduled_tasks.py          # Celery beat schedule definitions
│   │
│   ├── scripts/
│   │   ├── seed.py                         # Database seeding with Faker
│   │   ├── teardown.py                     # Test database cleanup
│   │   └── backup.py                       # Weekly pg_dump to R2
│   │
│   └── tests/
│       ├── conftest.py                     # Shared fixtures (test DB, mock AI, etc.)
│       ├── unit/
│       │   ├── test_scoring_engine.py
│       │   ├── test_dedup_algorithm.py
│       │   ├── test_content_generation.py
│       │   ├── test_circuit_breaker.py
│       │   └── test_encryption.py
│       ├── integration/
│       │   ├── test_auth_api.py
│       │   ├── test_profiles_api.py
│       │   ├── test_jobs_api.py
│       │   ├── test_applications_api.py
│       │   ├── test_review_api.py
│       │   └── test_health_api.py
│       └── tasks/
│           ├── test_discovery_tasks.py
│           ├── test_scoring_tasks.py
│           └── test_content_tasks.py
│
├── ──────────────────────────────────────────
│   INFRASTRUCTURE REPOSITORY (infra/)
│   ──────────────────────────────────────────
├── infra/
│   ├── .cursorrules
│   ├── docker-compose.yml                  # Production compose (all services)
│   ├── docker-compose.dev.yml              # Local dev override
│   ├── docker-compose.staging.yml
│   │
│   ├── docker/
│   │   ├── fastapi/
│   │   │   └── Dockerfile
│   │   ├── celery/
│   │   │   └── Dockerfile
│   │   ├── playwright/
│   │   │   └── Dockerfile
│   │   └── caddy/
│   │       └── Caddyfile
│   │
│   ├── terraform/
│   │   ├── main.tf                         # AWS provider + backend config
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── ec2.tf                          # EC2 instances (prod + staging)
│   │   ├── security_groups.tf
│   │   ├── iam.tf
│   │   ├── ecr.tf                          # Container registry
│   │   └── terraform.tfvars.example
│   │
│   ├── github-actions/
│   │   ├── ci-backend.yml                  # Lint + type + unit tests
│   │   ├── ci-frontend.yml                 # Lint + type + unit tests
│   │   ├── deploy-staging.yml              # Build → push ECR → SSH restart
│   │   ├── deploy-production.yml           # Manual trigger → rolling deploy
│   │   └── e2e-nightly.yml                 # Playwright against staging
│   │
│   └── scripts/
│       ├── deploy.sh                       # EC2 rolling deploy script
│       ├── health-check.sh                 # Post-deploy health verification
│       └── backup-cron.sh                  # Weekly pg_dump trigger
```

---

## 2. DATABASE SCHEMAS (SQLAlchemy Models)

### 2.1 Base Model & Mixins

```python
# backend/app/db/base.py

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Auto-managed created_at and updated_at."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """Soft delete for user-facing entities."""
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )


class UUIDPrimaryKeyMixin:
    """UUID primary key for all tables."""
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
```

### 2.2 Core Models

```python
# backend/app/models/user.py

from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin

import enum

class UserRole(str, enum.Enum):
    USER = "user"
    SUPER_ADMIN = "super_admin"


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), default=UserRole.USER, nullable=False
    )
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    supabase_uid: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    # Relationships
    profiles = relationship("Profile", back_populates="user", lazy="selectin")
    api_keys = relationship("APIKey", back_populates="user", lazy="selectin")
    notifications = relationship("Notification", back_populates="user")
```

```python
# backend/app/models/profile.py

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin

import uuid


class Profile(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_role: Mapped[str] = mapped_column(String(255), nullable=False)
    target_seniority: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target_employment_types: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    target_locations: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    negative_locations: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    years_of_experience: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    completeness_pct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Deep profile fields
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    social_urls: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    work_authorization: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    languages: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    work_preferences: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    notice_period: Mapped[str | None] = mapped_column(String(100), nullable=True)
    availability_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    writing_tones: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    custom_fields: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    ai_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio_snippet: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Scoring & automation config (per-profile)
    scoring_weights: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    automation_config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    discovery_config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    dream_companies: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    blacklist: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    # Relationships
    user = relationship("User", back_populates="profiles")
    jobs = relationship("Job", back_populates="profile")
    applications = relationship("Application", back_populates="profile")
```

```python
# backend/app/models/job.py

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin

import uuid


class Job(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "jobs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False
    )

    # Core fields
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    seniority: Mapped[str | None] = mapped_column(String(100), nullable=True)
    employment_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    apply_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    ats_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    posted_date: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Salary
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    salary_estimated: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Scoring
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_breakdown: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    decision: Mapped[str | None] = mapped_column(String(20), nullable=True)  # auto_apply / review / skip
    decision_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Skills analysis
    skills_required: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    skills_preferred: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    skills_matched: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    skills_missing: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    # Status
    status: Mapped[str] = mapped_column(
        String(30), default="new", nullable=False
    )  # new, scored, content_ready, applied, interview, offer, rejected, skipped, bookmarked, ghosted

    # Company intel (JSONB blob)
    company_intel: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Full-text search vector
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)

    # Relationships
    profile = relationship("Profile", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
    documents = relationship("Document", back_populates="job")
    sources = relationship("JobSource", back_populates="job")

    __table_args__ = (
        Index("ix_jobs_user_score", "user_id", "is_deleted", score.desc()),
        Index("ix_jobs_user_status", "user_id", "status"),
        Index("ix_jobs_user_created", "user_id", "created_at".desc()),
        Index("ix_jobs_search", "search_vector", postgresql_using="gin"),
    )
```

```python
# backend/app/models/raw_job.py

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin

class RawJob(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raw_jobs"

    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    dedup_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    raw_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    normalized_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    normalized_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    normalized_location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    sources = relationship("JobSource", back_populates="raw_job")
```

```python
# backend/app/models/job_source.py

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin
from datetime import datetime
import uuid

class JobSource(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "job_sources"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False
    )
    raw_job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raw_jobs.id"), nullable=False
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    job = relationship("Job", back_populates="sources")
    raw_job = relationship("RawJob", back_populates="sources")
```

```python
# backend/app/models/application.py

from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin
from datetime import datetime
import uuid


class Application(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "applications"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), default="pending", nullable=False
    )  # pending, submitted, screening, interview, offer, rejected, withdrawn, ghosted
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    submission_method: Mapped[str | None] = mapped_column(String(50), nullable=True)  # auto, manual, easy_apply
    submission_screenshot_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ats_debug_log: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    job = relationship("Job", back_populates="applications")
    profile = relationship("Profile", back_populates="applications")
    documents = relationship("Document", back_populates="application")
    interviews = relationship("Interview", back_populates="application")

    __table_args__ = (
        Index("ix_applications_user_status", "user_id", "status", "updated_at"),
    )
```

```python
# backend/app/models/document.py

from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
import uuid


class Document(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "documents"

    job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=True
    )
    application_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("applications.id"), nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True
    )
    type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # resume_v1, resume_v2, cover_letter, answer, screenshot, prep_pack, thank_you, outreach_draft, master_resume, template
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    r2_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    quality_score: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1-100
    quality_breakdown: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    qa_report: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    variant_label: Mapped[str | None] = mapped_column(String(50), nullable=True)  # A or B
    template_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    job = relationship("Job", back_populates="documents")
    application = relationship("Application", back_populates="documents")
```

```python
# backend/app/models/review_queue.py

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
import uuid


class ReviewQueue(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "review_queue"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    item_type: Mapped[str] = mapped_column(
        String(30), nullable=False
    )  # resume, cover_letter, outreach, answer, email
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=True
    )
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)  # 1=dream, 2=high, 3=medium
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )  # pending, approved, rejected
    reject_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        Index("ix_review_queue_user_priority", "user_id", "priority", "created_at"),
    )
```

```python
# backend/app/models/notification.py

from sqlalchemy import String, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
import uuid


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(
        String(10), default="medium", nullable=False
    )  # critical, high, medium, low
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    action_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    user = relationship("User", back_populates="notifications")
```

```python
# backend/app/models/activity_log.py

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
import uuid


class ActivityLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "activity_log"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    actor: Mapped[str] = mapped_column(
        String(20), default="system", nullable=False
    )  # system, user, ai
    entity_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    detail: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index("ix_activity_log_user_created", "user_id", "created_at".desc()),
        Index("ix_activity_log_user_action", "user_id", "action"),
    )
```

```python
# backend/app/models/api_key.py

from sqlalchemy import String, ForeignKey, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from datetime import datetime
import uuid


class APIKey(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "api_keys"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    provider: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # anthropic, openai, google
    encrypted_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    key_nonce: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    key_tag: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False
    )  # active, invalid, expired
    last_validated: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user = relationship("User", back_populates="api_keys")
```

```python
# backend/app/models/task.py

from sqlalchemy import String, Integer, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
import uuid


class Task(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "tasks"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    task_name: Mapped[str] = mapped_column(String(100), nullable=False)
    celery_task_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )  # pending, running, completed, failed
    progress_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class FailedTask(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "failed_tasks"

    task_name: Mapped[str] = mapped_column(String(100), nullable=False)
    celery_task_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    args: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error: Mapped[str] = mapped_column(Text, nullable=False)
    traceback: Mapped[str | None] = mapped_column(Text, nullable=True)
```

### 2.3 Additional Models (Condensed)

```python
# backend/app/models/skill.py
class Skill(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "skills"
    user_id: Mapped[uuid.UUID]  # FK → users.id
    name: Mapped[str]           # String(200)
    category: Mapped[str]       # String(50): language/framework/cloud/database/tool/domain/methodology/soft_skill
    proficiency: Mapped[int]    # 1-5 (aware → expert)
    years_used: Mapped[float | None]
    last_used_date: Mapped[str | None]
    want_to_use: Mapped[bool]   # default=True
    currently_learning: Mapped[bool]  # default=False
    context: Mapped[str | None] # Text

# backend/app/models/work_experience.py
class WorkExperience(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "work_experience"
    user_id: Mapped[uuid.UUID]
    company: Mapped[str]        # String(255)
    title: Mapped[str]          # String(255)
    start_date: Mapped[str]     # String(20)
    end_date: Mapped[str | None]
    is_current: Mapped[bool]
    location: Mapped[str | None]
    work_type: Mapped[str | None]  # remote/hybrid/onsite
    description: Mapped[str | None]  # Text
    key_achievement: Mapped[str | None]
    tech_stack: Mapped[list]    # JSONB

# backend/app/models/education.py
class Education(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "education"
    user_id: Mapped[uuid.UUID]
    institution: Mapped[str]
    degree: Mapped[str | None]
    field: Mapped[str | None]
    start_date: Mapped[str | None]
    end_date: Mapped[str | None]
    gpa: Mapped[float | None]
    show_gpa: Mapped[bool]      # default=False

# backend/app/models/outreach_contact.py
class OutreachContact(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "outreach_contacts"
    user_id: Mapped[uuid.UUID]
    job_id: Mapped[uuid.UUID | None]
    name: Mapped[str]
    title: Mapped[str | None]
    company: Mapped[str | None]
    linkedin_url: Mapped[str | None]
    email: Mapped[str | None]
    channel: Mapped[str]        # linkedin_dm, linkedin_inmail, email
    warmth: Mapped[str]         # cold, warm, hot
    status: Mapped[str]         # draft, queued, sent, replied, no_response, do_not_contact

# backend/app/models/outreach_message.py
class OutreachMessage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "outreach_messages"
    contact_id: Mapped[uuid.UUID]  # FK → outreach_contacts.id
    content: Mapped[str]        # Text
    channel: Mapped[str]
    status: Mapped[str]         # draft, queued, sent, opened, replied
    sent_at: Mapped[datetime | None]
    opened_at: Mapped[datetime | None]
    replied_at: Mapped[datetime | None]
    is_follow_up: Mapped[bool]
    follow_up_number: Mapped[int | None]

# backend/app/models/interview.py
class Interview(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "interviews"
    application_id: Mapped[uuid.UUID]  # FK → applications.id
    user_id: Mapped[uuid.UUID]
    round_type: Mapped[str]     # phone_screen, technical, system_design, hiring_manager, final, culture_fit
    scheduled_at: Mapped[datetime | None]
    platform: Mapped[str | None]  # zoom, meet, teams
    meeting_link: Mapped[str | None]
    interviewer_name: Mapped[str | None]
    interviewer_title: Mapped[str | None]
    interviewer_linkedin: Mapped[str | None]
    prep_pack_doc_id: Mapped[uuid.UUID | None]
    outcome: Mapped[str | None]  # passed, failed, pending
    difficulty_rating: Mapped[int | None]  # 1-5
    performance_rating: Mapped[int | None]  # 1-5
    questions_asked: Mapped[str | None]  # Text
    notes: Mapped[str | None]
    next_steps: Mapped[str | None]

# backend/app/models/copilot_conversation.py
class CopilotConversation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "copilot_conversations"
    user_id: Mapped[uuid.UUID]
    messages: Mapped[list]      # JSONB: [{role, content, timestamp}]
    context: Mapped[dict | None]  # JSONB: {page, job_id, profile_id, ...}
    model_used: Mapped[str | None]
```

---

## 3. CORE TYPESCRIPT INTERFACES (Frontend)

```typescript
// frontend/src/types/database.ts

// ─── Base Types ───

export type UUID = string;

export interface Timestamps {
  created_at: string;  // ISO 8601
  updated_at: string;
}

export interface SoftDeletable {
  is_deleted: boolean;
  deleted_at: string | null;
}

// ─── User ───

export type UserRole = "user" | "super_admin";

export interface User extends Timestamps {
  id: UUID;
  email: string;
  role: UserRole;
  full_name: string | null;
  avatar_url: string | null;
  timezone: string;
  settings: Record<string, unknown>;
  supabase_uid: string;
}

// ─── Profile ───

export interface Profile extends Timestamps, SoftDeletable {
  id: UUID;
  user_id: UUID;
  name: string;
  target_role: string;
  target_seniority: string | null;
  target_employment_types: string[];
  target_locations: LocationTarget[];
  negative_locations: string[];
  years_of_experience: number | null;
  current_title: string | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string;
  is_active: boolean;
  completeness_pct: number;
  linkedin_url: string | null;
  github_url: string | null;
  portfolio_url: string | null;
  social_urls: Record<string, string>;
  work_authorization: WorkAuthorization[];
  languages: Language[];
  work_preferences: WorkPreferences;
  notice_period: string | null;
  availability_date: string | null;
  writing_tones: WritingTones;
  custom_fields: Record<string, string>;
  ai_instructions: string | null;
  bio_snippet: string | null;
  scoring_weights: ScoringWeights;
  automation_config: AutomationConfig;
  discovery_config: DiscoveryConfig;
  dream_companies: string[];
  blacklist: string[];
}

export interface LocationTarget {
  type: "remote" | "remote_tz" | "hybrid_flex" | "hybrid_fixed" | "onsite";
  city?: string;
  country?: string;
  timezone?: string;
}

export interface WorkAuthorization {
  country: string;
  status: "citizen" | "permanent_resident" | "work_visa" | "need_sponsorship" | "not_authorized";
  visa_type?: string;
  expiry_date?: string;
  sponsorship_details?: string;
}

export interface Language {
  language: string;
  proficiency: "native" | "fluent" | "professional" | "conversational" | "basic";
  certification?: string;
}

export interface WorkPreferences {
  remote_priority: string[];
  company_size: string[];
  company_stage: string[];
  industry: string[];
  management_interest: string;
  deal_breakers: string[];
  pace?: string;
  team_size?: string;
  values?: string[];
}

export interface WritingTones {
  resume: string;
  cover_letter: string;
  outreach: string;
}

export interface ScoringWeights {
  skill: number;       // default 30
  title: number;       // default 20
  seniority: number;   // default 15
  location: number;    // default 10
  salary: number;      // default 10
  company: number;     // default 8
  culture: number;     // default 4
  freshness: number;   // default 3
}

export interface AutomationConfig {
  auto_apply_enabled: boolean;
  score_threshold: number;
  confidence_threshold: number;
  risk_threshold: number;
  cooldown_minutes: number;
  daily_application_limit: number;
  daily_outreach_limit: number;
  daily_easy_apply_limit: number;
  operating_mode: "manual" | "approval" | "auto";
  platform_preference: string[];
}

export interface DiscoveryConfig {
  keywords_per_source: Record<string, string[]>;
  locations_per_source: Record<string, string[]>;
  sources_enabled: string[];
  freshness_days: number;
  cron_schedule: string;
  custom_career_pages: string[];
}

// ─── Job ───

export type JobStatus =
  | "new" | "scored" | "content_ready" | "applied"
  | "interview" | "offer" | "rejected" | "skipped"
  | "bookmarked" | "ghosted";

export type JobDecision = "auto_apply" | "review" | "skip";

export interface Job extends Timestamps, SoftDeletable {
  id: UUID;
  user_id: UUID;
  profile_id: UUID;
  title: string;
  company: string;
  location: string | null;
  location_type: string | null;
  seniority: string | null;
  employment_type: string | null;
  description: string | null;
  apply_url: string | null;
  ats_type: string | null;
  posted_date: string | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string | null;
  salary_estimated: boolean;
  score: number | null;
  score_breakdown: ScoreBreakdown | null;
  confidence: number | null;
  risk_score: number | null;
  decision: JobDecision | null;
  decision_reasoning: string | null;
  skills_required: string[];
  skills_preferred: string[];
  skills_matched: string[];
  skills_missing: string[];
  status: JobStatus;
  company_intel: CompanyIntel | null;
}

export interface ScoreBreakdown {
  skill: number;
  title: number;
  seniority: number;
  location: number;
  salary: number;
  company: number;
  culture: number;
  freshness: number;
  bonus: number;
  total: number;
}

export interface CompanyIntel {
  description?: string;
  industry?: string;
  size?: string;
  stage?: string;
  hq_location?: string;
  founded?: string;
  funding?: FundingInfo;
  culture?: CultureInfo;
  tech_stack?: string[];
  news?: NewsItem[];
  health_signals?: HealthSignals;
}

// ─── Application ───

export type ApplicationStatus =
  | "pending" | "submitted" | "screening" | "interview"
  | "offer" | "rejected" | "withdrawn" | "ghosted";

export interface Application extends Timestamps, SoftDeletable {
  id: UUID;
  job_id: UUID;
  user_id: UUID;
  profile_id: UUID;
  status: ApplicationStatus;
  submitted_at: string | null;
  submission_method: string | null;
  submission_screenshot_key: string | null;
  ats_debug_log: Record<string, unknown> | null;
  notes: string | null;
  job?: Job;  // Populated via join
}

// ─── API Response Types ───

export interface PaginatedResponse<T> {
  data: T[];
  next_cursor: string | null;
  has_more: boolean;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: FieldError[];
  };
}

export interface FieldError {
  field: string;
  message: string;
}

// ─── Notification ───

export type NotificationPriority = "critical" | "high" | "medium" | "low";

export interface Notification extends Timestamps {
  id: UUID;
  user_id: UUID;
  type: string;
  priority: NotificationPriority;
  title: string;
  body: string | null;
  read: boolean;
  action_url: string | null;
  metadata: Record<string, unknown> | null;
}
```

---

## 4. THE API CONTRACT

### 4.1 Authentication

| Method | Path | Auth | Request Body | Response (200) | Error Codes |
|--------|------|------|-------------|----------------|-------------|
| POST | /api/v1/auth/signup | No | `{ email, password, full_name? }` | `{ user: User, session: Session }` | 422, 409 |
| POST | /api/v1/auth/login | No | `{ email, password }` | `{ user: User, session: Session }` | 401, 422 |
| POST | /api/v1/auth/logout | Yes | — | `{ success: true }` | 401 |
| POST | /api/v1/auth/refresh | Yes | `{ refresh_token }` | `{ session: Session }` | 401 |
| GET | /api/v1/auth/me | Yes | — | `{ user: User }` | 401 |

### 4.2 Profiles

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/profiles | Yes | — | `{ data: Profile[] }` | 401 |
| POST | /api/v1/profiles | Yes | `ProfileCreate` | `{ data: Profile }` | 401, 422 |
| GET | /api/v1/profiles/:id | Yes | — | `{ data: Profile }` | 401, 404 |
| PUT | /api/v1/profiles/:id | Yes | `ProfileUpdate` | `{ data: Profile }` | 401, 404, 422 |
| DELETE | /api/v1/profiles/:id | Yes | — | `{ success: true }` | 401, 404 |
| POST | /api/v1/profiles/:id/clone | Yes | `{ name, data_types[] }` | `{ data: Profile }` | 401, 404 |
| PUT | /api/v1/profiles/:id/activate | Yes | — | `{ data: Profile }` | 401, 404 |
| GET | /api/v1/profiles/:id/completeness | Yes | — | `{ pct, missing_items[] }` | 401, 404 |

### 4.3 Jobs

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/jobs | Yes | Query: `cursor, limit, sort, filters[]` | `PaginatedResponse<Job>` | 401 |
| GET | /api/v1/jobs/:id | Yes | — | `{ data: Job }` | 401, 404 |
| POST | /api/v1/jobs/manual | Yes | `{ url?, raw_text?, profile_id }` | `{ data: Job }` | 401, 422 |
| PUT | /api/v1/jobs/:id/status | Yes | `{ status }` | `{ data: Job }` | 401, 404, 422 |
| POST | /api/v1/jobs/:id/bookmark | Yes | — | `{ data: Job }` | 401, 404 |
| POST | /api/v1/jobs/:id/skip | Yes | — | `{ data: Job }` | 401, 404 |
| POST | /api/v1/jobs/:id/score | Yes | — | `{ task_id }` | 401, 404 |
| POST | /api/v1/jobs/:id/generate | Yes | `{ instructions? }` | `{ task_id }` | 401, 404 |
| POST | /api/v1/jobs/bulk-score | Yes | `{ job_ids[] }` | `{ task_id }` | 401, 422 |
| GET | /api/v1/jobs/search | Yes | Query: `q, limit` | `{ data: Job[] }` | 401 |
| POST | /api/v1/jobs/discover | Yes | `{ profile_id }` | `{ task_id }` | 401, 422 |

### 4.4 Content Generation

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| POST | /api/v1/content/generate-resume | Yes | `{ job_id, profile_id, instructions? }` | `{ task_id }` | 401, 404, 422 |
| POST | /api/v1/content/generate-cover-letter | Yes | `{ job_id, profile_id }` | `{ task_id }` | 401, 404, 422 |
| POST | /api/v1/content/generate-answers | Yes | `{ job_id, questions[] }` | `{ task_id }` | 401, 422 |
| POST | /api/v1/content/regenerate | Yes | `{ document_id, instructions }` | `{ task_id }` | 401, 404 |

### 4.5 Applications

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/applications | Yes | Query: `cursor, limit, status, profile_id` | `PaginatedResponse<Application>` | 401 |
| GET | /api/v1/applications/:id | Yes | — | `{ data: Application }` | 401, 404 |
| POST | /api/v1/applications/:id/submit | Yes | — | `{ task_id }` | 401, 404, 409 |
| POST | /api/v1/applications/:id/mark-applied | Yes | `{ method, notes? }` | `{ data: Application }` | 401, 404 |
| PUT | /api/v1/applications/:id/status | Yes | `{ status }` | `{ data: Application }` | 401, 404, 422 |
| POST | /api/v1/applications/:id/undo | Yes | — | `{ data: Application }` | 401, 404, 409 |

### 4.6 Review Queue

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/review | Yes | Query: `cursor, limit, type_filter` | `PaginatedResponse<ReviewQueueItem>` | 401 |
| GET | /api/v1/review/:id | Yes | — | `{ data: ReviewQueueItemDetail }` | 401, 404 |
| POST | /api/v1/review/:id/approve | Yes | `{ edited_content? }` | `{ data: ReviewQueueItem }` | 401, 404 |
| POST | /api/v1/review/:id/reject | Yes | `{ reason }` | `{ data: ReviewQueueItem }` | 401, 404, 422 |
| POST | /api/v1/review/:id/regenerate | Yes | `{ instructions }` | `{ task_id }` | 401, 404 |
| POST | /api/v1/review/bulk-approve | Yes | `{ item_ids[] }` | `{ approved: number }` | 401, 422 |

### 4.7 Files

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| POST | /api/v1/files/presign-upload | Yes | `{ filename, content_type, job_id? }` | `{ upload_url, file_key }` | 401, 422 |
| POST | /api/v1/files/confirm-upload | Yes | `{ file_key, filename, size, content_type, job_id? }` | `{ data: Document }` | 401, 422 |
| GET | /api/v1/files/:id/download-url | Yes | — | `{ url: string }` | 401, 404 |
| GET | /api/v1/files | Yes | Query: `job_id?, type?` | `{ data: Document[] }` | 401 |
| DELETE | /api/v1/files/:id | Yes | — | `{ success: true }` | 401, 404 |

### 4.8 AI Provider Management

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/ai/keys | Yes | — | `{ data: APIKeyInfo[] }` (masked) | 401 |
| POST | /api/v1/ai/keys | Yes | `{ provider, api_key }` | `{ data: APIKeyInfo }` | 401, 422, 400 |
| DELETE | /api/v1/ai/keys/:id | Yes | — | `{ success: true }` | 401, 404 |
| POST | /api/v1/ai/keys/:id/validate | Yes | — | `{ valid: boolean, error? }` | 401, 404 |
| GET | /api/v1/ai/models | Yes | — | `{ data: ModelConfig[] }` | 401 |
| PUT | /api/v1/ai/models | Yes | `{ task_model_map }` | `{ data: ModelConfig[] }` | 401, 422 |
| GET | /api/v1/ai/usage | Yes | Query: `period` | `{ data: UsageStats }` | 401 |

### 4.9 Copilot

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| POST | /api/v1/copilot/chat | Yes | `{ message, context?, conversation_id? }` | SSE stream | 401, 422, 504 |
| GET | /api/v1/copilot/conversations | Yes | — | `{ data: Conversation[] }` | 401 |
| DELETE | /api/v1/copilot/conversations/:id | Yes | — | `{ success: true }` | 401, 404 |
| POST | /api/v1/copilot/execute | Yes | `{ action, params, confirmation_token }` | `{ task_id? , result? }` | 401, 422 |

### 4.10 Notifications

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/notifications | Yes | Query: `cursor, limit, priority?, unread_only?` | `PaginatedResponse<Notification>` | 401 |
| PUT | /api/v1/notifications/:id/read | Yes | — | `{ data: Notification }` | 401, 404 |
| PUT | /api/v1/notifications/read-all | Yes | — | `{ updated: number }` | 401 |
| GET | /api/v1/notifications/unread-count | Yes | — | `{ count: number }` | 401 |

### 4.11 Analytics

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/analytics/funnel | Yes | Query: `period, profile_id?` | `{ data: FunnelData }` | 401 |
| GET | /api/v1/analytics/sources | Yes | Query: `period, profile_id?` | `{ data: SourceStats[] }` | 401 |
| GET | /api/v1/analytics/rejections | Yes | Query: `period` | `{ data: RejectionStats }` | 401 |
| GET | /api/v1/analytics/ai-cost | Yes | Query: `period` | `{ data: AICostStats }` | 401 |
| GET | /api/v1/analytics/dashboard-stats | Yes | — | `{ data: DashboardStats }` | 401 |
| GET | /api/v1/analytics/weekly-report | Yes | Query: `week?` | `{ data: WeeklyReport }` | 401 |
| POST | /api/v1/analytics/export | Yes | `{ type, period, format }` | File download | 401, 422 |

### 4.12 Health

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/health | No | — | `{ status, checks: {...}, version, uptime }` | 500 |

### 4.13 Admin (Super Admin Only)

| Method | Path | Auth | Request Body | Response | Error Codes |
|--------|------|------|-------------|----------|-------------|
| GET | /api/v1/admin/users | Admin | Query: `cursor, limit, search` | `PaginatedResponse<AdminUser>` | 401, 403 |
| GET | /api/v1/admin/users/:id | Admin | — | `{ data: AdminUserDetail }` | 401, 403, 404 |
| PUT | /api/v1/admin/users/:id/role | Admin | `{ role }` | `{ data: AdminUser }` | 401, 403, 404 |
| PUT | /api/v1/admin/users/:id/suspend | Admin | `{ reason }` | `{ data: AdminUser }` | 401, 403, 404 |
| GET | /api/v1/admin/system-health | Admin | — | `{ data: SystemHealth }` | 401, 403 |
| GET | /api/v1/admin/feature-flags | Admin | — | `{ data: FeatureFlags }` | 401, 403 |
| PUT | /api/v1/admin/feature-flags | Admin | `{ flags }` | `{ data: FeatureFlags }` | 401, 403, 422 |

---

> **End of Part 1.** Part 2 (Agentic Sprint Roadmap) and Part 3 (MCP & Infrastructure Preparation + All 15 Blueprint Modules) follow as separate deliverables due to their size.
