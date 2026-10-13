import { ApiError, request, utcInput, utcInstant } from "./api";
afterEach(() => vi.unstubAllGlobals());
it("preserves explicit UTC form instants", () => {
  expect(utcInput("2026-10-20T09:30:00+05:30")).toBe("2026-10-20T04:00");
  expect(utcInstant("2026-10-20T04:00")).toBe("2026-10-20T04:00:00.000Z");
});
it("maps validation errors to fields", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({
            detail: [{ loc: ["body", "patient_name"], msg: "Name required" }],
          }),
          { status: 422 },
        ),
      ),
  );
  try {
    await request("");
    throw new Error("Expected rejection");
  } catch (e) {
    expect(e).toBeInstanceOf(ApiError);
    expect((e as ApiError).fields.patient_name).toBe("Name required");
  }
});
it("handles missing records and empty delete responses", async () => {
  const fetcher = vi
    .fn()
    .mockResolvedValueOnce(new Response("", { status: 404 }))
    .mockResolvedValueOnce(new Response(null, { status: 204 }));
  vi.stubGlobal("fetch", fetcher);
  await expect(request("/missing")).rejects.toThrow("no longer exists");
  expect(await request("/id", { method: "DELETE" })).toBeUndefined();
});
it("provides useful connection failures", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockRejectedValue(new TypeError("Failed to fetch")),
  );
  await expect(request("")).rejects.toThrow("Cannot reach VisitDock");
});
