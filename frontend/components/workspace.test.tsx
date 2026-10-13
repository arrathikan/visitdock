import { fireEvent, render, screen } from "@testing-library/react";
import Workspace from "./workspace";
it("searches patient or doctor and combines status filters", () => {
 render(<Workspace />); fireEvent.change(screen.getByLabelText("Search"), { target: { value: "sage" } });
 expect(screen.getByText("Fictional Robin")).toBeInTheDocument(); expect(screen.queryByText("Fictional Rowan")).not.toBeInTheDocument();
 fireEvent.change(screen.getByLabelText("Status"), { target: { value: "scheduled" } });
 expect(screen.getByText("No matching appointments")).toBeInTheDocument();
 fireEvent.click(screen.getByRole("button", { name: "Clear filters" })); expect(screen.getByText("Fictional Rowan")).toBeInTheDocument();
});
