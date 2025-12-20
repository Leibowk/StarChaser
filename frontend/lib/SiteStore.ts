import { Site } from './types';

let currentSite: Site | null = null;

export function setCurrentSite(site: Site) {
  currentSite = site;
}

export function getCurrentSite(): Site | null {
  return currentSite;
}
