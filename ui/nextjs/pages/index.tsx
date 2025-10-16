import { useState } from 'react'
export default function Home(){const [q,setQ]=useState("");const[a,setA]=useState("");const[l,setL]=useState(false);
const ask=async()=>{setL(true);const r=await fetch("/api/proxy",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q})});const d=await r.json();setA(d.answer||JSON.stringify(d));setL(false);};
return (<main style={{maxWidth:720,margin:"2rem auto",fontFamily:"ui-sans-serif"}}>
<h1>Rate Case Advisor (Hackathon)</h1>
<textarea value={q} onChange={e=>setQ(e.target.value)} rows={4} style={{width:"100%"}} placeholder="Ask an intervenor-style question"/>
<button onClick={ask} disabled={l} style={{padding:"0.5rem 1rem",marginTop:"0.5rem"}}>{l?"Thinking...":"Ask"}</button>
<pre style={{whiteSpace:"pre-wrap",background:"#f7f7f7",padding:"1rem",marginTop:"1rem"}}>{a}</pre>
</main>)}