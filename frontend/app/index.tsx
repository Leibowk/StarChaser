import { View, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';
import { fetch } from 'expo/fetch';
import { Site } from '../lib/types';
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
            //small hack for now to fix mappings.
            const mapped: Site = {
              ...site,
              lightPollution: site.light_pollution && {
                lpIndex: site.light_pollution.lp_index,
                magArcSec: site.light_pollution.mag_arcsec,
                lpZone: site.light_pollution.lp_zone,
                colorZone: site.light_pollution.color_zone,
              },
            };

            return {
              id: mapped.id,
              name: mapped.name,
              description: mapped.description,
              latitude: mapped.latitude,
              longitude: mapped.longitude,
              lightPollution: mapped.lightPollution ?? undefined
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
