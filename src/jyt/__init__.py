__all__ = ['bandcamp', 'network', 'utils']

import argparse
import logging
import importlib.metadata
import pathlib
import subprocess
import urllib.parse

import bs4
import requests

from . import bandcamp
from . import network
from . import utils

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.root.setLevel(logging.INFO)

__version__ = importlib.metadata.version("jyt")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL for audio source")
    parser.add_argument("--dest", help="destination directory path", default=".")
    parser.add_argument("-v", "--version",        
        action="version",     
        version=f"%(prog)s {__version__}" 
    )
    args = parser.parse_args()
    
    url_parts = urllib.parse.urlsplit(args.url)
    
    dest = pathlib.Path(args.dest)
    
    # check if net location is bandcamp
    if network.NET_LOCS.BANDCAMP in url_parts.netloc:
        logging.info(f"bandcamp url found: \"{args.url}\"")
        # if url starts with album, then its an album
        if url_parts.path.startswith("/album"):
            logging.info(f'bandcamp album detected in url: \"{args.url}\"')
            bandcamp.download_album(args.url, dest)
        # if url starts with music or has empty path, then its a discography
        elif url_parts.path.startswith("/music") or url_parts.path == "/":
            logging.info(f'bandcamp discography detected in url: \"{args.url}\"')
            bandcamp.download_discography(args.url, dest)
    # check if net location is youtube
    elif network.NET_LOCS.YOUTUBE in url_parts.netloc:
        logging.info(f"youtube url found: \"{args.url}\"")
        command = f"cd \"{dest}\"; {utils.YT_DLP_COMMAND} {args.url}"
        ret = subprocess.run(command, capture_output=True, shell=True)
    # for all else
    else:
        logging.info(f"unknown net location for url: \"{args.url}\"")
        command = f"cd \"{dest}\"; {utils.YT_DLP_COMMAND} {args.url}"
        ret = subprocess.run(command, capture_output=True, shell=True)
    
        

if __name__ == "__main__":
    main()
