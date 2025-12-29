import { View, Text, StyleSheet, ActivityIndicator, ImageBackground } from 'react-native';
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
    <ImageBackground
      source={require('../../assets/milk_way_galaxy.png')}
      style={styles.background}
      imageStyle={{ opacity: 0.5 }}
      resizeMode="cover"
    >
      <View style={styles.overlay}>
        <Text style={styles.title}>{site.name}</Text>
        <Text style={styles.label}>Site ID: <Text style={styles.value}>{site.id}</Text></Text>
        <Text style={styles.label}>Description: <Text style={styles.value}>{site.description}</Text></Text>
        <Text style={styles.label}>Latitude: <Text style={styles.value}>{site.latitude}</Text></Text>
        <Text style={styles.label}>Longitude: <Text style={styles.value}>{site.longitude}</Text></Text>
        <Text style={styles.section}>Light Pollution</Text>
        <Text style={styles.label}>Zone: <Text style={styles.value}>{lightPollution?.lpZone ?? 'N/A'}</Text></Text>
        <Text style={styles.label}>Index: <Text style={styles.value}>{lightPollution?.lpIndex?.toFixed(3) ?? 'N/A'}</Text></Text>
        <Text style={styles.label}>mag/arcsec²: <Text style={styles.value}>{lightPollution?.magArcSec?.toFixed(2) ?? 'N/A'}</Text></Text>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: {     
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 18,
    textShadowColor: '#000',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 6,
    textAlign: 'center',},
    background: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(10, 10, 30, 0.7)',
    padding: 24,
    justifyContent: 'center',
  },
  section: {
    fontSize: 22,
    color: '#FFD700',
    fontWeight: 'bold',
    marginTop: 18,
    marginBottom: 8,
    textShadowColor: '#000',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 4,
  },
  label: {
    fontSize: 18,
    color: '#B0C4DE',
    marginBottom: 4,
  },
  value: {
    color: '#fff',
    fontWeight: '600',
  },
  errorText: {
    color: '#ff6666',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 40,
  },
});
