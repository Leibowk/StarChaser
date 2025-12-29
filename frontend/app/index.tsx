import { View, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';
import { fetch } from 'expo/fetch';
import { Site } from '../lib/types';
import { getLightPollution } from '../lib/lightPollution';
import { MapWebView } from '../webviews/MapWebView';
import { useNavigation } from 'expo-router';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL;

if (!API_URL) {
  throw new Error('EXPO_PUBLIC_BACKEND_API_URL is not set');
}

export default function MapScreen() {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const navigation = useNavigation();
  

  useEffect(() => {
    navigation.setOptions({ title: 'StarChaser' });
    async function load() {
      try {
        const response = await fetch(`${API_URL}/sites`);
        const rawSites = await response.json();

        const enriched: Site[] = await Promise.all(
          rawSites.map(async (site: any) => {
            const lp = await getLightPollution(site.latitude, site.longitude);

            return {
              id: site.id,
              name: site.name,
              description: site.description,
              latitude: site.latitude,
              longitude: site.longitude,
              lightPollution: lp ?? undefined
            };
          })
        );

        setSites(enriched);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  if (loading) return <View style={{ flex: 1 }} />;

  return (
    <View style={styles.container}>
      <MapWebView sites={sites} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 }
});
