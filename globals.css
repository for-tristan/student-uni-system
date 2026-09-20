"use client";

import * as React from "react";
import { DesignShell, type DesignPage } from "@/design/shell/design-shell";
import { FoundationsPage } from "@/design/foundations/foundations-page";
import { ComponentsPage } from "@/design/components/components-page";
import { MobileAuthPage } from "@/design/mobile/mobile-auth-page";
import { MobileStudentPage } from "@/design/mobile/mobile-student-page";
import { MobileAssistantPage } from "@/design/mobile/mobile-assistant-page";
import { WebAdminPage } from "@/design/web/web-admin-page";
import { ResponsivePage } from "@/design/web/responsive-page";
import { ExportPage } from "@/design/export/export-page";

export default function Page() {
  const [page, setPage] = React.useState<DesignPage>("foundations");

  return (
    <DesignShell page={page} onChange={setPage}>
      {renderPage(page)}
    </DesignShell>
  );
}

function renderPage(page: DesignPage) {
  switch (page) {
    case "foundations":
      return <FoundationsPage />;
    case "components":
      return <ComponentsPage />;
    case "mobile-auth":
      return <MobileAuthPage />;
    case "mobile-student":
      return <MobileStudentPage />;
    case "mobile-assistant":
      return <MobileAssistantPage />;
    case "web-admin":
      return <WebAdminPage />;
    case "web-assistant":
      return <WebAssistantStandalone />;
    case "responsive":
      return <ResponsivePage />;
    case "export":
      return <ExportPage />;
  }
}

import { AdminPageView } from "@/design/web/web-admin-page";

function WebAssistantStandalone() {
  return (
    <div className="space-y-6">
      <section>
        <div className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground mb-2">
          07 — Web · Assistant
        </div>
        <h1 className="text-[26px] font-semibold tracking-[-0.01em]">
          University assistant — desktop
        </h1>
        <p className="text-[14px] text-muted-foreground mt-2 max-w-2xl leading-relaxed">
          Conversation list on the left, conversation on the right. Student context is
          shown inline so the staff member can answer accurately without leaving the
          conversation.
        </p>
      </section>
      <div
        className="device-frame overflow-hidden bg-card"
        style={{ width: 1440, height: 900, borderRadius: 12 }}
      >
        <div className="h-9 border-b border-border flex items-center px-3 gap-2 bg-muted/40">
          <div className="flex gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-[#e4e4e1]" />
            <span className="h-2.5 w-2.5 rounded-full bg-[#e4e4e1]" />
            <span className="h-2.5 w-2.5 rounded-full bg-[#e4e4e1]" />
          </div>
          <div className="mx-auto h-6 min-w-64 px-3 bg-card border border-border rounded-md flex items-center text-[11px] text-muted-foreground">
            assistant.uni.edu/admin/assistant
          </div>
        </div>
        <div style={{ height: 900 - 36 }} className="overflow-hidden">
          <AdminPageView page="assistant" />
        </div>
      </div>
    </div>
  );
}
