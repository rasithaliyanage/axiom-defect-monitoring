# Axion Defect Monitoring

A local frontend mockup dashboard for motherboard defect detection statistics. The dashboard uses Next.js, TypeScript, Ant Design, and ECharts with mock inspection data embedded in the frontend.

## Local Development

Install dependencies:

```bash
npm install
```

Start the local dashboard:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

- `npm run dev` starts the Next.js development server.
- `npm run build` creates a production build.
- `npm run start` serves the production build.

## Mock Dashboard Scope

This first mockup is frontend-only. It includes KPI cards, trend analytics, defect category breakdowns, severity progress indicators, and a production line watchlist table. The data is mocked in the dashboard page and can later be moved behind the planned FastAPI layer.