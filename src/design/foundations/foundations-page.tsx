"use client";

import * as React from "react";
import { PALETTE, TYPE_SCALE, SPACING } from "../data/mock";
import {
  Home,
  BookOpen,
  MessageSquare,
  TrendingUp,
  User,
  Search,
  Bell,
  ChevronRight,
  Check,
  AlertTriangle,
  X,
  GraduationCap,
} from "lucide-react";
import { SectionTitle, Panel } from "../shell/primitives";

export function FoundationsPage() {
  return (
    <div className="space-y-12">
      <PageIntro />

      {/* COLORS */}
      <section>
        <SectionTitle
          title="Color"
          subtitle="Mostly neutral foundation. Accent used sparingly. No gradients."
        />
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {PALETTE.map((c) => (
            <div key={c.name} className="bg-card border border-border">
              <div className="h-20" style={{ background: c.value }} />
              <div className="p-3">
                <div className="flex items-center justify-between">
                  <div className="text-[13px] font-medium">{c.name}</div>
                  <code className="text-[11px] text-muted-foreground tabular-nums">
                    {c.value}
                  </code>
                </div>
                <div className="text-[12px] text-muted-foreground mt-1 leading-snug">
                  {c.usage}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="bg-card border border-border p-4">
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-2">
              Primary actions
            </div>
            <button className="h-9 px-4 bg-primary text-primary-foreground text-[13px] font-medium rounded-md">
              Sign in
            </button>
            <button className="ml-2 h-9 px-4 border border-border bg-card text-[13px] font-medium rounded-md">
              Cancel
            </button>
          </div>
          <div className="bg-card border border-border p-4">
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-2">
              Semantic
            </div>
            <div className="flex flex-wrap gap-2 text-[12px]">
              <span className="inline-flex items-center gap-1 px-1.5 h-5 rounded bg-[#ecf5ef] text-[#2f7d4a]">
                <Check className="h-3 w-3" /> Prerequisites met
              </span>
              <span className="inline-flex items-center gap-1 px-1.5 h-5 rounded bg-[#fbf2e3] text-[#a66a00]">
                <AlertTriangle className="h-3 w-3" /> Prerequisite missing
              </span>
              <span className="inline-flex items-center gap-1 px-1.5 h-5 rounded bg-[#fbeae8] text-[#b42318]">
                <X className="h-3 w-3" /> Failed
              </span>
            </div>
          </div>
          <div className="bg-card border border-border p-4">
            <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-2">
              Accent usage
            </div>
            <p className="text-[12px] text-muted-foreground leading-snug">
              Accent is reserved for primary actions, links, and the focus ring. It is never used as a background fill for entire sections.
            </p>
          </div>
        </div>
      </section>

      {/* TYPOGRAPHY */}
      <section>
        <SectionTitle
          title="Typography"
          subtitle="Inter · single family, clear hierarchy. No oversized headings inside application screens."
        />
        <div className="bg-card border border-border divide-y divide-border">
          {TYPE_SCALE.map((t) => (
            <div
              key={t.token}
              className="grid grid-cols-[120px_120px_1fr] items-center gap-4 px-5 py-4"
            >
              <code className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
                {t.token}
              </code>
              <code className="text-[11px] text-muted-foreground tabular-nums">
                {t.size} · {t.weight}
              </code>
              <div className={t.className}>
                {t.token === "caption"
                  ? "Section label"
                  : t.token === "label"
                    ? "Field label"
                    : t.token === "display"
                      ? "Computer Science"
                      : t.token === "h1"
                        ? "Academic progress"
                        : t.token === "h2"
                          ? "Current courses"
                          : t.token === "h3"
                            ? "Machine Learning"
                            : t.token === "small"
                              ? "3 credits · Advanced · CS-421"
                              : "Recommended courses based on your skills and interests."}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* SPACING */}
      <section>
        <SectionTitle
          title="Spacing"
          subtitle="4-based scale. Consistent across components. Avoid huge empty regions."
        />
        <div className="bg-card border border-border p-5">
          <div className="flex items-end gap-3 flex-wrap">
            {SPACING.map((s) => (
              <div key={s} className="flex flex-col items-center gap-1">
                <div
                  className="bg-primary/20 border border-primary/40"
                  style={{ width: s, height: s }}
                />
                <code className="text-[10px] text-muted-foreground tabular-nums">
                  {s}
                </code>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ICONOGRAPHY */}
      <section>
        <SectionTitle
          title="Iconography"
          subtitle="One family — Lucide outline icons. Used for meaning, not decoration."
        />
        <div className="bg-card border border-border p-5 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {[
            { icon: <Home className="h-4 w-4" />, label: "Home" },
            { icon: <BookOpen className="h-4 w-4" />, label: "Courses" },
            { icon: <MessageSquare className="h-4 w-4" />, label: "Assistant" },
            { icon: <TrendingUp className="h-4 w-4" />, label: "Progress" },
            { icon: <User className="h-4 w-4" />, label: "Profile" },
            { icon: <Search className="h-4 w-4" />, label: "Search" },
            { icon: <Bell className="h-4 w-4" />, label: "Notifications" },
            { icon: <ChevronRight className="h-4 w-4" />, label: "Navigate" },
            { icon: <Check className="h-4 w-4" />, label: "Completed" },
            { icon: <AlertTriangle className="h-4 w-4" />, label: "Warning" },
            { icon: <X className="h-4 w-4" />, label: "Close" },
            { icon: <GraduationCap className="h-4 w-4" />, label: "Academic" },
          ].map((it) => (
            <div
              key={it.label}
              className="flex flex-col items-center justify-center gap-2 py-4 border border-border rounded-md"
            >
              {it.icon}
              <span className="text-[11px] text-muted-foreground">{it.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* LAYOUT PRINCIPLES */}
      <section>
        <SectionTitle
          title="Layout principles"
          subtitle="Choose the layout based on information, not on a card-grid template."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {[
            {
              t: "Lists before cards",
              d: "A course list is a list. A row with title, credits, difficulty and a divider scans faster than a card grid.",
            },
            {
              t: "Tables for tabular data",
              d: "Students, courses, enrollments — tables with thin separators, not cards.",
            },
            {
              t: "Tabs for connected views",
              d: "When the same entity has several views (overview, prerequisites, skills) use tabs.",
            },
            {
              t: "Sections over panels",
              d: "On a profile page, a small section header with content under it is cleaner than a boxed card per fact.",
            },
            {
              t: "Cards only when they group",
              d: "Use a card only when content is loosely grouped and a border genuinely helps. Otherwise use whitespace.",
            },
            {
              t: "Whisper, don't shout",
              d: "Borders at #E4E4E1, surfaces at #FFFFFF. Shadows are used rarely — typography does the work.",
            },
          ].map((p) => (
            <div key={p.t} className="bg-card border border-border p-4">
              <div className="text-[13px] font-medium">{p.t}</div>
              <div className="text-[12px] text-muted-foreground mt-1 leading-snug">
                {p.d}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function PageIntro() {
  return (
    <section>
      <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
        01 — Foundations
      </div>
      <h1 className="text-[26px] font-semibold tracking-[-0.01em]">
        Foundations
      </h1>
      <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
        A restrained academic visual system. Neutral surfaces, thin borders, a single
        accent color used sparingly, and a strong typographic hierarchy. The interface
        still reads correctly if every shadow is removed.
      </p>

      <div className="mt-5 grid grid-cols-2 md:grid-cols-4 gap-3">
        <Panel pad={false} className="p-4">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
            Type family
          </div>
          <div className="text-[15px] font-medium mt-1">Inter</div>
          <div className="text-[12px] text-muted-foreground">Latin + numerals</div>
        </Panel>
        <Panel pad={false} className="p-4">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
            Accent
          </div>
          <div className="flex items-center gap-2 mt-1">
            <span className="h-4 w-4 rounded" style={{ background: "#315cff" }} />
            <span className="text-[14px] font-medium tabular-nums">#315CFF</span>
          </div>
        </Panel>
        <Panel pad={false} className="p-4">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
            Radius
          </div>
          <div className="text-[15px] font-medium mt-1">4 / 6 / 8 px</div>
          <div className="text-[12px] text-muted-foreground">Small, consistent</div>
        </Panel>
        <Panel pad={false} className="p-4">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
            Shadow
          </div>
          <div className="text-[15px] font-medium mt-1">Minimal</div>
          <div className="text-[12px] text-muted-foreground">Borders do the work</div>
        </Panel>
      </div>
    </section>
  );
}

