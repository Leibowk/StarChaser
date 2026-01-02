// app/search.tsx
import React, { useState } from 'react';
import { View, StyleSheet, FlatList, Text, TouchableOpacity } from 'react-native';
import { SearchPanel, SearchParams } from '../../webviews/SearchPanel';
import { Site } from '../../lib/types';
import apiFetch from '../../lib/api';
import { mapApiSiteToSiteSummary } from '../../lib/typeMapper';
import { useRouter } from 'expo-router';

export default function SearchScreen() {
  const [results, setResults] = useState<Site[]>([]);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSearch = async (params: SearchParams) => {
    setLoading(true);
    try {
      // Build query string
      const query = new URLSearchParams({
        ...(params.name ? { name: params.name } : {}),
        ...(params.lat !== undefined ? { lat: String(params.lat) } : {}),
        ...(params.lon !== undefined ? { lon: String(params.lon) } : {}),
        ...(params.radius_km !== undefined ? { radius_km: String(params.radius_km) } : {}),
        ...(params.site_visib ? { site_visib: 'true' } : {}),
      }).toString();

      const rawResults = await apiFetch(`/sites/search?${query}`);
      const enriched: Site[] = rawResults.map((site: any) => {
        const mapped = mapApiSiteToSiteSummary(site);
        return {
          id: mapped.id,
          name: mapped.name,
          description: mapped.description,
          latitude: mapped.latitude,
          longitude: mapped.longitude,
          lightPollution: mapped.lightPollution ?? undefined,
        };
      });

      setResults(enriched);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <SearchPanel onSearch={handleSearch} />

      <FlatList
        data={results}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() => router.push(`/site/${item.id}`)}
            style={styles.item}
          >
            <Text style={styles.title}>{item.name}</Text>
            <Text style={styles.desc}>{item.description}</Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={() => (
          !loading ? (
            <Text style={styles.emptyText}>
              No results. Try adjusting your search criteria.
            </Text>
          ) : null
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  item: { padding: 12, borderBottomWidth: 1, borderBottomColor: '#ccc' },
  title: { fontWeight: 'bold', fontSize: 16 },
  desc: { marginTop: 4, color: '#555' },
  emptyText: { textAlign: 'center', marginTop: 20, color: '#888' },
});
