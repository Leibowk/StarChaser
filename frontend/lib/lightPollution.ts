//Currently using code from https://github.com/djlorenz/djlorenz.github.io/blob/master/astronomy/lp/overlay/dark.html

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

  var brightnessRatio = compressed2full(compressed);
	    
  if (brightnessRatio < 0.01) {
  var LPzone = '0'
              var colorzone = 'rgba(  0,  0,  0, 0.8)'
    } else if (brightnessRatio < 0.06) {
  var LPzone = '1a'
              var colorzone = 'rgba( 34, 34, 34, 0.7)'
    } else if (brightnessRatio < 0.11) {
  var LPzone = '1b'
              var colorzone = 'rgba( 66, 66, 66, 0.6)'
    } else if (brightnessRatio < 0.19) {
  var LPzone = '2a'
              var colorzone = 'rgba( 20, 47,114, 0.7)'
    } else if (brightnessRatio < 0.33) {
  var LPzone = '2b'
              var colorzone = 'rgba( 33, 84,216, 0.6)'
    } else if (brightnessRatio < 0.58) {
  var LPzone = '3a'
              var colorzone = 'rgba( 15, 87, 20, 0.7)'
    } else if (brightnessRatio < 1.00) {
  var LPzone = '3b'
              var colorzone = 'rgba( 31,161, 42, 0.6)'
    } else if (brightnessRatio < 1.73) {
  var LPzone = '4a'
              var colorzone = 'rgba(110,100, 30, 0.7)'
    } else if (brightnessRatio < 3.00) {
  var LPzone = '4b'
              var colorzone = 'rgba(184,166, 37, 0.6)'
    } else if (brightnessRatio < 5.20) {
  var LPzone = '5a'
              var colorzone = 'rgba(191,100, 30, 0.7)'
    } else if (brightnessRatio < 9.00) {
  var LPzone = '5b'
              var colorzone = 'rgba(253,150, 80, 0.6)'
    } else if (brightnessRatio < 15.59) {
  var LPzone = '6a'
              var colorzone = 'rgba(251, 90, 73, 0.7)'
    } else if (brightnessRatio < 27.00) {
  var LPzone = '6b'
              var colorzone = 'rgba(251,153,138, 0.6)'
    } else if (brightnessRatio < 46.77) {
  var LPzone = '7a'
              var colorzone = 'rgba(160,160,160, 0.7)'
    } else {
  var LPzone = '7b'
              var colorzone = 'rgba(242,242,242, 0.8)'
    }

  return { lpIndex, magArcSec, lpZone: LPzone };
}

function compressed2full(x: number) {
    return (5.0/195.0) * ( Math.exp(0.0195*x) - 1.0);
}