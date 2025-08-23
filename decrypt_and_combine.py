import os

files = [l for l in os.listdir() if l.endswith('.gpg')]
pngs = []

for i, png in enumerate(files):
    pngs.append(png[:-4])
    os.system(f'gpg  --quiet --batch --yes --decrypt --passphrase="tiles" --output {png[:-4]} {png}')

dpngs = {}
for png in pngs:
    i = png.split("_")[0]
    if i not in dpngs: dpngs[i] = []

    dpngs[i].append(png)

if len(dpngs) > 1:
    png_group = [l for l in zip(*dpngs.values())]
    for group in png_group:
        assert group[0].split("_")[-1] == group[1].split("_")[-1]

    for i, group in enumerate(png_group):
        # combine image side by side, no config/option to easily set layout yet
        os.system(f'convert {" ".join(group)} +append {"%05d.png"%i}')
else:
    for i, png in enumerate(*dpngs.values()):
        os.rename(png, '%05d.png'%i)


os.system(r'ffmpeg -r 3 -i "%05d.png" -c:v libx264 -qp 0 '+f'{files[0][2:-8]}_{files[-1][2:-8]}.mp4')
#ffv1 result in giant file
#os.system(r'ffmpeg -r 3 -i "%05d.png" -c:v ffv1 '+f'{files[0][2:-8]}_{files[-1][2:-8]}.mkv')
os.system(r' ffmpeg -r 3 -i "%05d.png" -plays 0 '+f'{files[0][2:-8]}_{files[-1][2:-8]}.apng')
# ffmpeg -r 3 -i "%05d.png" -vf "crop=270:280:0:175" -y -plays 0 out.apng