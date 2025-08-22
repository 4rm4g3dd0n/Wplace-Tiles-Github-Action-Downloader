import os

files = [l for l in os.listdir() if l.endswith('.gpg')]

for i, png in enumerate(files):
    os.system(f'gpg  --quiet --batch --yes --decrypt --passphrase="tiles" --output {"%05d.png"%i} {png}')

os.system(r'ffmpeg -r 3 -i "%05d.png" -c:v libx264 -qp 0 '+f'{files[0][2:-8]}_{files[-1][2:-8]}.mp4')
#ffv1 result in giant file
#os.system(r'ffmpeg -r 3 -i "%05d.png" -c:v ffv1 '+f'{files[0][2:-8]}_{files[-1][2:-8]}.mkv')
os.system(r' ffmpeg -r 3 -i "%05d.png" -plays 0 '+f'{files[0][2:-8]}_{files[-1][2:-8]}.apng')
# ffmpeg -r 3 -i "%05d.png" -vf "crop=270:280:0:175" -y -plays 0 out.apng