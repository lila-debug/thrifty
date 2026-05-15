export function formatAmount(amount: string | null, currency: string | null): string {
  if (!amount || !currency) {
    return "unknown";
  }
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency,
  }).format(Number(amount));
}

export function formatRelativeEvent(value: string | null): string {
  if (!value) {
    return "unknown";
  }
  const deltaMs = new Date(value).getTime() - Date.now();
  const deltaHours = Math.round(deltaMs / (1000 * 60 * 60));
  const deltaDays = Math.round(deltaHours / 24);
  const formatter = new Intl.RelativeTimeFormat("en-GB", { numeric: "auto" });
  if (Math.abs(deltaDays) >= 1) {
    return formatter.format(deltaDays, "day");
  }
  return formatter.format(deltaHours, "hour");
}
