import { useQuery } from "@tanstack/react-query";
import { API_URL, getHealth } from "./api";

export default function App() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
  });

  const apiStatus = isLoading
    ? "checking…"
    : isError
      ? "unreachable"
      : (data?.status ?? "unknown");

  return (
    <main
      style={{
        fontFamily: "system-ui, sans-serif",
        padding: "2rem",
        maxWidth: 640,
      }}
    >
      <h1>stroke-master</h1>
      <p>Rowing analytics — scaffold.</p>
      <p>
        API status: <strong>{apiStatus}</strong>
      </p>
      <p>
        <a href={`${API_URL}/auth/strava/login`}>Connect Strava</a>
      </p>
    </main>
  );
}
