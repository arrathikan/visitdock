import { render, screen } from "@testing-library/react";
import Page from "./page";
it("renders the appointment workspace heading", () => { render(<Page />); expect(screen.getByRole("heading", { name: "Appointments" })).toBeInTheDocument(); });
