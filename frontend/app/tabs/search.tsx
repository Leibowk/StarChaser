// app/search.tsx
import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, Text, TouchableOpacity, ImageBackground, ActivityIndicator } from 'react-native';
import { SearchPanel, SearchParams } from '../../webviews/SearchPanel';
import { Site } from '../../lib/types';
import apiFetch from '../../lib/api';
import { mapApiSiteToSiteSummary } from '../../lib/typeMapper';
import { useRouter } from 'expo-router';

const PAGE_SIZE = 25;

export default function SearchScreen() {
  const [results, setResults] = useState<Site[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [searchTime, setSearchTime] = useState<string | undefined>(undefined);
  const [searchParams, setSearchParams] = useState<SearchParams | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);
  const router = useRouter();

  const buildQuery = useCallback(
    (params: SearchParams, off: number) => {
      const base: Record<string, string> = {
        lat: String(params.lat),
        lon: String(params.lon),
        drive_time: String(params.drive_time),
        limit: String(PAGE_SIZE),
        offset: String(off),
        order_by: params.order_by ?? 'Visibility',
      };
      if (params.name) base.name = params.name;
      if (params.visib && params.visib !== 'Any') base.visib = params.visib;
      if (params.time) base.time = params.time;
      return new URLSearchParams(base).toString();
    },
    []
  );

  const handleSearch = useCallback(
    async (params: SearchParams, appendOffset?: number) => {
      setSearchTime(params.time);
      const isAppend = appendOffset !== undefined;
      const nextOffset = isAppend ? appendOffset : 0;

      if (isAppend) {
        if (loadingMore || !hasMore || !searchParams) return;
        setLoadingMore(true);
      } else {
        setSearchParams(params);
        setOffset(0);
        setHasMore(true);
        setLoading(true);
      }

      try {
        const query = buildQuery(params, nextOffset);
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

        if (isAppend) {
          setResults((prev) => [...prev, ...enriched]);
          setOffset(nextOffset + enriched.length);
        } else {
          setResults(enriched);
          setOffset(enriched.length);
        }
        setHasMore(enriched.length >= PAGE_SIZE);
      } finally {
        setLoading(false);
        setLoadingMore(false);
      }
    },
    [hasMore, searchParams, loadingMore, buildQuery]
  );

  const loadMore = useCallback(() => {
    if (searchParams && hasMore && !loading && !loadingMore) {
      handleSearch(searchParams, offset);
    }
  }, [searchParams, hasMore, loading, loadingMore, offset, handleSearch]);

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
          onEndReached={loadMore}
          onEndReachedThreshold={0.5}
          ListFooterComponent={
            loadingMore ? (
              <View style={styles.footerLoader}>
                <ActivityIndicator size="small" color="#FFD700" />
              </View>
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
                <SearchPanel onSearch={(params) => handleSearch(params)} />
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
  footerLoader: {
    paddingVertical: 16,
    alignItems: 'center',
  },
});