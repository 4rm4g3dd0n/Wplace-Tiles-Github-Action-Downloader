import os
import glob

# Find all .gpg files in the automatic directory
gpg_files = glob.glob('automatic/*.gpg')
decrypted_files = []

# Decrypt all .gpg files
for gpg_file in gpg_files:
    output_file = gpg_file[:-4]  # Remove .gpg extension
    os.system(f'gpg --quiet --batch --yes --decrypt --passphrase="tiles" --output {output_file} {gpg_file}')
    decrypted_files.append(output_file)

# Group files by their source folder (first part of filename)
dpngs = {}
for png_file in decrypted_files:
    # Extract the folder number from the filename
    basename = os.path.basename(png_file)
    # The folder number should be at the start of the filename
    folder_num = basename.split('_')[0] if '_' in basename else '0'
    
    if folder_num not in dpngs:
        dpngs[folder_num] = []
    dpngs[folder_num].append(png_file)

# Sort files within each group by timestamp
for folder_num in dpngs:
    dpngs[folder_num].sort()

if len(dpngs) > 1:
    # Multiple folders - combine images side by side for each timestamp
    max_length = max(len(group) for group in dpngs.values())
    
    for i in range(max_length):
        group_files = []
        for folder_num in sorted(dpngs.keys()):
            if i < len(dpngs[folder_num]):
                group_files.append(dpngs[folder_num][i])
        
        if len(group_files) > 1:
            os.system(f'convert {" ".join(group_files)} +append {"%05d.png"%i}')
        elif len(group_files) == 1:
            os.rename(group_files[0], '%05d.png'%i)
else:
    # Single folder - just rename files sequentially
    folder_files = list(dpngs.values())[0]
    for i, png_file in enumerate(folder_files):
        os.rename(png_file, '%05d.png'%i)

# Create video and APNG from the sequenced images
if gpg_files:
    first_file = os.path.basename(gpg_files[0])
    last_file = os.path.basename(gpg_files[-1])
    
    # Extract timestamps for naming
    first_time = first_file.replace('.gpg', '')
    last_time = last_file.replace('.gpg', '')
    
    os.system(f'ffmpeg -r 3 -i "%05d.png" -c:v libx264 -qp 0 {first_time}_{last_time}.mp4')
    os.system(f'ffmpeg -r 3 -i "%05d.png" -plays 0 {first_time}_{last_time}.apng')