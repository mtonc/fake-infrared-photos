#!/bin/python3

import os
import argparse
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse

def parse_args() -> dict:
 parser = argparse.ArgumentParser()
 parser.add_argument('-b','--band', help='The band you want to isolate', choices=['R','G','B'], default='R')
 group = parser.add_mutually_exclusive_group()
 group.add_argument('-f', '--filename', help='file name to process')
 group.add_argument('-u', '--url',help='url of image to process')
 group.add_argument('-d','--directory',help='folder of images to process')
 return parser.parse_args()

def process_file(file: str) -> list[Image]:
  if not file:
    return
  exists : bool = os.path.isfile(file)
  if exists:
    im : Image = Image.open(file)
    return [im]

def process_dir(folder: str) -> list[Image]:
  if not folder:
    return
  exists: bool = os.path.isdir(folder)
  if exists:
    files: list[str] = os.listdir(folder)
    # remove .DS_Store
    try:
      index : int = files.index('.DS_Store')
      files.pop(index)
    # Do nothing if not there
    except:
      pass
    images: list[Image] = []
    for f in files:
      images.append(Image.open(folder + f))
  return images

def process_url(url: str) -> list[Image]:
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
  }
  parsed = urlparse(url);
  path = parsed[2] # url path
  filename = os.path.basename(path)
  response: requests.response = requests.get(url, headers=headers)
  if response.status_code == 200:
    im : Image = Image.open(BytesIO(response.content))
    response.close()
    im.filename = filename
  return [im]

def process(images: list[Image], band: str):
  for img in images:
    try:
      path = os.path.dirname(img.filename)
      print(path)
      filename = os.path.basename(img.filename)
      print(filename)
      name, ext = os.path.splitext(filename)
      print(f"name: {name} extension: {ext}")
      # make sure we can select the red channel
      if img.mode == 'RGB' or img.mode == 'RGBA':
        channel = img.getchannel(band)
        # convert to grayscale
        channel.convert('L')
        print(os.path.join(path, name + '_' + band, ext))
        channel.save(os.path.join(path, name + '_' + band + ext))
      else:
        continue
    except:
      print(f"Error processing {img.filename}")


def main():
  args :dict = parse_args()
  band = args.band
  filename = args.filename
  directory = args.directory
  url = args.url
  if filename:
    process(process_file(filename), band)
    return
  if directory:
    process(process_dir(directory), band)
    return
  if url:
    process(process_url(url), band)
    return 

if __name__ == "__main__":
  main()  