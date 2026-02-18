import { WebView, WebViewMessageEvent } from 'react-native-webview';
import { Asset } from 'expo-asset';
import { useEffect, useRef, useState } from 'react';
import { useUserLocation } from '../lib/locationService';
import { Site } from '../lib/types';
import { useRouter } from 'expo-router';

type Props = {
  sites: Site[];
};

export function MapWebView({ sites }: Props) {
  const [html, setHtml] = useState<string | null>(null);
  const { userLocation } = useUserLocation({ autoRequest: true });
  const webViewRef = useRef<WebView>(null);
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

  useEffect(() => {
    if (!userLocation) return;
    const script = `window.setMapCenter && window.setMapCenter(${userLocation.lat}, ${userLocation.lon}); true;`;
    webViewRef.current?.injectJavaScript(script);
  }, [userLocation]);

  const onMessage = (event: WebViewMessageEvent) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'siteClick' && data.site) {
        router.push(`/site/${data.site}`);
      }
    } catch (e) {
      // handle error
    }
  };

  if (!html) return null;

  const userLocationJs = userLocation
    ? JSON.stringify({ latitude: userLocation.lat, longitude: userLocation.lon })
    : 'null';

  return (
    <WebView
      ref={webViewRef}
      source={{ html }}
      injectedJavaScript={`
        window.SITES_DATA = ${JSON.stringify(sites)};
        window.__API_URL__ = '${process.env.EXPO_PUBLIC_BACKEND_API_URL}';
        window.__USER_LOCATION__ = ${userLocationJs};
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
