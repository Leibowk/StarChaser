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
  const [htmlContent, setHtmlContent] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMapData() {
      try {

        // how do I connect to my server? 
        let response = await fetch(`${API_URL}/sites`);
        let sites = await response.json();

        const parks = sites.map((site: any) => ({
          name: site.name,
          coordinates: [site.longitude, site.latitude], // maplibre uses [lng, lat]
          detailsHtml: `<h3>${site.name}</h3><p>${site.description}</p>`
        }));

        // Generate HTML with map and markers
        const html = `
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href='https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css' rel='stylesheet' />
    <script src='https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js'></script>
    <style>
        body { margin: 0; padding: 0; }
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        const map = new maplibregl.Map({
            container: 'map',
            style: {
                version: 8,
                sources: {
                    'raster-tiles': {
                        type: 'raster',
                        tiles: [
                            'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
                        ],
                        tileSize: 256,
                        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }
                },
                layers: [
                    {
                        id: 'simple-tiles',
                        type: 'raster',
                        source: 'raster-tiles',
                        minzoom: 0,
                        maxzoom: 22
                    }
                ]
            },
            center: [-122.519, 48.755],
            zoom: 10
        });
        
        map.addControl(new maplibregl.NavigationControl());
        map.addControl(new maplibregl.ScaleControl(), 'bottom-left');
        
        // Wait for map to load
        map.on('load', function() {
      // Parks data
      const parks = ${JSON.stringify(parks)};

      // Add source with park points
      map.addSource('parks', {
        'type': 'geojson',
        'data': {
          'type': 'FeatureCollection',
          'features': parks.map(park => ({
            'type': 'Feature',
            'geometry': {
              'type': 'Point',
              'coordinates': park.coordinates
            },
            'properties': {
              'name': park.name,
              'detailsHtml': park.detailsHtml
            }
          }))
        }
      });

      // Use a circle layer for parks (no external image required)
      map.addLayer({
        id: 'parks',
        type: 'circle',
        source: 'parks',
        paint: {
          'circle-radius': 6,
          'circle-color': '#2E8B57',
          'circle-stroke-color': '#ffffff',
          'circle-stroke-width': 1
        }
      });
                
                // Add click handler for parks
      map.on('click', 'parks', function(e) {
        const coordinates = e.features[0].geometry.coordinates.slice();
        const html = e.features[0].properties.detailsHtml || ('<strong>' + e.features[0].properties.name + '</strong>');

        new maplibregl.Popup()
          .setLngLat(coordinates)
          .setHTML(html)
          .addTo(map);
      });
                
      // Change cursor on hover
      map.on('mouseenter', 'parks', function() {
        map.getCanvas().style.cursor = 'pointer';
      });

      map.on('mouseleave', 'parks', function() {
        map.getCanvas().style.cursor = '';
      });
        });
    </script>
</body>
</html>
        `;

        setHtmlContent(html);
        setLoading(false);
      } catch (error) {
        console.error('Error loading map data:', error);
        setLoading(false);
      }
    }

    loadMapData();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <StatusBar style="auto" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <WebView
        source={{ html: htmlContent }}
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        allowsInlineMediaPlayback={true}
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