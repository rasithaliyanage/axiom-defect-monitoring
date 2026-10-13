"""Package the four infographic pages in Word with SVG and PNG fallbacks."""
from pathlib import Path
from html import escape
import zipfile
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parent
pages=sorted(root.glob('0*.svg'))
assert len(pages)==4
ns='http://schemas.openxmlformats.org/'
rels=[]
body=[]
for i,p in enumerate(pages,1):
    assert p.with_suffix('.png').exists(), 'Run export.ps1 first'
    for ext,ident in [('png',i),('svg',i+4)]:
        rels.append(f'<Relationship Id="rId{ident}" Type="{ns}officeDocument/2006/relationships/image" Target="media/{p.stem}.{ext}"/>')
    body.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:jc w:val="center"/>{'<w:pageBreakBefore/>' if i>1 else ''}</w:pPr><w:r><w:drawing>
    <wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="13716000" cy="8572500"/><wp:docPr id="{i}" name="Architecture page {i}" descr="{escape(p.stem)}"/>
    <a:graphic><a:graphicData uri="{ns}drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="{p.name}"/><pic:cNvPicPr/></pic:nvPicPr>
    <pic:blipFill><a:blip r:embed="rId{i}"><a:extLst><a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}"><asvg:svgBlip r:embed="rId{i+4}"/></a:ext></a:extLst></a:blip><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
    <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="13716000" cy="8572500"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
    </pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>''')
body.append('<w:sectPr><w:pgSz w:w="23040" w:h="14400" w:orient="landscape"/><w:pgMar w:top="360" w:right="720" w:bottom="360" w:left="720" w:header="0" w:footer="0"/></w:sectPr>')
doc=f'''<w:document xmlns:w="{ns}wordprocessingml/2006/main" xmlns:r="{ns}officeDocument/2006/relationships" xmlns:wp="{ns}drawingml/2006/wordprocessingDrawing" xmlns:a="{ns}drawingml/2006/main" xmlns:pic="{ns}drawingml/2006/picture" xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main"><w:body>{''.join(body)}</w:body></w:document>'''
files={
    '[Content_Types].xml':f'<Types xmlns="{ns}package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Default Extension="svg" ContentType="image/svg+xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>',
    '_rels/.rels':f'<Relationships xmlns="{ns}package/2006/relationships"><Relationship Id="rId1" Type="{ns}officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>',
    'word/_rels/document.xml.rels':f'<Relationships xmlns="{ns}package/2006/relationships">{"".join(rels)}</Relationships>',
    'word/document.xml':doc,
}
for p in pages:
    for ext in ['svg','png']:files[f'word/media/{p.stem}.{ext}']=p.with_suffix('.'+ext).read_bytes()
output=root/'architecture_journey.docx'
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
    for name,data in files.items():z.writestr(name,data)
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None
    for name in z.namelist():
        if name.endswith(('.xml','.rels','.svg')):ET.fromstring(z.read(name))
print('Created and validated Word package: 4 vector infographic pages with PNG fallbacks.')
