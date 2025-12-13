import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View } from 'react-native';
import { WebView } from 'react-native-webview';
import { useEffect, useState } from 'react';
import { Asset } from 'expo-asset';
import { formatParkPopup } from './parkDetails';
import { fetch } from 'expo/fetch'
import pako from 'pako';

// Calculate centroid of a polygon

const API_URL = "http://192.168.1.17:3000";


export default function App() {
  const [htmlContent, setHtmlContent] = useState('');
  const [parks, setParks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMapData() {
      try {
        const response = await fetch(`${API_URL}/sites`);
        const sites = await response.json();

        const mapped = await Promise.all(
          sites.map(async (site: any) => {
            const lpData = await getLightPollution(site.latitude, site.longitude);

            return {
              name: site.name,
              lat: site.latitude,
              lng: site.longitude,
              detailsHtml: `<h3>${site.name}</h3>
                            <p>${site.description}</p>
                            <b>Light Pollution (LP):</b><br>
                            LP Zone = ${lpData?.lpZone || 'N/A'} █<br>
                            LP Index = ${lpData?.lpIndex?.toFixed(3) || 'N/A'}<br>
                            mag/arcsec² = ${lpData?.magArcSec?.toFixed(2) || 'N/A'}`
            };
          })
        );

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

  async function getLightPollution(lat: number, lng: number) {
      // map lat/lng → tile index
      const lonFromDateLine = (lng + 180) % 360;
      const latFromStart = lat + 65;
      const tileX = Math.floor(lonFromDateLine / 5) + 1;
      const tileY = Math.floor(latFromStart / 5) + 1;

      if(tileY < 1 || tileY > 28) return null;

      // fetch gzip tile from your server
      const response = await fetch(
        `http://192.168.1.17:3000/bi_tiles/binary_tile_${tileX}_${tileY}.dat.gz`,
        { headers: { "Cache-Control": "no-cache" } }
      );
      const buffer = await response.arrayBuffer();
      const dataArray = new Int8Array(pako.ungzip(buffer));

      // compute ix, iy inside tile
      const ix = Math.round(120*(lonFromDateLine - 5*(tileX-1) + 1/240));
      const iy = Math.round(120*(latFromStart - 5*(tileY-1) + 1/240));

      // decode compressed value
      let firstNumber = 128*dataArray[0] + dataArray[1];
      let change = 0;
      for(let i=1; i<iy; i++) change += dataArray[600*i+1];
      for(let i=1; i<ix; i++) change += dataArray[600*(iy-1)+1+i];
      const compressed = firstNumber + change;

      const lpIndex = (5/195) * (Math.exp(0.0195*compressed) - 1);
      const magArcSec = 22 - 5 * Math.log(1+lpIndex)/Math.log(100);

      // simple LP Zone mapping
      let lpZone = '1a';
      if(lpIndex > 0.03) lpZone = '2'; // adapt thresholds

      return { lpIndex, magArcSec, lpZone };
  }


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
