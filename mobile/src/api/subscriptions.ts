import { apiFetch } from "./client";

export type Subscription = {
  id: string;
  service_name: string;
  source: "storekit" | "play_billing" | "plaid" | "manual";
  source_product_id: string | null;
  amount: string | null;
  currency: string | null;
  cadence: "weekly" | "monthly" | "quarterly" | "semi_annual" | "annual" | "custom" | null;
  custom_period_days: number | null;
  status: "trial" | "active" | "cancelled" | "expired" | "unknown";
  trial_ends_at: string | null;
  next_event_at: string | null;
  next_event_kind: "renewal" | "trial_conversion" | "unknown" | null;
  precision: "exact" | "estimated" | "unknown";
  cancel_by_at: string | null;
  cancel_url: string | null;
  terms_plain: string | null;
  notes: string | null;
};

export type SubscriptionInput = {
  service_name: string;
  amount?: string;
  currency?: string;
  cadence?: Subscription["cadence"];
  next_event_at?: string;
  next_event_kind?: Subscription["next_event_kind"];
  notes?: string;
};

export async function listSubscriptions(): Promise<Subscription[]> {
  const response = await apiFetch<{ subscriptions: Subscription[] }>("/v1/subscriptions");
  const now = Date.now();
  return response.subscriptions
    .filter((item) => !item.next_event_at || new Date(item.next_event_at).getTime() >= now)
    .sort((left, right) => {
      if (!left.next_event_at) return 1;
      if (!right.next_event_at) return -1;
      return new Date(left.next_event_at).getTime() - new Date(right.next_event_at).getTime();
    });
}

export async function createSubscription(input: SubscriptionInput): Promise<Subscription> {
  return apiFetch("/v1/subscriptions", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateSubscription(
  id: string,
  input: Partial<SubscriptionInput>,
): Promise<Subscription> {
  return apiFetch(`/v1/subscriptions/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteSubscription(id: string): Promise<void> {
  await apiFetch<void>(`/v1/subscriptions/${id}`, { method: "DELETE" });
}
