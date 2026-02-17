import { WebView, WebViewMessageEvent } from 'react-native-webview';
import { Asset } from 'expo-asset';
import { useEffect, useState, useMemo, useRef } from 'react';
import { Site } from '../lib/types';
import { useRouter } from 'expo-router';

export type MapView = { lat: number; lon: number; zoom: number };

type Props = {
  sites: Site[];
  initialView: MapView;
  onViewChange?: (lat: number, lon: number, zoom: number) => void;
};

const API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL ?? '';

const INITIAL_SCRIPT = `
  window.__API_URL__ = '${API_URL}';
  true;
`;

function renderSitesScript(sites: Site[]) {
  return `if (window.renderSites) window.renderSites(${JSON.stringify(sites)}); true;`;
}

export function MapWebView({ sites, initialView, onViewChange }: Props) {
  const [html, setHtml] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);
  const webViewRef = useRef<WebView>(null);
  const router = useRouter();

  const source = useMemo(() => (html ? { html } : null), [html]);

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
    if (loaded && webViewRef.current) {
      webViewRef.current.injectJavaScript(renderSitesScript(sites));
    }
  }, [loaded, sites]);

  const onMessage = (event: WebViewMessageEvent) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'siteClick' && data.site) {
        router.push(`/site/${data.site}`);
      } else if (data.type === 'viewChange' && onViewChange) {
        onViewChange(data.lat, data.lon, data.zoom);
      }
    } catch (e) {
      // handle error
    }
  };

  const onLoadEnd = () => {
    const initScript = `
      window.__INITIAL_VIEW__ = ${JSON.stringify(initialView)};
      if (window.initMap) window.initMap();
      true;
    `;
    webViewRef.current?.injectJavaScript(initScript);
    setLoaded(true);
  };

  if (!html || !source) return null;

  return (
    <WebView
      ref={webViewRef}
      source={source}
      injectedJavaScript={INITIAL_SCRIPT}
      onLoadEnd={onLoadEnd}
      javaScriptEnabled
      domStorageEnabled
      onMessage={onMessage}
    />
  );
}
