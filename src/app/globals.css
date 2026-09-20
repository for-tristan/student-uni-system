@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

/* =========================================================
   Smart University Assistant — Design Tokens
   Restrained academic palette. No gradients, no glow.
   ========================================================= */

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);

  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);

  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);

  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
  --color-error: var(--error);
  --color-error-foreground: var(--error-foreground);

  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);

  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
}

:root {
  --radius: 8px;

  /* Surface system — neutral foundation */
  --background: #f7f7f5;
  --foreground: #171717;

  --card: #ffffff;
  --card-foreground: #171717;

  --popover: #ffffff;
  --popover-foreground: #171717;

  /* Accent — used sparingly. Single accent color, no gradient. */
  --primary: #315cff;
  --primary-foreground: #ffffff;

  --secondary: #efefec;
  --secondary-foreground: #171717;

  --muted: #f1f1ee;
  --muted-foreground: #666666;

  --accent: #eef1ff;
  --accent-foreground: #1d3a8a;

  --destructive: #b42318;
  --destructive-foreground: #ffffff;

  --success: #2f7d4a;
  --success-foreground: #ffffff;
  --warning: #a66a00;
  --warning-foreground: #ffffff;
  --error: #b42318;
  --error-foreground: #ffffff;

  --border: #e4e4e1;
  --input: #e4e4e1;
  --ring: #315cff;

  /* Sidebar — slightly off-white for separation */
  --sidebar: #ffffff;
  --sidebar-foreground: #171717;
  --sidebar-primary: #315cff;
  --sidebar-primary-foreground: #ffffff;
  --sidebar-accent: #f1f1ee;
  --sidebar-accent-foreground: #171717;
  --sidebar-border: #e4e4e1;
  --sidebar-ring: #315cff;
}

.dark {
  --background: #0f0f0e;
  --foreground: #ededea;

  --card: #18181a;
  --card-foreground: #ededea;

  --popover: #18181a;
  --popover-foreground: #ededea;

  --primary: #5277ff;
  --primary-foreground: #ffffff;

  --secondary: #222226;
  --secondary-foreground: #ededea;

  --muted: #1c1c1e;
  --muted-foreground: #9a9a96;

  --accent: #1a2348;
  --accent-foreground: #c7d2ff;

  --destructive: #d4453a;
  --destructive-foreground: #ffffff;

  --success: #3f9463;
  --success-foreground: #ffffff;
  --warning: #c08422;
  --warning-foreground: #ffffff;
  --error: #d4453a;
  --error-foreground: #ffffff;

  --border: #2a2a2d;
  --input: #2a2a2d;
  --ring: #5277ff;

  --sidebar: #131316;
  --sidebar-foreground: #ededea;
  --sidebar-primary: #5277ff;
  --sidebar-primary-foreground: #ffffff;
  --sidebar-accent: #1f1f22;
  --sidebar-accent-foreground: #ededea;
  --sidebar-border: #2a2a2d;
  --sidebar-ring: #5277ff;
}

@layer base {
  * {
    @apply border-border;
  }
  html, body {
    background: var(--background);
    color: var(--foreground);
    font-family: var(--font-geist-sans), ui-sans-serif, system-ui, -apple-system,
      "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-feature-settings: "ss01", "cv11";
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  /* Tabular numerals everywhere by default — keeps tables and credits steady */
  table, .tnum {
    font-variant-numeric: tabular-nums;
  }

  /* Subtle, focused focus ring. Not glow. */
  :focus-visible {
    outline: 2px solid var(--ring);
    outline-offset: 2px;
    border-radius: 2px;
  }

  /* Hide default scrollbar styling — keep it subtle */
  .scroll-thin::-webkit-scrollbar { width: 8px; height: 8px; }
  .scroll-thin::-webkit-scrollbar-thumb { background: #d4d4d0; border-radius: 8px; }
  .scroll-thin::-webkit-scrollbar-track { background: transparent; }
}

/* Reusable primitives — used across the design system pages */
@layer components {
  .grid-dots {
    background-image: radial-gradient(circle, #d8d8d3 1px, transparent 1px);
    background-size: 16px 16px;
  }
  .device-frame {
    box-shadow:
      0 0 0 1px #e4e4e1,
      0 1px 2px rgba(15, 15, 15, 0.04),
      0 8px 24px rgba(15, 15, 15, 0.06);
    border-radius: 36px;
  }
  .hairline {
    background: var(--border);
  }
}
