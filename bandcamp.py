import pathlib
import subprocess

import bs4
import requests

import utils

def download_album(url, dest):
    # get bandcamp metadata
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    metadata = soup.find("title").text.split("|")
    metadata = [m.strip() for m in metadata]
    
    # create destination directory
    album_dest = dest / pathlib.Path(f"{metadata[1]} - {metadata[0]}")
    try:
        album_dest.mkdir()
    except FileExistsError:
        proceed = input(f"\"{album_dest}\" already exists. Overwrite? (Y/N)")
        if proceed.lower() == "y":
            album_dest.mkdir(exist_ok=True)
        else:
            exit()
    
    command = f"cd \"{album_dest}\"; {utils.YT_DLP_COMMAND} {url}"
    ret = subprocess.run(command, capture_output=True, shell=True)