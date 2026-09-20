"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

// ---------------------------------------------------------------
// Primitives — restrained academic style. Flat, thin borders.
// No glow, no gradients, no glassmorphism.
// ---------------------------------------------------------------

export function SectionTitle({
  title,
  subtitle,
  right,
  className,
}: {
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  right?: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("flex items-end justify-between gap-4 mb-3", className)}>
      <div>
        <h2 className="text-[15px] font-semibold tracking-[-0.01em] text-foreground">
          {title}
        </h2>
        {subtitle && (
          <p className="text-[13px] text-muted-foreground mt-0.5">{subtitle}</p>
        )}
      </div>
      {right && <div className="shrink-0">{right}</div>}
    </div>
  );
}

export function Panel({
  children,
  className,
  pad = true,
}: {
  children: React.ReactNode;
  className?: string;
  pad?: boolean;
}) {
  return (
    <div
      className={cn(
        "bg-card border border-border",
        pad && "p-5",
        className,
      )}
    >
      {children}
    </div>
  );
}

// Difficulty badge — neutral tone, not a color explosion.
export function DifficultyTag({
  level,
}: {
  level: "Introductory" | "Intermediate" | "Advanced";
}) {
  const label =
    level === "Introductory" ? "Introductory" : level === "Intermediate" ? "Intermediate" : "Advanced";
  return (
    <span className="text-[11px] font-medium uppercase tracking-[0.06em] text-muted-foreground">
      {label}
    </span>
  );
}

// Status pill — used for completed / in-progress / missing
export function StatusPill({
  kind,
  children,
}: {
  kind: "neutral" | "success" | "warning" | "error" | "accent";
  children: React.ReactNode;
}) {
  const styles: Record<typeof kind, string> = {
    neutral: "bg-muted text-muted-foreground border-transparent",
    success: "bg-[#ecf5ef] text-[#2f7d4a] border-transparent",
    warning: "bg-[#fbf2e3] text-[#a66a00] border-transparent",
    error: "bg-[#fbeae8] text-[#b42318] border-transparent",
    accent: "bg-accent text-accent-foreground border-transparent",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center h-5 px-1.5 text-[11px] font-medium rounded",
        styles[kind],
      )}
    >
      {children}
    </span>
  );
}

// Match meter — used in course details and recommendation rows.
// Linear, restrained. Not a circular AI gauge.
export function MatchMeter({ value }: { value: number }) {
  const v = Math.max(0, Math.min(100, value));
  const tone = v >= 85 ? "#2f7d4a" : v >= 70 ? "#315cff" : "#a66a00";
  return (
    <div className="flex items-center gap-2">
      <div className="relative h-1.5 w-full bg-muted overflow-hidden rounded-sm">
        <div
          className="absolute inset-y-0 left-0"
          style={{ width: `${v}%`, background: tone }}
        />
      </div>
      <span className="text-[12px] font-medium tabular-nums text-foreground">
        {v}%
      </span>
    </div>
  );
}

// Bottom navigation item — mobile only.
export function BottomNavItem({
  label,
  active,
  icon,
}: {
  label: string;
  active?: boolean;
  icon: React.ReactNode;
}) {
  return (
    <button
      className={cn(
        "flex flex-1 flex-col items-center justify-center gap-1 pt-2 pb-3 text-[10px] font-medium",
        active ? "text-foreground" : "text-muted-foreground",
      )}
    >
      <span
        className={cn(
          "flex h-6 w-12 items-center justify-center rounded-md",
          active && "bg-accent text-accent-foreground",
        )}
      >
        {icon}
      </span>
      <span>{label}</span>
    </button>
  );
}
