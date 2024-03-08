import cv2
import numpy as np
import json

# Function to detect and analyze circles
def detect_and_analyze_circles(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Define the region of interest (bottom 10% of the image)
    height, width = image.shape[:2]
    roi_height = int(height * 0.9)
    roi = gray[roi_height:, :]  # Selecting the bottom 10% of the image

    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=30)
    
    circle_data = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        # Iterate through detected circles
        for circle in circles[0, :]:
            x, y, r = circle
            
            # Define the region of interest around the circle
            circle_roi = gray[roi_height + y - r:roi_height + y + r,
                               x - r:x + r]
            
            # Threshold the region of interest to find marks
            _, threshold = cv2.threshold(circle_roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Check if there are any marks
            marked = len(contours) > 0
            
            # Append circle data to the list
            circle_data.append({"x": int(x), "y": int(y), "radius": int(r), "marked": marked})
            
            # Draw contour box around the circle
            cv2.circle(image, (x, roi_height + y), r, (0, 255, 0), 2)

    return circle_data, image

# Load the image
image = cv2.imread('lined_final_edited.jpg') 

# Detect and analyze circles in the bottom 10% of the page
circle_data, image_with_contours = detect_and_analyze_circles(image.copy())

# Write the circle data to a JSON file
output_file_path = "circle_data.json"
with open(output_file_path, "w") as json_file:
    json.dump(circle_data, json_file, indent=4)

print(f"Circle data has been stored in {output_file_path}")

# Display the image with contour boxes around the circles
cv2.imshow("Image with Contours", image_with_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()
