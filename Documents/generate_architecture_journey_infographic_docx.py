"""Build the Architecture Journey infographic (Tasks 1-6A) DOCX using standard-library OOXML.

The companion .md is the single source; this script regenerates the DOCX from it.
No application dependencies, source-document edits or application commands.
Run: python Documents/generate_architecture_journey_infographic_docx.py
"""
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
STEM = ROOT / 'BOARD_DEFECT_INSPECTION_ARCHITECTURE_JOURNEY_INFOGRAPHIC_TASKS_1_6A'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w', W)

SECTION_COUNT = 8


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
    else:
        # Markdown links and autolinks render as their visible text.
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'<(https?://[^>]+)>', r'\1', text)
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
        # Callouts are blockquotes containing headings, tables and paragraphs;
        # unwrap them so their content renders with the ordinary rules.
        if line.startswith('>') and not code:
            line = line[1:].lstrip(' ')
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
<dc:title>Board Defect Inspection AI - Architectural Journey (Tasks 1-6A)</dc:title>
<dc:creator>Board Defect Inspection Project</dc:creator>
<dc:description>Learning and system architecture infographic for Tasks 1-6A, verified against the repository.</dc:description>
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
    # Key sections and as-built facts must survive the conversion.
    for required in ('Executive Overview', 'Visual Architecture Progression',
                     'Task Milestone Breakdown', 'Deterministic Trust Boundary',
                     'Zero-Trust UI Security', 'Context Seam Design',
                     'Scope & Control Boundaries', 'Contract Quick-Reference Matrix',
                     'Appendix A', '/api/v1/ui/landing-page', 'flowchart LR',
                     'NOT adopted, awaiting business decision'):
        assert required in text, f'missing from generated document: {required}'

    print('Created editable DOCX and checked ZIP/XML integrity.')
    print(f'Verified all {SECTION_COUNT} sections and key infographic content.')
    print('Markdown companion is the single source; no DOCX hand-editing required.')


if __name__ == '__main__':
    main()
