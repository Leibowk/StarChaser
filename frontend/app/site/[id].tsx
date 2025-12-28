import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useLocalSearchParams} from 'expo-router';
import { useEffect, useState } from 'react';

type Site = {
  id: number;
  name: string;
  description: string;
  latitude: number;
  longitude: number;
};

export default function SiteDetailScreen() {
  const API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL;

  if (!API_URL) {
    throw new Error('EXPO_PUBLIC_BACKEND_API_URL is not set');
  }
  const { id } = useLocalSearchParams<{ id: string }>();
  const [site, setSite] = useState<Site | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetch(`${API_URL}/site/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch site');
        return res.json();
      })
      .then((data) => {
        setSite(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <ActivityIndicator />;
  if (error) return <Text>Error: {error}</Text>;
  if (!site) return <Text>Site not found.</Text>;

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold' }}>{site.name}</Text>
      <Text>{site.description}</Text>
      <Text>Latitude: {site.latitude}</Text>
      <Text>Longitude: {site.longitude}</Text>
      {/* Add more fields as needed */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
});
