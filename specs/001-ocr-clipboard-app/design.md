# odOcr Design System

**Applied UI/UX Pro Max rules**: Style Selection (P4), Typography & Color (P6),
Interaction (P2), Layout (P5), Forms & Feedback (P8)

## Product Type Analysis

- **Type**: Tool — OCR scanner/utility
- **Audience**: C-end users needing quick text extraction from clipboard images
- **Tone**: Precise, efficient, reliable, lightweight
- **Key UX principle**: Fast feedback, clear state communication, minimal friction

## Style Direction

**Minimal + Professional** — the tool should feel like a precision instrument:

- Clean, uncluttered terminal output with structured formatting
- System tray icon: simple, recognizable (document with magnifying glass motif)
- Monochromatic palette with a single accent color for status differentiation
- No decorative elements — every visual choice communicates state or action
- Respect platform-native system tray conventions (no custom chrome)

## Color System

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `surface` | #FAFAFA | #1A1A2E | Background (terminal/notification) |
| `surface-elevated` | #FFFFFF | #25253E | Card/popup background |
| `text-primary` | #1E1E2E | #E8E8F0 | Primary text |
| `text-secondary` | #6C6C80 | #9A9AB0 | Secondary/muted text |
| `accent` | #4A6CF7 | #6B8CFF | Success/status — OCR complete, focus |
| `success` | #22A67E | #34D399 | Text extracted successfully |
| `warning` | #E8A838 | #FBBF24 | Low confidence, partial text |
| `error` | #DC3E42 | #F87171 | No text found, processing failure |
| `border` | #E2E2EC | #3A3A52 | Dividers, card borders |

Rationale: Blue accent conveys precision and technology trust. Green/amber/red
for confidence levels follows universal traffic-light semantics (contrast ≥4.5:1
in both modes per WCAG AA). Dark mode uses desaturated tonal variants, not
inverted colors.

## Typography

- **Terminal output**: Monospace (`Cascadia Code` / `JetBrains Mono` /
  `Consolas`) — ensures aligned columns, JSON readability
- **Notifications/UI**: System UI font (`Segoe UI` on Windows) — native feel
- **Scale**: 11px (metadata), 13px (body), 15px (headings in notification)
- **Line-height**: 1.5 for body, 1.3 for headings
- **Font-weight**: 600 for labels/status, 400 for body text

## System Tray Icon

- **Size**: 16×16px (standard tray), 32×32px (high-DPI ready)
- **Design**: Document outline with a magnifying glass overlay — communicates
  "document scanner" in one glyph
- **States**:
  - Idle: default color (accent blue)
  - Processing: brief animated spin or pulse (≤300ms)
  - Success: green check overlay
  - Error: red badge overlay
- **Format**: ICO with embedded 16/32/48px PNG, SVG for fallback

## Notification Popup

- **Position**: Bottom-right (Windows standard), offset 16px from edge
- **Size**: 320×auto (width fixed, height grows with content)
- **Structure**:
  ```
  ┌──────────────────────────────┐
  │ [icon] Text Extracted    [×] │  ← header bar, 32px
  │──────────────────────────────│
  │ "Hello, this is the        │
  │  extracted text content    │  ← body, 2-4 lines max
  │  from your image..."       │
  │──────────────────────────────│
  │ Copied to clipboard  [Open]  │  ← footer, 28px
  └──────────────────────────────┘
  ```
- **Timing**: Auto-dismiss after 5s (per Skill §8 toast-dismiss)
- **Animation**: Slide-in from right, 200ms ease-out (per Skill §7 duration-timing)
- **Contains**: [NEEDS CLARIFICATION: Open action — should clicking Open paste
  into the active window?]

## Terminal Output Format

```
$ odOcr screenshot.png

 ┌─ odOcr ────────────────────────────────────┐
 │ ✓ Text extracted (98% confidence)          │
 │                                             │
 │ "Meeting at 3PM in Conference Room B       │
 │  Agenda: Q3 review, budget approval"        │
 │                                             │
 │ 📋 Copied to clipboard  ⏱ 1.2s             │
 └─────────────────────────────────────────────┘
```

For `--json` output:
```json
{
  "success": true,
  "text": "Meeting at 3PM...",
  "confidence": 0.98,
  "processing_time_ms": 1200,
  "source": "clipboard"
}
```

- **Error state** (per Skill §8 error-clarity): Show cause + how to fix
  ```
  ✗ No text detected
  The image appears to contain no legible text.
  Try: higher resolution image, clearer font, or check
  that the image contains printed/digital text.
  ```

## Interaction Design (per UI/UX Pro Max §2)

| Rule | Implementation |
|------|---------------|
| Touch target ≥44px | System tray icon click area extended via hit area |
| Loading feedback | Processing state in tray icon (pulse) + "Processing..." in notification |
| Error feedback | Toast stays until dismissed on error (no auto-dismiss) |
| Keyboard shortcut | Ctrl+O global hotkey — must not conflict with system shortcuts |
| Hover not relied on | All states visible without hover (tray icon context menu) |
| Press feedback | Tray icon shows brief highlight on click |

## Accessibility (per UI/UX Pro Max §1)

| Rule | Implementation |
|------|---------------|
| Focus states | CLI output uses high-contrast borders, not color-only |
| Keyboard nav | Full CLI with args/flags; no GUI dependency |
| Reduced motion | Respect system animation preferences |
| Screen reader | CLI output sent to stdout (screen-reader accessible) |
| Color not only | Confidence level shown as text + color (e.g., "98% confidence") |

## Settings (v1 Scope)

No settings window in v1. All configuration via CLI flags and a simple config
file (`~/.odOcr/config.json`):

```json
{
  "hotkey": "ctrl+o",
  "output_format": "text",
  "describe": false,
  "language": "eng"
}
```

Per UI/UX Pro Max §8 progressive-disclosure: reveal complex options (image
description, language packs) progressively as the user needs them.

## Dark Mode

System tray context menu includes "Toggle Dark Mode". Default follows system
theme. Terminal output uses ANSI color codes that respect the terminal's own
theme.

## Anti-Patterns to Avoid

- ❌ Emoji as structural icons (use SVG tray icon instead)
- ❌ Settings window with 2 options (use CLI flags + config file)
- ❌ Decorative animations in notifications (use only functional motion)
- ❌ Modal dialogs that block workflow (use non-blocking toasts)
- ❌ Over-engineered GUI when CLI + tray is sufficient (YAGNI)
