import { useCallback, useEffect, useState } from "react";
import { SafeAreaView, StyleSheet, Text } from "react-native";

import {
  createSubscription,
  deleteSubscription,
  listSubscriptions,
  type Subscription,
  type SubscriptionInput,
  updateSubscription,
} from "./src/api/subscriptions";
import { copy } from "./src/copy/en-GB";
import { registerForPush } from "./src/lib/push";
import { getSessionToken } from "./src/lib/session";
import { Navigation, type Screen } from "./src/navigation";
import { SignInScreen } from "./src/screens/SignInScreen";

export default function App() {
  const [signedIn, setSignedIn] = useState(false);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [screen, setScreen] = useState<Screen>({ name: "list" });
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setRefreshing(true);
    try {
      setSubscriptions(await listSubscriptions());
      setError(null);
    } catch {
      setError(copy.errors.network);
    } finally {
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    getSessionToken().then((token) => {
      if (token) {
        setSignedIn(true);
      }
    });
  }, []);

  useEffect(() => {
    if (!signedIn) {
      return;
    }
    void refresh();
    void registerForPush();
  }, [refresh, signedIn]);

  async function create(input: SubscriptionInput) {
    await createSubscription(input);
    setScreen({ name: "list" });
    await refresh();
  }

  async function update(subscription: Subscription, input: SubscriptionInput) {
    await updateSubscription(subscription.id, input);
    setScreen({ name: "list" });
    await refresh();
  }

  async function remove(subscription: Subscription) {
    await deleteSubscription(subscription.id);
    setScreen({ name: "list" });
    await refresh();
  }

  if (!signedIn) {
    return (
      <SafeAreaView style={styles.safe}>
        <SignInScreen onSignedIn={() => setSignedIn(true)} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safe}>
      {error ? <Text>{error}</Text> : null}
      <Navigation
        onAdd={() => setScreen({ name: "add" })}
        onCancel={() => setScreen({ name: "list" })}
        onCreate={create}
        onEdit={(subscription) => setScreen({ name: "edit", subscription })}
        onRefresh={refresh}
        onRemove={remove}
        onSelect={(subscription) => setScreen({ name: "detail", subscription })}
        onUpdate={update}
        refreshing={refreshing}
        screen={screen}
        subscriptions={subscriptions}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
  },
});
