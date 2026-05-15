import { Pressable, StyleSheet, Text, View } from "react-native";

import type { Subscription } from "../api/subscriptions";
import { CurrencyAmount } from "../components/CurrencyAmount";
import { EventCountdown } from "../components/EventCountdown";
import { UnknownBadge } from "../components/UnknownBadge";
import { copy } from "../copy/en-GB";

type Props = {
  subscription: Subscription;
  onEdit: () => void;
  onRemove: () => void;
};

export function SubscriptionDetailScreen({ subscription, onEdit, onRemove }: Props) {
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>{copy.detail.title}</Text>
      <Text style={styles.name}>{subscription.service_name}</Text>
      <CurrencyAmount amount={subscription.amount} currency={subscription.currency} />
      <EventCountdown nextEventAt={subscription.next_event_at} />
      {subscription.amount === null ? <UnknownBadge reason="amount" /> : null}
      {subscription.cancel_by_at === null ? <UnknownBadge reason="cancelBy" /> : null}
      {subscription.terms_plain ? <Text>{subscription.terms_plain}</Text> : <UnknownBadge reason="terms" />}
      <View style={styles.actions}>
        <Pressable accessibilityRole="button" onPress={onEdit} style={styles.button}>
          <Text>{copy.detail.edit}</Text>
        </Pressable>
        <Pressable accessibilityRole="button" onPress={onRemove} style={styles.button}>
          <Text>{copy.detail.remove}</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  actions: {
    flexDirection: "row",
    gap: 12,
  },
  button: {
    borderWidth: 1,
    padding: 12,
  },
  name: {
    fontSize: 20,
    fontWeight: "700",
  },
  screen: {
    flex: 1,
    padding: 24,
    rowGap: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: "800",
  },
});
