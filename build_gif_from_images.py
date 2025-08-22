import moviepy as mp
import os
import subprocess
from pathlib import Path


project_path = Path(__file__).parent.resolve()
source_path = "I:\\Meu Drive\\02 - MATERIAIS\\037_NOVA_APEX_ACREDITA EXPORTAÇÃO\\nova_apex_acredita_exportacao"
destination_path = "I:\\Meu Drive\\02 - MATERIAIS\\037_NOVA_APEX_ACREDITA EXPORTAÇÃO\\nova_apex_acredita_exportacao"
gifsicle_path = os.path.join(project_path, "gifsicle", "gifsicle.exe")

os.makedirs(destination_path, exist_ok=True)

subfolders = [f.name for f in Path(source_path).iterdir() if f.is_dir()]

for subfolder in subfolders:

    subfolder_path = os.path.join(source_path, subfolder)
    output_path = os.path.join(destination_path, f"{subfolder}.gif")

    # Config
    image_files = [os.path.join(subfolder_path, f"{i:03}.png") for i in range(1, 15)]
    # when each image appears (in seconds)
    timestamps = [0, 0.4, 0.8, 1.2, 5, 5.4, 5.8, 6.2, 10, 10.4, 10.8, 11.2, 15, 15.4]
    duration = 20

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
