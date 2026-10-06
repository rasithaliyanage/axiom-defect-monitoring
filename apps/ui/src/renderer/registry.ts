/**
 * The component registry: the only path from an approved component name to a
 * React implementation.
 *
 * Developer-authored and closed. There is no dynamic discovery, no string-to-
 * component lookup outside this map, and no fallback resolution. The mapped type
 * makes the map exhaustive — omitting an approved component, or adding a name
 * outside `ComponentName`, is a compile error.
 */

import type { JSX } from "react";

import {
  Alert,
  CTA,
  FeatureCard,
  FeatureGrid,
  Heading,
  Hero,
  InfoPanel,
  ProgressIndicator,
  Text,
} from "../components/approved";
import type { ComponentName, PropsByComponent, RenderContext } from "./types";

export type BlockRenderer<K extends ComponentName> = (
  props: PropsByComponent[K],
  ctx: RenderContext,
) => JSX.Element;

export type ComponentRegistry = {
  readonly [K in ComponentName]: BlockRenderer<K>;
};

export const componentRegistry: ComponentRegistry = {
  Hero,
  Heading,
  Text,
  FeatureCard,
  FeatureGrid,
  CTA,
  Alert,
  InfoPanel,
  ProgressIndicator,
};

/**
 * Own-property lookup. Guards against inherited keys such as `toString`,
 * `constructor` or `__proto__` resolving as if they were approved components.
 */
export function hasRegisteredComponent(name: string): name is ComponentName {
  return Object.prototype.hasOwnProperty.call(componentRegistry, name);
}
