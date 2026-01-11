import React, { useState, useEffect } from 'react';
import { View, TextInput, Text, Button, StyleSheet, Alert, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import * as Location from 'expo-location';
import { TIME_OPTIONS } from '../lib/types';

export type SearchParams = {
  name?: string;
  lat?: number;
  lon?: number;
  drive_time?: number;
  visib?: string;
  time?: string;
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
type TimeOption = typeof TIME_OPTIONS[number];

export const SearchPanel = ({ onSearch }: Props) => {
  const [name, setName] = useState('');
  const [useLocation, setUseLocation] = useState(true);
  const [driveTime, setDriveTime] = useState('60');
  const [siteVisib, setSiteVisib] = useState<VisibilityOption>('Any');
  const [timeVisibility, setTimeVisibility] = useState<TimeOption>('Tonight');
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
      time: timeVisibility,
      ...(useLocation && lat != null && lon != null ? { drive_time: parseFloat(driveTime) } : {}),
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
          <Text style={styles.label}>Drive Time (minutes):</Text>
          <TextInput
            style={styles.input}
            value={driveTime}
            onChangeText={setDriveTime}
            keyboardType="numeric"
            placeholder="Enter drive time in minutes"
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
        dropdownIconColor="#FFD700"
      >
        {VISIBILITY_OPTIONS.map((opt) => (
          <Picker.Item key={opt} label={opt} value={opt} color="#FFD700" />
        ))}
      </Picker>

      <Text style={styles.label}>Time window:</Text>
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
    color: '#FFD700', // text color
    backgroundColor: 'rgba(255,255,255,0.1)', // subtle dark background
    marginBottom: 12,
    borderRadius: 6, 
    paddingHorizontal: 8,
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
