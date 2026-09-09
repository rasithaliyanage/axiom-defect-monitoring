import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/browser',
  workers: 1,
  use: { baseURL: 'http://127.0.0.1:3101', browserName: 'chromium', channel: process.env.PLAYWRIGHT_CHANNEL || 'chrome', headless: true, screenshot: 'only-on-failure' },
  webServer: { command: 'node server/index.js', url: 'http://127.0.0.1:3101/api/health', env: { PORT:'3101', DB_PATH:'data/browser-test.sqlite' }, reuseExistingServer: false },
});
