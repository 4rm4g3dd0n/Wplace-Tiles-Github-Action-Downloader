import os
import glob

# Find all .gpg files in the automatic directory recursively
gpg_files = glob.glob('automatic/**/*.gpg', recursive=True)
decrypted_files = []

# Decrypt all .gpg files
for gpg_file in gpg_files:
    output_file = gpg_file[:-4]  # Remove .gpg extension
    os.system(f'gpg --quiet --batch --yes --decrypt --passphrase="tiles" --output {output_file} {gpg_file}')
    decrypted_files.append(output_file)

# Group files by their source folder number
dpngs = {}
for png_file in decrypted_files:
    # Extract the folder number from the path: automatic/0/filename.png -> folder number is 0
    path_parts = png_file.split('/')
    if len(path_parts) >= 3 and path_parts[0] == 'automatic':
        folder_num = path_parts[1]  # automatic/0/filename.png
    else:
        folder_num = '0'  # fallback
    
    if folder_num not in dpngs:
        dpngs[folder_num] = []
    dpngs[folder_num].append(png_file)

# Sort files within each group by timestamp
for folder_num in dpngs:
    dpngs[folder_num].sort()

# Process each folder separately to create individual timelapses
for folder_num in sorted(dpngs.keys()):
    folder_files = dpngs[folder_num]
    if not folder_files:
        continue
    
    print(f"Processing folder {folder_num} with {len(folder_files)} images...")
    
    # Create sequentially numbered files for this folder
    for i, png_file in enumerate(folder_files):
        os.system(f'cp "{png_file}" folder_{folder_num}_{"%05d.png"%i}')
    
    # Get first and last timestamps for naming
    first_file = os.path.basename(folder_files[0])
    last_file = os.path.basename(folder_files[-1])
    first_time = first_file.replace('.png', '')
    last_time = last_file.replace('.png', '')
    
    # Create video and APNG for this folder
    pattern = f'folder_{folder_num}_%05d.png'
    output_base = f'folder_{folder_num}_{first_time}_to_{last_time}'
    
    print(f"Creating video for folder {folder_num}...")
    os.system(f'ffmpeg -r 3 -i "{pattern}" -c:v libx264 -qp 0 "{output_base}.mp4" -y')
    
    print(f"Creating APNG for folder {folder_num}...")
    # Use the predefined wplace palette for consistent colors across all timelapses
    os.system(f'ffmpeg -r 3 -i "{pattern}" -i wplace-full.png -lavfi "paletteuse=dither=none" -plays 0 "{output_base}.apng" -y')
    
    # Clean up the temporary sequenced files for this folder
    os.system(f'rm -f folder_{folder_num}_*.png')

# Clean up all decrypted PNG files in automatic folders
print("Cleaning up decrypted files...")
for decrypted_file in decrypted_files:
    if os.path.exists(decrypted_file):
        os.remove(decrypted_file)

print("All folders processed!")
