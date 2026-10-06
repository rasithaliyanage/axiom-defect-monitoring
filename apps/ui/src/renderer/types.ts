/**
 * Types mirroring `specs/schemas/ui-spec.schema.json` (the authoritative copy,
 * the one `services/domain/validator.py` loads).
 *
 * These types describe the shape of an ALREADY-VALIDATED UISpec. They are not a
 * validator. Structural conformance is proved by the JSON Schema and grounding
 * by the Python validator; a TypeScript type is not evidence of either.
 */

export const COMPONENT_NAMES = [
  "Hero",
  "Heading",
  "Text",
  "FeatureCard",
  "FeatureGrid",
  "CTA",
  "Alert",
  "InfoPanel",
  "ProgressIndicator",
] as const;

export type ComponentName = (typeof COMPONENT_NAMES)[number];

export const ACTION_IDS = [
  "view-inspection-queue",
  "view-defect-reports",
  "view-ingest-activity",
  "open-documentation",
  "contact-support",
] as const;

export type ActionId = (typeof ACTION_IDS)[number];

/** Set lookup avoids prototype-chain keys resolving as approved names. */
const APPROVED_COMPONENTS: ReadonlySet<string> = new Set(COMPONENT_NAMES);
const APPROVED_ACTIONS: ReadonlySet<string> = new Set(ACTION_IDS);

export function isApprovedComponent(name: string): name is ComponentName {
  return APPROVED_COMPONENTS.has(name);
}

export function isApprovedAction(id: string): id is ActionId {
  return APPROVED_ACTIONS.has(id);
}

export type Tone = "default" | "muted";
export type Severity = "info" | "warning" | "critical";
export type Variant = "primary" | "secondary";
export type IconId = "inspection" | "defect" | "report" | "image" | "trend";
export type HeadingLevel = 2 | 3;
export type GridColumns = 2 | 3;

export interface HeroProps {
  readonly eyebrow?: string;
  readonly title: string;
  readonly subtitle?: string;
  readonly primaryAction?: ActionId;
}

export interface HeadingProps {
  readonly level: HeadingLevel;
  readonly text: string;
}

export interface TextProps {
  readonly text: string;
  readonly tone?: Tone;
}

export interface FeatureCardProps {
  readonly title: string;
  readonly body: string;
  readonly icon?: IconId;
  readonly capabilityId?: string;
}

export interface FeatureGridProps {
  readonly columns: GridColumns;
  readonly items: readonly FeatureCardProps[];
}

export interface CtaProps {
  readonly label: string;
  readonly action: ActionId;
  readonly variant?: Variant;
}

export interface AlertProps {
  readonly severity: Severity;
  readonly title: string;
  readonly body: string;
  readonly defectCategoryId?: string;
  readonly alertId?: string;
}

export interface InfoPanelRow {
  readonly metricId: string;
  readonly label: string;
  readonly value: string;
  readonly unit?: string;
}

export interface InfoPanelProps {
  readonly title: string;
  readonly rows: readonly InfoPanelRow[];
}

export interface ProgressIndicatorProps {
  readonly metricId: string;
  readonly label: string;
  readonly value: number;
  readonly caption?: string;
}

/** Props carried by each approved component name. */
export interface PropsByComponent {
  readonly Hero: HeroProps;
  readonly Heading: HeadingProps;
  readonly Text: TextProps;
  readonly FeatureCard: FeatureCardProps;
  readonly FeatureGrid: FeatureGridProps;
  readonly CTA: CtaProps;
  readonly Alert: AlertProps;
  readonly InfoPanel: InfoPanelProps;
  readonly ProgressIndicator: ProgressIndicatorProps;
}

export type Block = {
  [K in ComponentName]: { readonly component: K; readonly props: PropsByComponent[K] };
}[ComponentName];

export interface UISpec {
  readonly specVersion: "1.0";
  readonly page: "landing";
  readonly contextId: string;
  readonly blocks: readonly Block[];
}

/**
 * Human-readable action labels, sourced from `GroundedContext.actions[].label`.
 *
 * Supplied by the Domain Runtime, never by the model. `Hero.primaryAction` is an
 * identifier with no label prop in the contract, so without this map a Hero
 * action cannot be given an accessible name and no control is rendered.
 */
export type ActionLabels = Partial<Readonly<Record<ActionId, string>>>;

export type ActionHandler = (action: ActionId) => void;

/** Why a block or control was not rendered. Recorded, never hidden. */
export type OmissionReason = "unapproved-component" | "missing-action-label";

export interface Omission {
  readonly reason: OmissionReason;
  readonly path: string;
  readonly detail: string;
}

export interface RenderOptions {
  readonly actionLabels: ActionLabels;
  readonly onAction?: ActionHandler;
  readonly onOmission?: (omission: Omission) => void;
}

/** Everything a component may use beyond its own approved props. */
export interface RenderContext {
  readonly actionLabels: ActionLabels;
  readonly invoke: ActionHandler;
  readonly record: (omission: Omission) => void;
  readonly path: string;
}
