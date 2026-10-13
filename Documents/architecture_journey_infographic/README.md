# Architecture journey infographic — Tasks 1–6A

Four landscape pages: milestone journey, runtime flow, validation and rendering, contract and governance.

- `architecture_journey.pdf`: print-ready vector PDF, 16 × 10 inches.
- `architecture_journey.html`: self-contained browser version with page navigation.
- `architecture_journey.docx`: Word companion containing SVG pages with PNG fallbacks; text is part of the graphics, not editable Word paragraphs.
- `01_*.svg` through `04_*.svg`: scalable, editable vector artwork.
- Matching PNG files: 1600 × 1000 page images for presentations.

Based on the supplied `BOARD_DEFECT_INSPECTION_ARCHITECTURE_JOURNEY_INFOGRAPHIC_TASKS_1_6A.md`, its DOCX companion and its OOXML generator. Original sources remain unchanged. Content reflects their 2026-10-06 snapshot, including the reported test results; it is not a fresh repository audit. The original Markdown remains the full narrative reference. The visual generator contains curated summaries, which must be reviewed when the source changes.

Regenerate from the Documents directory:

```powershell
python generate_architecture_journey_visual.py
powershell -NoProfile -File .\architecture_journey_infographic\export.ps1
python .\architecture_journey_infographic\package_word.py
```

Export requires locally installed Google Chrome. No external web assets or Python packages are required. The seven milestones, four gates and thirteen codes are architectural counts, not measures of inspection accuracy. Future model calls, repair/fallback wiring and business-owned context dimensions are explicitly distinguished from the implemented scope.
