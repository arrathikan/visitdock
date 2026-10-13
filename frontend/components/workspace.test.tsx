import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import Workspace from "./workspace";
const row = { id:"fake", patient_name:"Fictional Rowan",doctor:"Dr. Fictional Avery",appointment_at:"2026-10-20T09:30:00Z",appointment_type:"consultation",status:"scheduled" };
afterEach(()=>vi.unstubAllGlobals());
it("loads real response rows and serializes search/status filters",async()=>{
 const fetcher=vi.fn().mockImplementation((url:string)=>Promise.resolve(new Response(JSON.stringify({items:url.includes("status=completed")?[]:[row],total:url.includes("status=completed")?0:1,page:1,page_size:20}))));vi.stubGlobal("fetch",fetcher);
 render(<Workspace/>);expect(screen.getByText("Loading appointments…")).toBeInTheDocument();await screen.findByText("Fictional Rowan");
 fireEvent.change(screen.getByLabelText("Search"),{target:{value:"Avery"}});fireEvent.change(screen.getByLabelText("Status"),{target:{value:"completed"}});
 await screen.findByText("No matching appointments");await waitFor(()=>expect(fetcher.mock.calls.at(-1)?.[0]).toContain("search=Avery"));expect(fetcher.mock.calls.at(-1)?.[0]).toContain("status=completed");
});
it("shows API error and supports retry",async()=>{const fetcher=vi.fn().mockRejectedValueOnce(new Error("offline")).mockResolvedValue(new Response(JSON.stringify({items:[],total:0,page:1,page_size:20})));vi.stubGlobal("fetch",fetcher);render(<Workspace/>);await screen.findByRole("alert");fireEvent.click(screen.getByRole("button",{name:"Retry"}));await screen.findByText("A clear appointment book");});
