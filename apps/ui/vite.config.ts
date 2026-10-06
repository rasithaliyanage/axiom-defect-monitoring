import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Same-origin proxy to the Domain Runtime. The browser only ever sees
    // http://localhost:5173, so no CORS configuration is needed on either side.
    //
    // Two prefixes are forwarded. `/health` sits outside the versioned API on
    // the service, so it needs its own entry — without it the dev server
    // answers with the SPA shell and a liveness check silently looks healthy.
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: false,
      },
      "/health": {
        target: "http://127.0.0.1:8000",
        changeOrigin: false,
      },
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    include: ["test/**/*.test.tsx", "test/**/*.test.ts"],
    restoreMocks: true,
  },
});
