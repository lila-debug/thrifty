import * as Linking from "expo-linking";

export function parseMagicLink(url: string): string | null {
  const parsed = Linking.parse(url);
  const token = parsed.queryParams?.token;
  return typeof token === "string" ? token : null;
}

export function subscribeToMagicLinks(onToken: (token: string) => void): () => void {
  const listener = Linking.addEventListener("url", ({ url }) => {
    const token = parseMagicLink(url);
    if (token) {
      onToken(token);
    }
  });
  return () => listener.remove();
}
