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

    # Initialize variables to store line lengths in each category
    category_lengths = [0] * 180

    # Categorize and sum the line lengths
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1)
        angle_degrees = np.degrees(angle)
        category = int(angle_degrees)  # Convert angle to degrees and round to the nearest integer
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        category_lengths[category] += length

    # Create a bar chart to visualize the results
    angles = range(180)
    plt.bar(angles, category_lengths)
    plt.xlabel('Angle Category')
    plt.ylabel('Sum of Line Lengths')
    plt.title('Line Lengths by Angle Category')
    plt.show()
