import { apiFetch } from "./client";

export type SignedInUser = {
  id: string;
  email: string;
  tier: "free" | "plus";
};

export async function startSignIn(email: string): Promise<void> {
  await apiFetch<{ status: "sent" }>("/v1/auth/start", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function verifySignIn(token: string): Promise<{
  session_token: string;
  user: SignedInUser;
}> {
  return apiFetch("/v1/auth/verify", {
    method: "POST",
    body: JSON.stringify({ token }),
  });
}
