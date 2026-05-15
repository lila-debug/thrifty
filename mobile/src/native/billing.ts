export type PlatformSubscriptionSnapshot = {
  source_product_id: string;
  service_name: string;
  amount: string | null;
  currency: string | null;
  cadence: "weekly" | "monthly" | "quarterly" | "semi_annual" | "annual" | "custom" | null;
  status: "trial" | "active" | "cancelled" | "expired" | "unknown";
  trial_ends_at: string | null;
  next_event_at: string | null;
  precision: "exact" | "estimated" | "unknown";
};

export async function readStoreKitSubscriptions(): Promise<PlatformSubscriptionSnapshot[]> {
  return [];
}

export async function readPlayBillingSubscriptions(): Promise<PlatformSubscriptionSnapshot[]> {
  return [];
}
