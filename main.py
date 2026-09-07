import argparse
import pathlib
import subprocess
import urllib.parse

import bs4
import requests

import bandcamp
import network

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
            bandcamp.download_album(args.url, dest)
        elif url_parts.path.starswith("/music"):
            # get bandcamp page
            page = requests.get(args.url)
            soup = bs4.BeautifulSoup(page.content, "html.parser")
            
        
    
    print(url_parts)

if __name__ == "__main__":
    main()
