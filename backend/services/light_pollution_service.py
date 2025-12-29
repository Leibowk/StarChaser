import math
import gzip
import numpy as np
from models.light_pollution import LightPollution
from pathlib import Path

TILE_DIR = Path(__file__).resolve().parent.parent / "binary_tiles"

class LightPollutionService:
    def get_for_location(self, lat: float, lng: float) -> LightPollution | None:
        lon_from_dateline = (lng + 180) % 360
        lat_from_start = lat + 65

        tile_x = int(lon_from_dateline // 5) + 1
        tile_y = int(lat_from_start // 5) + 1

        if tile_y < 1 or tile_y > 28:
            return None

        tile_path = TILE_DIR / f"binary_tile_{tile_x}_{tile_y}.dat.gz"
        if not tile_path.exists():
            return None

        with gzip.open(tile_path, "rb") as f:
            data = np.frombuffer(f.read(), dtype=np.int8)

        ix = round(120 * (lon_from_dateline - 5 * (tile_x - 1) + 1 / 240))
        iy = round(120 * (lat_from_start - 5 * (tile_y - 1) + 1 / 240))

        first = 128 * int(data[0]) + int(data[1])
        change = sum(int(data[600 * i + 1]) for i in range(1, iy))
        change += sum(int(data[600 * (iy - 1) + 1 + i]) for i in range(1, ix))

        compressed = first + change
        lp_index = (5 / 195) * (math.exp(0.0195 * compressed) - 1)
        mag_arcsec = 22 - 5 * math.log(1 + lp_index, 100)

        brightness_ratio = lp_index

        lp_zone, color = self._zone_from_ratio(brightness_ratio)

        return LightPollution(
            lp_index=lp_index,
            mag_arcsec=mag_arcsec,
            lp_zone=lp_zone,
            color_zone=color,
        )

    def _zone_from_ratio(self, r: float):
        if r < 0.01: return "0", "rgba(0,0,0,0.8)"
        if r < 0.06: return "1a", "rgba(34,34,34,0.7)"
        if r < 0.11: return "1b", "rgba(66,66,66,0.6)"
        if r < 0.19: return "2a", "rgba(20,47,114,0.7)"
        if r < 0.33: return "2b", "rgba(33,84,216,0.6)"
        if r < 0.58: return "3a", "rgba(15,87,20,0.7)"
        if r < 1.00: return "3b", "rgba(31,161,42,0.6)"
        if r < 1.73: return "4a", "rgba(110,100,30,0.7)"
        if r < 3.00: return "4b", "rgba(184,166,37,0.6)"
        if r < 5.20: return "5a", "rgba(191,100,30,0.7)"
        if r < 9.00: return "5b", "rgba(253,150,80,0.6)"
        if r < 15.59: return "6a", "rgba(251,90,73,0.7)"
        if r < 27.00: return "6b", "rgba(251,153,138,0.6)"
        if r < 46.77: return "7a", "rgba(160,160,160,0.7)"
        return "7b", "rgba(242,242,242,0.8)"
