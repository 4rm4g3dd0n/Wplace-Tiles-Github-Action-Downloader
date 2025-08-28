import requests
import time
import os
from datetime import datetime

with open("links") as f:
    links = [(i,l) for i,l in enumerate(f.read().split()) if l]

time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

s = requests.session()

for i, link in links:
    r = s.get(link)
    folder_path = os.path.join('processing', str(i))
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, f'{time}.png'), 'wb') as f:
        f.write(r.content)
