/**
 * Browser entry point.
 *
 * Mounts the application root. It accepts no input of any kind: no query
 * string, no hash payload, no fetch, no upload. The page it renders is fixed
 * at build time by the prepared fixture catalogue.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "./App";
import "./style.css";

const container = document.getElementById("root");
if (container === null) {
  throw new Error("Missing #root element in index.html");
}

createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
