const API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL!;
const API_KEY = process.env.EXPO_PUBLIC_BACKEND_API_Key!;

async function apiFetch(path: string, options: RequestInit = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'X-API-Key': API_KEY,
      'Accept': 'application/json',
      ...(options.headers || {}),
    },
  });

  if (!res.ok) throw new Error(`API Error ${res.status}: ${res.statusText}`);
  return res.json();
}

export default apiFetch;
