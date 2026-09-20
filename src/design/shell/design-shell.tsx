"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import {
  GraduationCap,
  LayoutGrid,
  Component,
  Smartphone,
  Monitor,
  Columns2,
  Download,
} from "lucide-react";

export type DesignPage =
  | "foundations"
  | "components"
  | "mobile-auth"
  | "mobile-student"
  | "mobile-assistant"
  | "web-admin"
  | "web-assistant"
  | "responsive"
  | "export";

const NAV: { id: DesignPage; label: string; group: string; icon: React.ReactNode }[] = [
  { id: "foundations", label: "Foundations", group: "System", icon: <LayoutGrid className="h-3.5 w-3.5" /> },
  { id: "components", label: "Components", group: "System", icon: <Component className="h-3.5 w-3.5" /> },
  { id: "responsive", label: "Responsive", group: "System", icon: <Columns2 className="h-3.5 w-3.5" /> },
  { id: "export", label: "Export", group: "System", icon: <Download className="h-3.5 w-3.5" /> },
  { id: "mobile-auth", label: "Mobile — Authentication", group: "Mobile", icon: <Smartphone className="h-3.5 w-3.5" /> },
  { id: "mobile-student", label: "Mobile — Student", group: "Mobile", icon: <Smartphone className="h-3.5 w-3.5" /> },
  { id: "mobile-assistant", label: "Mobile — Assistant", group: "Mobile", icon: <Smartphone className="h-3.5 w-3.5" /> },
  { id: "web-admin", label: "Web — Admin", group: "Web", icon: <Monitor className="h-3.5 w-3.5" /> },
  { id: "web-assistant", label: "Web — Assistant", group: "Web", icon: <Monitor className="h-3.5 w-3.5" /> },
];

export function DesignShell({
  page,
  onChange,
  children,
}: {
  page: DesignPage;
  onChange: (p: DesignPage) => void;
  children: React.ReactNode;
}) {
  const groups = Array.from(new Set(NAV.map((n) => n.group)));
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Top brand bar */}
      <header className="sticky top-0 z-40 bg-background/95 backdrop-blur border-b border-border">
        <div className="mx-auto max-w-[1640px] px-6 h-14 flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="h-7 w-7 rounded-md bg-foreground text-background grid place-items-center">
              <GraduationCap className="h-4 w-4" />
            </div>
            <div className="leading-tight">
              <div className="text-[13px] font-semibold">Smart University Assistant</div>
              <div className="text-[11px] text-muted-foreground">Design system · v1.0</div>
            </div>
          </div>

          <nav className="flex-1 overflow-x-auto scroll-thin">
            <ul className="flex items-center gap-1 text-[12px]">
              {groups.map((g) => {
                const items = NAV.filter((n) => n.group === g);
                return (
                  <React.Fragment key={g}>
                    <li className="px-2 text-[10px] uppercase tracking-[0.08em] text-muted-foreground/80">
                      {g}
                    </li>
                    {items.map((it) => (
                      <li key={it.id}>
                        <button
                          onClick={() => onChange(it.id)}
                          className={cn(
                            "inline-flex items-center gap-1.5 h-8 px-2.5 rounded-md transition-colors",
                            page === it.id
                              ? "bg-accent text-accent-foreground"
                              : "text-muted-foreground hover:text-foreground hover:bg-muted",
                          )}
                        >
                          {it.icon}
                          <span className="whitespace-nowrap">{it.label}</span>
                        </button>
                      </li>
                    ))}
                  </React.Fragment>
                );
              })}
            </ul>
          </nav>

          <div className="hidden md:flex items-center gap-3 text-[11px] text-muted-foreground">
            <span>Flutter · React + TypeScript</span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[1640px] px-6 py-8">{children}</main>

      <footer className="mt-12 border-t border-border">
        <div className="mx-auto max-w-[1640px] px-6 py-6 text-[11px] text-muted-foreground flex items-center justify-between">
          <span>Designed, not generated — restrained academic interface system.</span>
          <span>390 × 844 mobile · 1440 × 900 web</span>
        </div>
      </footer>
    </div>
  );
}
