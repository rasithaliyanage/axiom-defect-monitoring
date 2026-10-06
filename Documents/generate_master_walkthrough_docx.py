"""Build the documentation-only master walkthrough using standard-library OOXML.

No application dependencies, source-document edits or application commands.
Run: python Documents/generate_master_walkthrough_docx.py
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
STEM = ROOT / 'BOARD_DEFECT_INSPECTION_AI_MASTER_WALKTHROUGH_TASK_6_CHECKPOINT'
SOURCE = ROOT / 'Customer_Onboarding_AI_Walkthrough_Task_6_Checkpoint_Updated.docx.pdf'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w', W)


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
    try:
        original_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    except PermissionError:
        original_hash = None
        print('Reference PDF unreadable; source integrity check unavailable.')
    content = STEM.with_suffix('.md').read_text(encoding='utf-8-sig')
    assert [int(x) for x in re.findall(r'^## (\d+)\.', content, re.M)] == list(range(1, 49))
    prompt_blocks = re.findall(r'^```prompt\n(.*?)^```', content, re.M | re.S)
    provenance = json.loads(STEM.with_suffix('.provenance.json').read_text(encoding='utf-8'))
    expected = [block['sha256'] for record in provenance['prompt_records'] for block in record['blocks']]
    assert [hashlib.sha256(block.encode()).hexdigest() for block in prompt_blocks] == expected
    for record in provenance['prompt_records']:
        assert hashlib.sha256((ROOT / record['source']).read_bytes()).hexdigest() == record['source_sha256']
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
        elif line.startswith('## '):
            heading = paragraph(body, line[3:], 'Heading1')
            if re.match(r'## (1|9|12|17|31|38|39|42)\.', line):
                el('pageBreakBefore', heading.find(f'{{{W}}}pPr'))
        elif line.startswith('# '):
            paragraph(body, line[2:], 'Title')
        elif line.startswith('@ '):
            paragraph(body, line[2:], 'Subtitle')
        elif line.startswith('- '):
            paragraph(body, '\u2022 ' + line[2:])
        elif line.strip():
            paragraph(body, line)
    assert not code
    section = el('sectPr', body)
    el('pgSz', section, w=12240, h=15840)
    el('pgMar', section, top=1008, right=1152, bottom=1008, left=1152,
       header=720, footer=720, gutter=0)

    styles = el('styles')
    for ident, size, color in [('Normal', 21, '243746'), ('Title', 40, '123047'),
                                ('Subtitle', 24, '486578'), ('Heading1', 28, '123047')]:
        style = el('style', styles, type='paragraph', styleId=ident)
        el('name', style, val=ident)
        if ident == 'Normal':
            style.set(f'{{{W}}}default', '1')
        else:
            el('basedOn', style, val='Normal')
        pp = el('pPr', style)
        el('spacing', pp, after=100, before=160 if ident == 'Heading1' else 0)
        if ident != 'Normal':
            el('keepNext', pp)
        if ident == 'Heading1':
            el('outlineLvl', pp, val=0)
        rp = el('rPr', style)
        el('rFonts', rp, ascii='Arial', hAnsi='Arial')
        el('sz', rp, val=size)
        el('color', rp, val=color)
        if ident in ('Title', 'Heading1'):
            el('b', rp)

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
<dc:title>Board Defect Inspection AI - Master Beginner Teaching Walkthrough</dc:title>
<dc:creator>Board Defect Inspection Project</dc:creator>
<dc:description>Chronological Tasks 1-6 teaching companion. Historical prompt archive and implementation evidence. Git checkpoint pending; documentation only.</dc:description>
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
    for block in prompt_blocks:
        for line in block.splitlines():
            if line.strip():
                assert line in text, line
    assert len(prompt_blocks) == 16
    assert 'Task 6 is implemented locally' in text
    assert 'formal Git checkpoint is pending' in text
    if original_hash is not None:
        assert original_hash == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    print('Created editable DOCX and checked ZIP/XML integrity.')
    print('Verified all 48 sections and 16 verbatim source prompt blocks; provenance hashes match.')
    if original_hash is not None:
        print('Source PDF unchanged; SHA-256: ' + original_hash)


if __name__ == '__main__':
    main()
