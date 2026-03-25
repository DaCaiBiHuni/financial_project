# Investment Tracker

A desktop investment portfolio tracker focused on product trend tracking, portfolio visibility, financial analytics, and future extensibility.

---

## 1. What This Project Is

Investment Tracker is a **desktop-native investment tracking and portfolio analysis prototype**.

It is designed to help users:
- track selected products,
- monitor portfolio positions,
- review market value and profit/loss,
- inspect historical trend data,
- and evolve the product over time with a modular architecture.

This project is **not** intended to be a template-based note-taking tool.  
It is being built as a dedicated financial desktop application.

---

## 2. Current Product Scope

The current prototype already includes the following major areas:

### Products
- add products manually,
- quick-add recommended products,
- refresh current prices,
- refresh one-year trend history,
- inspect price trend chart.

### Portfolio
- add positions,
- track average cost,
- calculate market value,
- calculate profit/loss and profit/loss rate.

### Dashboard
- view high-level summary cards,
- inspect total cost,
- inspect total market value,
- inspect total profit/loss.

### Settings
- switch market data provider,
- persist provider selection locally.

---

## 3. Current Architecture Highlights

The project currently includes:
- desktop UI with PySide6,
- local persistence with SQLite,
- modular product / portfolio / dashboard / settings pages,
- market provider abstraction,
- historical price storage,
- chart rendering with matplotlib,
- strict refresh logic for real-data providers,
- asynchronous refresh handling to avoid blocking the UI.

---

## 4. Repository Structure

```text
investment-tracker/
├─ app/      # desktop application source code
├─ data/     # local database and runtime data
├─ docs/     # product, architecture, planning, and progress documents
└─ README.md
```

### Key folders
- `app/` — application code
- `docs/` — all major project documents
- `data/` — local application data and SQLite database

---

## 5. Documentation Map

Start here if you want to understand the project quickly:

1. `docs/PRD_v1.0.md` — product requirements
2. `docs/POSITIONING_AND_DIFFERENTIATION.md` — positioning and product direction
3. `docs/TECH_DESIGN_v1.0.md` — architecture and technical design
4. `docs/IMPLEMENTATION_PLAN_v1.0.md` — staged build plan
5. `docs/PROGRESS_SNAPSHOT.md` — latest implementation status
6. `docs/DOCS_INDEX.md` — documentation index

---

## 6. Current Status Summary

### Already implemented
- core documentation system
- desktop scaffold
- products page
- portfolio page
- dashboard page
- settings page
- recommended product quick-add
- provider switching
- strict refresh behavior
- split refresh actions for price and trend
- right-side / lower product trend visualization refinements
- asynchronous refresh behavior

### Still improving
- Alpha Vantage real-data validation and throttling behavior
- dashboard chart visualization
- time range switching
- provider-specific error display
- packaging as a standalone executable

---

## 7. Recommended Next Steps

The most valuable next steps are:

1. validate real market data behavior in-app,
2. continue polishing dashboard and chart UX,
3. package a trial executable for hands-on testing,
4. refine provider-specific error states.

---

## 8. Project Direction

The long-term direction remains:

**from prototype → to usable desktop investment tracking tool**

The focus is on:
- automation,
- portfolio analysis,
- trend tracking,
- extensible market data integration,
- and a clean desktop product experience.
