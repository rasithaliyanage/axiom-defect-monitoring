# Infographic generation prompts

Tool: built-in image_gen.
Source: Claude_Code_Rules_Enterprise_Infographic.mmd.
Final asset: Claude_Code_Rules_Enterprise_Infographic.png.

## Initial prompt

Use case: infographic-diagram.
Create one polished, high-resolution enterprise educational infographic from the following Mermaid diagram's content. This is a finished image for project documentation. Portrait poster with generous whitespace, crisp very readable typography, thin directional connectors and numbered section bands. Flat vector-like visual style, not photography. Navy title, blue guidance cards, amber task cards, teal rendering controls, red failure branches, violet verification. Use four stacked sections with section 3 largest. Preserve flow meaning, do not print Mermaid syntax. No decorative robots, logos or unnecessary illustrations.

Title: "CLAUDE CODE RULES"
Subtitle: "Enterprise standards applied to board inspection UI development"

Section 1: "01  ORGANIZE ENGINEERING GUIDANCE"
Flow: "Enterprise standards" (Architecture • Security • Quality) -> "CLAUDE.md" (Project purpose and boundaries) -> ".claude/rules/" (Focused, verifiable instructions).
Branch from .claude/rules/ into "Rules without paths" (General project guidance) and "Rules with paths" (Guidance when matching files are read).
Small annotation: "Conceptual organization, not instruction precedence."

Section 2: "02  APPLY TO A PROJECT TASK"
"Developer request" (Improve CTA spacing and test its action callback) -> "Claude Code" (Inspect existing code; make the scoped change).
A guidance card with a dotted arrow into Claude Code: "Proposed rule — not installed", filename ".claude/rules/frontend/controlled-uispec.md", small path labels "apps/ui/**/*" and "tests/renderer_fixtures/**/*.py".
A compact boundary strip: "No raw-model rendering • No executable content • No invented routes, live data or quality decisions".
Dotted arrows represent guidance, not data transport.

Section 3: "03  PRESERVE THE RENDERING BOUNDARY"
Main downward connected flow:
"Fixed synthetic UISpec + complete GroundedContext"
-> "Task 3 Python validator" (Selected schema • Grounding • Deterministic policy checks)
-> diamond "Validation passed?"
No branch right to red box "Stop fixture preparation" (Remove stale generated fixture and evidence).
Yes branch downward to "Static fixture module + verification evidence" (Privately issued ApprovedUISpec handle).
-> "Task 4 ControlledRenderer" (Issued-handle lookup • Whole-page preflight)
-> diamond "Registry entries and action bindings supported?"
No branch right to red box "Reject the whole rendering" (No omission, substitution or repair).
Yes branch downward to "Explicit nine-component registry".
List exactly these nine names in a compact three-row grid inside registry box:
"Hero • Heading • Text"
"FeatureCard • FeatureGrid • CTA"
"Alert • InfoPanel • ProgressIndicator"
-> "Safe React presentation" (Explicit DOM props • Supplied text and values • Five approved action IDs • Inert demo controls).
A small dotted connector from Claude Code above to ControlledRenderer labelled "Maintain this existing flow". It must not suggest Claude generates runtime model output.

Section 4: "04  VERIFY AND REVIEW"
"Required checks" (Renderer tests • TypeScript • Safety lint • Build • Python validator and fixture-handoff tests)
-> "Reviewable change" (Actual results • Changed files • Limitations • Human review).
Safe React presentation connects to checks with label "Rendering and action assertions".

Prominent footer with these three exact statements:
"Rules guide the coding assistant; code and checks enforce the boundary."
"VALID means presentation validation, never board PASS/FAIL or approval."
"No live model or validator-to-browser transport in this fixture demonstration."

Constraints: faithful technical labels, clear Yes/No arrows, no missing failure branches, clean margins, no clipping, no unsupported claims that the proposed rule is installed. Prioritize legibility over excessive decoration.

## Refinement 1

Edit this infographic only to correct these issues, preserving all other content and layout: 1. Title CLAUDE CODE RULES and subtitle must be dark navy on a plain white background, remove the dark shadow/gradient over the top. 2. Change 'Eveloper request' to exactly 'Developer request'. 3. In proposed-rule card print exact path strings 'apps/ui/**/*' and 'tests/renderer_fixtures/**/*.py' with no missing or extra asterisks. 4. The dashed blue 'Maintain this existing flow' connector must originate at the Claude Code box in section 2 and terminate at the Task 4 ControlledRenderer box. It must NOT originate at Fixed synthetic UISpec. Remove the existing solid line descending from Claude Code. Route dashed connector in left gutter without crossing labels. 5. Connect Safe React presentation to Required checks in section 4 with a downward arrow labelled 'Rendering and action assertions'. Remove that label from the arrow between Required checks and Reviewable change, leave that arrow unlabelled. Preserve both Yes/No diamonds and failure branches. No other wording changes.

## Final refinement

Make these specific corrections to the attached infographic. In section 02, replace the entire label 'Eeveloper request' with exactly 'Task request'. In the small blue paths inset replace both wildcard lines with the plain text 'UI and fixture-handoff files'. In section 03 erase the ENTIRE dashed blue line on the LEFT, including its arrowhead and the text 'Maintain this existing flow'; replace that area with the same plain pale teal background. This dashed line incorrectly bypasses validation and MUST be removed. Also erase the vertical line and arrow BELOW the Claude Code card in section 02 all the way to section 03; no connector may cross the boundary strip. Retain the horizontal developer-request arrow into Claude Code and the horizontal dashed proposed-rule arrow into Claude Code. Keep the vertical main validation flow and its yes/no failure branches, all nine component names, title and footer exactly unchanged. These targeted fixes are essential; do not add other elements.

