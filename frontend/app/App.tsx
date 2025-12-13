import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View } from 'react-native';
import { WebView } from 'react-native-webview';
import { useEffect, useState } from 'react';
import { Asset } from 'expo-asset';
import { formatParkPopup } from './parkDetails';
import { fetch } from 'expo/fetch'

// Calculate centroid of a polygon

const API_URL = "http://192.168.1.17:3000";

function calculateCentroid(coordinates: number[][][]): [number, number] {
  let x = 0;
  let y = 0;
  let count = 0;
  
  // Flatten all coordinates
  for (const ring of coordinates) {
    for (const coord of ring) {
      x += coord[0];
      y += coord[1];
      count++;
    }
  }
  
  return [x / count, y / count];
}

// Calculate centroid for MultiPolygon or Polygon geometry
function getFeatureCenter(feature: any): [number, number] | null {
  const geom = feature.geometry;
  if (geom.type === 'Polygon') {
    return calculateCentroid(geom.coordinates);
  } else if (geom.type === 'MultiPolygon') {
    // Use the first polygon for simplicity
    return calculateCentroid(geom.coordinates[0]);
  }
  return null;
}

export default function App() {
  const [htmlContent, setHtmlContent] = useState('');
  const [parks, setParks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMapData() {
      try {
        const response = await fetch(`${API_URL}/sites`);
        const sites = await response.json();

        const mapped = sites.map((site: any) => ({
          name: site.name,
          lat: site.latitude,
          lng: site.longitude,
          detailsHtml: `<h3>${site.name}</h3><p>${site.description}</p>`
        }));

        setParks(mapped);

        const asset = Asset.fromModule(require('./map.html'));
        await asset.downloadAsync();
        const html = await (await fetch(asset.uri)).text();

        setHtmlContent(html);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }

    loadMapData();
  }, []);

  if (loading) return <View style={{ flex: 1 }} />;

  return (
    <View style={styles.container}>
      <WebView
        source={{ html: htmlContent }}
        injectedJavaScript={`
          window.PARKS_DATA = ${JSON.stringify(parks)};
          if (window.renderParks) {
            window.renderParks(window.PARKS_DATA);
          }
          true;
        `}
        javaScriptEnabled
        domStorageEnabled
        style={styles.webview}
      />
      <StatusBar style="auto" />
    </View>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  webview: {
    flex: 1,
  },
});
