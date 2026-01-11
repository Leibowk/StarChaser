// app/search.tsx
import React, { useState } from 'react';
import { View, StyleSheet, FlatList, Text, TouchableOpacity, ImageBackground, ScrollView } from 'react-native';
import { SearchPanel, SearchParams } from '../../webviews/SearchPanel';
import { Site } from '../../lib/types';
import apiFetch from '../../lib/api';
import { mapApiSiteToSiteSummary } from '../../lib/typeMapper';
import { useRouter } from 'expo-router';

export default function SearchScreen() {
  const [results, setResults] = useState<Site[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTime, setSearchTime] = useState<string | undefined>(undefined);
  const router = useRouter();

  const handleSearch = async (params: SearchParams) => {
    setLoading(true);
    setSearchTime(params.time);
    try {
      // Build query string
      const query = new URLSearchParams({
        ...(params.name ? { name: params.name } : {}),
        ...(params.lat !== undefined ? { lat: String(params.lat) } : {}),
        ...(params.lon !== undefined ? { lon: String(params.lon) } : {}),
        ...(params.drive_time !== undefined ? { drive_time: String(params.drive_time) } : {}),
        ...(params.visib ? params.visib === 'Any' ? { visib: 'Terrible' } : { visib: String(params.visib) } : {}),
        ...(params.time !== undefined ? { time: String(params.time) } : {}),
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
      <ImageBackground
        source={require('../../assets/milk_way_galaxy.png')}
        style={styles.background}
        imageStyle={{ opacity: 0.5 }}
        resizeMode="cover"
      >
        <FlatList
          data={results}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <TouchableOpacity
              onPress={() =>
                router.push({
                  pathname: `/site/${item.id}`,
                  params: { time: searchTime },
                })
              }
              style={styles.itemCard}
            >
              <Text style={styles.itemTitle}>{item.name}</Text>
              <Text style={styles.itemDesc}>{item.description}</Text>
            </TouchableOpacity>
          )}
          ListEmptyComponent={() =>
            !loading ? (
              <Text style={styles.emptyText}>
                No results. Try adjusting your search criteria.
              </Text>
            ) : null
          }
          contentContainerStyle={{
            paddingTop: 60,
            paddingHorizontal: 16,
            paddingBottom: 40,
          }}
          ListHeaderComponent={
            <>
              <Text style={styles.pageTitle}>Search Sites</Text>
              <View style={styles.searchCard}>
                <SearchPanel onSearch={handleSearch} />
              </View>
            </>
          }
        />
      </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: { flex: 1 },
  scrollContainer: {
    paddingTop: 60, // move everything down from status bar
    paddingHorizontal: 16,
    paddingBottom: 20,
  },
  pageTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFD700',
    textAlign: 'center',
    marginBottom: 16,
    textShadowColor: '#000',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 6,
  },
  searchCard: {
    backgroundColor: 'rgba(10, 10, 30, 0.75)',
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
  },
  itemCard: {
    backgroundColor: 'rgba(10, 10, 30, 0.75)',
    borderRadius: 16,
    padding: 16,
    marginVertical: 8,
  },
  itemTitle: { fontWeight: 'bold', fontSize: 16, color: '#FFD700' },
  itemDesc: { color: '#fff', marginTop: 4 },
  emptyText: { marginTop: 16, color: '#FFD700', textAlign: 'center' },
});