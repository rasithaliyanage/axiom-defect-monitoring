import React from 'react';

export default function Board({ defects = [], selected, onSelect, overlays = true, zoom = 1, rotation = 0 }) {
  return <svg className="motherboard" viewBox="0 0 680 540" role="img" aria-label="Illustrated motherboard inspection evidence with selectable defect locations" style={{ transform: `scale(${zoom}) rotate(${rotation}deg)` }}>
    <defs>
      <linearGradient id="pcb" x2="1" y2="1"><stop stopColor="#15494a"/><stop offset="1" stopColor="#092d32"/></linearGradient>
      <linearGradient id="metal" x2="1" y2="1"><stop stopColor="#bdc8cb"/><stop offset=".5" stopColor="#758a92"/><stop offset="1" stopColor="#d3dcdb"/></linearGradient>
      <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".65" fill="#4b8380" opacity=".45"/></pattern>
      <filter id="shadow"><feDropShadow dx="0" dy="10" stdDeviation="9" floodOpacity=".3"/></filter>
    </defs>
    <rect x="45" y="28" width="590" height="480" rx="15" fill="url(#pcb)" stroke="#44726d" strokeWidth="3" filter="url(#shadow)"/>
    <rect x="50" y="33" width="580" height="470" rx="12" fill="url(#grid)"/>
    {Array.from({ length: 30 }, (_, i) => <path key={i} d={`M ${85 + i * 15} 480 V ${440 - i % 6 * 8} L ${135 + i * 12} ${390 - i % 4 * 13} V ${95 + i % 5 * 15}`} fill="none" stroke={i % 2 ? '#45716a' : '#376761'} strokeWidth="1.3" opacity=".6"/>)}
    {Array.from({ length: 16 }, (_, i) => <path key={i} d={`M 70 ${90 + i * 22} H ${115 + i % 4 * 30} L ${200 + i % 4 * 30} ${170 + i * 14} H 596`} fill="none" stroke="#567e70" strokeWidth="1" opacity=".4"/>)}
    {[[64,46],[617,46],[64,490],[617,490],[399,470],[399,58]].map(([x,y])=><g key={`${x}${y}`}><circle cx={x} cy={y} r="9" fill="#a8b4a0"/><circle cx={x} cy={y} r="4" fill="#1c292d"/></g>)}
    <g fill="url(#metal)" stroke="#3f5458" strokeWidth="2"><rect x="30" y="77" width="72" height="72" rx="3"/><rect x="30" y="159" width="72" height="80" rx="3"/><rect x="30" y="250" width="72" height="67" rx="3"/></g>
    {[90,118,173,203,265,290].map(y=><rect key={y} x="32" y={y} width="46" height="13" rx="2" fill="#263a42"/>)}
    <rect x="211" y="117" width="178" height="177" rx="9" fill="#849493" stroke="#17272c" strokeWidth="7"/>
    <rect x="227" y="133" width="146" height="145" rx="3" fill="#364f54" stroke="#b0bdb4"/>
    <rect x="243" y="149" width="113" height="111" rx="5" fill="url(#metal)"/>
    <text x="300" y="194" textAnchor="middle" fill="#31434a" fontSize="12" fontFamily="monospace">AXION</text><text x="300" y="216" textAnchor="middle" fill="#43555c" fontSize="9" fontFamily="monospace">CORE PROCESSOR</text>
    <path d="M 399 133 V 277 L 411 290" stroke="#c9d1c4" strokeWidth="5" fill="none"/>
    {[436,462,488,514].map((x,i)=><g key={x}><rect x={x} y="79" width="19" height="173" rx="3" fill={i%2 ? '#819792' : '#202d33'} stroke="#14262a" strokeWidth="3"/><rect x={x+7} y="91" width="3" height="145" fill="#c4ad68"/><rect x={x-2} y="78" width="23" height="12" fill="#a6b6a9"/><rect x={x-2} y="242" width="23" height="12" fill="#a6b6a9"/></g>)}
    {[324,367,440].map((y,i)=><g key={y}><rect x="133" y={y} width={i===2?238:271} height="19" rx="3" fill={i===1?'#7eaaa3':'#202f35'} stroke="#1b272d" strokeWidth="3"/><path d={`M 145 ${y+9} H ${i===2?354:388}`} stroke="#c0a96d" strokeWidth="3"/></g>)}
    <rect x="432" y="285" width="77" height="62" rx="4" fill="#26383d" stroke="#a1b0a5"/>
    {Array.from({length:12},(_,i)=><path key={i} d={`M ${438+i*6} 279 V 285 M ${438+i*6} 347 V 353`} stroke="#c4c9b4" strokeWidth="3"/>)}
    <path d="M 450 280 Q 455 270 460 280" fill="none" stroke="#d5dfd5" strokeWidth="4"/>
    <rect x="447" y="380" width="87" height="65" rx="5" fill="#879d98" stroke="#244746"/>
    {Array.from({length:8},(_,i)=><path key={i} d={`M 452 ${386+i*7} H 529`} stroke="#48635f" strokeWidth="3"/>)}
    <circle cx="570" cy="311" r="28" fill="url(#metal)" stroke="#253a3d" strokeWidth="5"/><text x="570" y="315" textAnchor="middle" fill="#526264" fontSize="10">CR2032</text>
    {[365,401,437].map(y=><g key={y}><rect x="567" y={y} width="42" height="27" rx="2" fill="#729b96"/><rect x="575" y={y+4} width="26" height="18" fill="#1c3338"/></g>)}
    {Array.from({length:9},(_,i)=><g key={i}><circle cx={129+i%3*24} cy={104+Math.floor(i/3)*35} r="8" fill="#bdc8b4" stroke="#263c3e" strokeWidth="3"/><path d={`M ${123+i%3*24} ${104+Math.floor(i/3)*35} h 12`} stroke="#7b9485"/></g>)}
    {[123,153,183,213,243,273,303,333].map(x=><g key={x}><rect x={x} y="65" width="18" height="17" fill="#182e33" stroke="#7d9681"/><rect x={x+4} y="88" width="9" height="13" fill="#bfbf99"/></g>)}
    <rect x="175" y="402" width="33" height="11" fill="none" stroke="#b5bb94" strokeDasharray="3 2"/><rect x="174" y="403" width="6" height="9" fill="#b2c4b6"/><rect x="204" y="403" width="6" height="9" fill="#b2c4b6"/>
    <text x="94" y="475" fill="#a0bcb2" fontSize="10" fontFamily="monospace">ATX CORE / REV B</text><text x="539" y="68" fill="#aac6b4" fontSize="9" fontFamily="monospace">AX-2409</text>
    {overlays && defects.map((d,i)=><g className="defect-box" key={d.id} role="button" tabIndex="0" aria-label={`Select defect ${i+1}: ${d.type}`} onClick={()=>onSelect?.(d.id)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onSelect?.(d.id);}}}>
      <rect x={d.x} y={d.y} width={d.width} height={d.height} rx="4" fill={selected===d.id?'#ff784533':'#ff784515'} stroke={selected===d.id?'#ffb089':'#fb784b'} strokeWidth={selected===d.id?3:2} strokeDasharray={selected===d.id?'0':'6 3'}/>
      <circle cx={d.x} cy={d.y} r="12" fill="#f57746"/><text x={d.x} y={d.y+4} textAnchor="middle" fontSize="12" fontWeight="bold" fill="#182e30">{i+1}</text>
    </g>)}
  </svg>;
}
