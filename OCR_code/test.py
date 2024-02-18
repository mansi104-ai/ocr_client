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

# Extract the tag and title from the text
first_line = text.split('\n')[0].strip()
last_word = first_line.split()[-1]  # Get the last word of the first line
tag = last_word
title = ' '.join(first_line.split()[:-1])  # Get all words except the last one

# Perform preprocessing to enhance text regions for contour detection
gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Find contours in the thresholded image
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Define lists to store left and right box contours
left_box_contours = []
right_box_contours = []

# Iterate through contours to detect left and right boxes in the header
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h
    
    # Define conditions to filter out boxes based on aspect ratio and position
    if aspect_ratio > 2 and aspect_ratio < 4 and y < 50:
        if x < 300:  # Adjust x-coordinate threshold as needed
            left_box_contours.append(contour)
        elif x > 500:  # Adjust x-coordinate threshold as needed
            right_box_contours.append(contour)

# Sort contours based on x-coordinate to ensure correct order
left_box_contours = sorted(left_box_contours, key=lambda x: cv2.boundingRect(x)[0])
right_box_contours = sorted(right_box_contours, key=lambda x: cv2.boundingRect(x)[0])

# Extract text from the left box (assuming one box is present)
left_box_text = ""
if left_box_contours:
    x, y, w, h = cv2.boundingRect(left_box_contours[0])
    left_box_roi = gray[y:y+h, x:x+w]
    left_box_text = pytesseract.image_to_string(left_box_roi, config=custom_config)

# Extract text from the right box (assuming one box is present)
right_box_text = ""
if right_box_contours:
    x, y, w, h = cv2.boundingRect(right_box_contours[0])
    right_box_roi = gray[y:y+h, x:x+w]
    right_box_text = pytesseract.image_to_string(right_box_roi, config=custom_config)

# Create a dictionary to store the extracted information
extracted_info = {
    "tag": tag,
    "title": title.strip(),
    # "left_box_text": left_box_text.strip(),
    # "right_box_text": right_box_text.strip(),
    "text": text.strip()
}

# Define the output JSON file path
output_file_path = "extracted_info.json"

# Write the extracted information to a JSON file
with open(output_file_path, "w") as json_file:
    json.dump(extracted_info, json_file, indent=4)

print(f"Extracted information has been stored in {output_file_path}")
