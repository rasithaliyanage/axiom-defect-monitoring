# Axion customer demonstration

Interactive React mock of existing backlog stories PB-021 through PB-027: login, production overview, line filters, inspection evidence, human decisions and history. The product backlog and architecture are unchanged. React replaces Angular **only for this requested demonstration**.

## Run locally

Requires Node.js 24 or newer (built-in SQLite) and npm.

```powershell
cd demo
npm install
npm run dev
```

Open **http://127.0.0.1:5173**. The development command starts the React/Vite frontend and local API together.

For a single-server customer presentation:

```powershell
npm run build
npm start
```

Open **http://127.0.0.1:3001**. Both commands run from `demo`.

Demo account: **inspector@axion.demo** / **Demo@123**. Credentials are prefilled. Sign-in uses a locally hashed password and an HTTP-only session cookie; this is not enterprise SSO.

## Presentation flow

1. Sign in as Maya Chen, Quality inspector.
2. Explore the production overview: four line cards, outcome counts, hourly activity and original defect distribution. Choose a line/time period or export the filtered records to CSV.
3. Click **Simulate inspection** to insert a new flagged board into the database.
4. Open **Review queue**, then the first board. Select defect boxes or findings; zoom, rotate or hide overlays.
5. Choose **Confirm failure**, **Override to pass**, or **Escalate review**. Enter a reason of at least 10 characters, then confirm.
6. Open **Decision history**, refresh, and return to the dashboard to show that saved decisions persist and metrics update.

## Database and sample data

The first API startup creates `data/demo.sqlite` with users, sessions, production lines, 181 inspection attempts, defects, reviews and audit history. Seed timestamps are relative to first startup. Use **All demo data** when presenting on a later day; recent-hour filters intentionally omit older data. The simulated equipment state is separate from inspection outcomes.

Review writes update the authoritative disposition and append review/audit rows in one transaction. Original AI disposition and defect findings remain unchanged. Stale record versions return a conflict; incomplete inspections cannot be passed through the review screen. A simulation adds one new REVIEW inspection. Data survives server restarts.

To start a fresh demo without losing an earlier presentation, stop the API and select a different database file:

```powershell
$env:DB_PATH = 'data/customer-session-2.sqlite'
npm start
```

The data directory, dependencies, builds and test outputs are ignored by Git. Do not use this database for production/customer confidential data.

## Verification

```powershell
npm test
npm run build
npm run test:ui
```

API tests use a temporary database. Browser tests use installed Google Chrome and `data/browser-test.sqlite` on port 3101, isolated from the presentation database. Browser tests require the build first. Set `PLAYWRIGHT_CHANNEL=msedge` to use installed Microsoft Edge instead. They exercise login, review persistence, history, navigation, filters and mobile width.

## Demonstration boundaries

This is a local customer-experience mock, not the full production implementation. Motherboard evidence is a code-drawn illustration with selectable synthetic defects, not a real camera image or AI inference. Model scores, inference timing, production targets and equipment status are sample values, not approved quality/performance claims. No PLC, MES, email, enterprise identity provider or manufacturing equipment is connected; saving a decision never releases a physical board.

The demo inspector is deliberately permitted all three simulated review actions. Production role scoping, review assignment, full evidence ingestion, HA, durable broker delivery and governed model deployment remain backlog work. The server binds to loopback by default. The optional Google font has a system-font fallback; the demo's code and board evidence are local assets.
