import moviepy as mp
import os
import subprocess
from pathlib import Path


project_path = Path(__file__).parent.resolve()
source_path = "I:\\Meu Drive\\02 - MATERIAIS\\034_APEX_BONIFICADO\\nova_apex_web_summit_lisboa"
destination_path = "I:\\Meu Drive\\02 - MATERIAIS\\034_APEX_BONIFICADO\\nova_apex_web_summit_lisboa"
gifsicle_path = os.path.join(project_path, "gifsicle", "gifsicle.exe")

os.makedirs(destination_path, exist_ok=True)

subfolders = [f.name for f in Path(source_path).iterdir() if f.is_dir()]

for subfolder in subfolders:

    subfolder_path = os.path.join(source_path, subfolder)
    output_path = os.path.join(destination_path, f"{subfolder}.gif")

    # Config
    image_files = [os.path.join(subfolder_path, f"{i:03}.png") for i in range(1, 16)]
    timestamps = [0, 0.2, 0.4, 0.6, 4, 4.2, 4.4, 4.6, 4.8, 5, 12,
                  12.2, 12.4, 12.6, 12.8]  # when each image appears (in seconds)
    duration = 16

    # Create base empty clip
    clips = []
    for i, img_path in enumerate(image_files):
        clip = mp.ImageClip(img_path).with_start(timestamps[i]).with_duration(duration - timestamps[i])
        clips.append(clip)

    final = mp.CompositeVideoClip(clips, size=clips[0].size).with_duration(duration)
    final.write_gif(output_path, fps=10)

    # Optimize GIF with pygifsicle
    optimized_gif_path = os.path.join(destination_path, f"{subfolder}_otimized.gif")
    subprocess.run([
        gifsicle_path,
        "-b",
        "--optimize=2",
        "--colors=256",
        "--lossy=20",
        output_path,
        "-o", optimized_gif_path,
    ], check=True)
