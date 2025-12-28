import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useLocalSearchParams, useNavigation} from 'expo-router';
import { useEffect, useState } from 'react';
import { LightPollutionData, Site } from '../../lib/types';
import { getLightPollution } from '../../lib/lightPollution';

export default function SiteDetailScreen() {
  const API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL;

  if (!API_URL) {
    throw new Error('EXPO_PUBLIC_BACKEND_API_URL is not set');
  }
  const { id } = useLocalSearchParams<{ id: string }>();
  const [site, setSite] = useState<Site | null>(null);
  const [lightPollution, setLightPollution] = useState<LightPollutionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigation = useNavigation();


useEffect(() => {
  async function fetchSite() {
    if (!id) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/site/${id}`);
      if (!res.ok) throw new Error('Failed to fetch site');
      const data = await res.json();
      setSite(data);
      navigation.setOptions({ title: data.name });
      setError(null);

      // Call getLightPollution after site is fetched
      const lp = await getLightPollution(data.latitude, data.longitude);
      setLightPollution(lp);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }
  fetchSite();
}, [id, navigation]);

  if (loading) return <ActivityIndicator />;
  if (error) return <Text>Error: {error}</Text>;
  if (!site) return <Text>Site not found.</Text>;

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold' }}>{site.name}</Text>
      <Text>Site ID: {site.id}</Text>
      <Text>Description: {site.description}</Text>
      <Text>Latitude: {site.latitude}</Text>
      <Text>Light Pollution</Text>
      <Text>Zone: {lightPollution?.lpZone ?? 'N/A'}</Text>
      <Text>Index: {lightPollution?.lpIndex?.toFixed(3) ?? 'N/A'}</Text>
      <Text>mag/arcsec²: {lightPollution?.magArcSec?.toFixed(2) ?? 'N/A'}</Text>
      {/* Add more fields as needed */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
});
