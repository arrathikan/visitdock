"use client";
import { useState } from "react";
const records = [
  { id: "demo-1", patient: "Fictional Rowan", doctor: "Dr. Fictional Avery", time: "09:30", type: "Consultation", status: "scheduled" },
  { id: "demo-2", patient: "Fictional Robin", doctor: "Dr. Fictional Sage", time: "10:15", type: "Follow up", status: "completed" },
];
export default function Workspace() {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [doctor, setDoctor] = useState("");
  const [notice, setNotice] = useState("");
  const filtered = records.filter(r => (!status || r.status === status) && (!doctor || r.doctor === doctor) && `${r.patient} ${r.doctor}`.toLowerCase().includes(search.toLowerCase()));
  return <main id="main"><p className="eyebrow">THE RECEPTION DESK · LOCAL PREVIEW</p><div className="heading"><div><h1>Appointments</h1><p className="subtitle">A little order for the day ahead.</p></div><button className="primary" onClick={() => setNotice("Preview only — API integration follows in F03.")}>＋ New appointment</button></div>
    <div className="dayline"><span>Tuesday, 20 October 2026</span><span>Times in UTC · fictional preview</span></div>
    <section className="filters" aria-label="Find appointments"><label>Search<input type="search" placeholder="Patient or doctor" value={search} onChange={e=>setSearch(e.target.value)} /></label><label>Doctor<select value={doctor} onChange={e=>setDoctor(e.target.value)}><option value="">All doctors</option>{records.map(r=><option key={r.id}>{r.doctor}</option>)}</select></label><label>Status<select value={status} onChange={e=>setStatus(e.target.value)}><option value="">All statuses</option><option>scheduled</option><option>completed</option><option>cancelled</option></select></label><button onClick={()=>{setSearch("");setStatus("");setDoctor("");}}>Clear filters</button></section>
    <p className="resultcount" aria-live="polite">{filtered.length} appointments</p>{notice && <p role="status">{notice}</p>}
    <div className="tablewrap"><table><thead><tr><th>Time</th><th>Patient</th><th>Doctor</th><th>Type</th><th>Status</th><th>Actions</th></tr></thead><tbody>{filtered.map(r=><tr key={r.id}><td className="time">{r.time}</td><td className="patient">{r.patient}</td><td>{r.doctor}</td><td>{r.type}</td><td><span className={`status ${r.status}`}>{r.status}</span></td><td><button onClick={()=>setNotice("Preview only — editing is not saved.")}>Preview edit</button></td></tr>)}</tbody></table></div>
    {!filtered.length && <div className="empty"><h2>No matching appointments</h2><p>Try another name or clear your filters.</p></div>}
  </main>;
}
