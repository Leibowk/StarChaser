import React, { useState, useEffect } from 'react';
import { View, TextInput, Text, Button, StyleSheet, Alert } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import * as Location from 'expo-location';

export type SearchParams = {
  name?: string;
  lat?: number;
  lon?: number;
  radius_km?: number;
  site_visib?: string;
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

  useEffect(() => {
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      setLocationGranted(status === 'granted');
    })();
  }, []);

  const handleSearch = async () => {
    let lat: number | undefined;
    let lon: number | undefined;

    if (useLocation) {
      if (!locationGranted) {
        Alert.alert(
          'Location required',
          'Please enable location permission to search nearby.'
        );
        return;
      }

      const current = await Location.getCurrentPositionAsync({});
      lat = current.coords.latitude;
      lon = current.coords.longitude;
    }

    // Build search params
    const params: SearchParams = {
      name: name.trim() || undefined,
      lat,
      lon,
      site_visib: siteVisib !== 'Any' ? siteVisib : undefined,
      ...(useLocation ? { radius_km: radiusKm ? parseFloat(radiusKm) : undefined } : {}),
    };

    onSearch(params);
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
      <Picker
        selectedValue={siteVisib}
        onValueChange={(value: VisibilityOption) => setSiteVisib(value)}
        style={styles.picker}
      >
        {VISIBILITY_OPTIONS.map((opt) => (
          <Picker.Item key={opt} label={opt} value={opt} />
        ))}
      </Picker>

      <Button title="Search" onPress={handleSearch} />
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
});
