"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

// iPhone-shaped frame, 390 × 844. Used for every mobile screen.
export function PhoneFrame({
  children,
  label,
  caption,
  className,
}: {
  children: React.ReactNode;
  label?: string;
  caption?: string;
  className?: string;
}) {
  return (
    <figure className={cn("flex flex-col items-start gap-2", className)}>
      <div
        className="device-frame relative bg-black overflow-hidden"
        style={{ width: 390, height: 844, borderRadius: 36 }}
      >
        {/* notch */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 h-7 w-32 bg-black rounded-b-2xl z-30" />
        {/* screen */}
        <div
          className="absolute inset-0 overflow-hidden bg-background"
          style={{ borderRadius: 32 }}
        >
          {children}
        </div>
      </div>
      {label && (
        <figcaption className="mt-2">
          <div className="text-[13px] font-medium text-foreground">{label}</div>
          {caption && (
            <div className="text-[12px] text-muted-foreground">{caption}</div>
          )}
        </figcaption>
      )}
    </figure>
  );
}

// Browser chrome frame for web screens
export function BrowserFrame({
  children,
  width = 1440,
  height = 900,
  url = "assistant.uni.edu",
  label,
  caption,
}: {
  children: React.ReactNode;
  width?: number;
  height?: number;
  url?: string;
  label?: string;
  caption?: string;
}) {
  return (
    <figure className="flex flex-col items-start gap-2">
      <div
        className="device-frame overflow-hidden bg-card"
        style={{ width, height, borderRadius: 12 }}
      >
        {/* browser top chrome */}
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
        <div className="overflow-hidden" style={{ height: height - 36 }}>
          {children}
        </div>
      </div>
      {label && (
        <figcaption className="mt-1">
          <div className="text-[13px] font-medium text-foreground">{label}</div>
          {caption && (
            <div className="text-[12px] text-muted-foreground">{caption}</div>
          )}
        </figcaption>
      )}
    </figure>
  );
}
