import * as Notifications from "expo-notifications";

import type { Subscription } from "../api/subscriptions";
import { copy } from "../copy/en-GB";
import { formatAmount, formatRelativeEvent } from "./format";

const leadTimes = [
  { label: copy.alerts.leadLabels.sevenDays, milliseconds: 7 * 24 * 60 * 60 * 1000 },
  { label: copy.alerts.leadLabels.threeDays, milliseconds: 3 * 24 * 60 * 60 * 1000 },
  { label: copy.alerts.leadLabels.oneDay, milliseconds: 24 * 60 * 60 * 1000 },
  { label: copy.alerts.leadLabels.twoHours, milliseconds: 2 * 60 * 60 * 1000 },
];

export async function scheduleLocalFallbacks(subscription: Subscription): Promise<void> {
  if (!subscription.next_event_at) {
    return;
  }
  const eventTime = new Date(subscription.next_event_at).getTime();
  const amount = formatAmount(subscription.amount, subscription.currency);
  const when = formatRelativeEvent(subscription.next_event_at);
  const title = subscription.service_name;
  const body =
    subscription.next_event_kind === "trial_conversion"
      ? copy.alerts.push.trialConversion(title, when, amount)
      : copy.alerts.push.renewal(title, when, amount);

  for (const lead of leadTimes) {
    const triggerAt = eventTime - lead.milliseconds;
    if (triggerAt <= Date.now()) {
      continue;
    }
    await Notifications.scheduleNotificationAsync({
      content: { title, body },
      trigger: {
        type: Notifications.SchedulableTriggerInputTypes.DATE,
        date: new Date(triggerAt),
      },
    });
  }
}

export async function clearLocalFallbacks(): Promise<void> {
  await Notifications.cancelAllScheduledNotificationsAsync();
}
