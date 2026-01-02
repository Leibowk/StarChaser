// SearchPanel.tsx
import React, { useState, useEffect } from 'react';
import { View, TextInput, Text, Button, StyleSheet, Alert, StatusBar } from 'react-native';
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

  // Request location permission once
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
      debugger;
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

    const params: SearchParams = {
      name: name.trim() || undefined,
      lat,
      lon,
      radius_km: radiusKm ? parseFloat(radiusKm) : undefined,
      site_visib: siteVisib,
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
      />

      <View style={styles.row}>
        <Text>Search near my location:</Text>
        <Button
          title={useLocation ? 'Yes' : 'No'}
          onPress={() => setUseLocation((prev) => !prev)}
        />
      </View>

      <Text style={styles.label}>Radius (km):</Text>
      <TextInput
        style={styles.input}
        value={radiusKm}
        onChangeText={setRadiusKm}
        keyboardType="numeric"
      />

      <Text style={styles.label}>Visibility rating:</Text>
      <Picker
        selectedValue={siteVisib}
        onValueChange={(value: VisibilityOption) => setSiteVisib(value)}
      >
        {VISIBILITY_OPTIONS.map((opt) => (
          <Picker.Item
            key={opt}
            label={opt}
            value={opt}
          />
        ))}
      </Picker>

      <Button title="Search" onPress={handleSearch} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { padding: 16, backgroundColor: '#fff', paddingTop: StatusBar.currentHeight ? StatusBar.currentHeight + 16 : 48, },
  label: { fontWeight: 'bold', marginTop: 12 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    borderRadius: 6,
    marginTop: 4,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginVertical: 12,
  },
  picker: { height: 50, width: '100%' },
});
