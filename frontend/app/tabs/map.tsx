import { View, StyleSheet } from 'react-native';
import { useCallback, useEffect, useState, useRef } from 'react';
import { Site } from '../../lib/types';
import { MapWebView } from '../../webviews/MapWebView';
import apiFetch from '../../lib/api';
import { mapApiSiteToSite } from '../../lib/typeMapper';

export const DEFAULT_VIEW = { lat: 48.75, lon: -122.52, zoom: 9 };

const VIEW_TOLERANCE = 0.0001;

function viewsMatch(a: { lat: number; lon: number; zoom: number }, b: { lat: number; lon: number; zoom: number }) {
  return (
    Math.abs(a.lat - b.lat) < VIEW_TOLERANCE &&
    Math.abs(a.lon - b.lon) < VIEW_TOLERANCE &&
    a.zoom === b.zoom
  );
}

export default function MapScreen() {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [mapView, setMapView] = useState(DEFAULT_VIEW);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const lastFetchedViewRef = useRef<{ lat: number; lon: number; zoom: number } | null>(null);

  const fetchSites = useCallback(async (lat: number, lon: number, zoom: number) => {
    const view = { lat, lon, zoom };
    if (lastFetchedViewRef.current && viewsMatch(lastFetchedViewRef.current, view)) {
      return;
    }
    lastFetchedViewRef.current = view;
    try {
      setLoading(true);
      const rawSites = await apiFetch(`/sites?lat=${lat}&lon=${lon}&zoom=${zoom}&limit=50`);
      const enriched: Site[] = rawSites.map((site: any) => mapApiSiteToSite(site));
      setSites(enriched);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSites(DEFAULT_VIEW.lat, DEFAULT_VIEW.lon, DEFAULT_VIEW.zoom);
  }, [fetchSites]);

  const handleViewChange = useCallback(
    (lat: number, lon: number, zoom: number) => {
      setMapView({ lat, lon, zoom });
      if (debounceRef.current) clearTimeout(debounceRef.current);
      debounceRef.current = setTimeout(() => {
        debounceRef.current = null;
        fetchSites(lat, lon, zoom);
      }, 400);
    },
    [fetchSites]
  );

  if (loading && sites.length === 0) return <View style={{ flex: 1 }} />;

  return (
    <View style={styles.container}>
      <MapWebView sites={sites} initialView={mapView} onViewChange={handleViewChange} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 }
});
