export type Site = {
  id: number;
  name: string;
  description: string;
  latitude: number;
  longitude: number;
  visibility?: Visibility;
};

export type SiteSummary = {
  id: number;
  name: string;
  description: string;
  latitude: number;
  longitude: number;
  lightPollution?: LightPollutionData;
};

export type Visibility = {
  score: number;
  category: string;
  lightPollution?: LightPollutionData;
  weather?: WeatherData;
}

export type LightPollutionData = {
  lpIndex: number;
  magArcSec: number;
  lpZone: string;
  colorZone: string;
};

export type WeatherData = {
  cloudCoverage: number;   
  avgvisKm: number;        
  avgvisMiles: number;     
  condition: string;
  aqi: number;
};

export const TIME_OPTIONS = [
  'Tonight',
  'Tomorrow Night',
  'Three Nights From Now',
] as const;
