import { WebView, WebViewMessageEvent } from 'react-native-webview';
import { Asset } from 'expo-asset';
import { useEffect, useState } from 'react';
import { Site } from '../lib/types';
import { useRouter } from 'expo-router';

type Props = {
  sites: Site[];
};

export function MapWebView({ sites }: Props) {
  const [html, setHtml] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    async function loadHtml() {
      const asset = Asset.fromModule(require('./map.html'));
      await asset.downloadAsync();
      const text = await (await fetch(asset.uri)).text();
      setHtml(text);
    }
    loadHtml();
  }, []);

  const onMessage = (event: WebViewMessageEvent) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'siteClick' && data.site) {
        // Push to the dynamic route with the site id
        router.push(`/site/${data.site}`);
      }
    } catch (e) {
      // handle error
    }
  };

  if (!html) return null;

  return (
    <WebView
      source={{ html }}
      injectedJavaScript={`
        window.SITES_DATA = ${JSON.stringify(sites)};
        window.__API_URL__ = '${process.env.EXPO_PUBLIC_BACKEND_API_URL}';
        if (window.initMap) {
         window.initMap();
        }
        if (window.renderSites) {
          window.renderSites(window.SITES_DATA);
        }
        true;
      `}
      javaScriptEnabled
      domStorageEnabled
      onMessage={onMessage}
    />
  );
}
