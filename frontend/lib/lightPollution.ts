import pako from 'pako';
import { fetch } from 'expo/fetch';
import { LightPollutionData } from './types';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL;

if (!API_URL) {
  throw new Error('EXPO_PUBLIC_BACKEND_API_URL is not set');
}

export async function getLightPollution(
  lat: number,
  lng: number
): Promise<LightPollutionData | null> {
  const lonFromDateLine = (lng + 180) % 360;
  const latFromStart = lat + 65;

  const tileX = Math.floor(lonFromDateLine / 5) + 1;
  const tileY = Math.floor(latFromStart / 5) + 1;

  if (tileY < 1 || tileY > 28) return null;

  const response = await fetch(
    `${API_URL}/bi_tiles/binary_tile_${tileX}_${tileY}.dat.gz`,
    { headers: { "Cache-Control": "no-cache" } }
  );

  const buffer = await response.arrayBuffer();
  const dataArray = new Int8Array(pako.ungzip(buffer));

  const ix = Math.round(120 * (lonFromDateLine - 5 * (tileX - 1) + 1 / 240));
  const iy = Math.round(120 * (latFromStart - 5 * (tileY - 1) + 1 / 240));

  let firstNumber = 128 * dataArray[0] + dataArray[1];
  let change = 0;

  for (let i = 1; i < iy; i++) change += dataArray[600 * i + 1];
  for (let i = 1; i < ix; i++) change += dataArray[600 * (iy - 1) + 1 + i];

  const compressed = firstNumber + change;

  const lpIndex = (5 / 195) * (Math.exp(0.0195 * compressed) - 1);
  const magArcSec = 22 - 5 * Math.log(1 + lpIndex) / Math.log(100);

  let lpZone = '1a';
  if (lpIndex > 0.03) lpZone = '2';

  return { lpIndex, magArcSec, lpZone };
}
