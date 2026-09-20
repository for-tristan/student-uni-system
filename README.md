# Smart University Assistant — Web (React + TypeScript)

The complete web design system: Foundations, Components, Mobile mockups (rendered in browser frames), and the University staff platform (Overview, Students, Courses, Recommendations, Assistant).

## Visual identity

Restrained academic palette — neutral foundation, single #315CFF accent used sparingly, no gradients, no glow, no glassmorphism.

- Background: #F7F7F5
- Surface: #FFFFFF
- Border: #E4E4E1
- Primary text: #171717
- Secondary text: #666666
- Accent: #315CFF
- Success: #2F7D4A
- Warning: #A66A00
- Error: #B42318

Type family: **Inter** (loaded via next/font/google in `src/app/layout.tsx`).
Spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 40 / 48 / 64.

## Stack

- Next.js 16 (App Router)
- TypeScript 5
- Tailwind CSS 4
- shadcn/ui (New York)
- Lucide icons
- Recharts (already installed — used for the recommendation activity bar chart if you wire data)

## File structure

```
src/
  app/
    page.tsx                          # Main router — switches between design pages
    layout.tsx                        # Inter font, metadata
    globals.css                       # Design tokens (CSS variables)
  design/
    data/mock.ts                      # Mock academic data
    shell/
      primitives.tsx                  # SectionTitle, Panel, DifficultyTag, StatusPill, MatchMeter, BottomNavItem
      frames.tsx                      # PhoneFrame, BrowserFrame
      design-shell.tsx                # Top navigation shell
    foundations/foundations-page.tsx
    components/components-page.tsx
    mobile/
      mobile-auth-page.tsx            # 4 login states
      mobile-student-page.tsx         # Home, Courses, Course details, Recommendations, Progress, Profile + states
      mobile-assistant-page.tsx       # Assistant empty / chat / reference
    web/
      web-admin-page.tsx              # 7 admin views
      responsive-page.tsx             # 1440 / 1024 / 768 / 390 demo
```

## Setup

```bash
bun install      # or npm install / pnpm install
bun run dev      # http://localhost:3000
```

## What's inside

8 design pages accessible via the top navigation:

1. **Foundations** — color tokens, type scale, spacing, iconography, layout principles
2. **Components** — button/input/badge/tabs/table/pagination/toast/modal/drawer/navigation with states
3. **Mobile — Authentication** — 4 login states (default, focus, error, loading)
4. **Mobile — Student** — Home, Courses, Course details, Recommendations, Progress, Profile + loading/empty/error/offline
5. **Mobile — Assistant** — empty / conversation / course-reference states
6. **Web — Admin** — Overview, Students, Student details, Courses, Course details, Recommendations, Assistant (switchable via sub-tabs)
7. **Web — Assistant** — conversation list | conversation layout
8. **Responsive** — Students table at 1440 / 1024 / 768 px + behavior matrix + Flutter/React handoff notes

## Customizing

- Replace `src/design/data/mock.ts` with real data (or wire to Prisma + your API).
- The accent color lives in `src/app/globals.css` — change `--primary` and everything updates.
- Mobile screens are rendered inside an iPhone-shaped frame (`PhoneFrame`). To convert them to a real Flutter app, download the Mobile (Flutter) bundle.
