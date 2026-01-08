from PIL import Image
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

# === CONFIG ===
INPUT_DIR = "../image_tiles/tiles2024"
OUTPUT_DIR = "../image_tiles/visibility2024"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Original 15 colors
ORIGINAL_COLORS = [
    (0,0,0), (34,34,34), (66,66,66), (20,47,114), (33,84,216),
    (15,87,20), (31,161,42), (110,100,30), (184,166,37), (191,100,30),
    (253,150,80), (251,90,73), (251,153,138), (160,160,160), (242,242,242)
]

# Target colors
TARGET_COLORS = [
    (0, 255, 0, 200), (50, 220, 50, 180), (100, 255, 100, 180), (150, 255, 100, 180),
    (200, 255, 100, 180), (255, 255, 0, 180), (255, 200, 50, 180), (255, 150, 50, 180),
    (255, 100, 50, 180), (255, 50, 50, 180), (200, 20, 20, 180), (100, 0, 0, 180),
    (60, 60, 60, 180), (40, 40, 40, 180), (20, 20, 20, 180)
]

# === HELPER: closest color mapping ===
def closest_color(r, g, b):
    r, g, b = int(r), int(g), int(b)
    best_dist = float('inf')
    best_idx = 0
    for idx, (or_r, or_g, or_b) in enumerate(ORIGINAL_COLORS):
        dr = r - or_r
        dg = g - or_g
        db = b - or_b
        dist = dr*dr + dg*dg + db*db
        if dist < best_dist:
            best_dist = dist
            best_idx = idx
    return np.array(TARGET_COLORS[best_idx], dtype=np.uint8)


# === PROCESS ONE TILE ===
def process_tile(filename):
    if not filename.lower().endswith(".png"):
        return filename, "skipped"

    img_path = os.path.join(INPUT_DIR, filename)
    out_path = os.path.join(OUTPUT_DIR, filename)

    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img, dtype=np.int16)
    out_arr = np.zeros_like(arr, dtype=np.uint8)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            r, g, b, a = arr[i, j]
            out_arr[i, j] = closest_color(r, g, b)

    out_img = Image.fromarray(out_arr, mode="RGBA")
    out_img.save(out_path)
    return filename, "done"


# === MAIN MULTIPROCESS LOOP ===
def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".png")]

    import multiprocessing
    max_workers = multiprocessing.cpu_count()  # use all CPU cores

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_tile, f): f for f in files}
        for future in as_completed(futures):
            filename, status = future.result()
            print(f"{filename}: {status}")


if __name__ == "__main__":
    main()
