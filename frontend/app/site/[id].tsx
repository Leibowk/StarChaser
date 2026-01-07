import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  ImageBackground,
  ScrollView,
} from 'react-native';
import { useLocalSearchParams, useNavigation} from 'expo-router';
import { useEffect, useState } from 'react';
import { Site, TIME_OPTIONS } from '../../lib/types';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import apiFetch from '../../lib/api';
import { mapApiSiteToSite } from '../../lib/typeMapper';
import { Picker } from '@react-native-picker/picker';


type TimeOption = typeof TIME_OPTIONS[number];

export default function SiteDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [site, setSite] = useState<Site | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeVisibility, setTimeVisibility] = useState<TimeOption>('Tonight');
  const navigation = useNavigation();
  const insets = useSafeAreaInsets();

useEffect(() => {
  async function fetchSite() {
    if (!id) return;
    setLoading(true);
    try {
      const data = await apiFetch(`/site/${id}?time=${encodeURIComponent(timeVisibility)}`);
      setSite(mapApiSiteToSite(data));
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }
  fetchSite();
}, [id, navigation, timeVisibility]);

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
    <ScrollView
    contentContainerStyle={[
      styles.scrollContent,
      { paddingTop: insets.top + 16, paddingBottom: insets.bottom + 16 },
    ]}
    showsVerticalScrollIndicator={false}
  >
        <View style={styles.card}>
          <Text style={styles.title}>{site.name}</Text>

          <Text style={styles.labelPicker}>Time window:</Text>
          <Text style={styles.subLabel}>(used to evaluate site visibility)</Text>
          <Picker
            selectedValue={timeVisibility}
            onValueChange={(value: TimeOption) => setTimeVisibility(value)}
            style={styles.picker}
            dropdownIconColor="#FFD700"
          >
            {TIME_OPTIONS.map((opt) => (
              <Picker.Item key={opt} label={opt} value={opt} color="#FFD700" />
            ))}
          </Picker>

          <Text style={styles.section}>Site Visibility</Text>
          <Text style={styles.label}>
            Conditions: <Text style={styles.value}>{site.visibility?.category ?? 'N/A'}</Text>
          </Text>
          <Text style={styles.label}>
            Score: <Text style={styles.value}>{site.visibility?.score ?? 'N/A'}</Text>
          </Text>

          <Text style={styles.section}>Light Pollution</Text>
          <Text style={styles.label}>
            Zone: <Text style={styles.value}>{site.visibility?.lightPollution?.lpZone ?? 'N/A'}</Text>
          </Text>
          <Text style={styles.label}>
            Index:{' '}
            <Text style={styles.value}>
              {site.visibility?.lightPollution?.lpIndex?.toFixed(3) ?? 'N/A'}
            </Text>
          </Text>
          <Text style={styles.label}>
            mag/arcsec²:{' '}
            <Text style={styles.value}>
              {site.visibility?.lightPollution?.magArcSec?.toFixed(2) ?? 'N/A'}
            </Text>
          </Text>

          <Text style={styles.section}>Current Weather</Text>
          <Text style={styles.label}>
            Condition:{' '}
            <Text style={styles.value}>{site.visibility?.weather?.condition ?? 'N/A'}</Text>
          </Text>
          <Text style={styles.label}>
            Cloud Coverage:{' '}
            <Text style={styles.value}>
              {site.visibility?.weather?.cloudCoverage ?? 'N/A'}%
            </Text>
          </Text>
          <Text style={styles.label}>
            Visibility:{' '}
            <Text style={styles.value}>
              {site.visibility?.weather?.avgvisKm ?? 'N/A'} km /{' '}
              {site.visibility?.weather?.avgvisMiles ?? 'N/A'} miles
            </Text>
          </Text>
          <Text style={styles.label}>
            AQI: <Text style={styles.value}>{site.visibility?.weather?.aqi ?? 'N/A'}</Text>
          </Text>

          <Text style={styles.section}>Site Information</Text>
          <Text style={styles.label}>
            Site ID: <Text style={styles.value}>{site.id}</Text>
          </Text>
          <Text style={styles.label}>
            Description: <Text style={styles.value}>{site.description}</Text>
          </Text>
          <Text style={styles.label}>
            Latitude: <Text style={styles.value}>{site.latitude}</Text>
          </Text>
          <Text style={styles.label}>
            Longitude: <Text style={styles.value}>{site.longitude}</Text>
          </Text>
        </View>
      </ScrollView>
  </ImageBackground>
);
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
  },

  safeArea: {
    flex: 1,
  },

  scrollContent: {
    paddingHorizontal: 16,
    alignItems: 'center',
  },
  subLabel: {
    fontSize: 12,         // smaller than main label
    fontStyle: 'italic',  // italic
    color: '#FFD700',     // optional, same color or slightly dimmer
    marginTop: 2,         // small gap to main label
    marginBottom: 6,      // optional: spacing before next input
  },

  picker: { 
    height: 60, 
    width: '100%', 
    color: '#FFD700', // text color
    backgroundColor: 'rgba(255,255,255,0.1)', // subtle dark background
    marginBottom: 12,
    borderRadius: 6, 
    paddingHorizontal: 8,
  },

  card: {
    width: '100%',
    maxWidth: 520,
    backgroundColor: 'rgba(10, 10, 30, 0.75)',
    borderRadius: 16,
    padding: 24,
  },

  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 20,
    textAlign: 'center',
    textShadowColor: '#000',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 6,
  },

  section: {
    fontSize: 22,
    color: '#FFD700',
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 8,
  },

  labelPicker: { fontWeight: 'bold', color: '#FFD700', marginTop: 12 },

  label: {
    fontSize: 18,
    color: '#B0C4DE',
    marginBottom: 6,
  },

  value: {
    color: '#fff',
    fontWeight: '600',
  },
});
