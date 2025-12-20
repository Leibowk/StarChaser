import { WebView } from 'react-native-webview';
import { Asset } from 'expo-asset';
import { useEffect, useState } from 'react';
import { Site } from '../lib/types';
import { useRouter } from 'expo-router';
import { setCurrentSite } from '../lib/SiteStore';

type Props = {
  sites: Site[];
};

export function MapWebView({ sites }: Props) {
  const [html, setHtml] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    async function loadHtml() {
      const asset = Asset.fromModule(require('../assets/map.html'));
      await asset.downloadAsync();
      const text = await (await fetch(asset.uri)).text();
      setHtml(text);
    }
    loadHtml();
  }, []);

  const handleMessage = (event: any) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'siteClick' && data.site) {
        setCurrentSite(data.site); // store the site in memory
        router.push('/SiteDetailScreen'); // just navigate to the page
      }
    } catch (e) {
      console.warn('Invalid message from WebView', e);
    }
  };

  if (!html) return null;

  return (
    <WebView
      source={{ html }}
      injectedJavaScript={`
        window.SITES_DATA = ${JSON.stringify(sites)};
        if (window.renderSites) {
          window.renderSites(window.SITES_DATA);
        }
        true;
      `}
      javaScriptEnabled
      domStorageEnabled
      onMessage={handleMessage}
    />
  );
}
