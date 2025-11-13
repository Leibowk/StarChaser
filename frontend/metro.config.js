// Learn more https://docs.expo.dev/guides/customizing-metro
const { getDefaultConfig } = require('expo/metro-config');

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

// Add .geojson to asset extensions so Metro treats it as an asset (not source code)
config.resolver.assetExts.push('geojson');

module.exports = config;
