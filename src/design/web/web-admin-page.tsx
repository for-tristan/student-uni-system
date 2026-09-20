"use client";

import * as React from "react";
import {
  GraduationCap,
  LayoutGrid,
  Users,
  BookOpen,
  Sparkles,
  MessageSquare,
  Settings,
  Search,
  ChevronRight,
  Bell,
  Plus,
  Filter,
  Pencil,
  Trash2,
  Eye,
  Download,
  CheckCircle2,
  TrendingUp,
  TrendingDown,
} from "lucide-react";
import { BrowserFrame } from "../shell/frames";
import {
  STAFF_STATS,
  POPULAR_COURSES,
  RECOMMENDATION_TREND,
  STUDENTS,
  COURSES,
  STUDENT,
  COMPLETED,
  IN_PROGRESS,
  RECOMMENDED,
} from "../data/mock";
import { DifficultyTag, StatusPill, MatchMeter } from "../shell/primitives";

type AdminPage =
  | "overview"
  | "students"
  | "student-details"
  | "courses"
  | "course-details"
  | "recommendations"
  | "assistant";

export function WebAdminPage() {
  const [page, setPage] = React.useState<AdminPage>("overview");

  return (
    <div className="space-y-8">
      <section>
        <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
          06 — Web · Admin
        </div>
        <h1 className="text-[26px] font-semibold tracking-[-0.01em]">
          University staff platform
        </h1>
        <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
          A serious internal application. Persistent sidebar, dense tables, information
          over decoration. Designed for the people who actually run the catalog and the
          recommendation system.
        </p>
      </section>

      <div className="flex flex-wrap gap-1">
        {[
          ["overview", "Overview"],
          ["students", "Students"],
          ["student-details", "Student details"],
          ["courses", "Courses"],
          ["course-details", "Course details"],
          ["recommendations", "Recommendations"],
          ["assistant", "Assistant"],
        ].map(([id, label]) => (
          <button
            key={id}
            onClick={() => setPage(id as AdminPage)}
            className={
              "h-8 px-3 text-[12px] rounded-md border " +
              (page === id
                ? "bg-foreground text-background border-foreground"
                : "bg-card border-border text-muted-foreground hover:text-foreground")
            }
          >
            {label}
          </button>
        ))}
      </div>

      <BrowserFrame
        width={1440}
        height={900}
        url="assistant.uni.edu/admin"
        label={currentLabel(page)}
        caption="1440 × 900"
      >
        <AdminLayout page={page}>{renderPage(page)}</AdminLayout>
      </BrowserFrame>
    </div>
  );
}

function currentLabel(page: AdminPage): string {
  const map: Record<AdminPage, string> = {
    overview: "Overview",
    students: "Students",
    "student-details": "Student details",
    courses: "Courses",
    "course-details": "Course details",
    recommendations: "Recommendations",
    assistant: "Assistant",
  };
  return map[page];
}

function renderPage(page: AdminPage): React.ReactNode {
  switch (page) {
    case "overview":
      return <OverviewPage />;
    case "students":
      return <StudentsPage />;
    case "student-details":
      return <StudentDetailsPage />;
    case "courses":
      return <CoursesPage />;
    case "course-details":
      return <CourseDetailsPage />;
    case "recommendations":
      return <RecommendationsPage />;
    case "assistant":
      return <AdminAssistantPage />;
  }
}

// ============================== Layout ==============================

export function AdminPageView({ page }: { page: AdminPage }) {
  return (
    <AdminLayout page={page}>{renderPage(page)}</AdminLayout>
  );
}

function AdminLayout({
  page,
  children,
}: {
  page: AdminPage;
  children: React.ReactNode;
}) {
  const navItems: { id: AdminPage; label: string; icon: React.ReactNode }[] = [
    { id: "overview", label: "Overview", icon: <LayoutGrid className="h-3.5 w-3.5" /> },
    { id: "students", label: "Students", icon: <Users className="h-3.5 w-3.5" /> },
    { id: "courses", label: "Courses", icon: <BookOpen className="h-3.5 w-3.5" /> },
    { id: "recommendations", label: "Recommendations", icon: <Sparkles className="h-3.5 w-3.5" /> },
    { id: "assistant", label: "Assistant", icon: <MessageSquare className="h-3.5 w-3.5" /> },
    { id: "assistant" as any, label: "Settings", icon: <Settings className="h-3.5 w-3.5" /> },
  ];
  return (
    <div className="h-full flex bg-background">
      <aside className="w-56 border-r border-border bg-card flex flex-col">
        <div className="h-12 px-4 flex items-center gap-2 border-b border-border">
          <div className="h-6 w-6 rounded-md bg-foreground text-background grid place-items-center">
            <GraduationCap className="h-3.5 w-3.5" />
          </div>
          <div>
            <div className="text-[12px] font-semibold leading-tight">Smart University</div>
            <div className="text-[10px] text-muted-foreground leading-tight">Admin</div>
          </div>
        </div>
        <nav className="flex-1 p-2 space-y-0.5">
          {navItems.map((it, i) => (
            <div
              key={i}
              className={
                "flex items-center gap-2 h-8 px-2 rounded-md text-[12px] " +
                ((it.id === page && it.label !== "Settings") ? "bg-accent text-accent-foreground font-medium" : "text-muted-foreground")
              }
            >
              {it.icon}
              {it.label}
            </div>
          ))}
        </nav>
        <div className="p-3 border-t border-border">
          <div className="flex items-center gap-2">
            <div className="h-7 w-7 rounded-full bg-muted text-foreground grid place-items-center text-[11px] font-medium">
              DK
            </div>
            <div className="min-w-0">
              <div className="text-[12px] font-medium truncate">Dr. Karim</div>
              <div className="text-[10px] text-muted-foreground truncate">Registrar</div>
            </div>
          </div>
        </div>
      </aside>
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-12 border-b border-border bg-card flex items-center px-5 gap-4">
          <Breadcrumbs page={page} />
          <div className="flex-1" />
          <div className="relative w-72">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <input
              className="h-8 w-full pl-8 pr-3 rounded-md border border-border bg-background text-[12px]"
              placeholder="Search students, courses…"
            />
          </div>
          <button className="h-8 w-8 grid place-items-center text-muted-foreground border border-border rounded-md">
            <Bell className="h-3.5 w-3.5" />
          </button>
        </header>
        <div className="flex-1 overflow-y-auto scroll-thin">{children}</div>
      </div>
    </div>
  );
}

function Breadcrumbs({ page }: { page: AdminPage }) {
  const map: Record<AdminPage, string[]> = {
    overview: ["Admin", "Overview"],
    students: ["Admin", "Students"],
    "student-details": ["Admin", "Students", "Ahmed Samir"],
    courses: ["Admin", "Courses"],
    "course-details": ["Admin", "Courses", "Machine Learning"],
    recommendations: ["Admin", "Recommendations"],
    assistant: ["Admin", "Assistant"],
  };
  const items = map[page];
  return (
    <nav className="flex items-center gap-1.5 text-[12px]">
      {items.map((it, i) => (
        <React.Fragment key={i}>
          {i > 0 && <ChevronRight className="h-3 w-3 text-muted-foreground" />}
          <span
            className={
              i === items.length - 1
                ? "text-foreground font-medium"
                : "text-muted-foreground"
            }
          >
            {it}
          </span>
        </React.Fragment>
      ))}
    </nav>
  );
}

// ============================== Pages ==============================

function OverviewPage() {
  return (
    <div className="p-6 space-y-5">
      <PageHead
        title="Overview"
        subtitle="A real summary of what is happening in the system today."
      />

      {/* Numbers — inline list, not a 6-card grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-border border-y border-border">
        <Kpi label="Students" value={STAFF_STATS.students.toLocaleString()} delta="+24 this week" trend="up" />
        <Kpi label="Courses" value={String(STAFF_STATS.courses)} delta="3 new this term" trend="up" />
        <Kpi
          label="Recommendations today"
          value={String(STAFF_STATS.recommendationsToday)}
          delta="+18% vs last week"
          trend="up"
        />
        <Kpi
          label="Active conversations"
          value={String(STAFF_STATS.activeConversations)}
          delta="— stable"
          trend="flat"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Recommendation activity chart */}
        <section className="lg:col-span-2 bg-card border border-border p-5">
          <div className="flex items-baseline justify-between">
            <div>
              <h2 className="text-[14px] font-semibold">Recommendation activity</h2>
              <p className="text-[12px] text-muted-foreground mt-0.5">
                Past 7 days · recommendations served across all students.
              </p>
            </div>
            <button className="text-[12px] text-muted-foreground inline-flex items-center gap-1">
              <Download className="h-3 w-3" /> Export
            </button>
          </div>
          <div className="mt-4">
            <BarChart data={RECOMMENDATION_TREND} />
          </div>
        </section>

        {/* Popular courses */}
        <section className="bg-card border border-border p-5">
          <h2 className="text-[14px] font-semibold">Popular courses</h2>
          <p className="text-[12px] text-muted-foreground mt-0.5">
            By enrollment this term.
          </p>
          <div className="mt-4 divide-y divide-border">
            {POPULAR_COURSES.map((c) => (
              <div key={c.code} className="py-2.5 flex items-center justify-between">
                <div className="min-w-0">
                  <div className="text-[13px] font-medium truncate">{c.name}</div>
                  <div className="text-[11px] text-muted-foreground tabular-nums">{c.code}</div>
                </div>
                <div className="text-right">
                  <div className="text-[13px] font-medium tabular-nums">{c.enrolled}</div>
                  <div
                    className={
                      "text-[10px] inline-flex items-center gap-0.5 " +
                      (c.trend >= 0 ? "text-[#2f7d4a]" : "text-[#b42318]")
                    }
                  >
                    {c.trend >= 0 ? <TrendingUp className="h-2.5 w-2.5" /> : <TrendingDown className="h-2.5 w-2.5" />}
                    {Math.abs(c.trend)}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Recent activity */}
      <section className="bg-card border border-border">
        <div className="px-5 py-4 border-b border-border">
          <h2 className="text-[14px] font-semibold">Recent activity</h2>
        </div>
        <div className="divide-y divide-border">
          {[
            ["Layla Hassan enrolled in CS-460", "12 min ago"],
            ["Mariam Tarek moved to probation", "1 hour ago"],
            ["New course CS-488 added to catalog", "3 hours ago"],
            ["Recommendation model retrained (v2.3.1)", "Today, 06:00"],
          ].map(([t, w]) => (
            <div key={t} className="px-5 py-3 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                <span className="text-[13px]">{t}</span>
              </div>
              <span className="text-[11px] text-muted-foreground">{w}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function StudentsPage() {
  return (
    <div className="p-6 space-y-4">
      <PageHead
        title="Students"
        subtitle="Search, filter, and review student records."
        right={
          <div className="flex gap-2">
            <button className="h-9 px-3 border border-border rounded-md text-[12px] bg-card inline-flex items-center gap-1.5">
              <Filter className="h-3 w-3" /> Filters
            </button>
            <button className="h-9 px-3 bg-primary text-primary-foreground rounded-md text-[12px] font-medium inline-flex items-center gap-1.5">
              <Plus className="h-3.5 w-3.5" /> Add student
            </button>
          </div>
        }
      />

      <div className="bg-card border border-border overflow-hidden">
        <div className="px-4 py-2 border-b border-border flex items-center gap-3">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <input
              className="h-8 w-full pl-8 pr-3 rounded-md border border-border bg-background text-[12px]"
              placeholder="Search by name, ID, or major"
            />
          </div>
          <select className="h-8 px-2 rounded-md border border-border bg-background text-[12px]">
            <option>All majors</option>
            <option>Computer Science</option>
            <option>Data Science</option>
          </select>
          <select className="h-8 px-2 rounded-md border border-border bg-background text-[12px]">
            <option>All years</option>
            <option>Year 1</option>
            <option>Year 2</option>
          </select>
          <select className="h-8 px-2 rounded-md border border-border bg-background text-[12px]">
            <option>All statuses</option>
            <option>Active</option>
            <option>Probation</option>
          </select>
          <div className="flex-1" />
          <span className="text-[11px] text-muted-foreground">{STUDENTS.length} students</span>
        </div>

        <table className="w-full text-[13px]">
          <thead>
            <tr className="border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground bg-muted/30">
              <Th>Student</Th>
              <Th>Student ID</Th>
              <Th>Major</Th>
              <Th>Year</Th>
              <Th>GPA</Th>
              <Th>Status</Th>
              <Th className="text-right">Actions</Th>
            </tr>
          </thead>
          <tbody>
            {STUDENTS.map((s, i) => (
              <tr key={s.id} className={"border-b border-border " + (i % 2 ? "bg-muted/20" : "")}>
                <Td>
                  <div className="flex items-center gap-2.5">
                    <div className="h-7 w-7 rounded-full bg-muted text-foreground grid place-items-center text-[11px] font-medium">
                      {s.name.split(" ").map((n) => n[0]).join("")}
                    </div>
                    <div className="font-medium">{s.name}</div>
                  </div>
                </Td>
                <Td><code className="text-[12px] text-muted-foreground tabular-nums">{s.id}</code></Td>
                <Td>{s.major}</Td>
                <Td>{s.year}</Td>
                <Td className="tabular-nums">{s.gpa.toFixed(2)}</Td>
                <Td>
                  <StatusPill
                    kind={
                      s.status === "Active" ? "success" : s.status === "Probation" ? "warning" : "neutral"
                    }
                  >
                    {s.status}
                  </StatusPill>
                </Td>
                <Td className="text-right">
                  <div className="inline-flex gap-1">
                    <RowAction icon={<Eye className="h-3.5 w-3.5" />} />
                    <RowAction icon={<Pencil className="h-3.5 w-3.5" />} />
                    <RowAction icon={<Trash2 className="h-3.5 w-3.5" />} danger />
                  </div>
                </Td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="px-4 py-3 border-t border-border flex items-center justify-between text-[12px] text-muted-foreground">
          <div>Showing 1–{STUDENTS.length} of 1,248</div>
          <div className="flex items-center gap-1">
            <PageBtn>‹</PageBtn>
            <PageBtn active>1</PageBtn>
            <PageBtn>2</PageBtn>
            <PageBtn>3</PageBtn>
            <PageBtn>…</PageBtn>
            <PageBtn>125</PageBtn>
            <PageBtn>›</PageBtn>
          </div>
        </div>
      </div>
    </div>
  );
}

function StudentDetailsPage() {
  return (
    <div className="p-6 space-y-5">
      <PageHead
        title={STUDENT.name}
        subtitle={`${STUDENT.id} · ${STUDENT.major} · ${STUDENT.year}`}
        right={
          <div className="flex gap-2">
            <button className="h-9 px-3 border border-border rounded-md text-[12px] bg-card inline-flex items-center gap-1.5">
              <Download className="h-3 w-3" /> Export transcript
            </button>
            <button className="h-9 px-3 bg-primary text-primary-foreground rounded-md text-[12px] font-medium inline-flex items-center gap-1.5">
              <Pencil className="h-3.5 w-3.5" /> Edit
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Student information */}
        <section className="bg-card border border-border p-5">
          <SectionH>Student information</SectionH>
          <dl className="mt-3 divide-y divide-border border-y border-border">
            <DetailRow label="Student ID" value={STUDENT.id} />
            <DetailRow label="Email" value={STUDENT.email} />
            <DetailRow label="Major" value={STUDENT.major} />
            <DetailRow label="Year" value={STUDENT.year} />
            <DetailRow label="GPA" value={STUDENT.gpa.toFixed(2)} />
            <DetailRow label="Graduation" value={STUDENT.graduation} />
          </dl>
        </section>

        {/* Academic progress */}
        <section className="bg-card border border-border p-5">
          <SectionH>Academic progress</SectionH>
          <div className="mt-3">
            <div className="flex items-baseline justify-between">
              <span className="text-[12px] text-muted-foreground">Credits completed</span>
              <span className="text-[12px] text-muted-foreground tabular-nums">
                {STUDENT.creditsCompleted} / {STUDENT.creditsRequired}
              </span>
            </div>
            <div className="mt-2 h-2 w-full bg-muted rounded-sm overflow-hidden">
              <div
                className="h-full bg-primary"
                style={{
                  width: `${(STUDENT.creditsCompleted / STUDENT.creditsRequired) * 100}%`,
                }}
              />
            </div>
            <div className="grid grid-cols-3 gap-2 mt-4">
              <MiniStat label="Completed" value={String(COMPLETED.length)} />
              <MiniStat label="In progress" value={String(IN_PROGRESS.length)} />
              <MiniStat label="Remaining" value={String(STUDENT.creditsRequired - STUDENT.creditsCompleted)} />
            </div>
          </div>
        </section>

        {/* Interests + skills */}
        <section className="bg-card border border-border p-5">
          <SectionH>Interests &amp; skills</SectionH>
          <div className="mt-3">
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">Interests</div>
            <div className="mt-1.5 flex flex-wrap gap-1.5">
              {STUDENT.interests.map((i) => (
                <span key={i} className="text-[12px] h-6 px-2 inline-flex items-center rounded-md bg-accent text-accent-foreground">
                  {i}
                </span>
              ))}
            </div>
            <div className="mt-3 text-[11px] uppercase tracking-[0.06em] text-muted-foreground">Skills</div>
            <div className="mt-1.5 flex flex-wrap gap-1.5">
              {STUDENT.skills.map((s) => (
                <span key={s} className="text-[12px] h-6 px-2 inline-flex items-center rounded-md border border-border">
                  {s}
                </span>
              ))}
            </div>
          </div>
        </section>
      </div>

      {/* Tabs: completed / current / recommended */}
      <section className="bg-card border border-border">
        <div className="border-b border-border">
          <div className="flex px-5 gap-6">
            <Tab2 active>Completed ({COMPLETED.length})</Tab2>
            <Tab2>Current ({IN_PROGRESS.length})</Tab2>
            <Tab2>Recommended ({RECOMMENDED.length})</Tab2>
          </div>
        </div>
        <table className="w-full text-[13px]">
          <thead>
            <tr className="border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground bg-muted/30">
              <Th>Course</Th>
              <Th>Category</Th>
              <Th className="text-right">Credits</Th>
              <Th>Difficulty</Th>
              <Th>Semester</Th>
              <Th className="text-right">Grade</Th>
            </tr>
          </thead>
          <tbody>
            {COMPLETED.map((c) => (
              <tr key={c.code} className="border-b border-border">
                <Td>
                  <div className="font-medium">{c.name}</div>
                  <div className="text-[11px] text-muted-foreground tabular-nums">{c.code}</div>
                </Td>
                <Td>{c.category}</Td>
                <Td className="text-right tabular-nums">{c.credits}</Td>
                <Td><DifficultyTag level={c.difficulty} /></Td>
                <Td>{c.semester}</Td>
                <Td className="text-right">
                  <span className="font-medium tabular-nums">{c.grade}</span>
                </Td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

function CoursesPage() {
  return (
    <div className="p-6 space-y-4">
      <PageHead
        title="Courses"
        subtitle="Manage the university catalog."
        right={
          <div className="flex gap-2">
            <button className="h-9 px-3 border border-border rounded-md text-[12px] bg-card inline-flex items-center gap-1.5">
              <Download className="h-3 w-3" /> Export
            </button>
            <button className="h-9 px-3 bg-primary text-primary-foreground rounded-md text-[12px] font-medium inline-flex items-center gap-1.5">
              <Plus className="h-3.5 w-3.5" /> Add course
            </button>
          </div>
        }
      />

      <div className="bg-card border border-border overflow-hidden">
        <div className="px-4 py-2 border-b border-border flex items-center gap-3">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <input
              className="h-8 w-full pl-8 pr-3 rounded-md border border-border bg-background text-[12px]"
              placeholder="Search by name or code"
            />
          </div>
          <select className="h-8 px-2 rounded-md border border-border bg-background text-[12px]">
            <option>All categories</option>
            <option>AI</option>
            <option>Systems</option>
            <option>Data</option>
          </select>
          <select className="h-8 px-2 rounded-md border border-border bg-background text-[12px]">
            <option>All difficulties</option>
            <option>Introductory</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
          <div className="flex-1" />
          <span className="text-[11px] text-muted-foreground">{COURSES.length} courses</span>
        </div>

        <table className="w-full text-[13px]">
          <thead>
            <tr className="border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground bg-muted/30">
              <Th>Course</Th>
              <Th>Category</Th>
              <Th className="text-right">Credits</Th>
              <Th>Difficulty</Th>
              <Th>Prerequisites</Th>
              <Th className="text-right">Students</Th>
              <Th className="text-right">Actions</Th>
            </tr>
          </thead>
          <tbody>
            {COURSES.slice(0, 8).map((c, i) => (
              <tr key={c.code} className={"border-b border-border " + (i % 2 ? "bg-muted/20" : "")}>
                <Td>
                  <div className="font-medium">{c.name}</div>
                  <div className="text-[11px] text-muted-foreground tabular-nums">{c.code}</div>
                </Td>
                <Td>{c.category}</Td>
                <Td className="text-right tabular-nums">{c.credits}</Td>
                <Td><DifficultyTag level={c.difficulty} /></Td>
                <Td>
                  <div className="flex flex-wrap gap-1">
                    {c.prerequisites.length === 0 ? (
                      <span className="text-[12px] text-muted-foreground">—</span>
                    ) : (
                      c.prerequisites.map((p) => (
                        <code key={p} className="text-[11px] text-muted-foreground tabular-nums px-1 py-0.5 border border-border rounded">
                          {p}
                        </code>
                      ))
                    )}
                  </div>
                </Td>
                <Td className="text-right tabular-nums">{c.enrolled}/{c.capacity}</Td>
                <Td className="text-right">
                  <div className="inline-flex gap-1">
                    <RowAction icon={<Eye className="h-3.5 w-3.5" />} />
                    <RowAction icon={<Pencil className="h-3.5 w-3.5" />} />
                    <RowAction icon={<Trash2 className="h-3.5 w-3.5" />} danger />
                  </div>
                </Td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="px-4 py-3 border-t border-border flex items-center justify-between text-[12px] text-muted-foreground">
          <div>Showing 1–8 of 86</div>
          <div className="flex items-center gap-1">
            <PageBtn>‹</PageBtn>
            <PageBtn active>1</PageBtn>
            <PageBtn>2</PageBtn>
            <PageBtn>3</PageBtn>
            <PageBtn>…</PageBtn>
            <PageBtn>11</PageBtn>
            <PageBtn>›</PageBtn>
          </div>
        </div>
      </div>
    </div>
  );
}

function CourseDetailsPage() {
  const course = COURSES[0];
  return (
    <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-5">
      {/* Course information — left, 2/3 width */}
      <div className="lg:col-span-2 space-y-5">
        <PageHead
          title={course.name}
          subtitle={`${course.code} · ${course.category} · ${course.credits} credits`}
        />

        <section className="bg-card border border-border p-5">
          <SectionH>Overview</SectionH>
          <p className="text-[13px] mt-2 leading-relaxed">
            An introduction to supervised, unsupervised, and reinforcement learning.
            Covers linear models, decision trees, neural networks, and model evaluation.
            Includes a semester-long applied project on a real dataset.
          </p>
        </section>

        <section className="bg-card border border-border p-5">
          <SectionH>Prerequisites</SectionH>
          <div className="mt-3 divide-y divide-border border-y border-border">
            {course.prerequisites.map((code) => {
              const p = COURSES.find((c) => c.code === code);
              return (
                <div key={code} className="py-2.5 flex items-center justify-between">
                  <div>
                    <div className="text-[13px] font-medium">{p?.name}</div>
                    <div className="text-[11px] text-muted-foreground tabular-nums">{code}</div>
                  </div>
                  <DifficultyTag level={p?.difficulty ?? "Introductory"} />
                </div>
              );
            })}
          </div>
        </section>

        <section className="bg-card border border-border p-5">
          <SectionH>Skills taught</SectionH>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {course.skills.map((s) => (
              <span key={s} className="text-[12px] h-6 px-2 inline-flex items-center rounded-md border border-border">
                {s}
              </span>
            ))}
          </div>
        </section>

        <section className="bg-card border border-border p-5">
          <SectionH>Enrollment</SectionH>
          <div className="mt-3 grid grid-cols-3 gap-4">
            <MiniStat label="Enrolled" value={`${course.enrolled}`} />
            <MiniStat label="Capacity" value={`${course.capacity}`} />
            <MiniStat label="Fill rate" value={`${Math.round((course.enrolled / course.capacity) * 100)}%`} />
          </div>
        </section>
      </div>

      {/* Edit panel — right, clearly separated from informational content */}
      <aside className="space-y-5">
        <section className="bg-card border border-border p-5">
          <div className="flex items-center justify-between">
            <SectionH>Edit course</SectionH>
            <span className="text-[11px] text-muted-foreground">Editing</span>
          </div>
          <div className="mt-3 space-y-3">
            <Field label="Name">
              <input
                className="h-9 w-full px-3 rounded-md border border-border bg-background text-[13px]"
                defaultValue={course.name}
              />
            </Field>
            <Field label="Credits">
              <input
                className="h-9 w-full px-3 rounded-md border border-border bg-background text-[13px] tabular-nums"
                defaultValue={String(course.credits)}
              />
            </Field>
            <Field label="Difficulty">
              <select className="h-9 w-full px-2 rounded-md border border-border bg-background text-[13px]">
                <option>Introductory</option>
                <option>Intermediate</option>
                <option selected>Advanced</option>
              </select>
            </Field>
            <Field label="Capacity">
              <input
                className="h-9 w-full px-3 rounded-md border border-border bg-background text-[13px] tabular-nums"
                defaultValue={String(course.capacity)}
              />
            </Field>
            <div className="flex gap-2 pt-1">
              <button className="h-9 flex-1 border border-border rounded-md text-[13px] bg-background">
                Cancel
              </button>
              <button className="h-9 flex-1 bg-primary text-primary-foreground rounded-md text-[13px] font-medium">
                Save
              </button>
            </div>
          </div>
        </section>

        <section className="bg-card border border-border p-5">
          <SectionH>Danger zone</SectionH>
          <button className="mt-3 w-full h-9 border border-[#b42318]/30 text-[#b42318] rounded-md text-[12px] font-medium inline-flex items-center justify-center gap-1.5">
            <Trash2 className="h-3.5 w-3.5" /> Delete course
          </button>
        </section>
      </aside>
    </div>
  );
}

function RecommendationsPage() {
  return (
    <div className="p-6 space-y-5">
      <PageHead
        title="Recommendations"
        subtitle="Understand what the recommendation engine is doing."
        right={
          <button className="h-9 px-3 border border-border rounded-md text-[12px] bg-card inline-flex items-center gap-1.5">
            <Download className="h-3 w-3" /> Export
          </button>
        }
      />

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-border border-y border-border">
        <Kpi label="Precision@5" value={STAFF_STATS.precisionAt5.toFixed(2)} delta="+0.04 vs v2.2" trend="up" />
        <Kpi label="Recall@5" value={STAFF_STATS.recallAt5.toFixed(2)} delta="+0.02" trend="up" />
        <Kpi label="Coverage" value={`${Math.round(STAFF_STATS.avgCoverage * 100)}%`} delta="stable" trend="flat" />
        <Kpi label="Model version" value="v2.3.1" delta="retrained 06:00" trend="flat" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Most recommended courses */}
        <section className="lg:col-span-2 bg-card border border-border">
          <div className="px-5 py-4 border-b border-border">
            <h2 className="text-[14px] font-semibold">Most recommended courses</h2>
            <p className="text-[12px] text-muted-foreground mt-0.5">
              Past 7 days · by recommendation count.
            </p>
          </div>
          <table className="w-full text-[13px]">
            <thead>
              <tr className="border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground bg-muted/30">
                <Th>Course</Th>
                <Th className="text-right">Recommendations</Th>
                <Th className="text-right">Acceptance</Th>
                <Th>Acceptance</Th>
              </tr>
            </thead>
            <tbody>
              {[
                ["Machine Learning", "CS-421", 412, 0.62],
                ["Data Mining", "CS-432", 318, 0.48],
                ["Distributed Systems", "CS-371", 274, 0.41],
                ["Database Systems II", "CS-352", 240, 0.55],
                ["Computer Vision", "CS-460", 188, 0.38],
              ].map(([name, code, count, acc], i) => (
                <tr key={code as string} className={"border-b border-border " + (i % 2 ? "bg-muted/20" : "")}>
                  <Td>
                    <div className="font-medium">{name}</div>
                    <div className="text-[11px] text-muted-foreground tabular-nums">{code}</div>
                  </Td>
                  <Td className="text-right tabular-nums">{count as number}</Td>
                  <Td className="text-right tabular-nums">{Math.round((acc as number) * 100)}%</Td>
                  <Td>
                    <div className="w-32">
                      <MatchMeter value={(acc as number) * 100} />
                    </div>
                  </Td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Recommendation evaluation */}
        <section className="bg-card border border-border p-5">
          <SectionH>Evaluation</SectionH>
          <p className="text-[12px] text-muted-foreground mt-1">
            Held-out test set · 1,000 students · Fall 2024.
          </p>
          <div className="mt-4 space-y-3">
            <MetricBar label="Precision@5" value={STAFF_STATS.precisionAt5} />
            <MetricBar label="Recall@5" value={STAFF_STATS.recallAt5} />
            <MetricBar label="Coverage" value={STAFF_STATS.avgCoverage} />
            <MetricBar label="Diversity" value={0.69} />
          </div>
        </section>
      </div>

      {/* Recent recommendations */}
      <section className="bg-card border border-border">
        <div className="px-5 py-4 border-b border-border">
          <h2 className="text-[14px] font-semibold">Recent recommendations</h2>
        </div>
        <div className="divide-y divide-border">
          {[
            ["Layla Hassan", "Machine Learning", "CS-421", "92% match", "3 min ago"],
            ["Omar Khaled", "Data Mining", "CS-432", "88% match", "12 min ago"],
            ["Mariam Tarek", "Database Systems II", "CS-352", "79% match", "28 min ago"],
            ["Yousef Adel", "Distributed Systems", "CS-371", "84% match", "1 hour ago"],
          ].map(([s, c, code, m, w], i) => (
            <div key={i} className="px-5 py-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="h-3.5 w-3.5 text-[#2f7d4a]" />
                <div>
                  <div className="text-[13px]">
                    <span className="font-medium">{s}</span> ←{" "}
                    <span className="font-medium">{c}</span>{" "}
                    <code className="text-[11px] text-muted-foreground tabular-nums">{code}</code>
                  </div>
                  <div className="text-[11px] text-muted-foreground">{m}</div>
                </div>
              </div>
              <span className="text-[11px] text-muted-foreground">{w}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function AdminAssistantPage() {
  return (
    <div className="h-full flex">
      {/* Conversation list */}
      <aside className="w-72 border-r border-border bg-card flex flex-col">
        <div className="px-4 h-12 border-b border-border flex items-center justify-between">
          <div className="text-[13px] font-medium">Conversations</div>
          <button className="h-7 px-2 text-[11px] border border-border rounded-md">New</button>
        </div>
        <div className="p-2 border-b border-border">
          <div className="relative">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <input
              className="h-8 w-full pl-8 pr-3 rounded-md border border-border bg-background text-[12px]"
              placeholder="Search conversations"
            />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto scroll-thin divide-y divide-border">
          {[
            ["Ahmed Samir", "Prerequisites for Machine Learning?", "12 min ago", true],
            ["Layla Hassan", "Which courses next semester?", "1 hour ago", false],
            ["Omar Khaled", "What courses have I completed?", "3 hours ago", false],
            ["Mariam Tarek", "Explain the Data Mining course", "Yesterday", false],
            ["Yousef Adel", "How many credits do I have left?", "Yesterday", false],
            ["Salma Nabil", "Prerequisites for Cloud Computing?", "2 days ago", false],
          ].map(([name, preview, w, active], i) => (
            <button
              key={i}
              className={
                "w-full text-left px-4 py-3 " +
                (active ? "bg-accent/60" : "hover:bg-muted/40")
              }
            >
              <div className="flex items-center justify-between">
                <div className="text-[13px] font-medium truncate">{name}</div>
                <span className="text-[10px] text-muted-foreground shrink-0 ml-2">{w}</span>
              </div>
              <div className="text-[12px] text-muted-foreground truncate mt-0.5">
                {preview}
              </div>
            </button>
          ))}
        </div>
      </aside>

      {/* Conversation */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="px-5 h-12 border-b border-border flex items-center justify-between bg-card">
          <div className="flex items-center gap-3">
            <div className="h-7 w-7 rounded-full bg-muted text-foreground grid place-items-center text-[11px] font-medium">
              AS
            </div>
            <div>
              <div className="text-[13px] font-medium">Ahmed Samir</div>
              <div className="text-[10px] text-muted-foreground">
                S-2023-1148 · {STUDENT.major} · {STUDENT.year}
              </div>
            </div>
          </div>
          <div className="text-[11px] text-muted-foreground">
            Student context: {STUDENT.major} · {STUDENT.year}
          </div>
        </header>

        <div className="flex-1 overflow-y-auto scroll-thin px-6 py-5 space-y-5 max-w-3xl">
          <WebMessage
            role="user"
            content="What are the prerequisites for Machine Learning?"
          />
          <WebMessage
            role="assistant"
            content={
              <>
                <p>Machine Learning (CS-421) requires the following prerequisites:</p>
                <ol className="mt-2 space-y-1 text-muted-foreground">
                  <li>1. Algorithms (CS-221) — completed, grade A.</li>
                  <li>2. Probability &amp; Statistics (MATH-204) — completed, grade A-.</li>
                </ol>
                <p className="mt-2">Both prerequisites are satisfied, so the student is eligible to enroll.</p>
              </>
            }
            sources={[
              { label: "Course catalog", code: "CS-421" },
              { label: "Student transcript", code: "S-2023-1148" },
            ]}
          />

          <WebMessage role="user" content="Which courses can I take next semester?" />
          <WebMessage
            role="assistant"
            content={
              <>
                <p>Based on completed courses and current skills, the following are available next semester:</p>
                <ul className="mt-2 space-y-1">
                  <li>• Machine Learning (CS-421) — Advanced, 3 credits</li>
                  <li>• Data Mining (CS-432) — Advanced, 3 credits</li>
                  <li>• Distributed Systems (CS-371) — Advanced, 4 credits</li>
                </ul>
                <p className="mt-2">The student can enroll in up to 18 credits without dean approval.</p>
              </>
            }
            sources={[
              { label: "Academic regulations", code: "§4.2" },
            ]}
          />
        </div>

        <div className="border-t border-border bg-card p-3">
          <div className="flex items-end gap-2 max-w-3xl">
            <textarea
              rows={1}
              placeholder="Reply as university assistant…"
              className="flex-1 resize-none min-h-[40px] max-h-32 px-3 py-2 rounded-md border border-border bg-background text-[13px]"
            />
            <button className="h-10 px-4 rounded-md bg-primary text-primary-foreground text-[13px] font-medium">
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================== Shared small components ==============================

function PageHead({
  title,
  subtitle,
  right,
}: {
  title: string;
  subtitle?: string;
  right?: React.ReactNode;
}) {
  return (
    <div className="flex items-end justify-between gap-4">
      <div>
        <h1 className="text-[20px] font-semibold tracking-[-0.01em]">{title}</h1>
        {subtitle && (
          <div className="text-[12px] text-muted-foreground mt-0.5">{subtitle}</div>
        )}
      </div>
      {right}
    </div>
  );
}

function SectionH({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground font-medium">
      {children}
    </h2>
  );
}

function Th({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <th className={"text-left font-medium px-4 py-2.5 " + className}>{children}</th>;
}

function Td({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <td className={"px-4 py-3 align-middle " + className}>{children}</td>;
}

function Kpi({
  label,
  value,
  delta,
  trend,
}: {
  label: string;
  value: string;
  delta: string;
  trend: "up" | "down" | "flat";
}) {
  return (
    <div className="px-5 py-4 bg-card">
      <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
        {label}
      </div>
      <div className="text-[22px] font-semibold tracking-[-0.01em] tabular-nums mt-1">
        {value}
      </div>
      <div
        className={
          "text-[11px] mt-1 inline-flex items-center gap-1 " +
          (trend === "up"
            ? "text-[#2f7d4a]"
            : trend === "down"
              ? "text-[#b42318]"
              : "text-muted-foreground")
        }
      >
        {trend === "up" && <TrendingUp className="h-3 w-3" />}
        {trend === "down" && <TrendingDown className="h-3 w-3" />}
        {delta}
      </div>
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="border border-border p-2.5">
      <div className="text-[10px] uppercase tracking-[0.06em] text-muted-foreground">
        {label}
      </div>
      <div className="text-[14px] font-medium mt-0.5 tabular-nums">{value}</div>
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="py-2.5 flex items-center justify-between">
      <dt className="text-[12px] text-muted-foreground">{label}</dt>
      <dd className="text-[13px] font-medium tabular-nums">{value}</dd>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
        {label}
      </label>
      <div className="mt-1">{children}</div>
    </div>
  );
}

function RowAction({
  icon,
  danger,
}: {
  icon: React.ReactNode;
  danger?: boolean;
}) {
  return (
    <button
      className={
        "h-7 w-7 grid place-items-center rounded-md border border-border bg-background " +
        (danger ? "text-[#b42318] hover:bg-[#fbeae8]" : "text-muted-foreground hover:text-foreground")
      }
    >
      {icon}
    </button>
  );
}

function PageBtn({ children, active }: { children: React.ReactNode; active?: boolean }) {
  return (
    <button
      className={
        "h-7 min-w-7 px-2 text-[12px] rounded-md tabular-nums " +
        (active ? "bg-foreground text-background" : "border border-border text-muted-foreground")
      }
    >
      {children}
    </button>
  );
}

function Tab2({ children, active }: { children: React.ReactNode; active?: boolean }) {
  return (
    <button
      className={
        "relative -mb-px py-2.5 text-[13px] border-b-2 " +
        (active ? "border-foreground text-foreground font-medium" : "border-transparent text-muted-foreground hover:text-foreground")
      }
    >
      {children}
    </button>
  );
}

function MetricBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="flex items-baseline justify-between">
        <span className="text-[12px] text-muted-foreground">{label}</span>
        <span className="text-[12px] font-medium tabular-nums">{value.toFixed(2)}</span>
      </div>
      <div className="mt-1.5 h-1.5 w-full bg-muted rounded-sm overflow-hidden">
        <div className="h-full bg-foreground" style={{ width: `${value * 100}%` }} />
      </div>
    </div>
  );
}

function BarChart({ data }: { data: { day: string; count: number }[] }) {
  const max = Math.max(...data.map((d) => d.count));
  return (
    <div>
      <div className="flex items-end gap-3 h-44">
        {data.map((d) => (
          <div key={d.day} className="flex-1 flex flex-col items-center justify-end gap-1">
            <div className="text-[10px] text-muted-foreground tabular-nums">{d.count}</div>
            <div
              className="w-full bg-foreground/85 rounded-t-sm"
              style={{ height: `${(d.count / max) * 150}px` }}
            />
            <div className="text-[11px] text-muted-foreground">{d.day}</div>
          </div>
        ))}
      </div>
      <div className="mt-3 border-t border-border pt-2 flex items-center justify-between text-[11px] text-muted-foreground">
        <span>Total · {data.reduce((a, b) => a + b.count, 0).toLocaleString()}</span>
        <span>Avg · {Math.round(data.reduce((a, b) => a + b.count, 0) / data.length)}</span>
      </div>
    </div>
  );
}

function WebMessage({
  role,
  content,
  sources,
}: {
  role: "user" | "assistant";
  content: React.ReactNode;
  sources?: { label: string; code?: string }[];
}) {
  if (role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[70%] bg-muted text-foreground px-4 py-2.5 rounded-lg rounded-br-sm text-[13px] leading-relaxed">
          {content}
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-start">
      <div className="max-w-[80%]">
        <div className="bg-card border border-border px-4 py-2.5 rounded-lg rounded-bl-sm text-[13px] leading-relaxed">
          {content}
        </div>
        {sources && sources.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1.5">
            {sources.map((s, i) => (
              <span
                key={i}
                className="text-[11px] inline-flex items-center gap-1 px-1.5 h-5 rounded border border-border text-muted-foreground bg-card"
              >
                {s.label}{s.code ? ` · ${s.code}` : ""}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
