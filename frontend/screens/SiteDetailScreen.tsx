import { View, Text, StyleSheet } from 'react-native';
import { getCurrentSite } from '../lib/SiteStore';

export default function SiteDetailScreen() {
  const site = getCurrentSite();

  if (!site) return (
    <View style={styles.container}>
      <Text>No site selected.</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{site.name}</Text>
      <Text>{site.description}</Text>
      <Text>LP Zone: {site.lightPollution?.lpZone ?? 'N/A'}</Text>
      <Text>LP Index: {site.lightPollution?.lpIndex?.toFixed(3) ?? 'N/A'}</Text>
      <Text>Mag/arcsec²: {site.lightPollution?.magArcSec?.toFixed(2) ?? 'N/A'}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
});
