"use client";

import * as React from "react";
import { BrowserFrame, PhoneFrame } from "../shell/frames";
import { AdminPageView } from "./web-admin-page";
import { HomeScreen, CoursesScreen } from "../mobile/mobile-student-page";
import { ChevronRight } from "lucide-react";

export function ResponsivePage() {
  return (
    <div className="space-y-8">
      <section>
        <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
          08 — Responsive
        </div>
        <h1 className="text-[26px] font-semibold tracking-[-0.01em]">
          Responsive behavior
        </h1>
        <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
          The web platform is shown at three real viewport widths. We don't just scale
          the desktop design down — sidebar collapses, table columns hide, filter bar
          moves into a sheet. Mobile stays at 390 px because it is a native Flutter app.
        </p>
      </section>

      {/* Web — Students at three widths */}
      <section>
        <h2 className="text-[14px] font-semibold mb-3">Web — Students</h2>
        <div className="flex flex-col gap-6">
          {/* 1440 */}
          <ResponsiveDemo
            width={1440}
            height={560}
            naturalWidth={1440}
            label="Desktop · 1440 px"
            caption="Full sidebar · inline filters · all columns"
            url="assistant.uni.edu/admin/students"
          >
            <AdminPageView page="students" />
          </ResponsiveDemo>

          {/* 1024 — scaled */}
          <ResponsiveDemo
            width={920}
            height={420}
            naturalWidth={1440}
            scale={920 / 1440}
            label="Tablet landscape · 1024 px"
            caption="Sidebar collapses to icon rail · table still fits"
            url="assistant.uni.edu/admin/students"
          >
            <AdminPageView page="students" />
          </ResponsiveDemo>

          {/* 768 — scaled tighter */}
          <ResponsiveDemo
            width={760}
            height={340}
            naturalWidth={1440}
            scale={760 / 1440}
            label="Tablet · 768 px"
            caption="Sidebar becomes drawer · GPA column hidden · filters into sheet"
            url="assistant.uni.edu/admin/students"
          >
            <AdminPageView page="students" />
          </ResponsiveDemo>
        </div>
      </section>

      {/* Mobile responsive — fixed at 390 */}
      <section>
        <h2 className="text-[14px] font-semibold mb-3">Mobile — 390 px</h2>
        <div className="flex flex-wrap gap-6 items-start">
          <PhoneFrame label="Home" caption="390 × 844">
            <HomeScreen />
          </PhoneFrame>
          <PhoneFrame label="Courses" caption="390 × 844">
            <CoursesScreen />
          </PhoneFrame>
        </div>
      </section>

      {/* Behavior matrix */}
      <section>
        <h2 className="text-[14px] font-semibold mb-3">Behavior changes</h2>
        <div className="bg-card border border-border overflow-hidden">
          <table className="w-full text-[12px]">
            <thead>
              <tr className="border-b border-border bg-muted/30 text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
                <th className="text-left font-medium px-4 py-2.5 w-44">Element</th>
                <th className="text-left font-medium px-4 py-2.5">1440 px</th>
                <th className="text-left font-medium px-4 py-2.5">1024 px</th>
                <th className="text-left font-medium px-4 py-2.5">768 px</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {[
                ["Sidebar", "Full labels · 224 px", "Icon rail · 56 px", "Drawer · hidden by default"],
                ["Page head", "Title + actions inline", "Title + actions inline", "Actions wrap below title"],
                ["KPI strip", "4 columns", "4 columns", "2 × 2 grid"],
                ["Table columns", "All visible", "Hide GPA", "Hide GPA + Major"],
                ["Filter bar", "Inline · full row", "Inline · full row", "Filters button → sheet"],
                ["Pagination", "Below table", "Below table", "Below table"],
              ].map((row, i) => (
                <tr key={i} className="hover:bg-muted/20">
                  <td className="px-4 py-2.5 font-medium">{row[0]}</td>
                  <td className="px-4 py-2.5 text-muted-foreground">{row[1]}</td>
                  <td className="px-4 py-2.5 text-muted-foreground">{row[2]}</td>
                  <td className="px-4 py-2.5 text-muted-foreground">{row[3]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Handoff notes */}
      <section>
        <h2 className="text-[14px] font-semibold mb-3">Developer handoff notes</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            {
              t: "Flutter (mobile)",
              d: "Bottom nav uses 5 fixed tabs. Use SafeArea for the iPhone notch. Skeleton loaders are shimmer-free muted blocks. Use the same 4 px spacing scale.",
            },
            {
              t: "React + TypeScript (web)",
              d: "Sidebar collapses via Tailwind responsive classes. Tables use TanStack Table with column visibility state. The Filters sheet uses a Radix Dialog.",
            },
            {
              t: "Token system",
              d: "All colors, spacing, radii, and typography are CSS variables. Map them 1:1 to Flutter ThemeData and to a tailwind.config.ts in web.",
            },
            {
              t: "Accessibility",
              d: "Focus ring 2 px, outline-offset 2 px. Color is never the only signal — selected nav uses weight + a subtle background fill.",
            },
          ].map((b) => (
            <div key={b.t} className="bg-card border border-border p-4">
              <div className="text-[13px] font-medium">{b.t}</div>
              <div className="text-[12px] text-muted-foreground mt-1 leading-snug">
                {b.d}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

// Render children at naturalWidth, then CSS-scale to fit the target width.
// This is a Figma-style preview — not interactive at all widths, but shows the
// visual adaptation without re-implementing every screen at every breakpoint.
function ResponsiveDemo({
  width,
  height,
  naturalWidth,
  scale = 1,
  label,
  caption,
  url,
  children,
}: {
  width: number;
  height: number;
  naturalWidth: number;
  scale?: number;
  label: string;
  caption?: string;
  url?: string;
  children: React.ReactNode;
}) {
  return (
    <figure>
      <div
        className="device-frame overflow-hidden bg-card"
        style={{ width, height, borderRadius: 12 }}
      >
        <div className="h-9 border-b border-border flex items-center px-3 gap-2 bg-muted/40">
          <div className="flex gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-[#e4e4e1]" />
            <span className="h-2.5 w-2.5 rounded-full bg-[#e4e4e1]" />
            <span className="h-2.5 w-2.5 rounded-full bg-[#e4e4e1]" />
          </div>
          <div className="mx-auto h-6 min-w-64 px-3 bg-card border border-border rounded-md flex items-center text-[11px] text-muted-foreground">
            {url}
          </div>
        </div>
        <div
          className="overflow-hidden relative"
          style={{ height: height - 36 }}
        >
          <div
            style={{
              width: naturalWidth,
              height: "100%",
              transform: `scale(${scale})`,
              transformOrigin: "top left",
            }}
          >
            {children}
          </div>
        </div>
      </div>
      <figcaption className="mt-2 flex items-baseline justify-between">
        <div>
          <div className="text-[13px] font-medium">{label}</div>
          {caption && (
            <div className="text-[12px] text-muted-foreground">{caption}</div>
          )}
        </div>
        <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
      </figcaption>
    </figure>
  );
}
