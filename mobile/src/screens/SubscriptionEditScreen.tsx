import type { Subscription, SubscriptionInput } from "../api/subscriptions";
import { SubscriptionAddScreen } from "./SubscriptionAddScreen";

type Props = {
  subscription: Subscription;
  onCancel: () => void;
  onSave: (input: SubscriptionInput) => Promise<void>;
};

export function SubscriptionEditScreen({ subscription, onCancel, onSave }: Props) {
  return <SubscriptionAddScreen initial={subscription} onCancel={onCancel} onSave={onSave} />;
}
