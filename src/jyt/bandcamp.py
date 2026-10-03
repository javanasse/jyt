import logging
import pathlib
import os
import subprocess
import urllib

import bs4
import requests

from . import utils

def download_album(url, dest):
    # get bandcamp metadata
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    metadata = soup.find("title").text.split("|")
    metadata = [m.strip() for m in metadata]
    
    # create destination directory
    album_dest_dirname = f"{metadata[1]} - {metadata[0]}"
    album_dest_dirname = album_dest_dirname.replace(os.sep, "__")
    album_dest = dest / pathlib.Path(album_dest_dirname)
    
    command = f"cd \"{album_dest}\"; {utils.YT_DLP_COMMAND} {url}"
    
    try:
        album_dest.mkdir()
    except FileExistsError:
        proceed = input(f"\"{album_dest}\" already exists. Overwrite? (Y/N): ")
        if proceed.lower() == "y":
            album_dest.mkdir(exist_ok=True)
            logging.info(f"directory created: \"{album_dest.absolute()}\"")
        else:
            logging.info("dictory will not be overwritten.")
            return
    
    ret = subprocess.run(command, capture_output=True, shell=True)
    
def download_discography(url, dest):
    
    url_parts = urllib.parse.urlsplit(url)
    
    # get bandcamp page
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    
    # get urls 
    releases = soup.find_all("li", {"class": "music-grid-item square first-four"})
    releases += soup.find_all("li", {"class": "music-grid-item square"})
    release_urls = []
    if releases:
        for n, url in enumerate(releases):
            release_urls.append(
                urllib.parse.SplitResult(
                    scheme=url_parts.scheme,
                    netloc=url_parts.netloc,
                    path=releases[n].find('a').get('href'),
                    query="",
                    fragment=""
                ).geturl()
            )
    else:
        logging.warning(f'no releases found in url: \"{url}\"')
    
    # download each release
    for url in release_urls:
        logging.info(f"downloading release at url: \"{url}\"")
        download_album(url, dest)
        logging.info(f"download complete.")