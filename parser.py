import shutil

import requests
from bs4 import BeautifulSoup
import warnings
from tqdm import tqdm
import os

with open("parse_pages.txt", "r") as fin:
    links = list(map(lambda x: x.strip(), fin.readlines()))

print(links)
warnings.filterwarnings("ignore")


def download_phrase_videos():
    data = "data"

    for link in tqdm(links):
        req = requests.get(link)
        soup = BeautifulSoup(req.text)

        dirname = link.split("/")[-2]
        os.mkdir(f"{data}/{dirname}")

        soup = soup.find_all("div", attrs={"id": "gallery-0"})[0]

        for el in soup.find_all("div", attrs={"class": "wikia-gallery-item"}):
            name = el.find_all("div", attrs={"class": "lightbox-caption"})[0].text.replace("/", "_")
            image_link = el.find_all("img", attrs={"class": "thumbimage"})[0]["src"]
            print(name, image_link)

            res = requests.get(image_link, stream=True)

            if res.status_code == 200:
                with open(f"{data}/{dirname}/{name}.png", 'wb') as f:
                    shutil.copyfileobj(res.raw, f)

download_phrase_videos()