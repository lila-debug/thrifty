import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import type { Subscription, SubscriptionInput } from "../api/subscriptions";
import { copy } from "../copy/en-GB";

type Props = {
  initial?: Subscription;
  onCancel: () => void;
  onSave: (input: SubscriptionInput) => Promise<void>;
};

export function SubscriptionAddScreen({ initial, onCancel, onSave }: Props) {
  const [serviceName, setServiceName] = useState(initial?.service_name ?? "");
  const [amount, setAmount] = useState(initial?.amount ?? "");
  const [currency, setCurrency] = useState(initial?.currency ?? "");
  const [nextEventAt, setNextEventAt] = useState(initial?.next_event_at ?? "");
  const [notes, setNotes] = useState(initial?.notes ?? "");
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    if (!serviceName.trim()) {
      setError(copy.add.validation.serviceNameRequired);
      return;
    }
    if (amount && Number(amount) <= 0) {
      setError(copy.add.validation.amountInvalid);
      return;
    }
    await onSave({
      service_name: serviceName.trim(),
      amount: amount || undefined,
      currency: currency || undefined,
      next_event_at: nextEventAt || undefined,
      notes: notes || undefined,
    });
  }

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>{initial ? copy.add.editTitle : copy.add.title}</Text>
      <Text>{copy.add.fields.serviceName}</Text>
      <TextInput
        accessibilityLabel={copy.add.fields.serviceName}
        onChangeText={setServiceName}
        placeholder={copy.add.fields.serviceNamePlaceholder}
        style={styles.input}
        value={serviceName}
      />
      <Text>{copy.add.fields.amount}</Text>
      <TextInput
        accessibilityLabel={copy.add.fields.amount}
        inputMode="decimal"
        onChangeText={setAmount}
        style={styles.input}
        value={amount}
      />
      <Text>{copy.add.fields.currency}</Text>
      <TextInput
        accessibilityLabel={copy.add.fields.currency}
        autoCapitalize="characters"
        maxLength={3}
        onChangeText={setCurrency}
        style={styles.input}
        value={currency}
      />
      <Text>{copy.add.fields.nextEvent}</Text>
      <TextInput
        accessibilityLabel={copy.add.fields.nextEvent}
        onChangeText={setNextEventAt}
        style={styles.input}
        value={nextEventAt}
      />
      <Text>{copy.add.fields.notes}</Text>
      <TextInput
        accessibilityLabel={copy.add.fields.notes}
        multiline
        onChangeText={setNotes}
        style={styles.input}
        value={notes}
      />
      {error ? <Text>{error}</Text> : null}
      <View style={styles.actions}>
        <Pressable accessibilityRole="button" onPress={onCancel} style={styles.button}>
          <Text>{copy.add.cancel}</Text>
        </Pressable>
        <Pressable accessibilityRole="button" onPress={submit} style={styles.button}>
          <Text>{copy.add.submit}</Text>
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
  input: {
    borderWidth: 1,
    padding: 12,
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
