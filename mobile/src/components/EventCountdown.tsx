import { Text } from "react-native";

import { formatRelativeEvent } from "../lib/format";

type Props = {
  nextEventAt: string | null;
};

export function EventCountdown({ nextEventAt }: Props) {
  return <Text>{formatRelativeEvent(nextEventAt)}</Text>;
}
