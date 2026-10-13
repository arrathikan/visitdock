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
  const fetcher = vi
    .fn()
    .mockResolvedValue(
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
