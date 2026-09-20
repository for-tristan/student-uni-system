"use client";

import * as React from "react";
import {
  Search,
  ChevronRight,
  Check,
  X,
  AlertTriangle,
  Loader2,
  Bell,
} from "lucide-react";
import { SectionTitle, Panel, DifficultyTag, StatusPill, MatchMeter } from "../shell/primitives";
import { COURSES, RECOMMENDED } from "../data/mock";

export function ComponentsPage() {
  return (
    <div className="space-y-10">
      <section>
        <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
          02 — Components
        </div>
        <h1 className="text-[26px] font-semibold tracking-[-0.01em]">Components</h1>
        <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
        
        </p>
      </section>

      {/* Buttons */}
      <section>
        <SectionTitle title="Button" subtitle="Default · Hover · Pressed · Disabled · Loading" />
        <div className="bg-card border border-border divide-y divide-border">
          <Row label="Primary">
            <button className="h-9 px-4 rounded-md bg-primary text-primary-foreground text-[13px] font-medium">
              Sign in
            </button>
            <button className="h-9 px-4 rounded-md bg-[#2849cc] text-white text-[13px] font-medium">
              Hover
            </button>
            <button className="h-9 px-4 rounded-md bg-[#2140b3] text-white text-[13px] font-medium">
              Pressed
            </button>
            <button
              disabled
              className="h-9 px-4 rounded-md bg-muted text-muted-foreground text-[13px] font-medium cursor-not-allowed"
            >
              Disabled
            </button>
            <button
              disabled
              className="h-9 px-4 rounded-md bg-primary text-primary-foreground text-[13px] font-medium inline-flex items-center gap-2 cursor-wait opacity-90"
            >
              <Loader2 className="h-3.5 w-3.5 animate-spin" /> Loading
            </button>
          </Row>
          <Row label="Secondary">
            <button className="h-9 px-4 rounded-md border border-border bg-card text-[13px] font-medium">
              Cancel
            </button>
            <button className="h-9 px-4 rounded-md border border-border bg-muted text-[13px] font-medium">
              Hover
            </button>
          </Row>
          <Row label="Ghost">
            <button className="h-9 px-3 rounded-md text-[13px] font-medium text-muted-foreground hover:bg-muted hover:text-foreground">
              View details
            </button>
          </Row>
          <Row label="Destructive">
            <button className="h-9 px-4 rounded-md bg-error text-error-foreground text-[13px] font-medium">
              Delete course
            </button>
          </Row>
        </div>
      </section>

      {/* Inputs */}
      <section>
        <SectionTitle title="Input" subtitle="Default · Focus · Filled · Error · Disabled" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Panel>
            <Label>Student ID</Label>
            <input
              className="mt-1 h-9 w-full px-3 rounded-md border border-border bg-card text-[13px] placeholder:text-muted-foreground/70"
              placeholder="S-2023-1148"
            />
            <Hint>Default</Hint>
          </Panel>
          <Panel>
            <Label>Email</Label>
            <input
              className="mt-1 h-9 w-full px-3 rounded-md border-2 border-primary bg-card text-[13px]"
              defaultValue="ahmed.samir@uni.edu"
            />
            <Hint>Focused</Hint>
          </Panel>
          <Panel>
            <Label>Password</Label>
            <input
              type="password"
              className="mt-1 h-9 w-full px-3 rounded-md border border-border bg-card text-[13px]"
              defaultValue="supersecret"
            />
            <Hint>Filled</Hint>
          </Panel>
          <Panel>
            <Label>Student ID</Label>
            <input
              className="mt-1 h-9 w-full px-3 rounded-md border border-error bg-card text-[13px]"
              defaultValue="abc"
            />
            <Hint tone="error">Use the format S-YYYY-NNNN.</Hint>
          </Panel>
          <Panel>
            <Label>Major</Label>
            <input
              disabled
              className="mt-1 h-9 w-full px-3 rounded-md border border-border bg-muted text-[13px] text-muted-foreground"
              defaultValue="Computer Science"
            />
            <Hint>Disabled</Hint>
          </Panel>
          <Panel>
            <Label>Search</Label>
            <div className="relative mt-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
              <input
                className="h-9 w-full pl-9 pr-3 rounded-md border border-border bg-card text-[13px]"
                placeholder="Search courses"
              />
            </div>
            <Hint>With leading icon</Hint>
          </Panel>
        </div>
      </section>

      {/* Badges & status */}
      <section>
        <SectionTitle title="Badge" subtitle="Used for status only. Never decorative." />
        <div className="bg-card border border-border p-5 flex flex-wrap gap-3">
          <StatusPill kind="neutral">Available</StatusPill>
          <StatusPill kind="success">Completed</StatusPill>
          <StatusPill kind="success">Prerequisites met</StatusPill>
          <StatusPill kind="warning">Prerequisite missing</StatusPill>
          <StatusPill kind="warning">Probation</StatusPill>
          <StatusPill kind="error">Failed</StatusPill>
          <StatusPill kind="accent">Recommended</StatusPill>
        </div>
      </section>

      {/* Tabs */}
      <section>
        <SectionTitle title="Tabs" subtitle="Underlined. Clear selected state without color." />
        <div className="bg-card border border-border p-5">
          <div className="flex gap-6 border-b border-border">
            <Tab active>Overview</Tab>
            <Tab>Prerequisites</Tab>
            <Tab>Skills</Tab>
            <Tab>Match</Tab>
          </div>
          <div className="pt-4 text-[13px] text-muted-foreground">
            Tab content area.
          </div>
        </div>
      </section>

      {/* Course row + course card */}
      <section>
        <SectionTitle
          title="Course row · Course card"
          subtitle="Row used in lists. Card used only when grouping genuinely helps."
        />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
          <Panel pad={false}>
            <div className="px-4 py-3 border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
              Course row
            </div>
            <div className="divide-y divide-border">
              {COURSES.slice(0, 4).map((c) => (
                <div key={c.code} className="px-4 py-3 hover:bg-muted/40 transition-colors cursor-pointer">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <div className="flex items-baseline gap-2">
                        <span className="text-[14px] font-medium truncate">{c.name}</span>
                        <span className="text-[11px] text-muted-foreground tabular-nums">{c.code}</span>
                      </div>
                      <div className="text-[12px] text-muted-foreground mt-0.5">
                        {c.category} · {c.credits} credits
                      </div>
                    </div>
                    <div className="flex flex-col items-end gap-1 shrink-0">
                      <DifficultyTag level={c.difficulty} />
                      <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Panel>

          <Panel pad={false}>
            <div className="px-4 py-3 border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
              Course card (only when grouping helps)
            </div>
            <div className="p-4 grid grid-cols-2 gap-3">
              {COURSES.slice(0, 2).map((c) => (
                <div key={c.code} className="border border-border p-3">
                  <div className="text-[11px] text-muted-foreground tabular-nums">{c.code}</div>
                  <div className="text-[14px] font-medium mt-0.5">{c.name}</div>
                  <div className="text-[12px] text-muted-foreground mt-1">
                    {c.category} · {c.credits} cr
                  </div>
                  <div className="mt-2"><DifficultyTag level={c.difficulty} /></div>
                </div>
              ))}
            </div>
          </Panel>
        </div>
      </section>

      {/* Recommendation row */}
      <section>
        <SectionTitle
          title="Recommendation row"
          subtitle="Ranked, scannable, no flashy score."
        />
        <div className="bg-card border border-border divide-y divide-border">
          {RECOMMENDED.slice(0, 3).map((c, i) => (
            <div key={c.code} className="px-4 py-4 flex items-start gap-4">
              <div className="text-[12px] font-medium text-muted-foreground tabular-nums w-6 shrink-0 pt-0.5">
                {String(i + 1).padStart(2, "0")}
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-baseline gap-2">
                  <span className="text-[14px] font-medium truncate">{c.name}</span>
                  <span className="text-[11px] text-muted-foreground tabular-nums">{c.code}</span>
                </div>
                <div className="text-[12px] text-muted-foreground mt-0.5">
                  {c.category} · {c.difficulty} · {c.credits} credits
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {c.skills.map((s) => (
                    <span key={s} className="text-[11px] px-1.5 h-5 inline-flex items-center rounded bg-muted text-muted-foreground">
                      {s}
                    </span>
                  ))}
                </div>
                <div className="text-[12px] text-foreground mt-2">
                  <span className="text-muted-foreground">Why:</span>{" "}
                  {c.matchReasons?.[0]}
                </div>
              </div>
              <div className="w-24 shrink-0">
                <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-1">
                  Match
                </div>
                <MatchMeter value={c.matchScore ?? 0} />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Table */}
      <section>
        <SectionTitle title="Table" subtitle="Thin separators. Tabular numerals. Hover row." />
        <div className="bg-card border border-border overflow-hidden">
          <table className="w-full text-[13px]">
            <thead>
              <tr className="border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
                <Th>Course</Th>
                <Th>Category</Th>
                <Th className="text-right">Credits</Th>
                <Th>Difficulty</Th>
                <Th className="text-right">Enrolled</Th>
              </tr>
            </thead>
            <tbody>
              {COURSES.slice(0, 5).map((c, i) => (
                <tr key={c.code} className={i % 2 ? "bg-muted/30" : ""}>
                  <Td>
                    <div className="font-medium">{c.name}</div>
                    <div className="text-[11px] text-muted-foreground tabular-nums">{c.code}</div>
                  </Td>
                  <Td>{c.category}</Td>
                  <Td className="text-right tabular-nums">{c.credits}</Td>
                  <Td><DifficultyTag level={c.difficulty} /></Td>
                  <Td className="text-right tabular-nums">
                    {c.enrolled}/{c.capacity}
                  </Td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Pagination + Toast + Modal + Drawer */}
      <section>
        <SectionTitle title="Pagination · Toast · Modal · Drawer" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Panel>
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-3">Pagination</div>
            <nav className="flex items-center gap-1">
              <PageBtn>‹</PageBtn>
              <PageBtn active>1</PageBtn>
              <PageBtn>2</PageBtn>
              <PageBtn>3</PageBtn>
              <PageBtn>…</PageBtn>
              <PageBtn>42</PageBtn>
              <PageBtn>›</PageBtn>
            </nav>
          </Panel>

          <Panel>
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-3">Toast</div>
            <div className="space-y-2">
              <Toast tone="neutral">
                <Check className="h-4 w-4 text-[#2f7d4a]" />
                Course saved.
              </Toast>
              <Toast tone="error">
                <AlertTriangle className="h-4 w-4 text-[#b42318]" />
                Courses couldn't be loaded.
              </Toast>
            </div>
          </Panel>

          <Panel className="md:col-span-2">
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-3">Modal · Drawer</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="relative border border-border p-4 h-40 overflow-hidden">
                <div className="absolute inset-0 bg-black/20" />
                <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-card border border-border p-4 w-72">
                  <div className="text-[13px] font-medium">Drop course?</div>
                  <div className="text-[12px] text-muted-foreground mt-1">
                    This will remove CS-322 from your current semester.
                  </div>
                  <div className="flex justify-end gap-2 mt-3">
                    <button className="h-8 px-3 text-[12px] border border-border rounded-md">Cancel</button>
                    <button className="h-8 px-3 text-[12px] bg-error text-error-foreground rounded-md">Drop</button>
                  </div>
                </div>
              </div>

              <div className="relative border border-border p-4 h-40 overflow-hidden bg-muted/30">
                <div className="absolute right-0 top-0 bottom-0 w-56 bg-card border-l border-border p-3">
                  <div className="flex items-center justify-between">
                    <div className="text-[12px] font-medium">Filters</div>
                    <X className="h-3.5 w-3.5 text-muted-foreground" />
                  </div>
                  <div className="text-[11px] text-muted-foreground mt-2">Difficulty</div>
                  <div className="flex gap-1 mt-1">
                    <button className="h-6 px-2 text-[11px] bg-accent text-accent-foreground rounded">All</button>
                    <button className="h-6 px-2 text-[11px] border border-border rounded">Advanced</button>
                  </div>
                </div>
              </div>
            </div>
          </Panel>
        </div>
      </section>

      {/* Navigation */}
      <section>
        <SectionTitle title="Navigation" subtitle="Bottom (mobile) · Sidebar (web)" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Panel>
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-3">
              Bottom navigation (mobile)
            </div>
            <div className="border border-border rounded-lg overflow-hidden max-w-[360px]">
              <div className="h-32 bg-muted/30" />
              <div className="grid grid-cols-5 border-t border-border bg-card">
                {["Home", "Courses", "Assistant", "Progress", "Profile"].map((l, i) => (
                  <button
                    key={l}
                    className={
                      "flex flex-col items-center gap-1 py-2.5 text-[10px] font-medium " +
                      (i === 0 ? "text-foreground" : "text-muted-foreground")
                    }
                  >
                    <span className={"h-6 w-10 inline-flex items-center justify-center rounded " + (i === 0 ? "bg-accent text-accent-foreground" : "")}>
                      <NavIcon i={i} />
                    </span>
                    {l}
                  </button>
                ))}
              </div>
            </div>
          </Panel>
          <Panel>
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-3">
              Sidebar (web)
            </div>
            <div className="border border-border rounded-lg w-full h-48 flex">
              <div className="w-44 border-r border-border bg-card p-2">
                {[
                  ["Overview", false],
                  ["Students", true],
                  ["Courses", false],
                  ["Recommendations", false],
                  ["Assistant", false],
                  ["Settings", false],
                ].map(([label, active]) => (
                  <div
                    key={label as string}
                    className={
                      "flex items-center gap-2 h-8 px-2 rounded-md text-[12px] " +
                      (active ? "bg-accent text-accent-foreground font-medium" : "text-muted-foreground")
                    }
                  >
                    <span className="h-3.5 w-3.5 inline-block rounded-sm border border-border" />
                    {label as string}
                  </div>
                ))}
              </div>
              <div className="flex-1 bg-muted/30" />
            </div>
          </Panel>
        </div>
      </section>

      {/* AI message */}
      <section>
        <SectionTitle
          title="Assistant message"
          subtitle="Restrained chat. Source tags when available. No robot avatars, no sparkles."
        />
        <div className="bg-card border border-border p-5 max-w-2xl">
          <div className="flex justify-end">
            <div className="max-w-[80%] bg-muted text-foreground px-3 py-2 rounded-lg rounded-br-sm text-[13px]">
              What are the prerequisites for Machine Learning?
            </div>
          </div>
          <div className="mt-3">
            <div className="max-w-[80%] bg-card border border-border px-3 py-2 rounded-lg rounded-bl-sm text-[13px]">
              <p className="leading-relaxed">
                Machine Learning (CS-421) requires:
              </p>
              <ul className="mt-1 list-disc pl-4 text-muted-foreground">
                <li>Algorithms (CS-221) — completed, grade A</li>
                <li>Probability &amp; Statistics (MATH-204) — completed, grade A-</li>
              </ul>
              <div className="mt-2 flex flex-wrap gap-1.5">
                <span className="text-[11px] inline-flex items-center gap-1 px-1.5 h-5 rounded border border-border text-muted-foreground">
                  Source · CS-421 catalog
                </span>
                <span className="text-[11px] inline-flex items-center gap-1 px-1.5 h-5 rounded border border-border text-muted-foreground">
                  Source · Your transcript
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Progress indicator */}
      <section>
        <SectionTitle title="Progress indicator" subtitle="One clear indicator. Not five decorative rings." />
        <div className="bg-card border border-border p-5 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div className="flex items-baseline justify-between">
              <div className="text-[13px] font-medium">Graduation progress</div>
              <div className="text-[12px] text-muted-foreground tabular-nums">84 / 132 credits</div>
            </div>
            <div className="mt-2 h-2 w-full bg-muted rounded-sm overflow-hidden">
              <div className="h-full bg-primary" style={{ width: "63.6%" }} />
            </div>
            <div className="text-[11px] text-muted-foreground mt-2">
              On track · Spring 2026
            </div>
          </div>
          <div>
            <div className="flex items-baseline justify-between">
              <div className="text-[13px] font-medium">Recommendation coverage</div>
              <div className="text-[12px] text-muted-foreground tabular-nums">81%</div>
            </div>
            <div className="mt-2 h-2 w-full bg-muted rounded-sm overflow-hidden">
              <div className="h-full bg-[#2f7d4a]" style={{ width: "81%" }} />
            </div>
            <div className="text-[11px] text-muted-foreground mt-2">
              Precision@5 · 0.78 · Recall@5 · 0.64
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="px-4 py-3 flex flex-wrap items-center gap-3">
      <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground w-24 shrink-0">
        {label}
      </div>
      <div className="flex flex-wrap items-center gap-3">{children}</div>
    </div>
  );
}

function Label({ children }: { children: React.ReactNode }) {
  return (
    <label className="text-[11px] font-medium uppercase tracking-[0.06em] text-muted-foreground">
      {children}
    </label>
  );
}

function Hint({ children, tone = "neutral" }: { children: React.ReactNode; tone?: "neutral" | "error" }) {
  return (
    <div className={"mt-1.5 text-[12px] " + (tone === "error" ? "text-[#b42318]" : "text-muted-foreground")}>
      {children}
    </div>
  );
}

function Tab({ children, active }: { children: React.ReactNode; active?: boolean }) {
  return (
    <button
      className={
        "relative -mb-px py-2 text-[13px] " +
        (active ? "text-foreground font-medium" : "text-muted-foreground hover:text-foreground")
      }
    >
      {children}
      {active && <span className="absolute inset-x-0 -bottom-px h-0.5 bg-foreground" />}
    </button>
  );
}

function Th({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <th className={"text-left font-medium px-3 py-2 " + className}>{children}</th>;
}

function Td({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <td className={"px-3 py-2.5 align-top " + className}>{children}</td>;
}

function PageBtn({ children, active }: { children: React.ReactNode; active?: boolean }) {
  return (
    <button
      className={
        "h-8 min-w-8 px-2 text-[12px] rounded-md tabular-nums " +
        (active ? "bg-foreground text-background" : "border border-border text-muted-foreground hover:text-foreground")
      }
    >
      {children}
    </button>
  );
}

function Toast({ tone, children }: { tone: "neutral" | "error"; children: React.ReactNode }) {
  return (
    <div
      className={
        "flex items-center gap-2 px-3 h-9 rounded-md text-[13px] border " +
        (tone === "error" ? "border-[#b42318]/30 bg-[#fbeae8] text-[#b42318]" : "border-border bg-card")
      }
    >
      {children}
    </div>
  );
}

function NavIcon({ i }: { i: number }) {
  const icons = [
    <Bell key={0} className="h-3.5 w-3.5" />,
    <Bell key={1} className="h-3.5 w-3.5" />,
    <Bell key={2} className="h-3.5 w-3.5" />,
    <Bell key={3} className="h-3.5 w-3.5" />,
    <Bell key={4} className="h-3.5 w-3.5" />,
  ];
  return icons[i];
}
