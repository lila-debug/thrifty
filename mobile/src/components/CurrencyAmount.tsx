import { Text } from "react-native";

import { formatAmount } from "../lib/format";

type Props = {
  amount: string | null;
  currency: string | null;
};

export function CurrencyAmount({ amount, currency }: Props) {
  return <Text>{formatAmount(amount, currency)}</Text>;
}
