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
