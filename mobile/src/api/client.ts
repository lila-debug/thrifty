import { getSessionToken } from "../lib/session";

export type ApiError = {
  code: string;
  message: string;
  field?: string;
};

export class ApiRequestError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly apiError?: ApiError,
  ) {
    super(message);
  }
}

const API_BASE_URL = "http://localhost:8000";

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = await getSessionToken();
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { error?: ApiError } | null;
    const message = body?.error?.message ?? `Request failed with status ${response.status}`;
    throw new ApiRequestError(message, response.status, body?.error);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}
