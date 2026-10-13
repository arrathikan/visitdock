export type Appointment = {
  id: string; patient_name: string; doctor: string; appointment_at: string;
  appointment_type: "consultation" | "follow_up" | "check_up";
  status: "scheduled" | "completed" | "cancelled";
  created_at: string; updated_at: string;
};
export type Payload = Omit<Appointment, "id" | "created_at" | "updated_at">;
export type AppointmentList = { items: Appointment[]; total: number; page: number; page_size: number };
export const clinicTimezone = process.env.NEXT_PUBLIC_CLINIC_TIMEZONE || "UTC";
const base = (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1").replace(/\/$/, "");
export class ApiError extends Error {
  constructor(message: string, public fields: Record<string, string> = {}) { super(message); }
}
export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response;
  try { response = await fetch(`${base}/appointments${path}`, { ...options, headers: { "Content-Type": "application/json", ...options.headers }, cache: "no-store" }); }
  catch (error) { if (error instanceof Error && error.name === "AbortError") throw error; throw new ApiError("Cannot reach VisitDock. Check the API connection and try again."); }
  if (!response.ok) {
    if (response.status === 404) throw new ApiError("This appointment no longer exists. Refresh the list.");
    if (response.status === 422) {
      const data = await response.json(); const fields: Record<string, string> = {};
      if (Array.isArray(data.detail)) for (const item of data.detail) fields[String(item.loc?.at(-1))] = item.msg;
      throw new ApiError("Please check the highlighted fields.", fields);
    }
    throw new ApiError("VisitDock could not complete this request. Please try again.");
  }
  return response.status === 204 ? undefined as T : response.json();
}
export function utcInput(instant: string): string { return new Date(instant).toISOString().slice(0,16); }
export function utcInstant(input: string): string { return new Date(`${input}:00Z`).toISOString(); }
export function formattedTime(instant: string): string {
  return new Intl.DateTimeFormat("en-GB", { timeZone: clinicTimezone, day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).format(new Date(instant));
}
