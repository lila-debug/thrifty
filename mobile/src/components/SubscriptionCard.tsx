import { Pressable, StyleSheet, Text, View } from "react-native";

import type { Subscription } from "../api/subscriptions";
import { CurrencyAmount } from "./CurrencyAmount";
import { EventCountdown } from "./EventCountdown";
import { UnknownBadge } from "./UnknownBadge";

type Props = {
  subscription: Subscription;
  onPress: (subscription: Subscription) => void;
};

export function SubscriptionCard({ subscription, onPress }: Props) {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={() => onPress(subscription)}
      style={styles.card}
    >
      <View style={styles.row}>
        <Text style={styles.name}>{subscription.service_name}</Text>
        <CurrencyAmount amount={subscription.amount} currency={subscription.currency} />
      </View>
      <EventCountdown nextEventAt={subscription.next_event_at} />
      {subscription.precision === "unknown" ? <UnknownBadge reason="nextEvent" /> : null}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    padding: 16,
    rowGap: 8,
  },
  name: {
    fontSize: 18,
    fontWeight: "700",
  },
  row: {
    alignItems: "flex-start",
    flexDirection: "row",
    justifyContent: "space-between",
  },
});
