import os
import tinify
import subprocess

from pathlib import Path
from PIL import Image
from tqdm import tqdm

from dotenv import load_dotenv

load_dotenv()


def main() -> None:

    # Load Tinify API key from enviroment
    tinify.key = os.getenv("TINIFY_KEY")

    # Provide the starting directory
    starting_directory = Path(
        "I:\\Meu Drive\\02 - MATERIAIS\\077_PROPEG_CAIXA_MEGA_VIRADA\\propeg_caixa_mega_virada_completo_v6"
    )

    # Running the tinify function
    optimize_pngs_in_directory(starting_directory, size_threshold_kb=20)
    # tinify_pngs_in_directory(starting_directory, size_threshold_kb=50)


def optimize_png(image_path):
    # Function to optimize PNG using Pillow + oxipng for maximum compression
    with Image.open(image_path) as img:
        # Keep original image mode (preserves alpha channel)
        # Just optimize without quantization (lossless compression)
        img.save(image_path, format="PNG", optimize=True, compress_level=6)
    
    # Further optimize with oxipng (very aggressive compression)
    oxipng_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Shssoichiro.Oxipng_Microsoft.Winget.Source_8wekyb3d8bbwe\oxipng-10.0.0-x86_64-pc-windows-msvc\oxipng.exe"
    )
    try:
        subprocess.run(
            [oxipng_path, "-o", "4", "--strip", "safe", str(image_path)],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Warning: oxipng failed for {image_path}: {e}")


def optimize_pngs_in_directory(directory, size_threshold_kb=50):
    # Function to optimize all PNGs in a directory using Pillow with size check
    print(f"Starting directory: {directory}")
    print(f"Directory exists: {directory.exists()}")
    optimized_count = 0
    all_png_files = []

    # Collecting all PNG files above the size threshold
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".png"):
                file_path = os.path.join(root, file)
                size_kb = os.stat(file_path).st_size / 1024
                # print(f"Found PNG: {file_path}, size: {size_kb:.2f} KB")
                if os.stat(file_path).st_size > size_threshold_kb * 1024:
                    all_png_files.append(file_path)

    print(f"Total PNG files above {size_threshold_kb} KB: {len(all_png_files)}")

    # Iterating with tqdm progress bar
    for file_path in tqdm(all_png_files, desc="Optimizing PNGs", unit="file"):
        optimize_png(file_path)
        optimized_count += 1

    print(f"\nTotal optimized PNG files: {optimized_count}")


def tinify_png(image_path):
    # Function to tinify PNG using tinify API
    source = tinify.from_file(image_path)
    source.to_file(image_path)


def tinify_pngs_in_directory(directory, size_threshold_kb=50):
    # Function to tinify all PNGs in a directory with size check
    tinified_count = 0
    all_png_files = []

    # Collecting all PNG files above the size threshold
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".png"):
                file_path = os.path.join(root, file)
                if os.stat(file_path).st_size > size_threshold_kb * 1024:
                    all_png_files.append(file_path)

    # Iterating with tqdm progress bar
    for file_path in tqdm(all_png_files, desc="Tinifying PNGs", unit="file"):
        tinify_png(file_path)
        tinified_count += 1

    print(f"\nTotal tinified PNG files: {tinified_count}")


if __name__ == "__main__":
    main()
