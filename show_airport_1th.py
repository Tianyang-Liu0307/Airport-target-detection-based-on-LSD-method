import cv2
import numpy as np
import time

# Record the start time
start_time = time.time()

# Load your binary image with extracted straight lines
image_path = 'canvas_56.jpg'
binary_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if binary_image is None:
    print("Image not found.")
else:
    # Define the expansion radius
    expansion_radius = 50  # Adjust this value as needed

    # Create a kernel for morphological operations
    kernel = np.ones((2 * expansion_radius + 1, 2 * expansion_radius + 1), np.uint8)

    # Perform morphological operations to expand the lines
    expanded_image = cv2.dilate(binary_image, kernel)

    # Perform connected component analysis with statistics to label connected regions in the expanded image
    _, labels, stats, _ = cv2.connectedComponentsWithStats(expanded_image, connectivity=4)

    # Find the index of the largest connected component based on area (last column in stats)
    largest_component_index = np.argmax(stats[1:, -1]) + 1  # Exclude background label (index 0)

    # Create an image to display the result
    result_image = np.zeros_like(expanded_image)

    # Copy only the lines that belong to the largest connected component
    result_image[labels != largest_component_index] = 255  # Set to white

    # Overlay the retained straight lines on the original image
    original_image_path = 'airport-001-0056.jpg'
    original_image = cv2.imread(original_image_path)

    if original_image is None:
        print("Original image not found.")
    else:
        retained_lines = cv2.cvtColor(result_image, cv2.COLOR_GRAY2BGR)
        result = cv2.addWeighted(original_image, 1, retained_lines, 1, 0)

        # Calculate and print the total execution time
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total execution time: {total_time:.4f} seconds")
        # Display the result
        cv2.imshow('Result with Retained Straight Lines', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('result_with_retained_straight_lines.jpg', result)
