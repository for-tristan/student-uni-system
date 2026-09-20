"use client";

import * as React from "react";
import { PhoneFrame } from "../shell/frames";
import { GraduationCap, Eye, EyeOff } from "lucide-react";

export function MobileAuthPage() {
  return (
    <div className="space-y-8">
      <section>
        <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
          03 — Mobile · Authentication
        </div>
        <h1 className="text-[26px] font-semibold tracking-[-0.01em]">
          Authentication
        </h1>
        <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
          A login screen that gets the user into the product quickly. No marketing copy,
          no illustrations. The form does the work.
        </p>
      </section>

      <div className="flex flex-wrap gap-8">
        <PhoneFrame label="Login — default" caption="Empty state">
          <LoginScreen state="default" />
        </PhoneFrame>
        <PhoneFrame label="Login — focus" caption="Field focused, show password on">
          <LoginScreen state="focus" />
        </PhoneFrame>
        <PhoneFrame label="Login — error" caption="Inline error message">
          <LoginScreen state="error" />
        </PhoneFrame>
        <PhoneFrame label="Login — loading" caption="Submitting credentials">
          <LoginScreen state="loading" />
        </PhoneFrame>
      </div>
    </div>
  );
}

function LoginScreen({ state }: { state: "default" | "focus" | "error" | "loading" }) {
  const [show, setShow] = React.useState(state === "focus");
  return (
    <div className="h-full flex flex-col bg-background px-6 pt-16 pb-8">
      {/* Brand */}
      <div className="flex items-center gap-2">
        <div className="h-8 w-8 rounded-md bg-foreground text-background grid place-items-center">
          <GraduationCap className="h-4 w-4" />
        </div>
        <div className="text-[14px] font-semibold tracking-[-0.01em]">
          Smart University Assistant
        </div>
      </div>

      <div className="mt-12">
        <h1 className="text-[22px] font-semibold tracking-[-0.01em]">Sign in</h1>
        <p className="text-[13px] text-muted-foreground mt-1">
          Use your university student ID.
        </p>
      </div>

      <div className="mt-8 space-y-4">
        <div>
          <label className="text-[11px] font-medium uppercase tracking-[0.06em] text-muted-foreground">
            Student ID or email
          </label>
          <input
            className={
              "mt-1 h-11 w-full px-3 rounded-md bg-card text-[14px] " +
              (state === "error"
                ? "border border-error"
                : state === "focus"
                  ? "border-2 border-primary"
                  : "border border-border")
            }
            placeholder="S-2023-1148"
            defaultValue={state === "error" ? "abc" : state === "focus" ? "ahmed.samir@uni.edu" : ""}
          />
        </div>

        <div>
          <label className="text-[11px] font-medium uppercase tracking-[0.06em] text-muted-foreground">
            Password
          </label>
          <div className="relative mt-1">
            <input
              type={show ? "text" : "password"}
              className={
                "h-11 w-full px-3 pr-10 rounded-md bg-card text-[14px] " +
                (state === "error"
                  ? "border border-error"
                  : "border border-border")
              }
              placeholder="••••••••"
              defaultValue={state !== "default" ? "supersecret" : ""}
            />
            <button
              onClick={() => setShow((s) => !s)}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 h-7 w-7 grid place-items-center text-muted-foreground"
            >
              {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
        </div>

        {state === "error" && (
          <div className="text-[12px] text-[#b42318]">
            Student ID or password is incorrect.
          </div>
        )}

        <button
          disabled={state === "loading"}
          className="h-11 w-full rounded-md bg-primary text-primary-foreground text-[14px] font-medium inline-flex items-center justify-center gap-2 disabled:opacity-80"
        >
          {state === "loading" && (
            <span className="h-3.5 w-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin" />
          )}
          {state === "loading" ? "Signing in…" : "Sign in"}
        </button>

        <div className="flex items-center justify-center">
          <button className="text-[13px] text-muted-foreground hover:text-foreground">
            Forgot password?
          </button>
        </div>
      </div>

      <div className="mt-auto pt-8 text-center">
        <div className="text-[11px] text-muted-foreground">
          University IT · v1.0.0
        </div>
      </div>
    </div>
  );
}
