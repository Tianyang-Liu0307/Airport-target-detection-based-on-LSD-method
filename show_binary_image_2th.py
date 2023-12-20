import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = 'airport-001-0056.jpg'
image = cv2.imread(image_path)

if image is None:
    print("Image not found.")
else:
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect lines using LSD
    lsd = cv2.createLineSegmentDetector(0)
    lines, _, _, _ = lsd.detect(gray_image)

    # Initialize variables to store line lengths and categories
    category_lengths = [0] * 90

    # Categorize and sum the line lengths
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1)
        angle_degrees = np.degrees(angle)
        category = int(angle_degrees // 2)  # Convert angle to degrees and round to the nearest integer
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        category_lengths[category] += length

    # Find the longest line
    longest_category = np.argmax(category_lengths)
    longest_length = np.max(category_lengths)

    # Display the length of the longest line and its category on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, f"Longest Line: {longest_length:.2f} pixels", (20, 20), font, 0.5, (255, 255, 255), 1)
    cv2.putText(image, f"Category: {longest_category}", (20, 40), font, 0.5, (255, 255, 255), 1)
    
    # Create a black canvas with the same size as the original image
    canvas = np.zeros_like(image, dtype=np.uint8)

    # Iterate through lines to display lines with the target angle
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if int((angle + 180) // 2) == longest_category:
            image = lsd.drawSegments(image, line)
            canvas = lsd.drawSegments(canvas, line)
    # Show the image
    cv2.imshow('Image with Line Info', image)
    cv2.imshow('Canvas', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('image_with_line_info_56.jpg', image)
    cv2.imwrite('canvas_56.jpg', canvas)