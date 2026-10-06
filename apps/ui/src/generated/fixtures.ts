// GENERATED FILE — DO NOT EDIT.
// Produced by apps/ui/scripts/prepare_fixtures.py.
// Every entry below was validated by services/domain/validator.py against its
// matching synthetic GroundedContext before this file was written. Editing it by
// hand breaks that guarantee, because nothing here is re-checked at runtime.
//
// Content is synthetic demonstration data. It is not a live production result.

import type { ActionLabels, UISpec } from "../renderer/types";

export type FixtureName = "full-catalogue" | "task4-demo" | "fallback";

export interface VerificationRecord {
  readonly name: FixtureName;
  readonly contextId: string;
  readonly status: "VALID";
  readonly specSha256: string;
  readonly contextSha256: string;
}

/** Evidence of the offline validation run that produced this file. */
export const VERIFICATION: readonly VerificationRecord[] = [
  {
    "name": "full-catalogue",
    "contextId": "task4-catalogue",
    "status": "VALID",
    "specSha256": "413e07cd153e026e32cc4d43f23631ceacf2872cc62704c12705e4a28d809a55",
    "contextSha256": "039f71698c604f30aa4d07fc4e668a50c14f125e80646b3b41011e68ea7bdb17"
  },
  {
    "name": "task4-demo",
    "contextId": "task4-demo",
    "status": "VALID",
    "specSha256": "4cb798f177c4ecb1b304a14fc404b28cb48ed9af45f6e30e1e92fbbd68f250d1",
    "contextSha256": "91e9a8a848c49250570555f81582c91566671a05cb846d5871facae76edcc6f5"
  },
  {
    "name": "fallback",
    "contextId": "fallback",
    "status": "VALID",
    "specSha256": "cb3a1ab0ff5e8252e2b0235e7efae134521d1927df9fa6058867519f51fad8a7",
    "contextSha256": "2c03559003f56a60af54133782b67e9a48075453904cdbba285d7252ae6c0090"
  }
] as const;

/** Action labels lifted from each validated context. Never model-authored. */
export const ACTION_LABELS: Readonly<Record<FixtureName, ActionLabels>> = {
  "full-catalogue": {
    "view-inspection-queue": "Open inspection queue",
    "view-defect-reports": "Open defect reports",
    "view-ingest-activity": "Open ingest activity",
    "open-documentation": "Open documentation",
    "contact-support": "Contact support"
  },
  "task4-demo": {
    "view-defect-reports": "Open defect reports"
  },
  "fallback": {}
};

/** Validated specifications, keyed by fixture name. */
export const FIXTURES: Readonly<Record<FixtureName, UISpec>> = {
  "full-catalogue": {
    "specVersion": "1.0",
    "page": "landing",
    "contextId": "task4-catalogue",
    "blocks": [
      {
        "component": "Hero",
        "props": {
          "eyebrow": "Internal tooling",
          "title": "Board inspection activity",
          "subtitle": "Recorded inspection records, defect reporting and ingest activity.",
          "primaryAction": "view-inspection-queue"
        }
      },
      {
        "component": "Heading",
        "props": {
          "level": 2,
          "text": "Recorded activity"
        }
      },
      {
        "component": "Text",
        "props": {
          "text": "Explore recorded inspection activity for the current shift.",
          "tone": "muted"
        }
      },
      {
        "component": "FeatureGrid",
        "props": {
          "columns": 2,
          "items": [
            {
              "title": "Inspection records",
              "body": "Recorded inspection entries for this line.",
              "icon": "inspection"
            },
            {
              "title": "Defect reporting",
              "body": "Recorded defect observations by category.",
              "icon": "defect"
            }
          ]
        }
      },
      {
        "component": "FeatureCard",
        "props": {
          "title": "Inspection history",
          "body": "Recorded inspection activity retained for later review.",
          "icon": "report",
          "capabilityId": "inspection-history"
        }
      },
      {
        "component": "CTA",
        "props": {
          "label": "Open defect reports",
          "action": "view-defect-reports",
          "variant": "primary"
        }
      },
      {
        "component": "CTA",
        "props": {
          "label": "Open ingest activity",
          "action": "view-ingest-activity",
          "variant": "secondary"
        }
      },
      {
        "component": "CTA",
        "props": {
          "label": "Open documentation",
          "action": "open-documentation"
        }
      },
      {
        "component": "CTA",
        "props": {
          "label": "Contact support",
          "action": "contact-support"
        }
      },
      {
        "component": "Alert",
        "props": {
          "severity": "warning",
          "title": "Recorded observations",
          "body": "Observations recorded during the current shift.",
          "defectCategoryId": "solder-bridge",
          "alertId": "alert-solder-001"
        }
      },
      {
        "component": "InfoPanel",
        "props": {
          "title": "Shift summary",
          "rows": [
            {
              "metricId": "boards-inspected-shift",
              "label": "Boards inspected",
              "value": "1,284"
            },
            {
              "metricId": "defect-rate-shift",
              "label": "Defect rate",
              "value": "2.4",
              "unit": "%"
            }
          ]
        }
      },
      {
        "component": "ProgressIndicator",
        "props": {
          "metricId": "shift-progress",
          "label": "Shift progress",
          "value": 62,
          "caption": "Recorded progress for the current shift."
        }
      }
    ]
  },
  "task4-demo": {
    "specVersion": "1.0",
    "page": "landing",
    "contextId": "task4-demo",
    "blocks": [
      {
        "component": "Hero",
        "props": {
          "title": "Board inspection activity",
          "subtitle": "Inspection records and defect reporting."
        }
      },
      {
        "component": "Text",
        "props": {
          "text": "Explore recorded inspection activity."
        }
      },
      {
        "component": "CTA",
        "props": {
          "label": "Open defect reports",
          "action": "view-defect-reports"
        }
      }
    ]
  },
  "fallback": {
    "specVersion": "1.0",
    "page": "landing",
    "contextId": "fallback",
    "blocks": [
      {
        "component": "Hero",
        "props": {
          "eyebrow": "Internal tooling",
          "title": "Board inspection activity",
          "subtitle": "A limited view is shown because the full presentation could not be prepared."
        }
      },
      {
        "component": "Alert",
        "props": {
          "severity": "warning",
          "title": "Limited view",
          "body": "Recorded inspection details are not shown here. Nothing on this page is a board quality result."
        }
      },
      {
        "component": "Heading",
        "props": {
          "level": 2,
          "text": "What this means"
        }
      },
      {
        "component": "Text",
        "props": {
          "text": "The usual content is unavailable, so this reduced page is shown instead. No inspection record has been changed.",
          "tone": "muted"
        }
      }
    ]
  }
} as unknown as Readonly<
  Record<FixtureName, UISpec>
>;
