import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { startSignIn, verifySignIn } from "../api/auth";
import { copy } from "../copy/en-GB";
import { parseMagicLink } from "../lib/deepLinks";
import { saveSessionToken } from "../lib/session";

type Props = {
  onSignedIn: () => void;
};

export function SignInScreen({ onSignedIn }: Props) {
  const [email, setEmail] = useState("");
  const [link, setLink] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  async function submitEmail() {
    await startSignIn(email.trim());
    setMessage(copy.signIn.sent);
  }

  async function submitLink() {
    const token = parseMagicLink(link) ?? link.trim();
    if (!token) {
      setMessage(copy.signIn.error.generic);
      return;
    }
    const result = await verifySignIn(token);
    await saveSessionToken(result.session_token);
    onSignedIn();
  }

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>{copy.signIn.title}</Text>
      <Text>{copy.signIn.subtitle}</Text>
      <Text>{copy.signIn.emailLabel}</Text>
      <TextInput
        accessibilityLabel={copy.signIn.emailLabel}
        autoCapitalize="none"
        inputMode="email"
        onChangeText={setEmail}
        placeholder={copy.signIn.emailPlaceholder}
        style={styles.input}
        value={email}
      />
      <Pressable accessibilityRole="button" onPress={submitEmail} style={styles.button}>
        <Text>{copy.signIn.submit}</Text>
      </Pressable>
      <TextInput
        accessibilityLabel={copy.signIn.sentSubtitle}
        autoCapitalize="none"
        onChangeText={setLink}
        placeholder={copy.signIn.sentSubtitle}
        style={styles.input}
        value={link}
      />
      <Pressable accessibilityRole="button" onPress={submitLink} style={styles.button}>
        <Text>{copy.signIn.title}</Text>
      </Pressable>
      {message ? <Text>{message}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  button: {
    alignItems: "flex-start",
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
    rowGap: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: "800",
  },
});
