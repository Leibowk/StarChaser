import { Site } from './types';

export function mapApiSiteToSite(data: any): Site {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    latitude: data.latitude,
    longitude: data.longitude,
    lightPollution: data.light_pollution
      ? {
          lpIndex: data.light_pollution.lp_index,
          magArcSec: data.light_pollution.mag_arcsec,
          lpZone: data.light_pollution.lp_zone,
          colorZone: data.light_pollution.color_zone,
        }
      : undefined,
    weather: data.weather
      ? {
          cloudCoverage: data.weather.cloud_coverage,
          avgvisKm: data.weather.avgvis_km,
          avgvisMiles: data.weather.avgvis_miles,
          condition: data.weather.condition,
          aqi: data.weather.aqi,
        }
      : undefined,
  };
}