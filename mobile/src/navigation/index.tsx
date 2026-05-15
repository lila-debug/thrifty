import type { Subscription, SubscriptionInput } from "../api/subscriptions";
import { SubscriptionAddScreen } from "../screens/SubscriptionAddScreen";
import { SubscriptionDetailScreen } from "../screens/SubscriptionDetailScreen";
import { SubscriptionEditScreen } from "../screens/SubscriptionEditScreen";
import { SubscriptionListScreen } from "../screens/SubscriptionListScreen";

export type Screen =
  | { name: "list" }
  | { name: "add" }
  | { name: "detail"; subscription: Subscription }
  | { name: "edit"; subscription: Subscription };

type Props = {
  screen: Screen;
  subscriptions: Subscription[];
  refreshing: boolean;
  onRefresh: () => void;
  onAdd: () => void;
  onSelect: (subscription: Subscription) => void;
  onCancel: () => void;
  onCreate: (input: SubscriptionInput) => Promise<void>;
  onUpdate: (subscription: Subscription, input: SubscriptionInput) => Promise<void>;
  onEdit: (subscription: Subscription) => void;
  onRemove: (subscription: Subscription) => void;
};

export function Navigation({
  screen,
  subscriptions,
  refreshing,
  onRefresh,
  onAdd,
  onSelect,
  onCancel,
  onCreate,
  onUpdate,
  onEdit,
  onRemove,
}: Props) {
  if (screen.name === "add") {
    return <SubscriptionAddScreen onCancel={onCancel} onSave={onCreate} />;
  }
  if (screen.name === "detail") {
    return (
      <SubscriptionDetailScreen
        onEdit={() => onEdit(screen.subscription)}
        onRemove={() => onRemove(screen.subscription)}
        subscription={screen.subscription}
      />
    );
  }
  if (screen.name === "edit") {
    return (
      <SubscriptionEditScreen
        onCancel={onCancel}
        onSave={(input) => onUpdate(screen.subscription, input)}
        subscription={screen.subscription}
      />
    );
  }
  return (
    <SubscriptionListScreen
      onAdd={onAdd}
      onRefresh={onRefresh}
      onSelect={onSelect}
      refreshing={refreshing}
      subscriptions={subscriptions}
    />
  );
}
