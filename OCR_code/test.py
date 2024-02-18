import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import json


# Open the image
image = Image.open('lined_final_edited.jpg')

# Perform OCR
custom_config = r'--oem 3 --psm 6'  # custom configurations
text = pytesseract.image_to_string(image, config=custom_config)

# Find the date in the format xx/xx/xxxx or xx/xx/xx
date_match = re.search(r'\b(\d{1,2}\/\d{1,2}\/\d{2,4})\b', text)
date_str = date_match.group(1) if date_match else "Not found"

# Create a dictionary to store the extracted information
extracted_info = {
    "date": date_str,
    "text": text
}

# Define the output JSON file path
output_file_path = "extracted_info.json"

# Write the extracted information to a JSON file
with open(output_file_path, "w") as json_file:
    json.dump(extracted_info, json_file, indent=4)

print(f"Extracted information has been stored in {output_file_path}")
