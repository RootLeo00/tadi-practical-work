import argparse
from PIL import Image
import os

def resize_images(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all files in the input directory
    files = os.listdir(input_dir)

    # Iterate through the files and resize the PNG images
    for file in files:
        if file.lower().endswith(".png"):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file)

            # Open the image
            image = Image.open(input_path)

            # Get the original width and height
            original_width, original_height = image.size

            # Calculate the new width and height (one-third of the original size)
            new_width = original_width // 2
            new_height = original_height // 2

            # Resize the image
            image = image.resize((new_width, new_height), Image.ANTIALIAS)

            # Save the resized image
            image.save(output_path, "PNG")

            print(f"Resized: {file} -> {new_width}x{new_height}")

    print("Resizing complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize PNG images in a directory")
    parser.add_argument("input_directory", help="Path to the input directory")
    parser.add_argument("output_directory", help="Path to the output directory")
    args = parser.parse_args()

    input_directory = args.input_directory
    output_directory = args.output_directory

    resize_images(input_directory, output_directory)
