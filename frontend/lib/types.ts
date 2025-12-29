export type LightPollutionData = {
  lpIndex: number;
  magArcSec: number;
  lpZone: string;
  colorZone: string;
};

export type Site = {
  id: string;
  name: string;
  description: string;
  latitude: number;
  longitude: number;
  lightPollution?: LightPollutionData;
};
