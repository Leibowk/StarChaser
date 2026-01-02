import { View, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';
import { Site } from '../../lib/types';
import { MapWebView } from '../../webviews/MapWebView';
import apiFetch from '../../lib/api';
import { mapApiSiteToSiteSummary } from '../../lib/typeMapper';

export default function MapScreen() {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);

  // Load all sites initially
  useEffect(() => {
    async function loadAll() {
      try {
        const rawSites = await apiFetch('/sites');
        const enriched: Site[] = rawSites.map((site: any) => {
          const mapped = mapApiSiteToSiteSummary(site);
          return {
            id: mapped.id,
            name: mapped.name,
            description: mapped.description,
            latitude: mapped.latitude,
            longitude: mapped.longitude,
            lightPollution: mapped.lightPollution ?? undefined
          };
        });
        setSites(enriched);
      } finally {
        setLoading(false);
      }
    }
    loadAll();
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
