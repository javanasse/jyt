import argparse
import logging
import pathlib
import subprocess
import urllib.parse

import bs4
import requests

import bandcamp
import network

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.root.setLevel(logging.NOTSET)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL for audio source")
    parser.add_argument("--dest", help="destination directory path", default=".")
    args = parser.parse_args()
    
    url_parts = urllib.parse.urlsplit(args.url)
    
    dest = pathlib.Path(args.dest)
    
    # check if net location is bandcamp
    if network.NET_LOCS.BANDCAMP in url_parts.netloc:
        # check if url starts with album
        if url_parts.path.startswith("/album"):
            logging.info(f'bandcamp discography detected in url: \"{args.url}\"')
            bandcamp.download_album(args.url, dest)
        elif url_parts.path.startswith("/music") or url_parts.path == "/":
            logging.info(f'bandcamp discography detected in url: \"{args.url}\"')
            # get bandcamp page
            page = requests.get(args.url)
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
                logging.warning(f'no releases found in url: \"{args.url}\"')
            
            # download each release
            for url in release_urls:
                logging.info(f"downloading release at url: \"{url}\"")
                bandcamp.download_album(url, dest)
                logging.info(f"download complete.")
            
        
    
    print(url_parts)

if __name__ == "__main__":
    main()
