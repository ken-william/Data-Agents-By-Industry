---
name: baseline-ui
description: Quickly deslop UI code by fixing spacing, hierarchy, typography, and small layout issues. Use when the interface needs a fast cleanup or polish pass.
---

# Baseline UI

Enforces an opinionated UI baseline to prevent AI-generated interface slop.

## How to use

- Apply these constraints to any UI work in this project.

## Stack & Utilities

- MUST use Tailwind CSS defaults unless custom values already exist or are explicitly requested.
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic.
- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs.
- MUST use `tabular-nums` for numerical data.
- SHOULD use `truncate` or `line-clamp` for dense UI.

## Components & Accessibility

- MUST add an `aria-label` to icon-only buttons.
- SHOULD prefer accessible component primitives for anything with keyboard or focus behavior.
- NEVER mix primitive systems within the same interaction surface.

## Interaction & Layout

- NEVER use `h-screen`, use `h-dvh` (dynamic viewport height).
- MUST respect `safe-area-inset` for fixed elements.
- MUST show errors next to where the action happens.
- NEVER block paste in `input` or `textarea` elements.
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`.

## Animation & Performance

- MUST animate only compositor props (`transform`, `opacity`).
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`).
- SHOULD avoid animating heavy `blur()` or `backdrop-filter` surfaces continuously.
- SHOULD respect `prefers-reduced-motion`.
- NEVER exceed `200ms` for interaction feedback.

## Design Discipline

- MUST give empty states one clear next action.
- SHOULD limit accent color usage to one primary accent per view.
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones.
