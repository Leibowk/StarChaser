import { Site, SiteSummary } from './types';

export function mapApiSiteToSite(data: any): Site {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    latitude: data.latitude,
    longitude: data.longitude,
    visibility: data.visibility
      ? {
          score: data.visibility.score,
          category: data.visibility.category,

          lightPollution: data.visibility.light_pollution
            ? {
                lpIndex: data.visibility.light_pollution.lp_index,
                magArcSec: data.visibility.light_pollution.mag_arcsec,
                lpZone: data.visibility.light_pollution.lp_zone,
                colorZone: data.visibility.light_pollution.color_zone,
              }
            : undefined,

          weather: data.visibility.weather
            ? {
                cloudCoverage: data.visibility.weather.cloud_coverage,
                avgvisKm: data.visibility.weather.avgvis_km,
                avgvisMiles: data.visibility.weather.avgvis_miles,
                condition: data.visibility.weather.condition,
                aqi: data.visibility.weather.aqi,
              }
            : undefined,
        }
      : undefined,
  };
}

export function mapApiSiteToSiteSummary(data: any): SiteSummary {
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
    };
  }