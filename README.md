# BirdMash Daily Bird Scrambler

This project selects random bird images, checks for solid borders, scrambles them into puzzles of varying difficulty, and organizes the output for daily use.

## Features
- Recursively selects images from a source directory
- Rejects images with solid color borders
- Scrambles images into puzzles with 9, 36, or 144 tiles ("ametaur", "birder", "bostik")
- Moves used images to a separate folder to avoid repeats

## Usage
1. Place your source images in `birdmash_images/images/` (subfolders allowed).
2. Run the script:
   ```bash
   python daily_bird_scrambler.py
   ```
3. Scrambled images will be saved in `output/<date>/<difficulty>/`.

## Requirements
- Python 3.7+
- Pillow
- numpy

Install dependencies with:
```bash
pip install -r requirements.txt
```

## File Structure
- `daily_bird_scrambler.py` — Main script
- `output/` — Scrambled images by date and difficulty
- `birdmash_images/images/` — Source images
- `birdmash_images/used_images/` — Used images

---

Enjoy your daily bird puzzles!
