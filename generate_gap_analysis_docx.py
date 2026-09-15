"""Generate an editable Word report using only Python's standard library."""
from pathlib import Path
import re
import zipfile
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'AI_NATIVE_GAP_ANALYSIS.md'
OUTPUT = ROOT / 'AI_NATIVE_GAP_ANALYSIS.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
relationships = []


def runs(text):
    result = []
    cursor = 0
    for match in re.finditer(r'\[([^\]]+)\]\((?:<([^>]+)>|([^\)]+))\)', text):
        result.append(run(text[cursor:match.start()]))
        target = match.group(2) or match.group(3)
        rid = f'rId{len(relationships) + 10}'
        relationships.append((rid, target))
        result.append(f'<w:hyperlink r:id="{rid}">{run(match.group(1), True)}</w:hyperlink>')
        cursor = match.end()
    result.append(run(text[cursor:]))
    return ''.join(result)


def run(text, link=False):
    props = '<w:rPr><w:color w:val="12618A"/><w:u w:val="single"/></w:rPr>' if link else ''
    return f'<w:r>{props}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>' if text else ''


def paragraph(text, style='Normal'):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs(text)}</w:p>'


def table(rows):
    columns = len(rows[0])
    width = 10460 // columns
    borders = ''.join(f'<w:{side} w:val="single" w:sz="4" w:color="CCD7E0"/>' for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'])
    result = [f'<w:tbl><w:tblPr><w:tblW w:w="10460" w:type="dxa"/><w:tblBorders>{borders}</w:tblBorders><w:tblCellMar><w:top w:w="90" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="90" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>']
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
while i < len(lines):
    line = lines[i]
    if line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = [cell.strip() for cell in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', cell.replace(' ', '')) for cell in cells):
                rows.append(cells)
            i += 1
        assert all(len(row) == len(rows[0]) for row in rows)
        body.append(table(rows))
        continue
    if line.startswith('# '):
        body.append(paragraph(line[2:], 'Title'))
    elif line.startswith('### '):
        body.append(paragraph(line[4:], 'Heading2'))
    elif line.startswith('## '):
        body.append(paragraph(line[3:], 'Subtitle' if i < 4 else 'Heading1'))
    elif line.startswith('- '):
        body.append(paragraph('• ' + line[2:], 'ListParagraph'))
    elif line:
        body.append(paragraph(line))
    i += 1

section = '<w:sectPr><w:headerReference w:type="default" r:id="rId2"/><w:footerReference w:type="default" r:id="rId3"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="900" w:right="890" w:bottom="900" w:left="890" w:header="360" w:footer="360"/></w:sectPr>'
document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>{"".join(body)}{section}</w:body></w:document>'
styles = f'''<w:styles xmlns:w="{W}">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/><w:color w:val="243746"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="260" w:lineRule="auto"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="200"/></w:pPr><w:rPr><w:b/><w:sz w:val="44"/><w:color w:val="173B57"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:pPr><w:keepNext/></w:pPr><w:rPr><w:sz w:val="28"/><w:color w:val="12618A"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:keepNext/><w:spacing w:before="260" w:after="130"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/><w:color w:val="173B57"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:keepNext/><w:spacing w:before="180" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="25"/><w:color w:val="12618A"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:pPr><w:spacing w:after="35" w:line="225" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableHead"><w:name w:val="Table Header"/><w:basedOn w:val="TableText"/><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:pPr><w:ind w:left="220" w:hanging="180"/></w:pPr></w:style>
</w:styles>'''
rel_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
rels = f'<Relationships xmlns="{rel_ns}"><Relationship Id="rId1" Type="{R}/styles" Target="styles.xml"/><Relationship Id="rId2" Type="{R}/header" Target="header1.xml"/><Relationship Id="rId3" Type="{R}/footer" Target="footer1.xml"/>'
for rid, target in relationships:
    rels += f'<Relationship Id="{rid}" Type="{R}/hyperlink" Target="{escape(target, {chr(34): "&quot;"})}" TargetMode="External"/>'
rels += '</Relationships>'
types = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
for name, typ in [('document','document.main'),('styles','styles'),('header1','header'),('footer1','footer')]:
    types += f'<Override PartName="/word/{name}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.{typ}+xml"/>'
types += '</Types>'
parts = {
    '[Content_Types].xml': types,
    '_rels/.rels': f'<Relationships xmlns="{rel_ns}"><Relationship Id="rId1" Type="{R}/officeDocument" Target="word/document.xml"/></Relationships>',
    'word/document.xml': document,
    'word/styles.xml': styles,
    'word/_rels/document.xml.rels': rels,
    'word/header1.xml': f'<w:hdr xmlns:w="{W}">{paragraph("BOARD DEFECT INSPECTION | Engineering gap analysis", "TableText")}</w:hdr>',
    'word/footer1.xml': f'<w:ftr xmlns:w="{W}"><w:p><w:pPr><w:jc w:val="right"/></w:pPr>{run("Version 1.0 | 9 September 2026 | Page ")}<w:fldSimple w:instr="PAGE"/></w:p></w:ftr>',
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
    for marker in ['G01', 'G20', 'AC-008', '17. Decision checklist', 'Appendix A']:
        assert marker in text, marker
print(f'Created {OUTPUT.name}: {OUTPUT.stat().st_size:,} bytes')
print(f'Source: {len(SOURCE.read_text(encoding="utf-8").split()):,} words; {len(root.findall(".//{" + W + "}tbl"))} tables')
print('Validated XML, package integrity and key section coverage.')
