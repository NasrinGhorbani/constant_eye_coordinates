import os
from PIL import Image

# Path to the directory containing the images
input_dir = 'files'

# Output directory to save the converted images
output_dir = 'files_jpg'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    img_path = os.path.join(input_dir, filename)
    
    # Check if the file is not a directory
    if os.path.isfile(img_path):
        # Check if the file is not already in JPEG format
        if not filename.lower().endswith('.jpg'):
            # Load the image
            img = Image.open(img_path)
            
            # Change the file extension to '.jpg'
            new_filename = os.path.splitext(filename)[0] + '.jpg'
            output_path = os.path.join(output_dir, new_filename)
            
            # Save the image in JPEG format
            img.save(output_path, 'JPEG')
            print(f"Converted {filename} to {new_filename}")
        else:
            # Copy the image to the output directory as is (already in JPEG format)
            new_path = os.path.join(output_dir, filename)
            os.rename(img_path, new_path)
            print(f"Image {filename} is already in JPEG format. Copied as is.")
    else:
        print(f"Skipping directory: {filename}")

print("Conversion complete!")
