"use client";

import * as React from "react";
import {
  MessageSquare,
  ChevronRight,
  Send,
  BookOpen,
  FileText,
  User,
  Clock,
} from "lucide-react";
import { PhoneFrame } from "../shell/frames";
import {
  ASSISTANT_CONVERSATION,
  SUGGESTED_PROMPTS,
  STUDENT,
} from "../data/mock";

export function MobileAssistantPage() {
  return (
    <div className="space-y-8">
      <section>
        <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
          05 — Mobile · Assistant
        </div>
        <h1 className="text-[26px] font-semibold tracking-[-0.01em]">Assistant</h1>
        <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
          A university assistant
        </p>
      </section>

      <div className="flex flex-wrap gap-8">
        <PhoneFrame label="Assistant — empty" caption="Suggested academic prompts">
          <AssistantScreen state="empty" />
        </PhoneFrame>
        <PhoneFrame label="Assistant — conversation" caption="Source tags, course references">
          <AssistantScreen state="chat" />
        </PhoneFrame>
        <PhoneFrame label="Assistant — course reference" caption="Inline course card with action">
          <AssistantScreen state="reference" />
        </PhoneFrame>
      </div>
    </div>
  );
}

function AssistantScreen({
  state,
}: {
  state: "empty" | "chat" | "reference";
}) {
  const messages =
    state === "empty"
      ? []
      : state === "reference"
        ? [ASSISTANT_CONVERSATION[0], { ...ASSISTANT_CONVERSATION[1], content: "Machine Learning (CS-421) is an advanced course covering supervised and unsupervised learning. It is offered in Fall 2025.", sources: [{ label: "Course catalog", code: "CS-421" }] }]
        : ASSISTANT_CONVERSATION;

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="h-12 px-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-7 w-7 rounded-md bg-foreground text-background grid place-items-center">
              <MessageSquare className="h-3.5 w-3.5" />
            </div>
            <div>
              <div className="text-[13px] font-medium">University Assistant</div>
              <div className="text-[10px] text-muted-foreground">
                {STUDENT.major} · {STUDENT.year}
              </div>
            </div>
          </div>
          <button className="text-[12px] text-muted-foreground">New</button>
        </div>
      </header>

      {/* Conversation area */}
      <div className="flex-1 overflow-y-auto scroll-thin px-4 py-4 space-y-4">
        {messages.length === 0 ? (
          <EmptyAssistant />
        ) : (
          <>
            {messages.map((m, i) => (
              <Message key={i} role={m.role} content={m.content} sources={m.sources} />
            ))}

            {state === "reference" && (
              <CourseReferenceCard
                code="CS-421"
                name="Machine Learning"
                meta="AI · Advanced · 3 credits"
              />
            )}

            <div className="text-center text-[10px] text-muted-foreground pt-2">
              Sources cited where available.
            </div>
          </>
        )}
      </div>

      {/* Suggested prompts (only when empty) */}
      {state === "empty" && (
        <div className="px-4 pb-3">
          <div className="text-[11px] uppercase tracking-[0.06em] text-muted-foreground mb-2">
            Try asking
          </div>
          <div className="grid grid-cols-1 gap-1.5">
            {SUGGESTED_PROMPTS.slice(0, 3).map((p) => (
              <button
                key={p}
                className="h-9 px-3 rounded-md border border-border bg-card text-[13px] text-left text-foreground inline-flex items-center justify-between"
              >
                {p}
                <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Composer */}
      <div className="border-t border-border bg-card p-3">
        <div className="flex items-end gap-2">
          <textarea
            rows={1}
            placeholder="Ask about courses, prerequisites, university rules…"
            className="flex-1 resize-none min-h-[40px] max-h-24 px-3 py-2 rounded-md border border-border bg-card text-[13px] placeholder:text-muted-foreground/70"
          />
          <button className="h-10 w-10 rounded-md bg-primary text-primary-foreground grid place-items-center shrink-0">
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

function EmptyAssistant() {
  return (
    <div className="h-full flex flex-col items-center justify-center text-center px-6">
      <div className="h-10 w-10 rounded-md border border-border bg-card grid place-items-center text-muted-foreground">
        <MessageSquare className="h-4 w-4" />
      </div>
      <div className="text-[15px] font-medium mt-3">Ask about your studies.</div>
      <p className="text-[13px] text-muted-foreground mt-1 leading-relaxed max-w-[260px]">
        Course prerequisites, next-semester options, completed courses, university rules.
      </p>
    </div>
  );
}

function Message({
  role,
  content,
  sources,
}: {
  role: "user" | "assistant";
  content: string;
  sources?: { label: string; code?: string }[];
}) {
  if (role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] bg-muted text-foreground px-3 py-2 rounded-lg rounded-br-sm text-[13px] leading-relaxed">
          {content}
        </div>
      </div>
    );
  }

  // assistant — border, not bubble tint
  return (
    <div className="flex justify-start">
      <div className="max-w-[88%]">
        <div className="bg-card border border-border px-3 py-2 rounded-lg rounded-bl-sm text-[13px] leading-relaxed">
          <FormattedContent text={content} />
        </div>
        {sources && sources.length > 0 && (
          <div className="mt-1.5 flex flex-wrap gap-1.5">
            {sources.map((s, i) => (
              <span
                key={i}
                className="text-[10px] inline-flex items-center gap-1 px-1.5 h-5 rounded border border-border text-muted-foreground bg-card"
              >
                {s.code ? <FileText className="h-3 w-3" /> : <BookOpen className="h-3 w-3" />}
                {s.label}{s.code ? ` · ${s.code}` : ""}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function FormattedContent({ text }: { text: string }) {
  // very light formatting — render numbered/bulleted lines and paragraphs
  const lines = text.split("\n");
  return (
    <div className="space-y-1.5">
      {lines.map((line, i) => {
        const numbered = /^\d+\.\s/.test(line);
        const bulleted = /^•\s/.test(line);
        if (numbered || bulleted) {
          return (
            <div key={i} className="text-muted-foreground pl-3">
              <span className="text-foreground tabular-nums">{line}</span>
            </div>
          );
        }
        if (line.trim() === "") return <div key={i} className="h-1.5" />;
        return <p key={i}>{line}</p>;
      })}
    </div>
  );
}

function CourseReferenceCard({
  code,
  name,
  meta,
}: {
  code: string;
  name: string;
  meta: string;
}) {
  return (
    <div className="border border-border rounded-lg overflow-hidden bg-card">
      <div className="px-3 py-2.5 border-b border-border">
        <div className="flex items-center gap-2">
          <BookOpen className="h-3.5 w-3.5 text-muted-foreground" />
          <span className="text-[10px] uppercase tracking-[0.06em] text-muted-foreground">
            Course reference
          </span>
        </div>
      </div>
      <div className="px-3 py-3">
        <div className="flex items-baseline justify-between">
          <div className="text-[14px] font-medium">{name}</div>
          <code className="text-[11px] text-muted-foreground tabular-nums">{code}</code>
        </div>
        <div className="text-[12px] text-muted-foreground mt-0.5">{meta}</div>
      </div>
      <div className="border-t border-border p-2 flex justify-end">
        <button className="h-8 px-3 rounded-md bg-primary text-primary-foreground text-[12px] font-medium inline-flex items-center gap-1">
          View course <ChevronRight className="h-3 w-3" />
        </button>
      </div>
    </div>
  );
}

// unused exports to silence lint
export const _icons = { User, Clock };
