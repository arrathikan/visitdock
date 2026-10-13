import { test, expect, request as independentRequest } from "@playwright/test";
import { randomUUID } from "node:crypto";
const api = process.env.E2E_API_BASE_URL || "http://localhost:8000/api/v1";
test("fictional appointment CRUD, search, filters, keyboard and responsive layout", async ({
  page,
  request,
}, testInfo) => {
  const name = `Fictional E2E ${randomUUID().slice(0, 8)}`;
  let id: string | undefined;
  try {
    await page.goto("/");
    await expect(
      page.getByRole("heading", { name: "Appointments", exact: true }),
    ).toBeVisible();
    const newButton = page.getByRole("button", { name: "New appointment" });
    await newButton.click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByRole("dialog")).not.toBeVisible();
    await expect(newButton).toBeFocused();
    await newButton.click();
    await page.getByLabel("Patient name", { exact: true }).fill(name);
    await page
      .getByLabel("Doctor", { exact: true })
      .last()
      .fill("Dr. Fictional E2E");
    await page.getByLabel("Date and time (UTC)").fill("2026-10-20T09:30");
    const created = page.waitForResponse(
      (r) =>
        r.url().endsWith("/appointments") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Save appointment" }).click();
    const response = await created;
    expect(response.status()).toBe(201);
    id = (await response.json()).id;
    await expect(page.getByRole("dialog")).not.toBeVisible();
    await page.getByLabel("Search", { exact: true }).fill(name);
    await expect(page.getByText(name, { exact: true })).toBeVisible();
    await page
      .getByRole("button", { name: `Edit ${name}`, exact: true })
      .click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await expect(page.getByLabel("Patient name", { exact: true })).toHaveValue(
      name,
    );
    await page
      .getByLabel("Doctor", { exact: true })
      .last()
      .fill("Dr. Fictional Updated");
    await page.getByLabel("Appointment status").selectOption("completed");
    await page.getByRole("button", { name: "Save appointment" }).click();
    await expect(page.getByRole("dialog")).not.toBeVisible();
    await page
      .getByRole("combobox", { name: "Status", exact: true })
      .selectOption("completed");
    await expect(
      page.getByText("Dr. Fictional Updated", { exact: true }),
    ).toBeVisible();
    await page.getByLabel("Clinic date").fill("2026-10-20");
    await expect(page.getByText(name, { exact: true })).toBeVisible();
    const row = page.getByRole("row").filter({ hasText: name });
    await expect(row.getByText("completed", { exact: true })).toBeVisible();
    await expect
      .poll(() =>
        page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      )
      .toBe(true);
    await page.screenshot({
      path: testInfo.outputPath("workspace.png"),
      fullPage: true,
    });
    await page
      .getByRole("button", { name: `Delete ${name}`, exact: true })
      .click();
    await page.getByRole("button", { name: "Keep appointment" }).click();
    await expect(page.getByText(name, { exact: true })).toBeVisible();
    await page
      .getByRole("button", { name: `Delete ${name}`, exact: true })
      .click();
    await page
      .getByRole("button", { name: "Delete appointment", exact: true })
      .click();
    await expect(page.getByRole("dialog")).not.toBeVisible();
    await expect(page.getByText("No matching appointments")).toBeVisible();
    expect((await request.get(`${api}/appointments/${id}`)).status()).toBe(404);
    id = undefined;
  } finally {
    if (id) {
      const cleanup = await independentRequest.newContext();
      try {
        await cleanup.delete(`${api}/appointments/${id}`);
      } finally {
        await cleanup.dispose();
      }
    }
  }
});
test("API failure can be retried and empty state is accessible", async ({
  page,
}) => {
  await page.route("**/api/v1/appointments?**", (route) =>
    route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({ detail: "unavailable" }),
    }),
  );
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Retry" })).toBeVisible();
  await page.unroute("**/api/v1/appointments?**");
  await page.getByRole("button", { name: "Retry" }).click();
  await expect(page.locator("main").getByRole("alert")).not.toBeVisible();
  await page
    .getByLabel("Search", { exact: true })
    .fill(`Fictional absent ${randomUUID()}`);
  await expect(page.getByText("No matching appointments")).toBeVisible();
});
test("maximum-length patient and doctor names wrap without clipping or overflow", async ({
  page,
}, testInfo) => {
  const patient = `Fictional${"X".repeat(141)}`;
  const doctor = `Fictional${"Y".repeat(141)}`;
  // Only the list is mocked; no database record is created for this layout edge.
  await page.route("**/api/v1/appointments?**", (route) =>
    route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        items: [
          {
            id: "06de9c6b-b96d-4c60-81c0-b89de0778523",
            patient_name: patient,
            doctor,
            appointment_at: "2026-10-20T09:30:00Z",
            appointment_type: "consultation",
            status: "scheduled",
            created_at: "2026-10-13T00:00:00Z",
            updated_at: "2026-10-13T00:00:00Z",
          },
        ],
        total: 1,
        page: 1,
        page_size: 20,
      }),
    }),
  );
  await page.goto("/");
  const row = page.getByRole("row").filter({ hasText: patient });
  await expect(row).toBeVisible();
  const viewportWidth = page.viewportSize()!.width;
  for (const [cell, name] of [
    [row.locator("td").nth(1), patient],
    [row.locator("td").nth(2), doctor],
  ] as const) {
    await expect(cell).toHaveText(name);
    expect(
      await cell.evaluate((element, viewport) => {
        const bounds = element.getBoundingClientRect();
        return (
          element.scrollWidth <= element.clientWidth &&
          bounds.left >= 0 &&
          bounds.right <= viewport
        );
      }, viewportWidth),
    ).toBe(true);
  }
  expect(
    await page.evaluate(
      (viewport) => document.documentElement.scrollWidth <= viewport,
      viewportWidth,
    ),
  ).toBe(true);
  await page.screenshot({
    path: testInfo.outputPath("maximum-length-names.png"),
    fullPage: true,
  });
  await row
    .getByRole("button", { name: `Delete ${patient}`, exact: true })
    .click();
  const dialog = page.getByRole("dialog");
  await expect(dialog.getByText(patient, { exact: true })).toBeVisible();
  expect(
    await dialog.evaluate(
      (element) => element.scrollWidth <= element.clientWidth,
    ),
  ).toBe(true);
  await dialog.getByRole("button", { name: "Keep appointment" }).click();
});
