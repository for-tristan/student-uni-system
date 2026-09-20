"use client";

import * as React from "react";
import {
  Home,
  BookOpen,
  MessageSquare,
  TrendingUp,
  User,
  Search,
  ChevronRight,
  Check,
  Plus,
  Clock,
  WifiOff,
  AlertTriangle,
  Loader2,
  Star,
  Filter,
  Settings,
  LogOut,
  Pencil,
  X,
} from "lucide-react";
import { PhoneFrame } from "../shell/frames";
import {
  STUDENT,
  COURSES,
  RECOMMENDED,
  COMPLETED,
  IN_PROGRESS,
} from "../data/mock";
import {
  DifficultyTag,
  StatusPill,
  MatchMeter,
  BottomNavItem,
} from "../shell/primitives";

export function MobileStudentPage() {
  return (
    <div className="space-y-8">
      <section>
        <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
          04 — Mobile · Student
        </div>
        <h1 className="text-[26px] font-semibold tracking-[-0.01em]">
          Student experience
        </h1>
        <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
          A real academic tool, not a social app. Bottom navigation: Home, Courses,
          Assistant, Progress, Profile. Typography and dividers establish hierarchy —
          not card grids.
        </p>
      </section>

      {/* Home + Courses + Course details + Recommendations */}
      <ScreenGroup title="Home · Courses · Course details · Recommendations">
        <PhoneFrame label="Home" caption="Answers: what do I need right now?">
          <HomeScreen />
        </PhoneFrame>
        <PhoneFrame label="Courses" caption="List, search, filters">
          <CoursesScreen />
        </PhoneFrame>
        <PhoneFrame label="Course details" caption="Match shown as data, not a score gimmick">
          <CourseDetailsScreen />
        </PhoneFrame>
        <PhoneFrame label="Recommendations" caption="Ranked list with reasons">
          <RecommendationsScreen />
        </PhoneFrame>
      </ScreenGroup>

      {/* Progress + Profile */}
      <ScreenGroup title="Progress · Profile">
        <PhoneFrame label="Progress" caption="One clear indicator. No decorative charts.">
          <ProgressScreen />
        </PhoneFrame>
        <PhoneFrame label="Profile" caption="Functional. No marketing copy.">
          <ProfileScreen />
        </PhoneFrame>
      </ScreenGroup>

      {/* States */}
      <ScreenGroup title="States — loading · empty · error · offline">
        <PhoneFrame label="Loading" caption="Subtle skeletons, no spinners in hero">
          <LoadingScreen />
        </PhoneFrame>
        <PhoneFrame label="Empty" caption="Useful, not pitiful">
          <EmptyScreen />
        </PhoneFrame>
        <PhoneFrame label="Error" caption="What failed. Try again.">
          <ErrorScreen />
        </PhoneFrame>
        <PhoneFrame label="Offline" caption="Explain what's unavailable">
          <OfflineScreen />
        </PhoneFrame>
      </ScreenGroup>
    </div>
  );
}

function ScreenGroup({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="text-[14px] font-semibold tracking-[-0.005em] mb-3">{title}</h2>
      <div className="flex flex-wrap gap-8">{children}</div>
    </section>
  );
}

// ============================== Home ==============================

function MobileShell({
  active,
  children,
}: {
  active: "home" | "courses" | "assistant" | "progress" | "profile";
  children: React.ReactNode;
}) {
  return (
    <div className="h-full flex flex-col bg-background">
      <div className="flex-1 overflow-hidden">{children}</div>
      <nav className="border-t border-border bg-card grid grid-cols-5">
        <BottomNavItem label="Home" active={active === "home"} icon={<Home className="h-3.5 w-3.5" />} />
        <BottomNavItem label="Courses" active={active === "courses"} icon={<BookOpen className="h-3.5 w-3.5" />} />
        <BottomNavItem label="Assistant" active={active === "assistant"} icon={<MessageSquare className="h-3.5 w-3.5" />} />
        <BottomNavItem label="Progress" active={active === "progress"} icon={<TrendingUp className="h-3.5 w-3.5" />} />
        <BottomNavItem label="Profile" active={active === "profile"} icon={<User className="h-3.5 w-3.5" />} />
      </nav>
    </div>
  );
}

function ScreenHeader({ title, right }: { title: React.ReactNode; right?: React.ReactNode }) {
  return (
    <header className="sticky top-0 z-10 bg-background/95 backdrop-blur border-b border-border">
      <div className="px-5 h-12 flex items-center justify-between">
        <h1 className="text-[15px] font-semibold tracking-[-0.005em]">{title}</h1>
        {right}
      </div>
    </header>
  );
}

export function HomeScreen() {
  const hour = 9;
  const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
  return (
    <MobileShell active="home">
      <div className="h-full overflow-y-auto scroll-thin pb-4">
        {/* Greeting — typography, not a card */}
        <div className="px-5 pt-5 pb-3">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
            {greeting}
          </div>
          <div className="text-[22px] font-semibold tracking-[-0.01em] mt-0.5">
            {STUDENT.name}
          </div>
          <div className="text-[12px] text-muted-foreground mt-0.5">
            {STUDENT.major} · {STUDENT.year}
          </div>
        </div>

        <Divider />

        {/* Academic progress — inline, no card */}
        <Section title="Academic progress">
          <div className="flex items-baseline justify-between">
            <div className="text-[12px] text-muted-foreground">Credits</div>
            <div className="text-[12px] text-muted-foreground tabular-nums">
              {STUDENT.creditsCompleted} / {STUDENT.creditsRequired}
            </div>
          </div>
          <div className="mt-2 h-1.5 bg-muted rounded-sm overflow-hidden">
            <div
              className="h-full bg-primary"
              style={{
                width: `${(STUDENT.creditsCompleted / STUDENT.creditsRequired) * 100}%`,
              }}
            />
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <Stat label="GPA" value={STUDENT.gpa.toFixed(2)} />
            <Stat label="In progress" value={`${STUDENT.creditsInProgress} cr`} />
            <Stat label="Graduation" value={STUDENT.graduation} />
          </div>
        </Section>

        <Divider />

        {/* Current courses */}
        <Section
          title="Current courses"
          right={
            <button className="text-[12px] text-primary inline-flex items-center gap-1">
              View all <ChevronRight className="h-3 w-3" />
            </button>
          }
        >
          <div className="divide-y divide-border border-y border-border">
            {IN_PROGRESS.map((c) => (
              <CourseRowMobile key={c.code} course={c} />
            ))}
          </div>
        </Section>

        <Divider />

        {/* Recommended */}
        <Section
          title="Recommended courses"
          right={
            <button className="text-[12px] text-primary inline-flex items-center gap-1">
              See more <ChevronRight className="h-3 w-3" />
            </button>
          }
        >
          <div className="divide-y divide-border border-y border-border">
            {RECOMMENDED.slice(0, 3).map((c, i) => (
              <RecommendedRowMobile key={c.code} course={c} rank={i + 1} compact />
            ))}
          </div>
        </Section>

        <Divider />

        {/* Assistant prompt */}
        <Section title="Assistant">
          <div className="border border-border p-3 rounded-md">
            <p className="text-[13px] text-foreground leading-relaxed">
              Ask about courses, prerequisites, or university rules.
            </p>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {[
                "Prerequisites for Machine Learning?",
                "Which courses next semester?",
              ].map((q) => (
                <button
                  key={q}
                  className="text-[12px] h-7 px-2.5 border border-border rounded-md text-muted-foreground inline-flex items-center gap-1"
                >
                  <MessageSquare className="h-3 w-3" /> {q}
                </button>
              ))}
            </div>
          </div>
        </Section>
      </div>
    </MobileShell>
  );
}

// ============================== Courses ==============================

export function CoursesScreen() {
  const [filter, setFilter] = React.useState("All");
  const filters = ["All", "AI", "Systems", "Data", "Mathematics"];

  return (
    <MobileShell active="courses">
      <ScreenHeader title="Courses" />
      <div className="h-full overflow-y-auto scroll-thin pb-4">
        {/* Search */}
        <div className="px-5 pt-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <input
              className="h-10 w-full pl-9 pr-3 rounded-md border border-border bg-card text-[13px]"
              placeholder="Search by name, code, or skill"
            />
          </div>
        </div>

        {/* Filter chips */}
        <div className="px-5 pt-3 flex gap-2 overflow-x-auto scroll-thin">
          {filters.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={
                "h-7 px-2.5 text-[12px] rounded-md border whitespace-nowrap " +
                (filter === f
                  ? "bg-foreground text-background border-foreground"
                  : "border-border text-muted-foreground")
              }
            >
              {f}
            </button>
          ))}
          <button className="h-7 px-2 text-[12px] rounded-md border border-border text-muted-foreground inline-flex items-center gap-1">
            <Filter className="h-3 w-3" /> Filters
          </button>
        </div>

        {/* Result count */}
        <div className="px-5 pt-3 text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
          {COURSES.length} courses
        </div>

        {/* List */}
        <div className="mt-1 divide-y divide-border border-y border-border">
          {COURSES.slice(0, 8).map((c) => (
            <CourseRowMobile key={c.code} course={c} showPrereq />
          ))}
        </div>
      </div>
    </MobileShell>
  );
}

function CourseRowMobile({
  course,
  showPrereq,
}: {
  course: (typeof COURSES)[number];
  showPrereq?: boolean;
}) {
  return (
    <button className="w-full text-left px-5 py-3 hover:bg-muted/40 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-baseline gap-2">
            <span className="text-[14px] font-medium truncate">{course.name}</span>
            <span className="text-[11px] text-muted-foreground tabular-nums">
              {course.code}
            </span>
          </div>
          <div className="text-[12px] text-muted-foreground mt-0.5">
            {course.category} · {course.credits} credits
          </div>
          {showPrereq && course.prerequisites.length > 0 && (
            <div className="text-[11px] text-muted-foreground mt-1">
              Prereq · {course.prerequisites.join(", ")}
            </div>
          )}
        </div>
        <div className="flex flex-col items-end gap-1 shrink-0">
          <DifficultyTag level={course.difficulty} />
          <ChevronRight className="h-3.5 w-3.5 text-muted-foreground mt-1" />
        </div>
      </div>
    </button>
  );
}

// ============================== Course details ==============================

function CourseDetailsScreen() {
  const course = COURSES[0]; // Machine Learning
  return (
    <MobileShell active="courses">
      <div className="h-full overflow-y-auto scroll-thin pb-6">
        {/* Back + title */}
        <header className="sticky top-0 bg-background/95 backdrop-blur border-b border-border z-10">
          <div className="h-12 px-3 flex items-center gap-2">
            <button className="h-8 w-8 grid place-items-center text-muted-foreground">
              <ChevronRight className="h-4 w-4 rotate-180" />
            </button>
            <div className="text-[13px] font-medium truncate">{course.code}</div>
          </div>
        </header>

        <div className="px-5 pt-5">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
            {course.category} · {course.credits} credits
          </div>
          <h1 className="text-[22px] font-semibold tracking-[-0.01em] mt-1">
            {course.name}
          </h1>
          <div className="mt-2"><DifficultyTag level={course.difficulty} /></div>
        </div>

        <Divider />

        <Section title="Overview">
          <p className="text-[13px] leading-relaxed text-foreground">
            An introduction to supervised, unsupervised, and reinforcement learning.
            Covers linear models, decision trees, neural networks, and model evaluation.
            Includes a semester-long applied project on a real dataset.
          </p>
        </Section>

        <Divider />

        <Section title="Prerequisites">
          <div className="space-y-2">
            {course.prerequisites.map((code) => {
              const prereq = COURSES.find((c) => c.code === code);
              const completed = COMPLETED.find((c) => c.code === code);
              return (
                <div key={code} className="flex items-center justify-between">
                  <div>
                    <div className="text-[13px] font-medium">{prereq?.name ?? code}</div>
                    <div className="text-[11px] text-muted-foreground tabular-nums">{code}</div>
                  </div>
                  {completed ? (
                    <StatusPill kind="success">
                      <Check className="h-3 w-3 mr-1" /> Completed · {completed.grade}
                    </StatusPill>
                  ) : (
                    <StatusPill kind="warning">Not completed</StatusPill>
                  )}
                </div>
              );
            })}
          </div>
        </Section>

        <Divider />

        <Section title="Skills">
          <div className="flex flex-wrap gap-1.5">
            {course.skills.map((s) => (
              <span
                key={s}
                className="text-[12px] h-6 px-2 inline-flex items-center rounded-md border border-border text-foreground"
              >
                {s}
              </span>
            ))}
          </div>
        </Section>

        <Divider />

        <Section title="Your match">
          <div className="flex items-baseline justify-between">
            <div className="text-[28px] font-semibold tracking-[-0.02em] tabular-nums">
              {course.matchScore}%
            </div>
            <div className="text-[11px] text-muted-foreground">based on skills &amp; interests</div>
          </div>
          <div className="mt-2">
            <MatchMeter value={course.matchScore ?? 0} />
          </div>
          <div className="mt-3 text-[12px] text-muted-foreground">
            Why this course appears here:
          </div>
          <ul className="mt-1.5 space-y-1">
            {course.matchReasons?.map((r) => (
              <li key={r} className="text-[13px] flex items-start gap-2">
                <span className="mt-1.5 h-1 w-1 rounded-full bg-foreground shrink-0" />
                {r}
              </li>
            ))}
          </ul>
        </Section>

        <div className="px-5 pt-5 pb-2">
          <button className="w-full h-11 rounded-md bg-primary text-primary-foreground text-[14px] font-medium">
            Add to next semester
          </button>
        </div>
      </div>
    </MobileShell>
  );
}

// ============================== Recommendations ==============================

function RecommendationsScreen() {
  return (
    <MobileShell active="courses">
      <ScreenHeader title="Recommended courses" />
      <div className="h-full overflow-y-auto scroll-thin pb-4">
        <div className="px-5 pt-4">
          <p className="text-[12px] text-muted-foreground leading-relaxed">
            Based on your courses, skills, and interests. Re-ranked nightly.
          </p>
        </div>

        {/* Ranked list, not cards */}
        <ol className="mt-3 divide-y divide-border border-y border-border">
          {RECOMMENDED.map((c, i) => (
            <RecommendedRowMobile key={c.code} course={c} rank={i + 1} />
          ))}
        </ol>

        <div className="px-5 pt-4">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-2">
            Improve recommendations
          </div>
          <button className="w-full h-10 border border-border rounded-md text-[13px] inline-flex items-center justify-center gap-2">
            <Plus className="h-3.5 w-3.5" /> Add interests and skills
          </button>
        </div>
      </div>
    </MobileShell>
  );
}

function RecommendedRowMobile({
  course,
  rank,
  compact,
}: {
  course: (typeof COURSES)[number];
  rank: number;
  compact?: boolean;
}) {
  return (
    <li className="px-5 py-3">
      <div className="flex items-start gap-3">
        <div className="text-[12px] font-medium text-muted-foreground tabular-nums w-6 shrink-0 pt-0.5">
          {String(rank).padStart(2, "0")}
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-baseline gap-2">
            <span className="text-[14px] font-medium truncate">{course.name}</span>
            <span className="text-[11px] text-muted-foreground tabular-nums">{course.code}</span>
          </div>
          <div className="text-[12px] text-muted-foreground mt-0.5">
            {course.category} · {course.difficulty} · {course.credits} credits
          </div>
          {!compact && (
            <>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {course.skills.map((s) => (
                  <span key={s} className="text-[11px] h-5 px-1.5 inline-flex items-center rounded bg-muted text-muted-foreground">
                    {s}
                  </span>
                ))}
              </div>
              <div className="text-[12px] mt-2">
                <span className="text-muted-foreground">Why:</span>{" "}
                {course.matchReasons?.[0]}
              </div>
            </>
          )}
        </div>
        <div className="w-20 shrink-0">
          <div className="text-[10px] uppercase tracking-[0.06em] text-muted-foreground mb-1">
            Match
          </div>
          <MatchMeter value={course.matchScore ?? 0} />
        </div>
      </div>
    </li>
  );
}

// ============================== Progress ==============================

function ProgressScreen() {
  const pct = Math.round(
    (STUDENT.creditsCompleted / STUDENT.creditsRequired) * 100,
  );
  return (
    <MobileShell active="progress">
      <ScreenHeader title="Progress" />
      <div className="h-full overflow-y-auto scroll-thin pb-4">
        {/* Single clear indicator */}
        <Section title="Graduation progress">
          <div className="flex items-baseline justify-between">
            <div className="text-[12px] text-muted-foreground">Credits completed</div>
            <div className="text-[12px] text-muted-foreground tabular-nums">
              {STUDENT.creditsCompleted} / {STUDENT.creditsRequired}
            </div>
          </div>
          <div className="mt-2 h-2 w-full bg-muted rounded-sm overflow-hidden">
            <div className="h-full bg-primary" style={{ width: `${pct}%` }} />
          </div>
          <div className="text-[11px] text-muted-foreground mt-2">
            {pct}% complete · On track for {STUDENT.graduation}
          </div>

          <div className="grid grid-cols-3 gap-3 mt-4">
            <Stat label="GPA" value={STUDENT.gpa.toFixed(2)} />
            <Stat label="In progress" value={`${STUDENT.creditsInProgress} cr`} />
            <Stat label="Remaining" value={`${STUDENT.creditsRequired - STUDENT.creditsCompleted} cr`} />
          </div>
        </Section>

        <Divider />

        <Section title="Current courses">
          <div className="divide-y divide-border border-y border-border">
            {IN_PROGRESS.map((c) => (
              <div key={c.code} className="py-2.5 flex items-center justify-between">
                <div>
                  <div className="text-[13px] font-medium">{c.name}</div>
                  <div className="text-[11px] text-muted-foreground tabular-nums">{c.code}</div>
                </div>
                <div className="inline-flex items-center gap-1 text-[12px] text-muted-foreground">
                  <Clock className="h-3 w-3" /> In progress
                </div>
              </div>
            ))}
          </div>
        </Section>

        <Divider />

        <Section title={`Completed · ${COMPLETED.length}`}>
          <div className="divide-y divide-border border-y border-border">
            {COMPLETED.map((c) => (
              <div key={c.code} className="py-2.5 flex items-center justify-between">
                <div className="min-w-0">
                  <div className="text-[13px] font-medium truncate">{c.name}</div>
                  <div className="text-[11px] text-muted-foreground tabular-nums">
                    {c.code} · {c.semester}
                  </div>
                </div>
                <span className="text-[13px] font-medium tabular-nums">{c.grade}</span>
              </div>
            ))}
          </div>
        </Section>
      </div>
    </MobileShell>
  );
}

// ============================== Profile ==============================

function ProfileScreen() {
  return (
    <MobileShell active="profile">
      <ScreenHeader
        title="Profile"
        right={
          <button className="h-8 w-8 grid place-items-center text-muted-foreground">
            <Settings className="h-4 w-4" />
          </button>
        }
      />
      <div className="h-full overflow-y-auto scroll-thin pb-4">
        {/* Student identity — typography, no avatar circle */}
        <div className="px-5 pt-5">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
            Student
          </div>
          <div className="text-[22px] font-semibold tracking-[-0.01em] mt-0.5">
            {STUDENT.name}
          </div>
          <div className="text-[12px] text-muted-foreground mt-0.5">
            {STUDENT.email}
          </div>
        </div>

        <Divider />

        <Section title="Student information">
          <dl className="divide-y divide-border border-y border-border">
            <Info label="Student ID" value={STUDENT.id} />
            <Info label="Major" value={STUDENT.major} />
            <Info label="Year" value={STUDENT.year} />
            <Info label="GPA" value={STUDENT.gpa.toFixed(2)} />
            <Info label="Graduation" value={STUDENT.graduation} />
          </dl>
        </Section>

        <Divider />

        <Section title="Interests">
          <div className="flex flex-wrap gap-1.5">
            {STUDENT.interests.map((i) => (
              <span
                key={i}
                className="text-[12px] h-6 px-2 inline-flex items-center rounded-md bg-accent text-accent-foreground"
              >
                {i}
              </span>
            ))}
          </div>
        </Section>

        <Divider />

        <Section title="Skills">
          <div className="flex flex-wrap gap-1.5">
            {STUDENT.skills.map((s) => (
              <span
                key={s}
                className="text-[12px] h-6 px-2 inline-flex items-center rounded-md border border-border"
              >
                {s}
              </span>
            ))}
          </div>
        </Section>

        <Divider />

        <div className="px-5 pt-4 space-y-1">
          <ProfileAction icon={<Pencil className="h-4 w-4" />}>Edit profile</ProfileAction>
          <ProfileAction icon={<Settings className="h-4 w-4" />}>Settings</ProfileAction>
          <ProfileAction icon={<LogOut className="h-4 w-4" />} danger>
            Log out
          </ProfileAction>
        </div>
      </div>
    </MobileShell>
  );
}

function ProfileAction({
  icon,
  children,
  danger,
}: {
  icon: React.ReactNode;
  children: React.ReactNode;
  danger?: boolean;
}) {
  return (
    <button
      className={
        "w-full h-11 px-3 rounded-md text-[14px] inline-flex items-center gap-3 border border-border bg-card " +
        (danger ? "text-[#b42318]" : "text-foreground")
      }
    >
      <span className={danger ? "text-[#b42318]" : "text-muted-foreground"}>{icon}</span>
      {children}
    </button>
  );
}

// ============================== States ==============================

function LoadingScreen() {
  return (
    <MobileShell active="home">
      <ScreenHeader title="Home" />
      <div className="h-full overflow-y-auto scroll-thin">
        <div className="px-5 pt-5">
          <Skeleton w="120px" h="11px" />
          <Skeleton w="200px" h="22px" className="mt-2" />
          <Skeleton w="160px" h="12px" className="mt-1" />
        </div>
        <Divider />
        <div className="px-5 pt-5 space-y-3">
          <Skeleton w="120px" h="11px" />
          <Skeleton w="100%" h="8px" />
          <Skeleton w="100%" h="40px" />
          <Skeleton w="100%" h="40px" />
        </div>
        <Divider />
        <div className="px-5 pt-5 space-y-3">
          <Skeleton w="140px" h="11px" />
          <Skeleton w="100%" h="56px" />
          <Skeleton w="100%" h="56px" />
          <Skeleton w="100%" h="56px" />
        </div>
      </div>
    </MobileShell>
  );
}

function EmptyScreen() {
  return (
    <MobileShell active="courses">
      <ScreenHeader title="Recommended courses" />
      <div className="h-full flex flex-col items-center justify-center text-center px-8">
        <div className="h-10 w-10 rounded-full border border-border grid place-items-center text-muted-foreground">
          <Star className="h-4 w-4" />
        </div>
        <div className="text-[15px] font-medium mt-3">No recommendations yet.</div>
        <p className="text-[13px] text-muted-foreground mt-1 leading-relaxed">
          Add your interests and skills to improve recommendations.
        </p>
        <button className="mt-4 h-10 px-4 rounded-md bg-primary text-primary-foreground text-[13px] font-medium inline-flex items-center gap-2">
          <Plus className="h-3.5 w-3.5" /> Add interests
        </button>
      </div>
    </MobileShell>
  );
}

function ErrorScreen() {
  return (
    <MobileShell active="courses">
      <ScreenHeader title="Courses" />
      <div className="h-full flex flex-col items-center justify-center text-center px-8">
        <div className="h-10 w-10 rounded-full border border-[#b42318]/30 bg-[#fbeae8] grid place-items-center text-[#b42318]">
          <AlertTriangle className="h-4 w-4" />
        </div>
        <div className="text-[15px] font-medium mt-3">Courses couldn't be loaded.</div>
        <p className="text-[13px] text-muted-foreground mt-1 leading-relaxed">
          Check your connection and try again.
        </p>
        <button className="mt-4 h-10 px-4 rounded-md border border-border bg-card text-[13px] font-medium inline-flex items-center gap-2">
          <Loader2 className="h-3.5 w-3.5" /> Try again
        </button>
      </div>
    </MobileShell>
  );
}

function OfflineScreen() {
  return (
    <MobileShell active="home">
      <ScreenHeader title="Home" />
      <div className="h-full flex flex-col items-center justify-center text-center px-8">
        <div className="h-10 w-10 rounded-full border border-border bg-muted grid place-items-center text-muted-foreground">
          <WifiOff className="h-4 w-4" />
        </div>
        <div className="text-[15px] font-medium mt-3">You're offline.</div>
        <p className="text-[13px] text-muted-foreground mt-1 leading-relaxed max-w-[260px]">
          Course browsing and the assistant are unavailable. Your completed courses and progress are still visible.
        </p>
        <div className="mt-4 text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
          Last synced · 9:42 AM
        </div>
      </div>
    </MobileShell>
  );
}

// ============================== Shared ==============================

function Divider() {
  return <div className="h-px bg-border" />;
}

function Section({
  title,
  right,
  children,
}: {
  title: React.ReactNode;
  right?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section className="px-5 py-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground font-medium">
          {title}
        </h2>
        {right}
      </div>
      {children}
    </section>
  );
}

function Stat({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="border border-border p-2.5">
      <div className="text-[10px] uppercase tracking-[0.06em] text-muted-foreground">
        {label}
      </div>
      <div className="text-[14px] font-medium mt-0.5 tabular-nums">{value}</div>
    </div>
  );
}

function Info({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="py-2.5 flex items-center justify-between">
      <dt className="text-[12px] text-muted-foreground">{label}</dt>
      <dd className="text-[13px] font-medium tabular-nums">{value}</dd>
    </div>
  );
}

function Skeleton({
  w,
  h,
  className = "",
}: {
  w: string;
  h: string;
  className?: string;
}) {
  return (
    <div
      className={"bg-muted animate-pulse rounded-sm " + className}
      style={{ width: w, height: h }}
    />
  );
}

// Unused — silence lint
export const _icons = { X, Star };
