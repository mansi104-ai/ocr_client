import cv2
import numpy as np
import pytesseract
import json
import random

# Function to perform OpenCV preprocessing on the image
def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to enhance text regions
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Perform dilation and erosion to further enhance text regions
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.dilate(threshold,kernel,iterations = 1)
    erode = cv2.erode(dilate,kernel,iterations = 1)
    
    return erode
'''
# Function to extract text from a box with specified tag and return in JSON format
def extract_text_from_box(image, tag):
    # Perform OCR on the image
    custom_config = r'--oem 3 --psm 6'  # custom configurations
    results = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)

    # Find the bounding box of the box with the specified tag
    for i, text in enumerate(results['text']):
        if text.lower() == tag:
            x, y, w, h = results['left'][i], results['top'][i], results['width'][i], results['height'][i]
            # Extract text from the specified box
            cropped_image = image[y:y+h, x:x+w]
            text = pytesseract.image_to_string(cropped_image, config=custom_config)

            # Print the extracted text
            print(f"Text extracted from '{tag}' box: {text.strip()}")

            # Convert the extracted text to JSON format
            json_data = {tag: text.strip()}
            return json_data
    
    # Handle case where tag is not found
    return {tag: "Tag not found"}'''

# Function to extract text from the body of the page and return in JSON format
def extract_text_from_body(image):
    # Perform OCR on the image
    custom_config = r'--oem 3 --psm 6'  # custom configurations
    text = pytesseract.image_to_string(image, config=custom_config)

    # Print the extracted text
    print("Text extracted from the body:")
    print(text)

    # Convert the extracted text to JSON format
    json_data = {"body_text": text.strip()}
    
    return json_data
'''
# Function to extract text between two hashes "#" and draw a contour box around it
def extract_text_between_hashes(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to enhance text regions
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through contours and draw a contour box around the text between two hashes "#"
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        
        # Crop the region between hashes and save as a separate image
        cropped_image = image[y:y+h, x:x+w]
        cv2.imwrite('cropped_image.jpg', cropped_image)
    
    return image

# Function to detect and analyze circles at the footer of the page
def detect_and_analyze_circles(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=30)
    
    circle_data = {}
    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        # Label the circles and check for ticks, crosses, or no markings
        for i, circle in enumerate(circles[0, :]):
            label = f"circle_{i+1}"
            x, y, r = circle
            
            # Check for ticks, crosses, or no markings
            roi = gray[y-r:y+r, x-r:x+r]
            _, threshold = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                # Check if there's a tick or cross
                area = cv2.contourArea(contours[0])
                if area > 0.8 * (2 * r) * (2 * r):
                    circle_data[label] = "tick"
                else:
                    circle_data[label] = "cross"
            else:
                circle_data[label] = "no"
    
    # Convert the circle data to JSON format
    json_data = {"circle_data": circle_data}
    
    return json_data
'''
# Load the image
image = cv2.imread('lined_final_edited.jpg')  # Change the image filename here

# Preprocess the image
preprocessed_image = preprocess_image(image)

# # Print the text extracted from the body of the page
json_body = extract_text_from_body(preprocessed_image)

# # Extract text from the topmost left box with tag "title" and print
# json_title = extract_text_from_box(preprocessed_image, "title")

# # Extract text from the top right box with tag "tag" and print
# json_tag = extract_text_from_box(preprocessed_image, "tag")

# # Extract text between hashes "#" and draw contour boxes around them
# image_with_contours = extract_text_between_hashes(image.copy())

# # Detect and analyze circles at the footer of the page and print
# json_circle_data = detect_and_analyze_circles(image)

# # Combine all JSON data
json_data= {**json_body}
# json_data = {**json_title, **json_tag, **json_body, **json_circle_data}

# # Convert the JSON data to a string
# json_string = json.dumps(json_data, indent=4)

# Print the JSON string
print("JSON Data:")
print(json_data)

# Send the JSON string to text.py for further processing
# (Assuming there's a function in text.py to receive the JSON string)
#text.py_process(json_string)
