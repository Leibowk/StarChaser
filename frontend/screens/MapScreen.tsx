import { View, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';
import { fetch } from 'expo/fetch';
import { Site } from '../lib/types';
import { getLightPollution } from '../lib/lightPollution';
import { MapWebView } from '../components/MapWebView';

const API_URL = "http://192.168.1.17:3000";

export function MapScreen() {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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
