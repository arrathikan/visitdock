"use client";
import { useState } from "react";
import {
  ApiError,
  Appointment,
  Payload,
  request,
  utcInput,
  utcInstant,
} from "../lib/api";
import Modal from "./dialog";
export default function AppointmentForm({
  appointment,
  close,
  saved,
}: {
  appointment: Appointment | null;
  close: () => void;
  saved: () => void;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    const form = new FormData(event.currentTarget);
    try {
      const payload: Payload = {
        patient_name: String(form.get("patient_name")).trim(),
        doctor: String(form.get("doctor")).trim(),
        appointment_at: utcInstant(
          String(form.get("appointment_at")),
          appointment?.appointment_at,
        ),
        appointment_type: form.get(
          "appointment_type",
        ) as Payload["appointment_type"],
        status: form.get("status") as Payload["status"],
      };
      await request(appointment ? `/${appointment.id}` : "", {
        method: appointment ? "PUT" : "POST",
        body: JSON.stringify(payload),
      });
      saved();
    } catch (e) {
      setError(
        e instanceof ApiError
          ? e
          : new ApiError("Could not save this appointment."),
      );
    } finally {
      setBusy(false);
    }
  }
  function fieldError(name: string) {
    return error?.fields[name] ? (
      <span id={`${name}-error`} className="field-error">
        {error.fields[name]}
      </span>
    ) : null;
  }
  return (
    <Modal
      title={appointment ? "Edit appointment" : "New appointment"}
      close={close}
      busy={busy}
      drawer
    >
      <p className="formnote">
        Use invented names only. Date and time are entered in{" "}
        <strong>UTC</strong>.
      </p>
      <form onSubmit={submit}>
        <fieldset disabled={busy}>
          <label>
            Patient name
            <input
              aria-label="Patient name"
              name="patient_name"
              required
              maxLength={150}
              defaultValue={appointment?.patient_name}
              aria-invalid={!!error?.fields.patient_name}
              aria-describedby={
                error?.fields.patient_name ? "patient_name-error" : undefined
              }
            />
            {fieldError("patient_name")}
          </label>
          <label>
            Doctor
            <input
              aria-label="Doctor"
              name="doctor"
              required
              maxLength={150}
              defaultValue={appointment?.doctor}
              aria-invalid={!!error?.fields.doctor}
              aria-describedby={
                error?.fields.doctor ? "doctor-error" : undefined
              }
            />
            {fieldError("doctor")}
          </label>
          <label>
            Date and time (UTC)
            <input
              aria-label="Date and time (UTC)"
              name="appointment_at"
              type="datetime-local"
              required
              defaultValue={
                appointment ? utcInput(appointment.appointment_at) : ""
              }
              aria-invalid={!!error?.fields.appointment_at}
              aria-describedby="time-help"
            />
            {fieldError("appointment_at")}
          </label>
          <p id="time-help" className="formnote">
            UTC avoids daylight-saving ambiguity. The list shows the clinic
            timezone.
          </p>
          <label>
            Appointment type
            <select
              name="appointment_type"
              defaultValue={appointment?.appointment_type || "consultation"}
            >
              <option value="consultation">Consultation</option>
              <option value="follow_up">Follow up</option>
              <option value="check_up">Check up</option>
            </select>
            {fieldError("appointment_type")}
          </label>
          <label>
            Appointment status
            <select
              name="status"
              defaultValue={appointment?.status || "scheduled"}
            >
              <option value="scheduled">Scheduled</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
            {fieldError("status")}
          </label>
        </fieldset>
        {error && (
          <p role="alert" className="error">
            {error.message}
          </p>
        )}
        <div className="dialogactions">
          <button type="button" disabled={busy} onClick={close}>
            Cancel
          </button>
          <button className="primary" type="submit" disabled={busy}>
            {busy ? "Saving…" : "Save appointment"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
