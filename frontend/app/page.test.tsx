import { render, screen } from "@testing-library/react";
import Page from "./page";
afterEach(() => vi.unstubAllGlobals());
it("renders the appointment workspace heading", () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ items: [], total: 0, page: 1, page_size: 20 }),
        ),
      ),
  );
  render(<Page />);
  expect(
    screen.getByRole("heading", { name: "Appointments" }),
  ).toBeInTheDocument();
});
