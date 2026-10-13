"use client";
import { useEffect, useState } from "react";
import { Appointment, AppointmentList, clinicTimezone, formattedTime, request } from "../lib/api";
import AppointmentForm from "./appointment-form";
import Modal from "./dialog";
export default function Workspace() {
  const [search, setSearch] = useState(""); const [doctor, setDoctor] = useState("");
  const [status, setStatus] = useState(""); const [date, setDate] = useState("");
  const [page, setPage] = useState(1); const [version, setVersion] = useState(0);
  const [data, setData] = useState<AppointmentList>({ items: [], total: 0, page: 1, page_size: 20 });
  const [loading, setLoading] = useState(true); const [error, setError] = useState(""); const [notice, setNotice] = useState("");
  const [editing, setEditing] = useState<Appointment | null | undefined>(undefined);
  const [deleting, setDeleting] = useState<Appointment | null>(null); const [busy, setBusy] = useState(false); const [deleteError, setDeleteError] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    const timer = setTimeout(async () => {
      setLoading(true); setError("");
      const params = new URLSearchParams({ page: String(page), page_size: "20" });
      for (const [key, value] of Object.entries({ search, doctor, status, date })) if (value.trim()) params.set(key,value.trim());
      try {
        const result = await request<AppointmentList>(`?${params}`, { signal: controller.signal });
        if (!controller.signal.aborted) { setData(result); if (page > 1 && !result.items.length) setPage(page-1); }
      } catch (e) { if (!controller.signal.aborted) setError(e instanceof Error ? e.message : "Unable to load appointments."); }
      finally { if (!controller.signal.aborted) setLoading(false); }
    }, 200);
    return () => { clearTimeout(timer); controller.abort(); };
  }, [search,doctor,status,date,page,version]);
  function reset() { setSearch(""); setDoctor(""); setStatus(""); setDate(""); setPage(1); }
  async function edit(appointment: Appointment) {
    setError(""); setBusy(true);
    try { setEditing(await request<Appointment>(`/${appointment.id}`)); }
    catch (e) { setError((e as Error).message); } finally { setBusy(false); }
  }
  async function remove() {
    if (!deleting) return; setBusy(true); setDeleteError("");
    try { await request(`/${deleting.id}`, { method: "DELETE" }); setDeleting(null); setNotice("Appointment deleted."); setVersion(v=>v+1); }
    catch (e) { setDeleteError((e as Error).message); } finally { setBusy(false); }
  }
  const active = !!(search || doctor || status || date);
  return <main id="main"><p className="eyebrow">THE RECEPTION DESK</p><div className="heading"><div><h1>Appointments</h1><p className="subtitle">A little order for the day ahead.</p></div><button className="primary" onClick={()=>setEditing(null)}>＋ New appointment</button></div>
    <div className="dayline"><span>{date ? `Appointments for ${date}` : "Your appointment book"}</span><span>Clinic times · {clinicTimezone}</span></div>
    <section className="filters" aria-label="Find appointments">
      <label>Search<input type="search" placeholder="Patient or doctor" maxLength={150} value={search} onChange={e=>{setSearch(e.target.value);setPage(1);}} /></label>
      <label>Doctor<input placeholder="Exact doctor name" maxLength={150} value={doctor} onChange={e=>{setDoctor(e.target.value);setPage(1);}} /></label>
      <label>Status<select value={status} onChange={e=>{setStatus(e.target.value);setPage(1);}}><option value="">All statuses</option><option value="scheduled">Scheduled</option><option value="completed">Completed</option><option value="cancelled">Cancelled</option></select></label>
      <label>Clinic date<input type="date" value={date} onChange={e=>{setDate(e.target.value);setPage(1);}} /></label><button onClick={reset}>Clear filters</button>
    </section>
    {notice && <p role="status" className="notice">{notice}</p>}
    {error ? <div role="alert" className="error">{error} <button onClick={()=>setVersion(v=>v+1)}>Retry</button></div> : loading ? <p role="status" className="empty">Loading appointments…</p> : <>
      <p className="resultcount" aria-live="polite">{data.total} {data.total === 1 ? "appointment" : "appointments"}{active ? " matching your filters" : " in the book"}</p>
      {data.items.length ? <div className="tablewrap"><table><caption className="sr-only">Appointments in {clinicTimezone}</caption><thead><tr><th scope="col">Date / Time</th><th scope="col">Patient</th><th scope="col">Doctor</th><th scope="col">Type</th><th scope="col">Status</th><th scope="col">Actions</th></tr></thead><tbody>{data.items.map(r=><tr key={r.id}><td className="time">{formattedTime(r.appointment_at)}</td><td className="patient">{r.patient_name}</td><td>{r.doctor}</td><td>{r.appointment_type.replaceAll("_"," ")}</td><td><span className={`status ${r.status}`}>{r.status}</span></td><td className="rowactions"><button disabled={busy} aria-label={`Edit ${r.patient_name}`} onClick={()=>edit(r)}>Edit</button><button disabled={busy} aria-label={`Delete ${r.patient_name}`} onClick={()=>{setDeleteError("");setDeleting(r);}}>Delete</button></td></tr>)}</tbody></table></div> : <div className="empty"><h2>{active ? "No matching appointments" : "A clear appointment book"}</h2><p>{active ? "Try another name, date or status, or clear your filters." : "Add your first fictional appointment to get started."}</p></div>}
      <nav className="pagination" aria-label="Pagination"><button disabled={page === 1} onClick={()=>setPage(p=>p-1)}>Previous</button><span>Page {page} of {Math.max(1,Math.ceil(data.total/20))}</span><button disabled={page*20 >= data.total} onClick={()=>setPage(p=>p+1)}>Next</button></nav>
    </>}
    {editing !== undefined && <AppointmentForm appointment={editing} close={()=>setEditing(undefined)} saved={()=>{setEditing(undefined);setNotice("Appointment saved.");setVersion(v=>v+1);}} />}
    {deleting && <Modal title="Delete appointment?" close={()=>setDeleting(null)} busy={busy}><p>Remove the appointment for <strong>{deleting.patient_name}</strong> on {formattedTime(deleting.appointment_at)} ({clinicTimezone})?</p><p className="formnote">This removes the booking permanently.</p>{deleteError && <p role="alert" className="error">{deleteError}</p>}<div className="dialogactions"><button disabled={busy} onClick={()=>setDeleting(null)}>Keep appointment</button><button className="danger" disabled={busy} onClick={remove}>{busy ? "Deleting…" : "Delete appointment"}</button></div></Modal>}
  </main>;
}
