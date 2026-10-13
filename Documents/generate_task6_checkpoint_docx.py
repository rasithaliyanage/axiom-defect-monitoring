"""Build the Task 6 checkpoint guide DOCX using standard-library OOXML.

This document previously existed only as a DOCX, with no Markdown source and no
generator, and drifted out of step with the code while its siblings were kept
current. The text was extracted to the companion .md, which is now the single
source; this script regenerates the DOCX from it.

No application dependencies, source-document edits or application commands.
Run: python Documents/generate_task6_checkpoint_docx.py
"""
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
STEM = ROOT / 'BOARD_DEFECT_INSPECTION_TASK_6_CHECKPOINT_BEGINNER_FRIENDLY_ENTERPRISE_GRADE'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w', W)

SECTION_COUNT = 13


def el(name, parent=None, text=None, **attrs):
    node = ET.Element(f'{{{W}}}{name}', {f'{{{W}}}{k}': str(v) for k, v in attrs.items()})
    if parent is not None:
        parent.append(node)
    if text is not None:
        node.text = text
    return node


def xml(node):
    return ET.tostring(node, encoding='utf-8', xml_declaration=True)


def paragraph(parent, text, style=None, code=False):
    p = el('p', parent)
    props = el('pPr', p)
    if style:
        el('pStyle', props, val=style)
    if code:
        el('spacing', props, after=0, line=220, lineRule='auto')
        el('shd', props, fill='F3F5F7', val='clear')
    for part in ([text] if code else re.split(r'(\*\*.*?\*\*|`[^`]+`)', text)):
        if not part:
            continue
        run = el('r', p)
        rprops = el('rPr', run)
        if not code and part.startswith('**'):
            el('b', rprops)
            part = part[2:-2]
        mono = code or part.startswith('`')
        if not code and part.startswith('`'):
            part = part[1:-1]
        if mono:
            el('rFonts', rprops, ascii='Consolas', hAnsi='Consolas')
            el('sz', rprops, val=17 if code else 19)
        t = el('t', run, text=part or ' ')
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return p


def table(parent, rows):
    tbl = el('tbl', parent)
    props = el('tblPr', tbl)
    el('tblW', props, w=0, type='auto')
    borders = el('tblBorders', props)
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el(side, borders, val='single', sz=4, color='CAD3DC')
    for index, cells in enumerate(rows):
        tr = el('tr', tbl)
        trprops = el('trPr', tr)
        el('cantSplit', trprops)
        if index == 0:
            el('tblHeader', trprops)
        for cell in cells:
            tc = el('tc', tr)
            tcp = el('tcPr', tc)
            el('tcW', tcp, w=9936 // len(cells), type='dxa')
            if index == 0:
                el('shd', tcp, fill='E7EEF5', val='clear')
            paragraph(tc, f'**{cell}**' if index == 0 else cell)


def main():
    content = STEM.with_suffix('.md').read_text(encoding='utf-8-sig')

    numbers = [int(x) for x in re.findall(r'^## (\d+)\.', content, re.M)]
    assert numbers == list(range(1, SECTION_COUNT + 1)), f'section numbering broken: {numbers}'

    document = el('document')
    body = el('body', document)
    code = False
    pending_rows = []
    for line in content.splitlines():
        if line.startswith('|') and not code:
            cells = [c.strip() for c in line.strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                pending_rows.append(cells)
            continue
        if pending_rows:
            table(body, pending_rows)
            pending_rows = []
        if line.startswith('```'):
            code = not code
        elif code:
            paragraph(body, line or ' ', code=True)
        elif line.startswith('#### '):
            paragraph(body, line[5:], 'Heading3')
        elif line.startswith('### '):
            paragraph(body, line[4:], 'Heading2')
        elif line.startswith('## '):
            heading = paragraph(body, line[3:], 'Heading1')
            if line.startswith('## 1.'):
                el('pageBreakBefore', heading.find(f'{{{W}}}pPr'))
        elif line.startswith('# '):
            paragraph(body, line[2:], 'Title')
        elif line.startswith('> '):
            paragraph(body, line[2:], 'Subtitle')
        elif line.startswith('- '):
            paragraph(body, '• ' + line[2:])
        elif line.strip():
            paragraph(body, line)
    if pending_rows:
        table(body, pending_rows)
    assert not code, 'unclosed code fence in the Markdown source'

    section = el('sectPr', body)
    el('pgSz', section, w=12240, h=15840)
    el('pgMar', section, top=1008, right=1152, bottom=1008, left=1152,
       header=720, footer=720, gutter=0)

    styles = el('styles')
    for ident, size, color in [('Normal', 21, '243746'), ('Title', 40, '123047'),
                                ('Subtitle', 20, '486578'), ('Heading1', 28, '123047'),
                                ('Heading2', 24, '123047'), ('Heading3', 22, '486578')]:
        style = el('style', styles, type='paragraph', styleId=ident)
        el('name', style, val=ident)
        if ident == 'Normal':
            style.set(f'{{{W}}}default', '1')
        else:
            el('basedOn', style, val='Normal')
        pp = el('pPr', style)
        el('spacing', pp, after=100, before=160 if ident.startswith('Heading') else 0)
        if ident != 'Normal':
            el('keepNext', pp)
        if ident == 'Heading1':
            el('outlineLvl', pp, val=0)
        if ident == 'Heading2':
            el('outlineLvl', pp, val=1)
        rp = el('rPr', style)
        el('rFonts', rp, ascii='Arial', hAnsi='Arial')
        el('sz', rp, val=size)
        el('color', rp, val=color)
        if ident in ('Title', 'Heading1', 'Heading2'):
            el('b', rp)
        if ident == 'Subtitle':
            el('i', rp)

    package = {
        '[Content_Types].xml': '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>''',
        '_rels/.rels': '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>''',
        'word/_rels/document.xml.rels': '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''',
        'docProps/core.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>Board Defect Inspection AI - Task 6 Checkpoint</dc:title>
<dc:creator>Board Defect Inspection Project</dc:creator>
<dc:description>Task 6 checkpoint report. Local implementation verified; Git checkpoint pending. No commit or push.</dc:description>
</cp:coreProperties>''',
        'word/document.xml': xml(document),
        'word/styles.xml': xml(styles),
    }
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else STEM.with_suffix('.docx')
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, value in package.items():
            archive.writestr(name, value)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            ET.fromstring(archive.read(name))
        doc = ET.fromstring(archive.read('word/document.xml'))
    text = '\n'.join(t.text or '' for t in doc.iter(f'{{{W}}}t'))

    # Corrected facts must be present.
    for required in ('{ "page": "landing", "view": "overview", "locale": "en-US" }',
                     '400 BAD_REQUEST', '282 passed', '93 passed',
                     '/api/v1/inspection/queue', 'Task 7 NOT STARTED',
                     # Parameter policy: the scope of the rule, and the three
                     # properties that make the filters safe to expose.
                     '/api/v1/inspection/board/{boardId}',
                     'ignored, never honoured',
                     'derived from the fixture at load',
                     'BOARD_NOT_FOUND',
                     'This endpoint accepts: limit, line'):
        assert required in text, f'missing from generated document: {required}'

    # Stale facts must be gone from the body. These drifted while the DOCX had
    # no Markdown source. Scanned against the Markdown rather than the rendered
    # runs, because inline bold and code split a line across several runs.
    #
    # The correction note is excluded: it names the old values deliberately, to
    # record what changed and why.
    body_source = '\n'.join(
        line for line in content.splitlines() if not line.startswith('> ')
    )
    for stale in ('8001', '197 passed', '63 passed', 'invalid_request',
                  'apps/ui/fixtures', 'HTTP 422'):
        assert stale not in body_source, f'stale content still present in body: {stale}'

    print('Created editable DOCX and checked ZIP/XML integrity.')
    print(f'Verified all {SECTION_COUNT} sections, corrected payload contract and test counts.')
    print('Markdown companion is the single source; no DOCX hand-editing required.')


if __name__ == '__main__':
    main()
