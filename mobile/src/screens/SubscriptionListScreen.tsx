import { FlatList, Pressable, RefreshControl, StyleSheet, Text, View } from "react-native";

import type { Subscription } from "../api/subscriptions";
import { SubscriptionCard } from "../components/SubscriptionCard";
import { copy } from "../copy/en-GB";

type Props = {
  subscriptions: Subscription[];
  refreshing: boolean;
  onRefresh: () => void;
  onAdd: () => void;
  onSelect: (subscription: Subscription) => void;
};

export function SubscriptionListScreen({
  subscriptions,
  refreshing,
  onRefresh,
  onAdd,
  onSelect,
}: Props) {
  return (
    <View style={styles.screen}>
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>{copy.list.title}</Text>
          <Text>{copy.list.headerSubtitle}</Text>
        </View>
        <Pressable accessibilityRole="button" onPress={onAdd} style={styles.button}>
          <Text>{copy.list.add}</Text>
        </Pressable>
      </View>
      <FlatList
        data={subscriptions}
        keyExtractor={(item) => item.id}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.name}>{copy.list.empty.title}</Text>
            <Text>{copy.list.empty.subtitle}</Text>
            <Pressable accessibilityRole="button" onPress={onAdd} style={styles.button}>
              <Text>{copy.list.empty.cta}</Text>
            </Pressable>
          </View>
        }
        refreshControl={
          <RefreshControl
            accessibilityLabel={copy.list.pullToRefresh}
            onRefresh={onRefresh}
            refreshing={refreshing}
          />
        }
        renderItem={({ item }) => <SubscriptionCard onPress={onSelect} subscription={item} />}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  button: {
    borderWidth: 1,
    padding: 12,
  },
  empty: {
    padding: 16,
    rowGap: 12,
  },
  header: {
    alignItems: "flex-start",
    flexDirection: "row",
    justifyContent: "space-between",
    padding: 16,
  },
  name: {
    fontSize: 18,
    fontWeight: "700",
  },
  screen: {
    flex: 1,
  },
  title: {
    fontSize: 28,
    fontWeight: "800",
  },
});
