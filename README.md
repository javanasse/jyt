# Julian's YouTube to Mp3 You-Tility (`jyt`)

I wrote this to help me archive audio files, maybe it could help you too!

## Installation

### Requirements

#### Python
`jyt` is a Python package and command line utility (CLI). You must have Python installed. To check that you have Python, open your Terminal and run 
```
python --version
```
If you see a version number, you're good! If not, install Python from [here](https://www.python.org/downloads/). 

### Install

The simplest way to install this tool is to run:
```
pip install git+https://github.com/javanasse/jyt 
```

If you don't see any errors, then check the installation was successful by running in your Terminal:
```
jyt --version
```
Which should print a version string.

## Usage

`jyt` is a simple tool to archive audio from internet sources. The simplest way to run:
```
jyt https://some-place.bandcamp.com/album/some-album
```
Where URL may be a link to a Youtube video or Bandcamp album. This will archive the album to the directory from which you ran the command. 

If you want to specify a destination directory, the syntax is:
```
jyt https://some-place.bandcamp.com/album/some-album --dest ~/Downloads
```
