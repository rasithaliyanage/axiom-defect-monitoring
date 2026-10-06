/**
 * The nine approved components. Every pixel the renderer can produce originates
 * here, so the whole renderable surface is kept in one reviewable file.
 *
 * Rules that hold in every component below:
 *   - Props are destructured by name. No object spreading onto any DOM element.
 *   - Model-supplied strings are rendered as React text children only, so React
 *     escapes them. No `dangerouslySetInnerHTML`, no markup parsing.
 *   - Closed enums select from fixed literal maps. No value from the spec is
 *     ever used as a tag name, URL, style string, or event handler.
 *   - Identifiers (`capabilityId`, `alertId`, `metricId`, `defectCategoryId`)
 *     are grounding references, not display text, and are not rendered.
 */

import type { JSX } from "react";

import type {
  AlertProps,
  CtaProps,
  FeatureCardProps,
  FeatureGridProps,
  HeadingProps,
  HeroProps,
  IconId,
  InfoPanelProps,
  ProgressIndicatorProps,
  RenderContext,
  Severity,
  TextProps,
} from "../renderer/types";

/** Fixed literal maps. A spec value can only select, never supply, a class. */
const ICON_CLASS: Readonly<Record<IconId, string>> = {
  inspection: "icon icon-inspection",
  defect: "icon icon-defect",
  report: "icon icon-report",
  image: "icon icon-image",
  trend: "icon icon-trend",
};

/** Severity is conveyed as text, not colour alone. */
const SEVERITY_TEXT: Readonly<Record<Severity, string>> = {
  info: "Information",
  warning: "Warning",
  critical: "Critical",
};

const SEVERITY_CLASS: Readonly<Record<Severity, string>> = {
  info: "alert alert-info",
  warning: "alert alert-warning",
  critical: "alert alert-critical",
};

export function Hero(props: HeroProps, ctx: RenderContext): JSX.Element {
  const { eyebrow, title, subtitle, primaryAction } = props;

  // `primaryAction` is an identifier; the contract carries no label prop for it.
  // The label comes from the grounded context. Without one there is no
  // accessible name, so no control is rendered and the gap is recorded.
  let action: JSX.Element | null = null;
  if (primaryAction !== undefined) {
    const label = ctx.actionLabels[primaryAction];
    if (label === undefined || label.length === 0) {
      ctx.record({
        reason: "missing-action-label",
        path: `${ctx.path}/props/primaryAction`,
        detail: `No supplied label for action "${primaryAction}"; control omitted`,
      });
    } else {
      action = (
        <button type="button" className="hero-action" onClick={() => ctx.invoke(primaryAction)}>
          {label}
        </button>
      );
    }
  }

  return (
    <section className="hero">
      {eyebrow === undefined ? null : <p className="hero-eyebrow">{eyebrow}</p>}
      <h1 className="hero-title">{title}</h1>
      {subtitle === undefined ? null : <p className="hero-subtitle">{subtitle}</p>}
      {action}
    </section>
  );
}

export function Heading(props: HeadingProps): JSX.Element {
  const { level, text } = props;
  // Explicit branches. The level never becomes a computed tag name.
  return level === 2 ? (
    <h2 className="heading heading-2">{text}</h2>
  ) : (
    <h3 className="heading heading-3">{text}</h3>
  );
}

export function Text(props: TextProps): JSX.Element {
  const { text, tone } = props;
  return <p className={tone === "muted" ? "text text-muted" : "text"}>{text}</p>;
}

export function FeatureCard(props: FeatureCardProps): JSX.Element {
  const { title, body, icon } = props;
  return (
    <article className="feature-card">
      {icon === undefined ? null : <span className={ICON_CLASS[icon]} aria-hidden="true" />}
      <h3 className="feature-card-title">{title}</h3>
      <p className="feature-card-body">{body}</p>
    </article>
  );
}

export function FeatureGrid(props: FeatureGridProps): JSX.Element {
  const { columns, items } = props;
  return (
    <div className={columns === 2 ? "feature-grid feature-grid-2" : "feature-grid feature-grid-3"}>
      {items.map((item, index) => (
        // `items` holds FeatureCard PROPS objects, not blocks. Order preserved.
        // Invoked directly rather than spread as JSX props, so nothing from the
        // spec is ever spread onto an element.
        <div className="feature-grid-cell" key={`${index}-${item.title}`}>
          {FeatureCard(item)}
        </div>
      ))}
    </div>
  );
}

export function CTA(props: CtaProps, ctx: RenderContext): JSX.Element {
  const { label, action, variant } = props;
  return (
    <button
      type="button"
      className={variant === "secondary" ? "cta cta-secondary" : "cta cta-primary"}
      onClick={() => ctx.invoke(action)}
    >
      {label}
    </button>
  );
}

export function Alert(props: AlertProps): JSX.Element {
  const { severity, title, body } = props;
  return (
    <section
      className={SEVERITY_CLASS[severity]}
      role={severity === "info" ? "status" : "alert"}
    >
      <p className="alert-severity">{SEVERITY_TEXT[severity]}</p>
      <h3 className="alert-title">{title}</h3>
      <p className="alert-body">{body}</p>
    </section>
  );
}

export function InfoPanel(props: InfoPanelProps): JSX.Element {
  const { title, rows } = props;
  return (
    <section className="info-panel">
      <h3 className="info-panel-title">{title}</h3>
      <dl className="info-panel-rows">
        {rows.map((row) => (
          <div className="info-panel-row" key={row.metricId}>
            <dt className="info-panel-label">{row.label}</dt>
            {/* Value and unit are copied verbatim. Never parsed or reformatted. */}
            <dd className="info-panel-value">
              {row.value}
              {row.unit === undefined ? null : <span className="info-panel-unit">{row.unit}</span>}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

export function ProgressIndicator(props: ProgressIndicatorProps): JSX.Element {
  const { label, value, caption } = props;
  // `String(value)` preserves the supplied number exactly. No rounding, no
  // formatting, no derived figure.
  const shown = String(value);
  return (
    <section className="progress">
      <p className="progress-label" id={`progress-${props.metricId}`}>
        {label}
      </p>
      <div
        className="progress-bar"
        role="progressbar"
        aria-labelledby={`progress-${props.metricId}`}
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuetext={`${shown} percent`}
      />
      <p className="progress-value">{shown}</p>
      {caption === undefined ? null : <p className="progress-caption">{caption}</p>}
    </section>
  );
}
