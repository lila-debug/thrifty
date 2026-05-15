import { apiFetch } from "./client";

export type Alert = {
  id: string;
  subscription_id: string;
  alert_at: string;
  lead_label: string;
  status: "scheduled" | "sent" | "failed" | "cancelled";
};

export async function listAlerts(): Promise<Alert[]> {
  const response = await apiFetch<{ alerts: Alert[] }>("/v1/alerts?status=scheduled");
  return response.alerts;
}

export async function recomputeAlerts(subscriptionId?: string): Promise<{
  alerts_created: number;
  alerts_cancelled: number;
}> {
  return apiFetch("/v1/alerts/recompute", {
    method: "POST",
    body: JSON.stringify({ subscription_id: subscriptionId }),
  });
}
