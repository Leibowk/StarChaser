import * as Location from 'expo-location';
import { useCallback, useEffect, useRef, useState } from 'react';

export type UserLocation = { lat: number; lon: number };

export async function getPermissionStatus(): Promise<boolean> {
  const { status } = await Location.getForegroundPermissionsAsync();
  return status === 'granted';
}

export async function requestForegroundPermission(): Promise<boolean> {
  const { status } = await Location.requestForegroundPermissionsAsync();
  return status === 'granted';
}

export async function getCurrentLocation(): Promise<UserLocation | null> {
  try {
    const loc = await Location.getCurrentPositionAsync({});
    return { lat: loc.coords.latitude, lon: loc.coords.longitude };
  } catch {
    return null;
  }
}

type UseUserLocationOptions = {
  /** If true, request permission automatically on mount (e.g. for map). Default false. */
  autoRequest?: boolean;
};

export function useUserLocation(options?: UseUserLocationOptions) {
  const [locationGranted, setLocationGranted] = useState(false);
  const [userLocation, setUserLocation] = useState<UserLocation | null>(null);
  const autoRequestAttempted = useRef(false);

  useEffect(() => {
    getPermissionStatus().then(setLocationGranted);
  }, []);

  useEffect(() => {
    if (locationGranted && !userLocation) {
      getCurrentLocation()
        .then((loc) => loc && setUserLocation(loc))
        .catch((err) => console.warn(err));
    }
  }, [locationGranted, userLocation]);

  const requestPermission = useCallback(async () => {
    const granted = await requestForegroundPermission();
    setLocationGranted(granted);
    return granted;
  }, []);

  useEffect(() => {
    if (options?.autoRequest && !locationGranted && !autoRequestAttempted.current) {
      autoRequestAttempted.current = true;
      requestPermission();
    }
  }, [options?.autoRequest, locationGranted, requestPermission]);

  return { locationGranted, userLocation, requestPermission };
}
