import { Text, View } from "react-native";

import { copy } from "../copy/en-GB";

type Props = {
  reason: keyof typeof copy.unknown.reasons;
};

export function UnknownBadge({ reason }: Props) {
  return (
    <View accessibilityRole="text">
      <Text>{copy.unknown.badge}</Text>
      <Text>{copy.unknown.reasons[reason]}</Text>
    </View>
  );
}
