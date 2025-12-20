import { WebView } from 'react-native-webview';
import { Asset } from 'expo-asset';
import { useEffect, useState } from 'react';
import { Site } from '../lib/types';
import { useNavigation } from '@react-navigation/native';
import { RootStackParamList } from '../lib/navigation';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

type Props = {
  sites: Site[];
};

export function MapWebView({ sites }: Props) {
  const [html, setHtml] = useState<string | null>(null);

  useEffect(() => {
    async function loadHtml() {
      const asset = Asset.fromModule(require('../assets/map.html'));
      await asset.downloadAsync();
      const text = await (await fetch(asset.uri)).text();
      setHtml(text);
    }

    loadHtml();
  }, []);

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
    />
  );
}
