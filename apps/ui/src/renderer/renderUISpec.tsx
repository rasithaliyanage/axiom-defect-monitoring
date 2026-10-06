/**
 * The controlled renderer.
 *
 * Entry point contract:  render(approvedUISpec, options)
 *
 * The argument is an ALREADY-VALIDATED UISpec. This module performs no schema
 * validation and no grounding checks — those belong to
 * `specs/schemas/ui-spec.schema.json` and `services/domain/validator.py`, and
 * duplicating them here would create a second, divergent authority.
 *
 * There is deliberately no `render(rawAIOutput)`. Raw model output has no entry
 * point into this module.
 *
 * `options.actionLabels` carries `GroundedContext.actions[].label`. It is
 * domain-supplied data, never model output.
 */

import type { JSX } from "react";

import type { ApprovedUISpec } from "./approved";
import { componentRegistry, hasRegisteredComponent } from "./registry";
import {
  isApprovedComponent,
  type Block,
  type Omission,
  type RenderContext,
  type RenderOptions,
} from "./types";

function renderBlock(block: Block, ctx: RenderContext): JSX.Element {
  // Exhaustive switch over the discriminated union. Each case narrows `props`
  // to that component's own type, so the registry entry is called with exactly
  // the props it declares. `noFallthroughCasesInSwitch` and the `never` default
  // make a missing case a compile error.
  switch (block.component) {
    case "Hero":
      return componentRegistry.Hero(block.props, ctx);
    case "Heading":
      return componentRegistry.Heading(block.props, ctx);
    case "Text":
      return componentRegistry.Text(block.props, ctx);
    case "FeatureCard":
      return componentRegistry.FeatureCard(block.props, ctx);
    case "FeatureGrid":
      return componentRegistry.FeatureGrid(block.props, ctx);
    case "CTA":
      return componentRegistry.CTA(block.props, ctx);
    case "Alert":
      return componentRegistry.Alert(block.props, ctx);
    case "InfoPanel":
      return componentRegistry.InfoPanel(block.props, ctx);
    case "ProgressIndicator":
      return componentRegistry.ProgressIndicator(block.props, ctx);
    default: {
      const unreachable: never = block;
      throw new Error(`Unhandled approved component: ${JSON.stringify(unreachable)}`);
    }
  }
}

export interface UISpecRendererProps {
  /**
   * An approved handle, not a raw specification. The type makes it impossible
   * to pass unprepared JSON here — see `approved.ts` for what the brand does
   * and does not prove.
   */
  readonly spec: ApprovedUISpec;
  readonly options: RenderOptions;
}

export function UISpecRenderer({ spec, options }: UISpecRendererProps): JSX.Element {
  const record = (omission: Omission): void => {
    options.onOmission?.(omission);
  };

  const invoke = (action: Parameters<NonNullable<RenderOptions["onAction"]>>[0]): void => {
    options.onAction?.(action);
  };

  return (
    <main className="uispec-page" data-page={spec.page}>
      {spec.blocks.map((block, index) => {
        const path = `/blocks/${index}`;

        // Defence in depth. A validated spec cannot reach here with an
        // unapproved component — the schema's `oneOf` over nine discriminated
        // blocks rejects it at Gate 1, and the validator at Gate 2. This guard
        // exists for inputs that bypassed validation; per docs/architecture.md
        // the block is omitted and the omission recorded, never resolved by any
        // other means and never repaired or relabelled.
        const name: string = (block as { component: string }).component;
        if (!isApprovedComponent(name) || !hasRegisteredComponent(name)) {
          record({
            reason: "unapproved-component",
            path,
            detail: `Component "${name}" is not in the registry; block omitted`,
          });
          return null;
        }

        const ctx: RenderContext = {
          actionLabels: options.actionLabels,
          invoke,
          record,
          path,
        };

        return (
          <div className="uispec-block" key={`${index}-${name}`}>
            {renderBlock(block, ctx)}
          </div>
        );
      })}
    </main>
  );
}
