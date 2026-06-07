export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function getHealth(): Promise<{ status: string }> {
  const res = await fetch(`${API_URL}/health`);
  if (!res.ok) throw new Error(`health check failed: ${res.status}`);
  return res.json();
}
