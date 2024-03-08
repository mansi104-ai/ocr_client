import cv2
import numpy as np
import os
import json

def extract_drawing(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area to remove noise
    min_contour_area = 100  # Adjust as needed
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    
    # Draw contours on a blank canvas
    drawing_contours = np.zeros_like(gray)
    cv2.drawContours(drawing_contours, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
    
    # Apply bitwise AND to extract the drawing region
    drawing = cv2.bitwise_and(gray, drawing_contours)
    
    # Save the extracted drawing
    drawing_path = os.path.join("extracted_drawing.png")
    cv2.imwrite(drawing_path, drawing)
    
    # Store information about the extraction
    info = {
        "original_image": image_path,
        "extracted_drawing": drawing_path,
        "num_contours": len(contours)
    }
    with open("extraction_info.json", "w") as f:
        json.dump(info, f, indent=4)

# Example usage
image_path = "lined_final_edited.jpg"
extract_drawing(image_path)
