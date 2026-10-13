import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import AppointmentForm from "./appointment-form";
beforeAll(() => {
  HTMLDialogElement.prototype.showModal = function () {
    this.setAttribute("open", "");
  };
  HTMLDialogElement.prototype.close = function () {
    this.removeAttribute("open");
  };
});
afterEach(() => vi.unstubAllGlobals());
it("keeps form input after field validation failure", async () => {
  const fetcher = vi.fn().mockResolvedValue(
    new Response(
      JSON.stringify({
        detail: [
          { loc: ["body", "patient_name"], msg: "Invalid patient name" },
        ],
      }),
      { status: 422 },
    ),
  );
  vi.stubGlobal("fetch", fetcher);
  const saved = vi.fn();
  render(<AppointmentForm appointment={null} close={vi.fn()} saved={saved} />);
  fireEvent.change(screen.getByLabelText("Patient name"), {
    target: { value: "Fictional Rowan" },
  });
  fireEvent.change(screen.getByLabelText("Doctor"), {
    target: { value: "Dr. Fictional Avery" },
  });
  fireEvent.change(screen.getByLabelText("Date and time (UTC)"), {
    target: { value: "2026-10-20T09:30" },
  });
  fireEvent.submit(
    screen.getByRole("button", { name: "Save appointment" }).closest("form")!,
  );
  await screen.findByText("Invalid patient name");
  expect(screen.getByLabelText("Patient name")).toHaveValue("Fictional Rowan");
  expect(saved).not.toHaveBeenCalled();
  await waitFor(() => expect(fetcher).toHaveBeenCalled());
  expect(JSON.parse(fetcher.mock.calls[0][1].body).appointment_at).toBe(
    "2026-10-20T09:30:00.000Z",
  );
});
it("preserves timestamp precision when editing other fields", async () => {
  const appointment = {
    id: "test-id",
    patient_name: "Fictional Rowan",
    doctor: "Dr. Fictional Avery",
    appointment_at: "2026-10-20T09:30:42.123Z",
    appointment_type: "consultation" as const,
    status: "scheduled" as const,
    created_at: "2026-10-13T00:00:00Z",
    updated_at: "2026-10-13T00:00:00Z",
  };
  const fetcher = vi
    .fn()
    .mockResolvedValue(new Response(JSON.stringify(appointment)));
  vi.stubGlobal("fetch", fetcher);
  const saved = vi.fn();
  render(
    <AppointmentForm appointment={appointment} close={vi.fn()} saved={saved} />,
  );
  fireEvent.change(screen.getByLabelText("Doctor"), {
    target: { value: "Dr. Fictional Updated" },
  });
  fireEvent.submit(
    screen.getByRole("button", { name: "Save appointment" }).closest("form")!,
  );
  await waitFor(() => expect(saved).toHaveBeenCalled());
  expect(JSON.parse(fetcher.mock.calls[0][1].body).appointment_at).toBe(
    appointment.appointment_at,
  );
});
it.each([
  ["appointment_at", "Date and time (UTC)", "Invalid appointment time"],
  ["appointment_type", "Appointment type", "Invalid appointment type"],
  ["status", "Appointment status", "Invalid appointment status"],
])(
  "associates %s validation with its field while retaining the form",
  async (field, label, message) => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            detail: [{ loc: ["body", field], msg: message }],
          }),
          { status: 422 },
        ),
      ),
    );
    const saved = vi.fn();
    render(
      <AppointmentForm appointment={null} close={vi.fn()} saved={saved} />,
    );
    const time = screen.getByLabelText("Date and time (UTC)");
    const help =
      "UTC avoids daylight-saving ambiguity. The list shows the clinic timezone.";
    expect(time).toHaveAccessibleDescription(help);
    expect(time).toHaveAttribute("aria-describedby", "time-help");
    fireEvent.change(screen.getByLabelText("Patient name"), {
      target: { value: "Fictional Rowan" },
    });
    fireEvent.change(screen.getByLabelText("Doctor"), {
      target: { value: "Dr. Fictional Avery" },
    });
    fireEvent.change(time, { target: { value: "2026-10-20T09:30" } });
    fireEvent.change(screen.getByLabelText("Appointment type"), {
      target: { value: "follow_up" },
    });
    fireEvent.change(screen.getByLabelText("Appointment status"), {
      target: { value: "completed" },
    });
    fireEvent.submit(
      screen.getByRole("button", { name: "Save appointment" }).closest("form")!,
    );
    await screen.findByText(message);
    const input = screen.getByLabelText(label);
    expect(input).toHaveAttribute("aria-invalid", "true");
    expect(input).toHaveAttribute(
      "aria-describedby",
      field === "appointment_at"
        ? `time-help ${field}-error`
        : `${field}-error`,
    );
    expect(input).toHaveAccessibleDescription(
      field === "appointment_at" ? `${help} ${message}` : message,
    );
    expect(screen.getByText(message)).toHaveAttribute("id", `${field}-error`);
    expect(screen.getByLabelText("Patient name")).toHaveValue(
      "Fictional Rowan",
    );
    expect(screen.getByLabelText("Doctor")).toHaveValue("Dr. Fictional Avery");
    expect(time).toHaveValue("2026-10-20T09:30");
    expect(screen.getByLabelText("Appointment type")).toHaveValue("follow_up");
    expect(screen.getByLabelText("Appointment status")).toHaveValue(
      "completed",
    );
    expect(saved).not.toHaveBeenCalled();
  },
);
