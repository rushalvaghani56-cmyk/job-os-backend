# UI/UX DESIGN BLUEPRINT — Job Application OS

> **Version:** 1.0 | **Date:** March 13, 2026 | **Status:** READY FOR UI GENERATION
>
> **Purpose:** Translate the Technical Documentation into exact v0/Stitch prompts for consistent, production-quality UI generation across all 21 pages.
>
> **Stack:** Next.js 14 (App Router) + shadcn/ui + Tailwind CSS + Radix Primitives + Recharts + D3 Sankey + @dnd-kit + Tiptap + react-pdf + Sonner

---

## PART 1: THE GLOBAL DESIGN SYSTEM (Tokens)

---

### 1.1 Color Palette

#### Light Mode

| Token | Hex | Tailwind Variable | Usage |
|-------|-----|-------------------|-------|
| **Primary** | `#6366F1` | `--primary` | Action buttons, active nav, links, score highlights, focus rings |
| **Primary Hover** | `#4F46E5` | `--primary-hover` | Button hover, link hover |
| **Primary Muted** | `#EEF2FF` | `--primary-muted` | Selected row backgrounds, tag backgrounds, subtle highlights |
| **Secondary** | `#8B5CF6` | `--secondary` | AI/Copilot accent, dream company badges, premium features |
| **Background** | `#FFFFFF` | `--background` | Page background |
| **Surface** | `#F8FAFC` | `--surface` | Card backgrounds, sidebar background, panel backgrounds |
| **Surface Raised** | `#F1F5F9` | `--surface-raised` | Hover states on surface, filter sidebar, table header |
| **Border** | `#E2E8F0` | `--border` | Card borders, dividers, input borders |
| **Border Subtle** | `#F1F5F9` | `--border-subtle` | Inner dividers, separator lines |
| **Text Primary** | `#0F172A` | `--text-primary` | Headings, body text, primary labels |
| **Text Secondary** | `#64748B` | `--text-secondary` | Descriptions, timestamps, helper text |
| **Text Muted** | `#94A3B8` | `--text-muted` | Placeholders, disabled text, footnotes |
| **Success** | `#10B981` | `--success` | Matched skills, applied status, healthy service, green scores |
| **Success Muted** | `#D1FAE5` | `--success-muted` | Success backgrounds |
| **Warning** | `#F59E0B` | `--warning` | Review needed, warm outreach, medium confidence |
| **Warning Muted** | `#FEF3C7` | `--warning-muted` | Warning backgrounds |
| **Error** | `#EF4444` | `--error` | Missing skills, failed submissions, critical alerts, delete actions |
| **Error Muted** | `#FEE2E2` | `--error-muted` | Error backgrounds |
| **Info** | `#3B82F6` | `--info` | Cold outreach, informational badges |

#### Dark Mode

| Token | Hex | Usage |
|-------|-----|-------|
| **Primary** | `#818CF8` | Slightly lighter indigo for dark backgrounds |
| **Background** | `#0B0F1A` | Deep navy-black |
| **Surface** | `#111827` | Card/panel backgrounds |
| **Surface Raised** | `#1E293B` | Hover states, sidebars |
| **Border** | `#1E293B` | Subtle borders |
| **Text Primary** | `#F1F5F9` | Main text |
| **Text Secondary** | `#94A3B8` | Secondary text |
| **Text Muted** | `#64748B` | Muted text |

#### Score Badge Colors (Both Modes)

| Score Range | Color | Badge Style |
|-------------|-------|-------------|
| 85–100 | `#10B981` (Green) | Solid green bg, white text |
| 70–84 | `#3B82F6` (Blue) | Solid blue bg, white text |
| 60–69 | `#F59E0B` (Amber) | Solid amber bg, dark text |
| Below 60 | `#94A3B8` (Gray) | Subtle gray bg, gray text |
| Dream Company | `#8B5CF6` (Purple) | Purple border + star icon |

---

### 1.2 Typography

**Font Family:** `Geist Sans` (primary), `Geist Mono` (code blocks, technical data)

| Level | Element | Tailwind Class | Size | Weight | Line Height |
|-------|---------|---------------|------|--------|-------------|
| Display | Hero headlines | `text-4xl md:text-5xl` | 36–48px | `font-bold` | `leading-tight` |
| H1 | Page titles | `text-2xl` | 24px | `font-semibold` | `leading-8` |
| H2 | Section headers | `text-xl` | 20px | `font-semibold` | `leading-7` |
| H3 | Card titles, tab labels | `text-base` | 16px | `font-medium` | `leading-6` |
| Body | Paragraphs, descriptions | `text-sm` | 14px | `font-normal` | `leading-5` |
| Caption | Timestamps, helper text | `text-xs` | 12px | `font-normal` | `leading-4` |
| Mono | Scores, counts, code | `font-mono text-sm` | 14px | `font-medium` | `leading-5` |

---

### 1.3 Spacing, Radius & Shadows

| Token | Tailwind | Usage |
|-------|---------|-------|
| Page padding | `px-6 py-6` | All page content areas |
| Card padding | `p-5` | Card internal padding |
| Card gap | `gap-4` | Space between cards in a grid |
| Section gap | `gap-6` | Space between major page sections |
| Input padding | `px-3 py-2` | Form inputs |
| Card radius | `rounded-xl` | Cards, panels, modals |
| Button radius | `rounded-lg` | Buttons, badges, tags |
| Input radius | `rounded-md` | Form inputs, dropdowns |
| Avatar radius | `rounded-full` | Avatars, status dots |
| Card shadow | `shadow-sm` | Cards at rest |
| Card hover shadow | `shadow-md` | Cards on hover |
| Modal shadow | `shadow-xl` | Modals, command palette |
| Sidebar width | `w-[260px]` | Desktop sidebar |
| Sidebar collapsed | `w-[68px]` | Collapsed sidebar (icons only) |
| Copilot panel | `w-[380px]` min, resizable | Side panel |
| Topbar height | `h-14` | 56px |

---

## PART 2: THE COMPONENT LIBRARY ARCHITECTURE

---

### 2.1 Base Components (shadcn/ui + Custom)

| Component | Source | Notes |
|-----------|--------|-------|
| Button | shadcn/ui | Variants: default, secondary, outline, ghost, destructive. Sizes: sm, default, lg, icon |
| Input | shadcn/ui | With label, helper text, error state |
| Textarea | shadcn/ui | Auto-resize variant for notes/descriptions |
| Select | shadcn/ui | Single + multi-select. Searchable variant for company/skill lookups |
| Dialog / Modal | shadcn/ui (Radix) | Confirm dialogs, detail modals |
| Sheet | shadcn/ui | Side panels (Copilot uses this as base) |
| DropdownMenu | shadcn/ui | Context menus, profile switcher, status dropdowns |
| Command | shadcn/ui | Command palette (Cmd+K) base |
| Tabs | shadcn/ui | Job Detail 7 tabs, Settings 9 tabs, Analytics 9 tabs |
| Table | shadcn/ui | Sortable, filterable data tables |
| Badge | shadcn/ui | Status pills, priority tags, score badges |
| Avatar | shadcn/ui | User avatars, company logos |
| Tooltip | shadcn/ui | Info tooltips throughout |
| Slider | shadcn/ui | Score range filters, weight sliders |
| Switch | shadcn/ui | Feature toggles, automation switches |
| Progress | shadcn/ui | Completeness rings, goal bars, discovery progress |
| Card | shadcn/ui | Universal container |
| Skeleton | shadcn/ui | Loading states |
| Toast / Sonner | Sonner | Bottom-right notifications, undo toasts |

### 2.2 Feature Components (Custom Built)

| Component | Props/Purpose |
|-----------|---------------|
| **ScoreBadge** | `score: number` → renders color-coded badge (green/blue/amber/gray/purple) |
| **StatusPill** | `status: string` → color-coded pill (new=blue, applied=green, rejected=red, etc.) |
| **PriorityTag** | `priority: 1\|2\|3` → Dream (purple star), High (orange), Medium (gray) |
| **WarmthIndicator** | `warmth: cold\|warm\|hot` → blue/amber/red dot or pill |
| **ConfidenceBar** | `confidence: number` → mini horizontal bar (0–1) |
| **CompanyLogo** | `company: string` → fetches logo via Clearbit, fallback to initials avatar |
| **QualityScoreRing** | `score: number` → circular progress ring (1–100) with color |
| **SkillMatch** | `matched: string[], missing: string[], preferred: string[]` → green/red/yellow pills |
| **TrendArrow** | `direction: up\|down\|flat, value: string` → ↑12% green, ↓5% red, →0% gray |
| **TimeAgo** | `date: string` → "3 hours ago", "2 days ago" |
| **UndoToast** | `seconds: number, onUndo: fn` → countdown timer with undo button |
| **ProfileSwitcher** | Active profile name + dropdown with all profiles + "Create New" |
| **NotificationBell** | Unread count badge, dropdown with last 5, "View All" link |
| **CommandPalette** | Cmd+K → search across jobs, profiles, pages, actions |
| **ErrorBoundary** | `fallback: ReactNode` → catches errors, shows retry button |
| **SectionErrorBoundary** | Same but for individual dashboard sections/tabs |
| **FileUploader** | Drag-and-drop zone → presigned URL upload → progress bar |
| **PDFViewer** | react-pdf wrapper with page nav, zoom |
| **RichTextEditor** | Tiptap wrapper for review queue inline editing |
| **DiffViewer** | Side-by-side or inline diff with green/yellow highlights |
| **EmptyState** | Icon + title + description + CTA button |
| **LoadingSkeleton** | Variants for cards, tables, lists, detail views |

---

## PART 3: "COPY-PASTE" PROMPTS FOR v0 / GOOGLE STITCH

---

### GLOBAL STYLE DIRECTIVE (Prepend to Every Prompt)

```
STYLE DIRECTIVES (apply to ALL prompts below):
- Framework: Next.js 14 App Router with React Server Components
- Component library: shadcn/ui (built on Radix UI primitives)
- Styling: Tailwind CSS only — no inline styles, no CSS modules
- Font: Geist Sans (body) + Geist Mono (code/data)
- Design language: Clean, minimal, professional. Dense but not cluttered. 
  Inspired by Linear, Vercel Dashboard, and Notion.
- Color: Indigo primary (#6366F1), navy-black dark mode (#0B0F1A), 
  slate grays for text hierarchy
- Radius: rounded-xl for cards, rounded-lg for buttons, rounded-md for inputs
- Spacing: consistent p-5 card padding, gap-4 between cards, gap-6 between sections
- Dark mode: MUST support both light and dark modes using CSS variables 
  and Tailwind dark: prefix
- Typography: text-2xl font-semibold for page titles, text-sm for body, 
  text-xs for captions, font-mono for scores/numbers
- Animations: Subtle — hover:shadow-md on cards, transition-colors on buttons, 
  no flashy animations
- Responsive: Mobile-first. 3-column grid on desktop, 2 on tablet, 1 on mobile
- ALL interactive elements must have focus-visible ring (ring-2 ring-primary)
```

---

### PROMPT 1: Landing Page (Public)

```
CONTEXT: This is the public marketing landing page for "Job Application OS" — an 
AI-powered job search command center. Visitors are job seekers evaluating the product. 
The page must convey power, intelligence, and simplicity. No pricing — everything is free.

LAYOUT:
- Full-width page, no sidebar, no dashboard chrome
- Sticky top nav: logo (left), nav links (Features, How It Works), CTA button "Start Free" (right)
- Hero section: large headline, subheadline, primary CTA, secondary ghost CTA, 
  subtle gradient background (indigo-50 to white)
- Feature grid: 8 cards in a 4x2 grid (2x4 on mobile). Each card: icon, title, 
  2-line description. Features: Discovery, Scoring, Resume Tailoring, Auto-Apply, 
  Outreach, Analytics, AI Copilot, Market Intelligence
- How-it-works: 5 horizontal steps with numbered circles and connecting lines. 
  Steps: Create Profile → AI Discovers Jobs → Scores & Generates → Auto-Applies → Track & Iterate
- Final CTA section: dark background, "Ready to automate your job search?" + large button
- Footer: 3-column grid — Product (Features, Pricing, Changelog, Status), 
  Legal (Privacy, Terms), Company (Blog, Support, Contact)

FUNCTIONALITY:
- "Start Free" buttons link to /auth/signup
- Feature cards are static (no interaction)
- Responsive: hero stacks vertically on mobile, feature grid 2-col on tablet, 1-col on mobile
- Dark mode supported

STYLE: Apply the global style directives. Hero uses a subtle gradient from indigo-50 
to white. Feature cards have hover:shadow-md and an indigo icon. The overall feel should 
be clean and confident like vercel.com or linear.app.
```

---

### PROMPT 2: Auth Pages (Login / Signup)

```
CONTEXT: Authentication pages for Job Application OS. Clean, centered card layout. 
Users log in with email/password or Google OAuth. Must feel secure and fast.

LAYOUT:
- Centered layout: full-screen with subtle gradient or pattern background
- Auth card: max-w-md, rounded-xl, shadow-lg, p-8
- Logo + app name at top of card
- Tab toggle: "Log In" | "Sign Up" (active has underline + bold)

LOGIN FORM:
- Email input (with label, placeholder "you@company.com")
- Password input (with show/hide toggle eye icon)
- "Forgot password?" link (text-sm, right-aligned)
- Primary button: "Log In" (full width, rounded-lg, bg-primary)
- Divider: "or continue with" line
- Google OAuth button: outline variant, Google "G" icon left, "Continue with Google"
- Bottom: "Don't have an account? Sign up" link

SIGNUP FORM:
- Full name input
- Email input
- Password input with strength indicator bar below (red→yellow→green as typing)
- Confirm password input
- Primary button: "Create Account"
- Same Google OAuth button
- Bottom: "Already have an account? Log in" link

FORGOT PASSWORD (separate view):
- Email input
- "Send Reset Link" button
- "Back to login" link

STYLE: The card should feel elevated against the background. Use the indigo primary for 
the main button. Google button is outline with subtle border. Password strength bar 
animates smoothly. Inputs use rounded-md, border-border, focus:ring-2 focus:ring-primary.
Error states show red border + red text-xs below the input.
```

---

### PROMPT 3: Onboarding Wizard (5 Steps)

```
CONTEXT: First-time user onboarding flow after signup. A 5-step wizard that collects 
profile data progressively. Steps 1 and 5 are required, steps 2-4 are skippable.

LAYOUT:
- Full screen, no sidebar (onboarding has its own layout)
- Top: horizontal progress bar showing 5 steps with labels 
  (Basics | Import | Deep Profile | Resumes | AI Keys)
- Active step is highlighted in primary color, completed steps show checkmark
- Center: form content area (max-w-2xl, card with p-8)
- Bottom: "Back" ghost button (left), "Skip" text button (center, steps 2-4 only), 
  "Continue" primary button (right)

STEP 1 — Profile Basics:
- Profile name input (e.g., "Backend Engineer Search")
- Target role input with autocomplete
- Seniority dropdown (Intern through C-Level, 8 options)
- Employment types multi-select checkboxes (Full-time, Part-time, Contract, Temporary)
- Location section: Google Places autocomplete for cities + toggles for Remote/Hybrid/Onsite
- Negative locations: "Never show jobs in..." with tag input
- Years of experience number input
- Current title input
- Salary range: min-max dual input with currency selector dropdown

STEP 2 — Import Data:
- Three large option cards in a row: "Upload Resume" (PDF/DOCX icon), 
  "Import LinkedIn PDF" (LinkedIn icon), "Add Manually" (pencil icon)
- Upload cards have a drag-and-drop zone with dotted border
- After upload: AI extraction progress bar, then editable extracted data preview 
  in a table/form
- "Skip for now" button

STEP 3 — Deep Profile:
- Collapsible sections (accordions): Social URLs, Work Authorization, Languages, 
  Work Preferences, Writing Tones, Custom Fields, AI Instructions
- Each section shows completeness indicator
- AI Instructions: large textarea with placeholder "e.g., Always emphasize 
  distributed systems. Never mention Company X."

STEP 4 — Master Resumes:
- File upload zone: "Upload your existing resume(s)"
- Uploaded files shown as cards: filename, type badge (PDF/DOCX), size, "Remove" button
- Option: "Upload a resume template for AI to fill"
- Skip button prominent

STEP 5 — AI Keys:
- Three provider cards in a row: Anthropic (orange), OpenAI (green), Google (blue)
- Each card: provider logo, API key input (masked with show toggle), 
  "How to get a key →" link, "Test Key" button (shows ✓ or ✗), status indicator
- Minimum 1 valid key required (show validation message)
- Below cards: "Default model assignments" table — Task | Provider | Model dropdowns
- "Copilot model" separate selector with note "Configurable separately"

STYLE: Wizard should feel progressive and encouraging. Steps that are complete show 
green checkmarks. The progress bar uses primary color for active/completed, 
gray-300 for upcoming. Cards in Step 2 and Step 5 should be large with icons 
and have hover:border-primary effect.
```

---

### PROMPT 4: Dashboard Home — Command Center

```
CONTEXT: The main dashboard after login. This is the "command center" — a single-screen 
overview of the user's entire job search. It shows 7 sections in a responsive grid. 
The user is an active job seeker checking their morning status.

LAYOUT:
- Uses the App Shell: left sidebar (260px, collapsible), top bar (56px), main content area
- Page title: "Dashboard" with active profile name badge next to it
- Content organized in a responsive grid:
  - Row 1: 4 stat cards (full width, 4-column grid)
  - Row 2: 2 columns — Action Required panel (left, 60%) | Copilot Preview (right, 40%)
  - Row 3: 2 columns — Discovery Status (left, 40%) | Goal Progress (right, 60%)
  - Row 4: 2 columns — Recent Activity (left, 60%) | Quick Actions (right, 40%)

SECTION A — Stats Row (4 cards):
- Card 1: "Jobs Discovered" — large number (font-mono text-3xl), 
  "Today: 12 | This week: 47", trend arrow (↑15% vs last week, green)
- Card 2: "Pending Reviews" — count with priority breakdown mini-bar 
  (3 dream, 5 high, 8 medium), "Oldest: 2 hours ago"
- Card 3: "Active Applications" — non-terminal count, trend arrow
- Card 4: "Response Rate" — percentage (font-mono), trend arrow
- Each card: rounded-xl, p-5, subtle left border accent color, icon top-right corner

SECTION B — Action Required Panel:
- Card with header "Action Required" + count badge
- Priority-sorted list items, each row: priority tag (Dream/High/Medium), 
  icon (star/document/mail/clock), title, company logo mini, age ("2h ago"), 
  action button (right-aligned)
- Max 5 items shown, "View all →" link at bottom
- Item types: dream company match, review items, due follow-ups, failed submissions, 
  interview prep ready

SECTION C — Copilot Preview:
- Card with "AI Copilot" header + sparkle icon
- Input: "Ask me anything..." with send button
- Below: 2 proactive insight cards (small, horizontal): 
  "3 jobs >85 unprocessed" with action button,
  "Your fintech CLs get 2x responses" 
- "Open full Copilot →" link

SECTION D — Discovery Status:
- Card showing: "Last run: 2 hours ago" | "Next: in 4 hours" | Active profile name
- Source health row: 5-6 colored dots (green=healthy, yellow=slow, red=error) 
  with source names
- "Run Now" primary button

SECTION E — Goal Progress:
- If goals set: "Interviews This Month: 3/5" with progress bar (60% filled, primary color)
- Copilot advice snippet: "You're on pace. Consider targeting smaller companies for faster cycles."
- If no goals: empty state with "Set a goal →" button

SECTION F — Recent Activity:
- Scrollable list of last 15 events
- Each row: icon (colored by type), title text, company name (bold), timestamp (text-xs, right)
- Clickable rows → navigate to related page

SECTION G — Quick Actions:
- 4 large action buttons in a 2x2 grid:
  - "Discover Now" (search icon, primary outline)
  - "Generate for Top Jobs" (sparkle icon, primary outline)
  - "View Weekly Report" (chart icon, outline)
  - "Open Copilot" (chat icon, secondary)
- Each: rounded-xl, p-4, icon + label, hover:bg-surface-raised

STYLE: Dense but breathable. Cards have consistent p-5 padding and rounded-xl. 
The stats row should pop visually (slightly larger, subtle left border colors). 
The action required panel uses priority colors. Activity feed is compact with 
text-sm. Overall: think Linear dashboard meets Notion home page.
```

---

### PROMPT 5: App Shell (Sidebar + Topbar)

```
CONTEXT: The persistent navigation shell wrapping all authenticated pages. 
It contains a collapsible left sidebar, a top bar, and the main content area. 
An optional AI Copilot panel can slide in from the right.

LAYOUT:
- CSS Grid: sidebar (fixed left) | main area (flexible) | copilot panel (optional right)
- Sidebar: 260px default, 68px collapsed (icons only). Toggle via hamburger button.
- Topbar: 56px height, sticky, spans the main content area (not the sidebar)
- Content area: scrollable, padded (px-6 py-6)

SIDEBAR:
- Top: App logo + name ("Job App OS"), collapse toggle button
- Navigation items, each: icon (lucide-react) + label + optional badge count
  - Dashboard (Home icon)
  - Jobs (Briefcase icon) + badge: new job count
  - Review Queue (CheckSquare icon) + badge: pending count (red if >10)
  - Applications (Kanban icon) + badge: active count
  - Outreach (Users icon)
  - Email Hub (Mail icon)
  - Interviews (Calendar icon) + badge: upcoming count
  - Analytics (BarChart icon)
  - Market Intel (TrendingUp icon)
  - --- divider ---
  - Settings (Settings icon)
  - Profiles (UserCircle icon)
  - Files (Folder icon)
  - Activity Log (Clock icon)
  - --- divider ---
  - What's New (Sparkles icon) + dot if unread
- Active item: bg-primary/10 text-primary font-medium, left border accent
- Hover: bg-surface-raised
- Collapsed: only icons shown, tooltip on hover shows label
- Bottom: user avatar mini + "Upgrade" or version info

TOPBAR:
- Left: global search input (with Cmd+K hint badge), magnifying glass icon
- Center: (empty, or breadcrumb on deep pages)
- Right group:
  - Profile switcher: active profile name as button → dropdown with all profiles + 
    "Create New" + "Manage Profiles →"
  - Notification bell: badge with unread count (red dot if >0) → dropdown with 
    last 5 notifications + "View All →"
  - Copilot toggle button: chat bubble icon, toggles the right panel
  - Dark/light mode toggle: sun/moon icon
  - User avatar: circular, dropdown with "Settings", "Activity Log", "Sign Out"

COPILOT PANEL (when open):
- Right side, 380px default width, resizable (drag handle on left edge)
- Pushes main content narrower (not overlay)
- Header: "AI Copilot" + model name badge + close X button
- Chat area: message list with user/AI bubbles
- Input area: text input + send button + slash command hint

RESPONSIVE:
- Tablet (768-1279px): Sidebar collapsed to icons by default, copilot as full overlay
- Mobile (<768px): Sidebar hidden, bottom nav with 5 icons 
  (Dashboard, Jobs, Review, Applications, More), copilot as full overlay, 
  topbar simplified

STYLE: Sidebar has bg-surface with right border. Topbar has bg-background with 
bottom border. Active nav items are clearly distinguished. The overall feel is 
workspace-like — think VS Code sidebar meets Linear navigation. Transition 
animations on sidebar collapse (200ms ease).
```

---

### PROMPT 6: Job Browser

```
CONTEXT: The primary job discovery and browsing page. Shows all discovered jobs with 
powerful filtering, sorting, and multiple view modes. Users spend the most time here. 
Think of it as a job-specific Airtable with score intelligence.

LAYOUT:
- Top section: View toggle (Table | Cards | Compact), global search bar, 
  sort dropdown, bulk action bar
- Left: collapsible filter sidebar (280px, scrollable)
- Right: main content area with job list (virtualized for 2000+ items)

TOP BAR:
- Left: View toggle — 3 icon buttons (table, grid, list), active has bg-primary/10
- Center: Search input (full-text: "Search titles, companies, skills...")
- Right: Sort dropdown (Score ↓, Date ↓, Company A→Z, Salary ↓, Status), 
  Saved Searches dropdown, Bulk Actions button

FILTER SIDEBAR (15+ dimensions):
- Score range: dual-thumb slider (0-100) with mini histogram above showing distribution
- Confidence range: dual-thumb slider (0-1)
- Status: multi-select checkboxes (New, Scored, Content Ready, Applied, Interview, 
  Offer, Rejected, Skipped, Bookmarked, Ghosted) with counts next to each
- Seniority: multi-select (Intern through C-Level)
- Employment: multi-select (Full-time, Part-time, Contract, Temporary)
- Location type: multi-select (Remote, Remote TZ, Hybrid flex, Hybrid fixed, Onsite)
- Location: searchable multi-select (cities/countries)
- Company: searchable input with autocomplete
- Salary range: dual-thumb slider with currency selector
- Source: multi-select with source icons
- Date range: date picker (posted date)
- Toggles: "Dream Company Only", "Has Content", "Show Blacklisted", "Potential Scam"
- "Clear All Filters" button at bottom
- Each filter section: collapsible with item count

TABLE VIEW (default):
- Columns: Checkbox | Company (logo + name) | Title | Score (badge) | 
  Confidence | Status (pill) | Location | Seniority | Salary | Posted | Source icon | Actions
- Sortable column headers (click to sort)
- Row hover: bg-surface-raised
- Row click → navigate to Job Detail
- Quick actions on hover: Bookmark star, Generate sparkle, Apply arrow

CARD VIEW:
- 3-column grid (2 on tablet, 1 on mobile)
- Each card: rounded-xl, p-4
  - Top: Company logo (32px) + Company name (text-sm text-secondary) + Source icon
  - Title: text-base font-medium (1 line, truncate)
  - Tags row: Seniority badge, Location type badge, Employment badge
  - Score section: large ScoreBadge + confidence bar + decision badge (auto/review/skip)
  - Skills: 3-4 matched skill pills (green), 1-2 missing (red), "+N more"
  - Salary: range or "Estimated: $X-Y"
  - Bottom: posted date + status pill
  - Hover: shadow-md, show quick action buttons

COMPACT VIEW:
- Dense rows, less whitespace
- Each row: Score badge | Title | Company | Location | Status pill | Posted | Quick actions
- Optimized for scanning large volumes

BULK ACTIONS (when checkboxes selected):
- Floating bar at bottom: "{N} selected" + "Score All" + "Generate All" + 
  "Bookmark" + "Skip" + "Apply" buttons

STYLE: Dense information display but highly scannable. Score badges are the visual 
anchor — they should be immediately visible. Filter sidebar uses a lighter background 
(bg-surface) with clear section dividers. The histogram above the score slider is 
a mini bar chart (30px tall) in muted gray. Everything scrolls smoothly — the filter 
sidebar is independently scrollable from the main content.
```

---

### PROMPT 7: Job Detail — CRM 7-Tab View

```
CONTEXT: Detailed view of a single job. CRM-style layout with a persistent header 
and 7 switchable tabs below. This is where users decide to apply, review generated 
content, research the company, and manage outreach.

LAYOUT:
- Persistent header (sticky, ~120px): always visible above tabs
- Tab bar below header: 7 tabs
- Tab content area: scrollable

PERSISTENT HEADER:
- Row 1: Company logo (48px) | Title (text-xl font-semibold) | Company name (text-secondary) | 
  Location badge | Seniority badge | Employment badge
- Row 2: Large ScoreBadge (48px circle with score number) | Confidence bar | 
  Risk indicator | Decision badge ("Auto Apply" green / "Review" amber / "Skip" gray) | 
  Status dropdown (shadcn Select) | "Apply" primary button | "Generate Content" button | 
  Bookmark toggle | External "View Original →" link
- Posted date, Source icon, ATS type badge on far right

7 TABS: Overview | Documents | Timeline | Analytics | Company | Outreach | AI Copilot

TAB 1 — Overview:
- Left column (60%):
  - AI Summary card: 3-sentence assessment (why it matches, main risk, recommended action)
  - Skills Match: two rows — "Required" (green matched / red missing pills) and 
    "Preferred" (green matched / yellow missing pills)
  - Full JD: rendered markdown with key requirements highlighted in yellow, 
    your matched skills underlined in green
- Right column (40%):
  - Score Breakdown: 8 horizontal bars (one per dimension) with numeric values, 
    color-coded (green >7, amber 4-7, red <4), bonus points shown separately
  - Salary card: range (or estimated with badge), your target comparison, 
    market context sentence
  - Interview Probability: "Similar applications: X% interview rate"
  - Content Quality: if generated, mini quality scores for both variants

TAB 2 — Documents:
- Grid of document cards: filename, type badge (Resume V1, Resume V2, Cover Letter, etc.), 
  quality score ring, variant label (A/B), template used
- Click → inline PDF preview (react-pdf) or markdown render
- Version history expandable
- Upload button + "Download All as ZIP" button + "Regenerate" button

TAB 3 — Timeline:
- Vertical timeline (left line, right content)
- Each event: icon (colored circle), timestamp, actor badge (System/User/AI), 
  title, expandable detail
- Events: discovered → scored → generated → reviewed → approved → submitted → 
  confirmation → follow-up → reply → status change → interview → outcome
- "Add Note" button for manual entries

TAB 4 — Analytics:
- Score vs pipeline average chart (Recharts bar)
- Time-in-stage metrics
- Similar jobs at same company
- A/B test results if 2 variants used
- Company application history

TAB 5 — Company:
- Overview card: description, industry, size, stage, HQ, founded
- Funding card: last round, total raised, investors
- Culture card: Glassdoor rating (star icons), work-life balance, pros/cons
- Tech Stack: tag pills from blog + JD analysis
- News: recent items with dates
- Health Signals: employee growth, Glassdoor trend, layoff signals
- Your History: all applications at this company across profiles

TAB 6 — Outreach:
- Contact cards: name, title, company, LinkedIn link, warmth indicator, channel, status
- Message history per contact: expandable thread
- Follow-up schedule: next date, adaptive timing
- "Generate New Message" + "Add Contact Manually" buttons

TAB 7 — AI Copilot (Job-Specific):
- Same chat interface as global Copilot but pre-loaded with this job's full context
- Suggested prompts: "What are the risks?", "Draft a follow-up", 
  "Compare to other Google applications", "Practice interview questions"

STYLE: The persistent header should feel like a CRM record header — dense, informative, 
always accessible. Tabs use underline style (not boxed). The Overview tab is the most 
information-dense — use clear visual hierarchy to prevent overwhelm. Score breakdown 
bars should be the same height, with numbers right-aligned. Company tab should feel 
like a dossier.
```

---

### PROMPT 8: Review Queue (Split Panel)

```
CONTEXT: The approval workflow page. AI-generated content (resumes, cover letters, 
outreach messages) lands here for human review before submission. Split-panel layout: 
left side shows the queue, right side shows the detail of the selected item.

LAYOUT:
- Split panel: Left 40% | Right 60%, with draggable divider
- No page-level scroll — each panel scrolls independently

LEFT PANEL — Queue List:
- Header: "Review Queue" + total count badge + filter tabs 
  (All | Resumes | Cover Letters | Outreach | Emails | Answers)
- Bulk actions: "Select All" checkbox + "Approve Selected" button
- Scrollable list of items, each card:
  - Priority tag: Dream (purple + star) | High (orange) | Medium (gray)
  - Company logo (24px) + Job title (truncate)
  - Type icon (document/envelope/message) + type label
  - Quality score (small ring, number inside)
  - Age: "2h ago"
  - Selected state: bg-primary/5, left border primary
- Sorted: Dream → High Score → Medium → Oldest
- Real-time count updates (sidebar badge mirrors this)

RIGHT PANEL — Detail View (Resume):
- Top bar: "Resume Review" + variant tabs (Variant A | Variant B) + quality score ring
- Two-column compare:
  - Left sub-panel (45%): "Job Requirements" header, then the JD requirements listed, 
    required vs preferred sections clearly labeled
  - Right sub-panel (55%): "Generated Resume" header, then the tailored resume content 
    with diff highlights (green = new content, yellow = modified from base)
- Below compare: QA Report expandable panel (hallucination check results, warnings)
- Template indicator: "Used: Modern Professional template"
- Inline editing: clicking on resume text enables Tiptap rich text editing

ACTION BAR (sticky bottom of right panel):
- "Approve & Submit" primary button (strongest)
- "Approve" default button
- "Edit & Approve" outline button
- "Reject" destructive outline button → opens reason dropdown/input
- "Regenerate" ghost button → opens instruction textarea modal
- After approval: Sonner toast with 5-minute countdown + "Undo" button

DETAIL VIEW — Cover Letter:
- Left: JD + company context. Right: formatted letter
- Word count, quality score, personalization highlights on hover

DETAIL VIEW — Outreach:
- Contact info card + warmth indicator + channel
- Message content with character count
- Personalization hooks highlighted in yellow
- Auto-send or draft toggle

STYLE: Split panel should feel like an email client (Superhuman, Gmail). Left panel 
is compact and scannable. Right panel is spacious for detailed review. The diff 
highlights must be visually clear — use bg-success-muted for additions and 
bg-warning-muted for modifications. The action bar should be prominent but not 
overwhelming — the "Approve & Submit" button is the largest and uses bg-primary.
```

---

### PROMPT 9: Application Tracker (Kanban + Table + Calendar)

```
CONTEXT: Tracks all job applications through their lifecycle. Three view modes: 
Kanban board (default), Table, and Calendar. The Kanban supports drag-and-drop 
between status columns.

LAYOUT:
- Top: View toggle (Kanban | Table | Calendar), filter dropdowns, search
- Main: full-width content area for the active view

KANBAN VIEW:
- Horizontal scrolling columns: Discovered → Scored → In Review → Applied → 
  Screening → Interview → Offer → Rejected → Withdrawn → Ghosted
- Each column: header with status name + count badge + column color accent (top border)
- Cards within columns (draggable via @dnd-kit):
  - Company logo (20px) + Company name (text-xs)
  - Job title (text-sm font-medium, 1 line truncate)
  - Score badge (small)
  - Days in stage: "3 days" (text-xs text-muted)
  - Interview probability mini badge (if applicable)
- Drag visual: card lifts with shadow-lg, drop zone highlights with dashed border
- 30-second undo toast on drop (Sonner)
- Empty column: dotted border box with "No applications" text

TABLE VIEW:
- Full data table with columns: Company | Title | Score | Status (dropdown) | 
  Submitted Date | Days in Stage | Interview Date | Last Activity | Actions
- Inline status dropdown: can change status directly in the table
- Sortable columns, filterable
- CSV Export button
- Row click → Job Detail

CALENDAR VIEW:
- Monthly calendar grid (like Google Calendar)
- Color-coded events:
  - Blue: application submitted dates
  - Green: interview dates
  - Orange: follow-up due dates
  - Red: deadlines
- Click date → shows all events for that day in a popover
- Week view toggle available

STYLE: Kanban columns should have subtle top border color coding (green for positive 
stages, amber for middle, red/gray for terminal). Cards are compact — max 80px height. 
The drag interaction should feel smooth and responsive. Table view is a clean data 
table with alternating row backgrounds. Calendar uses a clean grid with rounded event 
pills.
```

---

### PROMPT 10: Settings Hub (9 Tabs)

```
CONTEXT: User configuration page with 9 tabs covering all settings. Each tab is a 
form with save functionality. Heavy use of sliders, toggles, and dropdowns.

LAYOUT:
- Left: vertical tab navigation (list of 9 tabs, full height)
- Right: form content area for the active tab (scrollable)

TABS: General | AI Models | API Keys | Automation | Scoring | Sources | 
Schedules | Email | Feature Flags

TAB: Scoring (most complex — describe this one in detail):
- 8 weight sliders in a vertical list:
  - Each row: label (e.g., "Skill Match"), slider (0-100), numeric value, 
    percentage of total
  - Sliders auto-normalize: when one changes, others adjust proportionally 
    to always sum to 100%
  - Color indicator: matches the score breakdown chart colors
- Below sliders: "Bonus Rules" section — table of configurable bonuses 
  (e.g., "+5 if Glassdoor > 4.0", "+3 if company size < 200")
- Right side: Live Preview panel — shows top 5 jobs from current data 
  re-scored with the current slider values. Updates in real-time as sliders move.
- Buttons: "Save Weights" primary, "AI Suggestion" secondary (AI recommends 
  optimal weights based on outcome data), "Reset to Defaults" ghost

TAB: API Keys:
- 3 provider cards (Anthropic, OpenAI, Google), each:
  - Provider logo + name
  - Masked key display (•••••••• + last 4 chars)
  - Status badge: Active (green) / Invalid (red) / Not Set (gray)
  - "Validate" button, "Remove" destructive button, "Update Key" button
  - Last validated timestamp
- "Add New Key" button at bottom

TAB: Automation:
- Auto-apply master toggle (large switch)
- Score threshold slider (0-100) with current value
- Confidence threshold slider (0-1)
- Risk threshold slider
- Cool-down delay: select (0min, 15min, 30min, 1hr, 2hr, 4hr, 12hr, 24hr)
- Daily limits: 3 number inputs (Applications, Outreach, Easy Apply)
- Operating mode: 3 radio cards (Manual, Approval Required, Full Auto)
- Dream company list: tag input with autocomplete
- Blacklist: tag input

STYLE: Settings should feel clean and organized, not overwhelming. Each tab's content 
fits in a single scrollable area. Sliders use the primary color for the filled track. 
Toggle switches are the shadcn Switch component. The live preview panel in Scoring 
has a subtle bg-surface background and updates with a quick fade animation.
```

---

### PROMPT 11: AI Copilot Panel (Full Interface)

```
CONTEXT: The AI assistant panel that slides in from the right side. It's a 
conversational interface with streaming text, slash commands, action execution 
with confirmation, and proactive suggestion cards. Think ChatGPT sidebar meets 
Notion AI meets GitHub Copilot Chat.

LAYOUT:
- Right side panel: 380px default, resizable (drag handle on left edge)
- Pushes main content (not overlay) on desktop. Full overlay on mobile.
- Header (48px): "AI Copilot" title + model name badge (e.g., "Claude 4") + 
  close X button
- Chat area: scrollable message list (flex-grow)
- Input area (sticky bottom): text input + send button + slash command hint

CHAT MESSAGES:
- User message: right-aligned, bg-primary text-white, rounded-xl, 
  rounded-br-md, max-w-[80%]
- AI message: left-aligned, bg-surface, rounded-xl, rounded-bl-md, max-w-[85%]
  - Supports markdown rendering (bold, italic, lists, code blocks)
  - Streaming: text appears word-by-word with a blinking cursor at the end
- System messages: centered, text-xs text-muted (e.g., "Context: Viewing Google SWE III")

PROACTIVE SUGGESTION CARDS (shown when chat is empty or at top):
- Horizontal scrollable row of cards (3-4):
  - Each: compact card, icon + 1-line text + action button
  - Examples: "3 jobs >85 unprocessed — Generate?" | "Your fintech CLs get 2x responses" |
    "Follow-up due for Stripe recruiter"
  - Click card → auto-sends as message

SLASH COMMANDS:
- When user types "/", show a floating command palette dropdown:
  - /apply — Apply to top N jobs
  - /generate — Generate content
  - /score — Re-score jobs
  - /discover — Run discovery
  - /stats — Show quick stats
  - /compare — Compare jobs
  - /mock — Start mock interview
  - /negotiate — Start negotiation roleplay
  - /help — Show all commands
- Each command: name + description + icon

ACTION EXECUTION:
- When AI proposes an action: special "Action Card" message with:
  - Title: "Apply to 5 jobs"
  - Description: list of jobs
  - "Confirm" primary button + "Cancel" ghost button
  - After confirm: progress indicator + completion message

INPUT AREA:
- Expandable textarea (min 1 line, max 4 lines, then scroll)
- Send button (arrow icon, bg-primary, disabled when empty)
- Keyboard: Enter to send, Shift+Enter for newline
- Slash command detection on "/"
- "Cmd+J to toggle" hint text (text-xs text-muted)

STYLE: The panel should feel like a premium chat experience. Messages have 
subtle shadows. Streaming text is smooth. The overall feel is intimate and 
helpful — not robotic. Use Geist Mono for any code snippets in AI responses. 
The model badge uses a subtle outline style. Proactive cards have a gentle 
gradient background (primary-muted to transparent).
```

---

### PROMPT 12: Analytics Dashboard (9 Tabs)

```
CONTEXT: Comprehensive analytics showing job search performance metrics. 
9 tabs with charts, tables, and exportable data. Uses Recharts for standard 
charts and D3 Sankey for the funnel visualization.

LAYOUT:
- Top: Page title "Analytics" + date range selector (Today, 7d, 30d, 90d, All, Custom) + 
  profile filter dropdown + Export button (CSV/PDF)
- Tab bar: Funnel | Sources | Rejections | AI Cost | Skills & Market | A/B Testing | 
  Goals | Timing | Reports
- Content area: charts and data for active tab

TAB: Funnel (most important — describe in detail):
- Sankey diagram (D3 Sankey): flowing from left to right
  - Nodes: Discovered → Scored ≥60 → Generated → Applied → Response → Interview → Offer
  - Link widths proportional to count
  - Node colors: gradient from blue (left) to green (right)
  - Hover on a node: tooltip with exact count + conversion rate
  - Hover on a link: highlight the flow path
- Below diagram: conversion rate table — From | To | Count | Rate | Change vs Last Period
- Filterable by date, profile, source

TAB: Sources:
- Grouped bar chart: per source (LinkedIn, Google Jobs, Indeed, etc.)
  - Bars: Jobs Found, Scored ≥80, Applied, Interviews (4 bars per group)
  - Color coded: blue, green, purple, orange
- Table below: source | total | score avg | applied | interviews | cost per interview

TAB: AI Cost:
- Line chart: daily spending over time (last 30 days)
- Stacked bar: spending by provider (Anthropic blue, OpenAI green, Google red)
- Donut chart: spending by task (Scoring, Resume Gen, Cover Letter, Copilot, etc.)
- Stat cards: This Month Total, Projected Monthly, Cost Per Application, 
  Most Expensive Task

TAB: Goals:
- Goal cards: each with title (e.g., "5 Interviews This Month"), 
  progress bar, current/target numbers, pace indicator
- Copilot advice snippet per goal
- "Add Goal" button → modal with goal type + target + timeframe

STYLE: Charts should be clean with generous padding. Use the primary color family 
for chart colors (indigo-400, indigo-500, indigo-600) with secondary colors for 
contrast (emerald, amber). The Sankey diagram is the visual centerpiece — it should 
be at least 400px tall with smooth curved links. All charts have a consistent 
white/surface card background with subtle borders. Axis labels are text-xs text-muted. 
Tooltips are shadcn-style (rounded-lg, shadow-md, p-3).
```

---

### PROMPT 13: Notification Center

```
CONTEXT: Full-page notification history with filtering by priority and read status. 
Also defines the notification bell dropdown behavior in the top bar.

LAYOUT:
- Page title: "Notifications" + "Mark All Read" button (ghost)
- Filter bar: tab buttons (All | Critical | High | Medium | Low | Unread)
- Scrollable list of notification cards

NOTIFICATION CARD:
- Left: icon (colored by type — star for dream, target for high score, 
  document for content, check for applied, calendar for interview, etc.)
- Center: title (text-sm font-medium), body (text-xs text-secondary, 2 lines max), 
  timestamp (text-xs text-muted)
- Right: unread dot (blue dot if unread) + click-to-navigate arrow
- Read vs unread: unread has bg-primary/5, read has bg-background
- Click → navigate to relevant page (job detail, review queue, etc.)

BELL DROPDOWN (in topbar):
- Max 5 most recent notifications
- Each: mini card with icon + title (1 line) + time
- "View All →" link at bottom
- Header: "Notifications" + unread count badge

TOAST (bottom-right):
- Appears for critical notifications
- Sonner toast: icon + title + body + dismiss X
- Auto-dismiss in 5 seconds
- Stacks up to 3

STYLE: Notifications should feel clean and scannable. Priority determines the 
icon color (red for critical, orange for high, blue for medium, gray for low). 
Unread items have a subtle highlight. The bell dropdown uses shadow-xl and appears 
below the bell icon with an arrow pointer.
```

---

### PROMPT 14: Profile Manager

```
CONTEXT: Page showing all user's candidate profiles. Users can have multiple 
profiles (e.g., "Backend Engineer Search", "ML Engineer Search") with independent 
settings but shared data (skills, experience).

LAYOUT:
- Page title: "Profiles" + "Create New Profile" primary button
- Grid of profile cards (3 columns desktop, 2 tablet, 1 mobile)

PROFILE CARD:
- Rounded-xl card, p-5
- Top row: profile name (text-lg font-semibold) + active badge (green "Active" or 
  gray "Inactive")
- Target role + seniority
- Stats row: "47 jobs | 12 applications | Last active 2h ago"
- Completeness ring (circular progress, percentage in center, color: 
  green >80%, amber 50-80%, red <50%)
- Missing items hint: "Add languages (+5%), work preferences (+8%)"
- Market fit score badge: "78/100 market fit"
- Action buttons: Edit | Clone | Switch | Deactivate | Delete (destructive)
- Active card has a primary border highlight

PROFILE COMPARISON (accessible via button):
- Side-by-side table: metrics per profile (jobs found, avg score, 
  interview rate, response rate)

STYLE: Cards should feel like player cards or profile tiles. The completeness 
ring is the visual anchor — render it as a circular SVG progress indicator 
(120px diameter) with the percentage number in the center. Active profile has 
border-primary and a subtle glow (shadow with primary color tint).
```

---

### PROMPT 15: Activity Log

```
CONTEXT: Searchable audit trail of every system action. Used for debugging, 
transparency, and compliance. Dense tabular data.

LAYOUT:
- Page title: "Activity Log" + search input + "Export CSV" button
- Filter row: date range picker, actor dropdown (System/User/AI), 
  action type dropdown, profile dropdown, entity type dropdown
- Scrollable data table

TABLE COLUMNS:
- Timestamp (text-xs font-mono, sort by default desc)
- Action (text-sm, e.g., "job.scored", "content.generated", "application.submitted")
- Actor badge: System (gray), User (blue), AI (purple)
- Entity: type + truncated ID (link to detail page)
- Detail: expandable — click row to show JSON-formatted detail

STYLE: Dense data table optimized for scanning. Font-mono for timestamps and IDs. 
Actor badges are small colored pills. Alternating row backgrounds (bg-background / 
bg-surface). Expandable detail rows use bg-surface-raised with pre-formatted JSON 
in a code block with syntax highlighting.
```

---

### PROMPT 16: Status Page (Public)

```
CONTEXT: Public-facing page showing system health. Accessible without login. 
Displays real-time status of all services and 90-day uptime history.

LAYOUT:
- Full-width, no sidebar (public page)
- Top: logo + "Status" title + overall status indicator 
  ("All Systems Operational" green or "Partial Outage" amber)
- Service grid: one row per service

SERVICES:
- API Server: status dot + "Operational" + 90-day uptime bar
- Celery Workers: same
- Database (PostgreSQL): same
- R2 Storage: same
- Gmail Integration: same
- Supabase Realtime: same

90-DAY UPTIME BAR:
- Horizontal bar of 90 tiny squares (one per day)
- Green = operational, Yellow = degraded, Red = outage, Gray = no data
- Hover day → tooltip with date + status + details if incident

INCIDENT HISTORY:
- Below services: list of past incidents, newest first
- Each: date + title + severity badge + description + resolution

STYLE: Clean, minimal, trustworthy. Status dots are animated (subtle pulse for 
"operational"). The 90-day bar is compact (2px height per square, 4px width). 
Overall feel: Instatus or Atlassian Statuspage. Green dominates when healthy.
```

---

### PROMPT 17: Outreach Hub

```
CONTEXT: Manages all recruiter and hiring manager contacts across all applications. 
Shows contact cards, message history, warmth scoring, and follow-up scheduling.

LAYOUT:
- Top: "Outreach Hub" title + search + filter dropdowns (Company, Warmth, Status, Channel)
- Left: contact list (scrollable, 40%)
- Right: selected contact detail (60%)
- Bottom stats bar: sent, open rate, reply rate, best templates, best timing

CONTACT CARD (in list):
- Avatar/initials + name + title + company
- Warmth indicator: Cold (blue snowflake), Warm (amber flame), Hot (red fire)
- Channel badges: LinkedIn DM, InMail, Email
- Status pill: Draft, Queued, Sent, Opened, Replied, No Response, Do Not Contact
- Last activity timestamp

CONTACT DETAIL (right panel):
- Header: full contact info + LinkedIn link + warmth badge + channel
- Message thread: chronological, each message: content, sent timestamp, 
  status (sent/opened/replied), channel
- Follow-up schedule: next date, adaptive timing recommendation
- "Generate New Message" + "Add Contact Manually" + "Schedule Follow-Up" buttons

STYLE: Contact-management feel, like a lightweight CRM. Warmth colors should be 
immediately scannable. Message threads feel like a chat history. The stats bar 
at bottom uses 4 small stat cards with font-mono numbers.
```

---

### PROMPT 18: Interview Calendar

```
CONTEXT: Calendar showing all upcoming and past interviews, color-coded by round 
type, with prep pack links and post-interview logging.

LAYOUT:
- Top: "Interviews" title + Month/Week toggle + navigation arrows 
  (< Previous | Today | Next >)
- Main: calendar grid (monthly or weekly view)
- Sidebar or modal: event detail on click

CALENDAR GRID:
- Monthly: 7-column grid (Mon-Sun), dates in cells
- Event pills in cells: color-coded by round type
  - Phone screen: blue
  - Technical: orange
  - System design: teal
  - Hiring manager: purple
  - Final round: red
  - Culture fit: green
- Each pill: company logo mini + role title (truncated) + time

EVENT DETAIL (click to expand):
- Card with: company logo + role + round type badge
- Date/time with timezone conversion
- Platform: Zoom/Meet/Teams icon + "Join Meeting" button
- Interviewer: name, title, LinkedIn link
- Prep pack: "View Prep Pack →" link
- Checklist: interactive checkboxes (Prep reviewed?, STAR answers ready?, 
  Questions prepared?, Tech setup tested?)
- Notes textarea
- Post-interview: "How did it go?" prompt with difficulty (1-5 stars), 
  performance (1-5 stars), questions asked textarea, next steps

STYLE: Clean calendar like Google Calendar but purpose-built. Round type colors 
should be the primary visual differentiator. Event detail modals are comprehensive 
but not overwhelming. The prep checklist uses checkboxes with satisfying check 
animations.
```

---

### PROMPT 19: Market Intelligence Dashboard

```
CONTEXT: Data-driven market insights derived from all discovered job postings. 
Shows skill demand trends, hot companies, salary movements, and competition analysis.

LAYOUT:
- Top: "Market Intelligence" title + date range selector + profile filter
- 5 sections stacked vertically, each in a card

SECTION 1 — Trending Skills:
- Table: Skill Name | Tier (1-4 badge) | Demand % | 8-Week Trend (sparkline) | Direction arrow
- Tiers: Core >60% (green), Valued 30-60% (blue), Differentiator 10-30% (amber), 
  Niche <10% (gray)
- "Skills You Should Learn" recommendation box below
- Filterable by role type, location

SECTION 2 — Hot Companies:
- Table rows: Company logo + name | Open Roles Count | Hiring Velocity 
  (accelerating ↑ / stable → / decelerating ↓) | Your Avg Match Score | 
  "Set as Dream" button
- Sorted by hiring velocity

SECTION 3 — Salary Trends:
- Line chart: market salary over 30/60/90 days for user's target role
- Your target horizontal line overlaid (dashed)
- Regional comparison: grouped bar chart (India vs US vs Europe vs Remote)
- Histogram: salary distribution for target roles

SECTION 4 — Hiring Velocity:
- Area chart: weekly job posting volume over time
- Layoff tracker: cards with company name + "Recent layoffs reported" badge
- Growth signals: company cards with "Increasing headcount" badge
- Overall market indicator: "Market is HOT for Senior Backend Engineers" (green badge)

SECTION 5 — Competition Analysis:
- Competition level badges per job: Low (green), Medium (amber), 
  High (orange), Very High (red)
- Best time to apply chart
- Hidden gems: companies with fewer applicants than average

STYLE: Data-dense but well-organized. Each section is a separate card with its own 
header. Sparklines are tiny (30px tall) and inline. The salary comparison chart 
should clearly show the user's position vs market. Use muted colors for 
background data and bold colors for the user's data overlay.
```

---

### PROMPT 20: Email Intelligence Hub

```
CONTEXT: Gmail integration page showing auto-detected job-related emails 
(rejections, interview invites, recruiter responses), email templates, and 
the outbox for sent emails.

LAYOUT:
- Top: "Email Hub" title + connection status indicator (green "Connected" or 
  red "Not Connected" + "Connect Gmail" button)
- 4 sections: Auto-Detected Emails, Email Templates, Outbox, Privacy Note

SECTION 1 — Auto-Detected:
- 4 category tabs: Rejections | Interview Invites | Recruiter Responses | Confirmations
- Each tab: list of detected emails with: date, from, subject, classification 
  confidence badge, linked application, auto-action taken
- Rejections: red indicator, linked to application (auto-updated status)
- Interview invites: calendar icon, extracted date/time/platform, 
  "Created calendar event" badge
- Click → shows email snippet + linked application card

SECTION 2 — Templates:
- Grid of template cards: template name, category, preview (2 lines), 
  "Use" button, "Edit" button
- Categories: Follow-Up, Thank-You, Withdrawal, Referral Request, Cold Email, 
  Counter-Offer, Accept Offer
- Each template: variable pills ({company}, {title}, {interviewer_name}) shown inline
- "Create Custom Template" button

SECTION 3 — Outbox:
- Table: Recipient | Subject | Status (queued/sent/delivered/opened/replied) | 
  Sent Date | Open tracking icon
- Click → see full email content + linked application

PRIVACY NOTE:
- Card with lock icon: "We only scan for job-related emails. Nothing else is 
  read or stored. Disconnect at any time."
- "Disconnect Gmail" danger button

STYLE: Professional email management feel. Status indicators are clear 
(green sent, blue opened, purple replied, gray queued). Template cards 
have a "preview" aesthetic — show formatted email with variable placeholders 
highlighted in primary-muted background. The privacy note is reassuring — 
subtle, not alarming.
```

---

### PROMPT 21: File Manager

```
CONTEXT: Central file management for all documents across jobs and profiles. 
Tree structure on the left, file grid on the right.

LAYOUT:
- Left (30%): folder tree — organized by profile → job folders + 
  "Master Resumes" and "Resume Templates" top-level folders
- Right (70%): file grid for selected folder

FOLDER TREE:
- Collapsible tree nodes: Profile name → Job title folders
- Top-level: "Master Resumes", "Resume Templates"
- Each folder: name + file count badge
- Active folder: bg-primary/10

FILE GRID:
- Cards per file: filename, type badge (PDF/DOCX), file size, 
  quality score ring (if applicable), variant label (A/B), 
  uploaded date, preview thumbnail
- Actions per file: Preview, Download, Delete
- Top: "Upload" button + "Download All as ZIP" button + storage stats 
  ("Using 24MB of 500MB")
- Click → inline PDF preview (react-pdf) or document viewer

STYLE: File manager feel like Google Drive or Dropbox. Folder tree uses 
indentation with folder icons. File cards are compact with clear type badges. 
Preview uses a modal overlay with the PDF viewer.
```

---

> **End of UI/UX Design Blueprint.** 21 page prompts + Global Design System + Component Architecture. Feed each prompt (with the Global Style Directive prepended) into v0 or Google Stitch to generate consistent, production-quality React components.
