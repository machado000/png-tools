import moviepy as mp
import os
import subprocess
from pathlib import Path


project_path = Path(__file__).parent.resolve()
source_path = "I:\\Meu Drive\\02 - MATERIAIS\\056_NACIONAL_CAMARA_APROVA_FASE_4_BANNERS\\pngs"
destination_path = "I:\\Meu Drive\\02 - MATERIAIS\\056_NACIONAL_CAMARA_APROVA_FASE_4_BANNERS\\gifs_v1"  # noqa
# destination_path = source_path
gifsicle_path = os.path.join(project_path, "gifsicle", "gifsicle.exe")

os.makedirs(destination_path, exist_ok=True)

# folders = [f.name for f in Path(source_path).iterdir() if f.is_dir()]

folders = [
    'banner_1_728x90',
    'banner_1_970x90',
    'banner_1_970x150',
    'banner_1_970x250',
    'banner_1_1040x210',
    'banner_1_468x60',
    'banner_1_320x150',
    'banner_1_320x100',
    'banner_1_300x100',
]
file_range = range(1, 14)
timestamps = [0, 0.3, 0.6, 0.9, 5, 5.3, 5.6, 5.9, 10, 10.3, 10.6, 10.9, 11.2]
duration = 15

# folders = [
#     'banner_1_300x250',
#     'banner_1_336x280',
#     'banner_1_250x250',
#     'banner_1_200x200',
# ]
# file_range = range(1, 13)
# timestamps = [0, 0.3, 0.6, 0.9, 5, 5.3, 5.6, 10, 10.3, 10.6, 10.9, 11.2]
# duration = 15

# folders = [
#     'banner_1_320x50',
#     'banner_1_300x50',
# ]
# file_range = range(1, 13)
# timestamps = [0, 0.3, 0.6, 5, 5.3, 5.6, 5.9, 10, 10.3, 10.6, 10.9, 11.2]
# duration = 15

for subfolder in folders:

    subfolder_path = os.path.join(source_path, subfolder)
    output_path = os.path.join(destination_path, f"{subfolder}.gif")

    image_files = [os.path.join(subfolder_path, f"{i:03}.png") for i in file_range]

    # Create base empty clip
    clips = []
    for i, img_path in enumerate(image_files):
        clip = mp.ImageClip(img_path).with_start(timestamps[i]).with_duration(duration - timestamps[i])
        clips.append(clip)

    final = mp.CompositeVideoClip(clips, size=clips[0].size).with_duration(duration)
    final.write_gif(output_path, fps=2)

    # Optimize GIF with pygifsicle

    # If you want to save the optimized GIF as a new file instead of overwriting the original, uncomment the next line
    # optimized_gif_path = os.path.join(destination_path, f"{subfolder}_otimized.gif")

    # Only optimize if file is bigger than 150kb
    file_size = os.path.getsize(output_path)
    # if file_size > 60 * 1024:  # 150kb in bytes
    print(f"Optimizing {output_path} ({file_size / 1024:.2f} KB)")
    subprocess.run([
        gifsicle_path,
        "-b",
        "--optimize=1",
        # "--colors=256",
        # "--lossy=5",  # Use 100 for more aggressive compression, but may reduce quality
        output_path,
        # "-o", optimized_gif_path,
    ], check=True)
