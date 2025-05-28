import os
import random
import shutil
from PIL import Image
import numpy as np
import math
from datetime import date

# Constants
NUM_IMAGES = 10
IMAGES_DIR = "/Users/alfieprettyman/birdmash_images/images"
USED_DIR = "/Users/alfieprettyman/birdmash_images/used_images"
BASE_OUTPUT_DIR = os.path.join("output", str(date.today()))
DIFFICULTY_LEVELS = {
    "ametaur": 9,
    "birder": 36,
    "bostik": 144
}

# Ensure required directories exist
os.makedirs(USED_DIR, exist_ok=True)
for diff in DIFFICULTY_LEVELS:
    os.makedirs(os.path.join(BASE_OUTPUT_DIR, diff), exist_ok=True)

def has_border(image_path, border_width=6, tolerance=10):
    """
    Returns True if the image has a solid color border of 6 or more pixels (within tolerance).
    border_width: minimum border width in pixels to check from each edge (reject if >=6).
    tolerance: max color difference to consider as 'solid'.
    """
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape

    # Get border pixels
    top = arr[0:border_width, :, :]
    bottom = arr[-border_width:, :, :]
    left = arr[:, 0:border_width, :]
    right = arr[:, -border_width:, :]

    # Concatenate all border pixels
    border_pixels = np.concatenate([top.reshape(-1,3), bottom.reshape(-1,3), left.reshape(-1,3), right.reshape(-1,3)], axis=0)
    mean_color = np.mean(border_pixels, axis=0)
    diffs = np.abs(border_pixels - mean_color)
    max_diff = np.max(diffs)

    return max_diff < tolerance

def scramble_image(input_path, output_path, num_tiles):
    img = Image.open(input_path).convert('RGB')
    arr = np.array(img)
    h, w, c = arr.shape

    num_tiles_y = int(math.floor(math.sqrt(num_tiles)))
    num_tiles_x = int(math.ceil(num_tiles / num_tiles_y))
    tile_h = h // num_tiles_y
    tile_w = w // num_tiles_x

    tiles = []
    positions = []
    for i in range(num_tiles_y):
        for j in range(num_tiles_x):
            y1 = i * tile_h
            y2 = (i + 1) * tile_h if i < num_tiles_y - 1 else h
            x1 = j * tile_w
            x2 = (j + 1) * tile_w if j < num_tiles_x - 1 else w
            tiles.append(arr[y1:y2, x1:x2])
            positions.append((y1, y2, x1, x2))

    dest_positions = positions.copy()
    random.shuffle(dest_positions)

    scrambled_arr = np.zeros_like(arr)
    for tile, (y1, y2, x1, x2) in zip(tiles, dest_positions):
        resized_tile = np.array(Image.fromarray(tile).resize((x2 - x1, y2 - y1)))
        scrambled_arr[y1:y2, x1:x2] = resized_tile

    scrambled_img = Image.fromarray(scrambled_arr)
    scrambled_img.save(output_path)

# Recursively find all images in images/ subfolders
all_images = []
for root, dirs, files in os.walk(IMAGES_DIR):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            all_images.append(os.path.join(root, f))

if len(all_images) < NUM_IMAGES:
    raise ValueError("Not enough images in images folder and its subfolders!")

selected_images = []
random.shuffle(all_images)
idx = 0
while len(selected_images) < NUM_IMAGES and idx < len(all_images):
    img_path = all_images[idx]
    if has_border(img_path):
        os.remove(img_path)
        idx += 1
        continue
    selected_images.append(img_path)
    idx += 1

if len(selected_images) < NUM_IMAGES:
    raise ValueError("Not enough borderless images available!")

for src_path in selected_images:
    filename = os.path.basename(src_path)
    used_path = os.path.join(USED_DIR, filename)

    for diff, num_tiles in DIFFICULTY_LEVELS.items():
        output_dir = os.path.join(BASE_OUTPUT_DIR, diff)
        output_path = os.path.join(output_dir, filename)
        scramble_image(src_path, output_path, num_tiles)

    # Move original to used_images (flattened)
    shutil.move(src_path, used_path)

print(f"Processed {NUM_IMAGES} images. Scrambled versions saved in {BASE_OUTPUT_DIR}.")
