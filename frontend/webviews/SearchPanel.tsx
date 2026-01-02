// SearchPanel.tsx
import React, { useState, useEffect } from 'react';
import { View, TextInput, Text, Button, StyleSheet, Alert, Switch } from 'react-native';
import * as Location from 'expo-location';

export type SearchParams = {
  name?: string;
  lat?: number;
  lon?: number;
  radius_km?: number;
  site_visib?: boolean;
};

type Props = {
  onSearch: (params: SearchParams) => void;
};

export const SearchPanel = ({ onSearch }: Props) => {
  const [name, setName] = useState('');
  const [useLocation, setUseLocation] = useState(false);
  const [radiusKm, setRadiusKm] = useState('50');
  const [siteVisib, setSiteVisib] = useState(false);
  const [locationGranted, setLocationGranted] = useState(false);

  // Request location permission once
  useEffect(() => {
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      setLocationGranted(status === 'granted');
    })();
  }, []);

  const handleSearch = async () => {
    debugger;
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

    // Build params in the format expected by your API
    const params: SearchParams = {
      name: name.trim() || undefined,
      lat,
      lon,
      radius_km: radiusKm ? parseFloat(radiusKm) : undefined,
      site_visib: siteVisib || undefined
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
        <Switch value={useLocation} onValueChange={setUseLocation} />
      </View>

      <Text style={styles.label}>Radius (km):</Text>
      <TextInput
        style={styles.input}
        value={radiusKm}
        onChangeText={setRadiusKm}
        keyboardType="numeric"
      />

      <View style={styles.row}>
        <Text>Only visible sites:</Text>
        <Switch value={siteVisib} onValueChange={setSiteVisib} />
      </View>

      <Button title="Search" onPress={handleSearch} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { padding: 16, backgroundColor: '#fff' },
  label: { fontWeight: 'bold', marginTop: 12 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    borderRadius: 6,
    marginTop: 4
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginVertical: 12
  }
});
