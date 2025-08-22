import os

for i, png in enumerate([l for l in os.listdir() if l.endswith('.gpg')]):
    os.system(f'gpg  --quiet --batch --yes --decrypt --passphrase="tiles" --output {"%05d.png"%i} {png}')

os.system(r'ffmpeg -r 3 -i "%05d.png" -c:v libx264 -qp 0 out.mp4')
os.system(r' ffmpeg -r 3 -i "%05d.png" -plays 0 out.apng')
# ffmpeg -r 3 -i "%05d.png" -vf "crop=270:280:0:175" -y -plays 0 out.apng