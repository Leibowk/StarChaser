const API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL!;
const API_KEY = process.env.EXPO_PUBLIC_BACKEND_API_Key!;

type FetchOptions = RequestInit & { params?: Record<string, any> };

async function apiFetch(path: string, options: FetchOptions = {}) {
  let url = `${API_URL}${path}`;

  // Handle query params
  if (options.params) {
    const query = new URLSearchParams(
      Object.entries(options.params)
        .filter(([_, v]) => v !== undefined && v !== null)
        .map(([k, v]) => [k, String(v)])
    ).toString();
    if (query) url += `?${query}`;
  }

  const res = await fetch(url, {
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