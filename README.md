
- Background: #F7F7F5
- Surface: #FFFFFF
- Border: #E4E4E1
- Primary text: #171717
- Secondary text: #666666
- Accent: #315CFF
- Success: #2F7D4A
- Warning: #A66A00
- Error: #B42318

Type family: **Inter** (drop the Inter-*.ttf files into `fonts/`).

Spacing scale: 4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64.

## Project structure

```
lib/
  main.dart                          # App entry, route table
  theme/
    app_theme.dart                  # AppColors, AppSpacing, AppRadii, AppTheme.light()
  data/
    models.dart                     # Course, Student, AssistantMessage + mock data
  widgets/
    primitives.dart                 # SectionHeader, DifficultyTag, StatusPill, MatchMeter, MobileScaffold, ScreenHeader, HairlineDivider
  screens/
    login_screen.dart                # 4 login states (default / focus / error / loading)
    home_screen.dart                 # Home — what do I need right now?
    courses_screen.dart              # Course browsing with filters
    course_details_screen.dart       # Course details + match score + reasons
    recommendations_screen.dart      # Ranked recommended courses
    progress_screen.dart             # Graduation progress + completed + current
    profile_screen.dart              # Student info + interests + skills
    assistant_screen.dart            # University assistant chat
```

## Routes

- `/` — Login
- `/home` — Home
- `/courses` — Courses list
- `/course` (with `code` argument) — Course details
- `/recommendations` — Recommended courses
- `/progress` — Academic progress
- `/profile` — Profile
- `/assistant` — University assistant
