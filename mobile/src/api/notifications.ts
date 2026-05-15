import { apiFetch } from "./client";

export async function registerNotificationToken(
  platform: "ios" | "android",
  token: string,
): Promise<void> {
  await apiFetch("/v1/notifications/token", {
    method: "POST",
    body: JSON.stringify({ platform, token }),
  });
}

export async function removeNotificationToken(id: string): Promise<void> {
  await apiFetch<void>(`/v1/notifications/token/${id}`, { method: "DELETE" });
}
