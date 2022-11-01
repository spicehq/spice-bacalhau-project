import io
import json
import math
import os
import pickle

from PIL import Image
import requests
from web3 import Web3


def extract_image_uri(metadata):
    if "image" in metadata:
        return metadata["image"]
    raise RuntimeError("Image not found in metadata")


def format_image(image: Image, min_size: int):
    factor = min(image.size) / min_size
    new_size = (round(image.size[0] / factor), round(image.size[1] / factor))
    image = image.resize(new_size).convert("RGB")

    # Crop to square
    left = (new_size[0] - min_size)/2
    top = (new_size[1] - min_size)/2
    right = (new_size[0] + min_size)/2
    bottom = (new_size[1] + min_size)/2
    image = image.crop((left, top, right, bottom))

    return image


def make_collage(images, num_cols):
    image_width, image_height = images[0].size
    num_rows = int(math.ceil(len(images) * 1.0 / num_cols))
    collage=Image.new('RGB', (num_cols * image_width, num_rows * image_height))

    i = 0
    x = 0
    y = 0
    for i, img in enumerate(images):
        x = (i % num_cols) * image_width
        y = (i // num_cols) * image_height
        collage.paste(images[i], (x, y))

    return collage

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run job to download and process NFT metadata and images')
    parser.add_argument('operation', type=str)
    parser.add_argument('--input-dir', default="/inputs", type=str)
    parser.add_argument('--output-dir', default="/outputs", type=str)
    
    args = parser.parse_args()

    if args.operation == "parse_metadata":
        image_uris = []
        for file in os.scandir(args.input_dir):
            if file.is_dir():
                continue
            with open(file.path, "r") as f:
                image_uris.append(extract_image_uri(json.load(f)))
        
        with open(f"{args.output_dir}/image_uris.pkl", "wb") as f:
            pickle.dump(image_uris, f)

    elif args.operation == "create_collage":
        images = []
        for file in os.scandir(args.input_dir):
            with open(file.path, "rb") as f:
                try:
                    image = Image.open(f)
                    images.append(format_image(image, 512))
                except:
                    pass
        
        collage = make_collage(images, 4)
        collage.save(f"{args.output_dir}/collage.jpg")

    else:
        raise RuntimeError(f"Unknown operation {args.operation}")

    print("Job finished successfully!")
