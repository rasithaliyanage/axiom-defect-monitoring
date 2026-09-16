"""Generate an editable Word report using only Python's standard library.

Extends the gap-analysis generator with fenced code-block support, since the
initial discussion document carries prompts, trees and terminal snippets.
"""
from pathlib import Path
import re
import zipfile
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.md'
OUTPUT = ROOT / 'AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
relationships = []


def clean_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def runs(text, mono=False):
    result = []
    cursor = 0
    for match in re.finditer(r'\[([^\]]+)\]\((?:<([^>]+)>|([^\)]+))\)', text):
        result.append(run(text[cursor:match.start()], mono=mono))
        target = match.group(2) or match.group(3)
        rid = f'rId{len(relationships) + 10}'
        relationships.append((rid, target))
        result.append(f'<w:hyperlink r:id="{rid}">{run(match.group(1), link=True)}</w:hyperlink>')
        cursor = match.end()
    result.append(run(text[cursor:], mono=mono))
    return ''.join(result)


def run(text, link=False, mono=False):
    if not text:
        return ''
    text = clean_inline(text) if not mono else text
    props = ''
    if link:
        props = '<w:rPr><w:color w:val="12618A"/><w:u w:val="single"/></w:rPr>'
    elif mono:
        props = '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="17"/></w:rPr>'
    return f'<w:r>{props}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def paragraph(text, style='Normal', mono=False):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs(text, mono=mono)}</w:p>'


def code_block(lines):
    """Render a fenced block as a single shaded, bordered table cell."""
    borders = ''.join(
        f'<w:{side} w:val="single" w:sz="4" w:color="D4DEE6"/>'
        for side in ['top', 'left', 'bottom', 'right']
    )
    body = ''.join(paragraph(line if line.strip() else ' ', 'CodeText', mono=True) for line in lines)
    return (
        f'<w:tbl><w:tblPr><w:tblW w:w="10460" w:type="dxa"/><w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/>'
        '<w:bottom w:w="120" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tblCellMar></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="10460"/></w:tblGrid>'
        '<w:tr><w:tc><w:tcPr><w:tcW w:w="10460" w:type="dxa"/>'
        f'<w:shd w:fill="F5F8FA"/></w:tcPr>{body}</w:tc></w:tr></w:tbl>'
        + paragraph('')
    )


def table(rows):
    columns = len(rows[0])
    width = 10460 // columns
    borders = ''.join(
        f'<w:{side} w:val="single" w:sz="4" w:color="CCD7E0"/>'
        for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']
    )
    result = [
        f'<w:tbl><w:tblPr><w:tblW w:w="10460" w:type="dxa"/><w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblCellMar><w:top w:w="90" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="90" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
    ]
    result.append('<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{width}"/>' for _ in range(columns)) + '</w:tblGrid>')
    for index, row in enumerate(rows):
        result.append('<w:tr><w:trPr>' + ('<w:tblHeader/>' if index == 0 else '') + '</w:trPr>')
        for value in row:
            shade = '173B57' if index == 0 else ('F0F5F8' if index % 2 else 'FFFFFF')
            result.append(f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:shd w:fill="{shade}"/><w:vAlign w:val="top"/></w:tcPr>')
            result.append(paragraph(value, 'TableHead' if index == 0 else 'TableText'))
            result.append('</w:tc>')
        result.append('</w:tr>')
    result.append('</w:tbl>' + paragraph(''))
    return ''.join(result)


lines = SOURCE.read_text(encoding='utf-8').splitlines()
body = []
i = 0
heading_count = 0
code_blocks = 0
while i < len(lines):
    line = lines[i]

    if line.startswith('```'):
        i += 1
        block = []
        while i < len(lines) and not lines[i].startswith('```'):
            block.append(lines[i])
            i += 1
        i += 1
        body.append(code_block(block))
        code_blocks += 1
        continue

    if line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = [cell.strip() for cell in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', cell.replace(' ', '')) for cell in cells):
                rows.append(cells)
            i += 1
        assert all(len(row) == len(rows[0]) for row in rows), 'ragged table'
        body.append(table(rows))
        continue

    if line.startswith('# '):
        body.append(paragraph(line[2:], 'Title'))
    elif line.startswith('### '):
        body.append(paragraph(line[4:], 'Heading2'))
    elif line.startswith('## '):
        heading_count += 1
        body.append(paragraph(line[3:], 'Subtitle' if heading_count == 1 else 'Heading1'))
    elif line.startswith('---'):
        pass
    elif line.startswith('> '):
        body.append(paragraph(line[2:], 'Quote'))
    elif line.startswith('- ') or line.startswith('* '):
        body.append(paragraph('• ' + line[2:], 'ListParagraph'))
    elif re.match(r'^\d+\.\s', line):
        body.append(paragraph(line, 'ListParagraph'))
    elif line.strip():
        body.append(paragraph(line))
    i += 1

section = (
    '<w:sectPr><w:headerReference w:type="default" r:id="rId2"/>'
    '<w:footerReference w:type="default" r:id="rId3"/>'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="900" w:right="890" w:bottom="900" w:left="890" w:header="360" w:footer="360"/></w:sectPr>'
)
document = (
    f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>{"".join(body)}{section}</w:body></w:document>'
)
styles = f'''<w:styles xmlns:w="{W}">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/><w:color w:val="243746"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="260" w:lineRule="auto"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="200"/></w:pPr><w:rPr><w:b/><w:sz w:val="44"/><w:color w:val="173B57"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:pPr><w:keepNext/></w:pPr><w:rPr><w:sz w:val="28"/><w:color w:val="12618A"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:keepNext/><w:spacing w:before="260" w:after="130"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/><w:color w:val="173B57"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:keepNext/><w:spacing w:before="180" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="25"/><w:color w:val="12618A"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:pPr><w:spacing w:after="35" w:line="225" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableHead"><w:name w:val="Table Header"/><w:basedOn w:val="TableText"/><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="CodeText"><w:name w:val="Code Text"/><w:pPr><w:spacing w:after="0" w:line="210" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="17"/><w:color w:val="1D2E3D"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:pPr><w:ind w:left="220" w:hanging="180"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:pPr><w:ind w:left="260"/><w:spacing w:before="100" w:after="100"/></w:pPr><w:rPr><w:i/><w:color w:val="46617A"/></w:rPr></w:style>
</w:styles>'''
rel_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
rels = (
    f'<Relationships xmlns="{rel_ns}">'
    f'<Relationship Id="rId1" Type="{R}/styles" Target="styles.xml"/>'
    f'<Relationship Id="rId2" Type="{R}/header" Target="header1.xml"/>'
    f'<Relationship Id="rId3" Type="{R}/footer" Target="footer1.xml"/>'
)
for rid, target in relationships:
    rels += f'<Relationship Id="{rid}" Type="{R}/hyperlink" Target="{escape(target, {chr(34): "&quot;"})}" TargetMode="External"/>'
rels += '</Relationships>'
types = (
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
)
for name, typ in [('document', 'document.main'), ('styles', 'styles'), ('header1', 'header'), ('footer1', 'footer')]:
    types += f'<Override PartName="/word/{name}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.{typ}+xml"/>'
types += '</Types>'
parts = {
    '[Content_Types].xml': types,
    '_rels/.rels': f'<Relationships xmlns="{rel_ns}"><Relationship Id="rId1" Type="{R}/officeDocument" Target="word/document.xml"/></Relationships>',
    'word/document.xml': document,
    'word/styles.xml': styles,
    'word/_rels/document.xml.rels': rels,
    'word/header1.xml': f'<w:hdr xmlns:w="{W}">{paragraph("BOARD DEFECT INSPECTION | AI-Native Engineering - Initial Discussion", "TableText")}</w:hdr>',
    'word/footer1.xml': f'<w:ftr xmlns:w="{W}"><w:p><w:pPr><w:jc w:val="right"/></w:pPr>{run("Version 1.0 | 15 September 2026 | Page ")}<w:fldSimple w:instr="PAGE"/></w:p></w:ftr>',
}
for name, xml in parts.items():
    ET.fromstring(xml)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name, xml in parts.items():
        archive.writestr(name, xml.encode('utf-8'))
with zipfile.ZipFile(OUTPUT) as archive:
    assert archive.testzip() is None
    root = ET.fromstring(archive.read('word/document.xml'))
    text = '\n'.join(node.text or '' for node in root.iter(f'{{{W}}}t'))
    for marker in ['PROMPT 01', 'PROMPT 10', 'Harness Engineering',
                   'Appendix C', 'Deterministic vs Probabilistic Boundaries',
                   'The Backend — Deterministic Spine and Action Gateway',
                   'Backend action gateway', 'backend-contracts.md',
                   'Three Architectural Views',
                   'The UI Runtime — Deterministic and Generative Interface',
                   'DispositionControl', 'ui-composition',
                   'What UI composition evaluations must check',
                   'Structural rules this layout protects',
                   'What is deliberately not in the tree',
                   'Three API surfaces, not one',
                   'Gates belong to the Domain Runtime',
                   'How to validate this structure',
                   'simulators/', 'policies/']:
        assert marker in text, marker
    numbers = []
    for p in root.iter(f'{{{W}}}p'):
        style = p.find(f'{{{W}}}pPr/{{{W}}}pStyle')
        if style is None or style.get(f'{{{W}}}val') != 'Heading1':
            continue
        heading = ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))
        match = re.match(r'(\d+)\.\s', heading)
        if match:
            numbers.append(int(match.group(1)))
    assert numbers == list(range(1, 30)), f'section numbering broken: {numbers}'
print(f'Created {OUTPUT.name}: {OUTPUT.stat().st_size:,} bytes')
print(f'Source: {len(SOURCE.read_text(encoding="utf-8").split()):,} words')
print(f'{len(root.findall(".//{" + W + "}tbl"))} tables/code blocks ({code_blocks} code blocks)')
print('Validated XML, package integrity and key section coverage.')
