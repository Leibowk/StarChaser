import React, { useState, useEffect } from 'react';
import { View, TextInput, Text, Button, StyleSheet, Alert, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import * as Location from 'expo-location';

export type SearchParams = {
  name?: string;
  lat?: number;
  lon?: number;
  radius_km?: number;
  visib?: string;
};

type Props = {
  onSearch: (params: SearchParams) => void;
};

const VISIBILITY_OPTIONS = [
  'Any',
  'Perfect',
  'Amazing',
  'Great',
  'Good',
  'Ok',
  'Bad',
  'Terrible',
] as const;

type VisibilityOption = typeof VISIBILITY_OPTIONS[number];

export const SearchPanel = ({ onSearch }: Props) => {
  const [name, setName] = useState('');
  const [useLocation, setUseLocation] = useState(false);
  const [radiusKm, setRadiusKm] = useState('50');
  const [siteVisib, setSiteVisib] = useState<VisibilityOption>('Any');
  const [locationGranted, setLocationGranted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [cachedLocation, setCachedLocation] = useState<{lat:number, lon:number} | null>(null);
  useEffect(() => {
    if (useLocation && !cachedLocation && locationGranted) {
    Location.getCurrentPositionAsync({}).then(loc => {
      setCachedLocation({ lat: loc.coords.latitude, lon: loc.coords.longitude });
    }).catch(err => console.warn(err));
  }
}, [useLocation, locationGranted]);

  const handleSearch = async () => {
    if (loading) return; // prevent double taps
    setLoading(true);

    let lat: number | undefined;
    let lon: number | undefined;

    if (useLocation) {
      try {
        const { status } = await Location.getForegroundPermissionsAsync();
        if (status !== 'granted') {
          Alert.alert('Location required', 'Please enable location permission to search nearby.');
        } else {
          // fetch location if not cached
          if (cachedLocation) {
            lat = cachedLocation.lat;
            lon = cachedLocation.lon;
          } else {
            const current = await Location.getCurrentPositionAsync({});
            lat = current.coords.latitude;
            lon = current.coords.longitude;
            setCachedLocation({ lat, lon }); // cache for next time
          }
        }
      } catch (err) {
        console.warn('Location fetch failed', err);
        Alert.alert('Error', 'Could not get your current location.');
      }
    }

    const params: SearchParams = {
      name: name.trim() || undefined,
      lat,
      lon,
      visib: siteVisib !== 'Any' ? siteVisib : undefined,
      ...(useLocation && lat != null && lon != null ? { radius_km: parseFloat(radiusKm) } : {}),
    };

    try {
      await onSearch(params); // await backend call
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Search by name:</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
        placeholder="Enter site name"
        placeholderTextColor="#ccc"
      />

      <View style={styles.row}>
        <Text style={styles.label}>Search near my location:</Text>
        <Button
          title={useLocation ? 'Yes' : 'No'}
          onPress={() => setUseLocation((prev) => !prev)}
        />
      </View>

      {useLocation && (
        <>
          <Text style={styles.label}>Radius (km):</Text>
          <TextInput
            style={styles.input}
            value={radiusKm}
            onChangeText={setRadiusKm}
            keyboardType="numeric"
            placeholder="Enter radius in km"
            placeholderTextColor="#ccc"
          />
        </>
      )}

      <Text style={styles.label}>Visibility rating:</Text>
      <Text style={styles.subLabel}>(returns all sites better than selected Visibility)</Text>
      <Picker
        selectedValue={siteVisib}
        onValueChange={(value: VisibilityOption) => setSiteVisib(value)}
        style={styles.picker}
      >
        {VISIBILITY_OPTIONS.map((opt) => (
          <Picker.Item key={opt} label={opt} value={opt} />
        ))}
      </Picker>

      
      <TouchableOpacity
        onPress={handleSearch}
        activeOpacity={0.6} // decreases opacity when pressed
        style={styles.searchButton}
        disabled={loading} // disable while searching
      >
        <Text style={styles.searchButtonText}>{loading ? 'Searching...' : 'Search'}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: 'rgba(10, 10, 30, 0.75)',
    borderRadius: 12,
    marginBottom: 16,
  },
  label: { fontWeight: 'bold', color: '#FFD700', marginTop: 12 },
  subLabel: {
    fontSize: 12,         // smaller than main label
    fontStyle: 'italic',  // italic
    color: '#FFD700',     // optional, same color or slightly dimmer
    marginTop: 2,         // small gap to main label
    marginBottom: 6,      // optional: spacing before next input
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    borderRadius: 6,
    marginTop: 4,
    color: '#fff',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginVertical: 12,
  },
  picker: { 
    height: 60, 
    width: '100%', 
    color: '#fff', 
    backgroundColor: 'rgba(255,255,255,0.1)',
    marginBottom: 12, 
  },
  searchButton: {
    backgroundColor: '#FFD700',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 16,
  },
  searchButtonText: {
    color: '#000',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
