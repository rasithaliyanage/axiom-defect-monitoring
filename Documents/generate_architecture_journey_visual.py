"""Create a vector infographic companion to the source Markdown and DOCX.

Run with Python, then use Chromium's headless print for the HTML PDF.
No third-party Python dependencies. Source documents are preserved.
"""
from pathlib import Path
from html import escape
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'architecture_journey_infographic'
NAVY, INK, MUTED = '#102B46', '#203C53', '#526B7D'
TEAL, BLUE, AMBER = '#087F83', '#315DC5', '#A96B0B'
parts = []

def rect(x,y,w,h,fill,stroke='none',radius=14):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

def text(x,y,s,size=20,color=INK,bold=False):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}">{escape(s)}</text>')

def para(x,y,s,width=65,size=20,color=INK,leading=None):
    lines=textwrap.wrap(s,width=width,break_long_words=False,break_on_hyphens=False)
    for i,line in enumerate(lines): text(x,y+i*(leading or size*1.42),line,size,color)
    return y+len(lines)*(leading or size*1.42)

def line(x1,y1,x2,y2,color=TEAL,dash=False):
    parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="3" {"stroke-dasharray=\"8 7\"" if dash else ""} marker-end="url(#arrow)"/>')

def card(x,y,w,h,kicker,title,body,color=TEAL):
    rect(x,y,w,h,'#FFFFFF','#D6E1E8')
    rect(x,y,5,h,color,radius=2)
    text(x+22,y+31,kicker,15,color,True)
    text(x+22,y+65,title,24,INK,True)
    size, leading, offset = (17,21,91) if h < 150 or w < 380 else (19,26,99)
    width=max(20,int((w-44)/(size*0.51)))
    lines=textwrap.wrap(body,width=width,break_long_words=False,break_on_hyphens=False)
    assert offset+(len(lines)-1)*leading <= h-8, (title, 'body overflow')
    para(x+22,y+offset,body,width,size,leading=leading)

def start(n,kicker,title,sub):
    parts.clear()
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img">')
    parts.append(f'<title>{escape(title)}</title><desc>{escape(sub)}</desc>')
    parts.append('<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="#087F83"/></marker></defs><g font-family="Segoe UI, Arial, sans-serif">')
    rect(0,0,1600,1000,'#F1F5F8',radius=0)
    rect(0,0,1600,192,NAVY,radius=0)
    rect(48,37,7,26,'#38D0BD',radius=2)
    text(70,58,'AXION  /  BOARD DEFECT INSPECTION',19,'#80E0D3',True)
    text(1450,57,f'0{n} / 04',19,'#BCCDDD',True)
    text(48,113,title,41,'#FFFFFF',True)
    text(48,153,sub,20,'#CDDAE5')
    text(48,225,kicker,16,TEAL,True)
    parts.append('<path d="M48 945 H1552" stroke="#CAD7E0"/>')
    text(48,972,'PHASE 0  •  TASKS 1–6A  |  Educational architecture summary; not a specification or quality outcome.',15,MUTED)
    text(1120,972,'Source snapshot: 06 Oct 2026  •  165511d',15,MUTED)

def save(name):
    parts.append('</g></svg>')
    s=''.join(parts); ET.fromstring(s)
    (OUT/f'{name}.svg').write_text(s,encoding='utf-8')
    return s

def main():
    OUT.mkdir(exist_ok=True)
    source=(ROOT/'BOARD_DEFECT_INSPECTION_ARCHITECTURE_JOURNEY_INFOGRAPHIC_TASKS_1_6A.md').read_text(encoding='utf-8-sig')
    for fact in ['217 passed','88 passed','E_CONTEXT_MISMATCH','ProgressIndicator','POST /api/v1/ui/landing-page']:
        assert fact in source, f'Source changed; review infographic: {fact}'
    pages=[]
    start(1,'01  /  ARCHITECTURE JOURNEY','Build the safety boundary before the AI','From written requirements to a validated, API-backed presentation pipeline.')
    for x,num,label in [(48,'7','task milestones'),(430,'4','validation gates'),(812,'9','approved components'),(1194,'0','model calls in this scope')]:
        rect(x,247,358,90,'#E3ECF3'); text(x+20,308,num,48,TEAL,True); text(x+93,299,label,20,INK,True)
    for x,c,title,caption in [(48,BLUE,'I  /  FOUNDATION & BOUNDARY','Define what is allowed'),(556,TEAL,'II  /  UI EXECUTION','Render only approved input'),(1064,AMBER,'III  /  RUNTIME & SEAM','Serve only validated output')]:
        rect(x,361,488,62,c);text(x+18,388,title,19,'#FFFFFF',True);text(x+18,410,caption,16,'#FFFFFF')
    card(48,442,488,134,'T1  /  REQUIREMENTS','Domain & specifications','BR / FR / VR traceability; runtime boundaries; seven non-negotiable rules.',BLUE)
    card(48,590,488,134,'T2  /  CONTRACT','UISpec v1 + JSON Schema','specVersion 1.0; closed vocabulary, props, actions and presentation policy.',BLUE)
    card(48,738,488,134,'T3  /  VALIDATOR','Deterministic acceptance','Four ordered gates report all rejections with stable code, field path and gate.',BLUE)
    card(556,442,488,208,'T4  /  CONTROLLED RENDERER','A closed component registry','Nine components; exhaustive TypeScript map; own-property lookup. ApprovedUISpec records provenance from the offline Python validation gate.')
    card(556,668,488,204,'T5  /  RUNNABLE UI','Prove the browser path','Vite + React + strict TypeScript. Static approved fixtures render through the registry before a network boundary is introduced.')
    card(1064,442,488,208,'T6  /  DOMAIN RUNTIME','Move trust to the server','FastAPI validates each fixture against complete server-owned GroundedContext on every request. The client accepts a checked response envelope.',AMBER)
    card(1064,668,488,204,'T6A  /  CONTEXT SEAM','Type the presentation request','Required page, view and locale become an immutable ContextPayload. The service checks page / locale against its owned context.',AMBER)
    text(48,916,'DESIGN LESSON',16,TEAL,True);text(225,916,'Contract → validator → renderer → browser → API → typed context seam.',23,INK,True)
    pages.append(save('01_architecture_journey'))

    start(2,'02  /  AS-BUILT REQUEST & RESPONSE','One request. One deterministic trust boundary.','The caller selects a presentation. The Domain Runtime supplies the grounded context.')
    card(48,250,370,182,'UI RUNTIME  /  :5173','React browser','Fixed API path and method. Same-origin Vite development proxy for /api and /health.',BLUE)
    rect(456,250,1096,447,'#E4EFEE','#B4D5D1')
    text(480,281,'DOMAIN RUNTIME  /  FastAPI · 127.0.0.1:8000',19,TEAL,True)
    card(480,306,324,171,'1  /  TRANSPORT','Validate the body','LandingPageRequest: all fields required; extra="forbid". Bad inputs → HTTP 400.')
    card(835,306,324,171,'2  /  DOMAIN VALUE','ContextPayload','Frozen, slotted enum value. Presentation request only; no metrics or contextId.')
    card(1190,306,338,171,'3  /  ORCHESTRATION','LandingService','Check page / locale against server context. Never rewrite a fixture to fit the caller.')
    line(418,347,476,347);line(805,389,831,389);line(1160,389,1186,389)
    card(480,503,510,162,'4  /  SERVER-OWNED INPUT','Fixture + GroundedContext','Approved presentation fixture and complete grounded context; supplied by the server.')
    card(1020,503,508,162,'5  /  ACCEPTANCE GATE','Deterministic Python validator','Structure → vocabulary → grounding → text policy. The same input yields the same result.',AMBER)
    parts.append('<path d="M1360 477 V491 H735 V499" fill="none" stroke="#087F83" stroke-width="3" marker-end="url(#arrow)"/>')
    line(994,586,1016,586)
    rect(48,456,370,241,NAVY)
    text(68,488,'POST /api/v1/ui/landing-page',19,'#80E0D3',True)
    for i,s in enumerate(['{','  "page": "landing",','  "view": "overview",','  "locale": "en-US"','}']):text(68,525+i*29,s,21,'#FFFFFF')
    card(48,731,460,164,'6  /  HTTP 200','Accepted response','{spec, bindings, meta}; meta carries contextId, source: "fixture", validation: "VALID".')
    card(545,731,460,164,'7  /  CLIENT ACCEPTANCE','unknown → checked envelope','acceptLandingResponse() narrows the response before registry-only rendering.',BLUE)
    card(1042,731,510,164,'REJECTION  /  FAIL CLOSED','Sanitized error state','Invalid fixture → 500 VALIDATION_FAILED. Codes stay in logs; the invalid spec is never returned.',AMBER)
    line(509,812,541,812)
    line(1270,668,1270,727)
    parts.append('<path d="M1100 668 V710 H275 V727" fill="none" stroke="#087F83" stroke-width="3" marker-end="url(#arrow)"/>')
    text(48,927,'GET /health → {"status":"ok"} indicates process liveness only. It does not establish inspection readiness.',19,MUTED)
    pages.append(save('02_runtime_and_trust_boundary'))

    start(3,'03  /  DEFENCE IN DEPTH','Schema-valid is only the first gate','Four ordered validator gates • 13 stable rejection codes • all rejections reported.')
    gates=[('01','STRUCTURE','Well formed and bounded','E_SCHEMA  ·  E_SIZE_LIMIT  ·  E_DEPTH_LIMIT','Reject malformed structure and size / depth abuse.'),('02','VOCABULARY','Only approved building blocks','E_UNKNOWN_COMPONENT  ·  E_PROP_INVALID','Reject unknown components and invalid component props.'),('03','GROUNDING','Every claim traces to context','E_UNGROUNDED_METRIC  ·  E_UNKNOWN_DEFECT_CATEGORY\nE_UNKNOWN_ACTION  ·  E_UNGROUNDED_CAPABILITY\nE_CONTEXT_MISMATCH','Reject invented metrics, categories, actions or capabilities.'),('04','TEXT POLICY','Presentation never becomes code or verdict','E_TEXT_POLICY  ·  E_CODE_LIKE_CONTENT\nE_DECISION_LANGUAGE','Reject disallowed markup, URLs, code-like text and decision language.')]
    y=250
    for num,k,title,codes,body in gates:
        h=177 if num=='03' else 151
        rect(48,y,958,h,'#FFFFFF','#D6E1E8');rect(65,y+18,61,51,'#FFF0CF');text(77,y+53,num,28,AMBER,True)
        text(146,y+32,k,15,AMBER,True);text(146,y+62,title,24,INK,True)
        text(146,y+90,body,18,MUTED)
        for j,c in enumerate(codes.split('\n')):text(146,y+119+j*23,c,17,INK,True)
        y+=h+14
    rect(1032,250,520,353,NAVY)
    text(1056,284,'THE ONLY RENDER PATH',16,'#80E0D3',True)
    text(1056,323,'Closed registry · 9 components',27,'#FFFFFF',True)
    for j,(a,b) in enumerate([('Hero','Heading'),('Text','FeatureCard'),('FeatureGrid','CTA'),('Alert','InfoPanel'),('ProgressIndicator','')]):
        text(1056,366+j*39,a,22,'#FFFFFF');text(1310,366+j*39,b,22,'#FFFFFF')
    card(1032,621,520,155,'COMPILE + BUILD CONTROLS','Provenance, then enforcement','ApprovedUISpec brand; exhaustive registry map; own-property lookup; safety lint.',BLUE)
    card(1032,794,520,130,'MEANING OF VALID','Presentation validity only','VALID never means that a board passed inspection.',AMBER)
    pages.append(save('03_validation_and_rendering'))

    start(4,'04  /  CONTRACT, GOVERNANCE & NEXT SEAM','Keep the implemented contract explicit','Future extension belongs behind the service and ahead of the validator.')
    rect(48,250,720,268,'#FFFFFF','#D6E1E8')
    text(70,283,'AS BUILT  /  REQUIRED REQUEST FIELDS',17,TEAL,True)
    for yy,a,b in [(331,'page','landing'),(377,'view','overview | minimal'),(423,'locale','en-US')]:
        rect(70,yy-26,676,38,'#EDF3F7',radius=5);text(86,yy,a,21,INK,True);text(266,yy,b,21)
    para(70,465,'No defaults. Additional fields → HTTP 400. Query parameters do not select the presentation.',61,19)
    card(792,250,760,268,'FUTURE  /  NOT IMPLEMENTED IN TASKS 1–6A','A model gateway plugs into the seam','Service → future model-generated UISpec → unchanged validator → controlled renderer. One bounded repair and deterministic fallback are specified, but not wired. No model calls, database, authentication subsystem, camera / PLC / MES integrations or production deployment.',AMBER)
    rect(48,542,720,244,NAVY)
    text(70,578,'SEVEN ARCHITECTURAL RULES',17,'#80E0D3',True)
    rules=['UI specification only; never executable content.','Registry is the only render path.','Validate; bounded repair / fallback are future wiring.','Model reads no data directly.','Model makes no quality decisions.','Model invents nothing; claims must be grounded.','No authentication subsystem in this phase.']
    for i,s in enumerate(rules):text(70,611+i*24,f'{i+1:02}  {s}',18,'#FFFFFF')
    card(792,542,760,144,'BUSINESS DECISIONS  /  CANDIDATES ONLY','Line, board type and inspection mode','Value sets remain undecided. Manufacturing owns line IDs; Manufacturing / Quality own board taxonomy; Quality owns modes.',AMBER)
    card(792,701,760,145,'CONTRACT CHANGE  /  GOVERNED TOGETHER','No generated_for response field','Request echoing is not adopted. New dimensions require coordinated contract, schema, deterministic test and eval changes.',BLUE)
    rect(48,807,720,117,'#DDEDE8')
    text(70,840,'REPORTED VERIFICATION  /  06 OCT 2026',16,TEAL,True)
    text(70,875,'217 pytest passed  ·  88 UI tests passed',27,INK,True)
    text(70,906,'Typecheck, safety lint and build clean; source report, not a fresh run.',17,MUTED)
    text(792,878,'SOURCE AUTHORITY',15,TEAL,True)
    para(792,904,'CLAUDE.md → specs/spec.md → model-contracts.md → ui-spec.schema.json. Repository wins if this summary differs.',75,16,leading=21)
    pages.append(save('04_contract_and_governance'))
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Board defect inspection — Architecture journey</title><style>
    *{box-sizing:border-box}body{margin:0;background:#d8e1e9}main{max-width:1600px;margin:auto}.page{margin:24px 0;box-shadow:0 8px 35px #102b4626}.page svg{display:block;width:100%;height:auto}nav{font:16px Arial;padding:20px;background:#102b46;color:white;text-align:center}nav a{color:#80e0d3;margin:0 16px} @page{size:16in 10in;margin:0}@media print{nav{display:none}body{background:white}main{max-width:none}.page{margin:0;box-shadow:none;break-after:page;width:16in;height:10in}.page:last-child{break-after:auto}}
    </style><nav>ARCHITECTURE JOURNEY · TASKS 1–6A <a href="#p1">Journey</a><a href="#p2">Runtime</a><a href="#p3">Validation</a><a href="#p4">Contract</a></nav><main>'''
    html+=''.join(f'<section class="page" id="p{i}">{s}</section>' for i,s in enumerate(pages,1))+'</main></html>'
    (OUT/'architecture_journey.html').write_text(html,encoding='utf-8')
    print(f'Created {len(pages)} vector pages and print-ready HTML in {OUT}')

if __name__=='__main__':main()
