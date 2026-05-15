import * as Notifications from "expo-notifications";
import { Platform } from "react-native";

import { registerNotificationToken } from "../api/notifications";

export async function registerForPush(): Promise<string | null> {
  const permission = await Notifications.requestPermissionsAsync();
  if (!permission.granted) {
    return null;
  }
  const token = await Notifications.getExpoPushTokenAsync();
  const platform = Platform.OS === "android" ? "android" : "ios";
  await registerNotificationToken(platform, token.data);
  return token.data;
}
