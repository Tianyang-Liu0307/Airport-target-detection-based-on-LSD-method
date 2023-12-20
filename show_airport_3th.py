import cv2
import numpy as np
import time

# Record the start time
start_time = time.time()

# Load your binary image with extracted straight lines
image_path = 'canvas_56.jpg'
binary_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)


def count_connected_components(image):
    # Convert the image to grayscale if it's not already
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get a binary image
    _, binary = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)

    # Find the connected components
    num_labels, _, _, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    return num_labels

def process_image():

    # Initialize the variable to keep track of the number of connected components for each radius
    num_components_for_radius = []

    # Try different radii for the dilation
    for radius in range(1, 50):  # you might need to adjust the range depending on your specific case
        # Create a circular structuring element for the dilation
        structuring_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*radius+1, 2*radius+1))

        # Dilate the binary image
        dilated_image = cv2.dilate(binary_image, structuring_element)

        # Count the number of connected components in the dilated image
        num_components = count_connected_components(dilated_image)

        # Append the number of connected components to the list
        num_components_for_radius.append(num_components)

    # Find the radius that gives the minimum number of connected components
    optimal_radius = np.argmin(num_components_for_radius) + 1  # add 1 because radius starts from 1

    return optimal_radius

def find_minimum_bounding_quadrilateral(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a mask for non-white pixels (assuming white is (255, 255, 255) in BGR)
    non_white_mask = cv2.inRange(gray_image, 0, 254)

    # Find contours based on the mask
    contours, _ = cv2.findContours(non_white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour based on the area
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the minimum area bounding rectangle for the largest contour
    rect = cv2.minAreaRect(largest_contour)

    # Get the corner points of the bounding box
    box = cv2.boxPoints(rect)
    box = np.int0(box)  # Convert to integer

    return box

if binary_image is None:
    print("Image not found.")
else:
    # Define the expansion radius
    optimal_radius = process_image()
    expansion_radius = optimal_radius  # Adjust this value as needed
    print('Optimal radius:', optimal_radius)
    # Create a kernel for morphological operations
    kernel = np.ones((2 * expansion_radius + 1, 2 * expansion_radius + 1), np.uint8)

    # Perform morphological operations to expand the lines
    expanded_image = cv2.dilate(binary_image, kernel)
    #cv2.imshow('Expanded Result', expanded_image)
    #cv2.waitKey(0)
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
        bounding_quadrilateral = find_minimum_bounding_quadrilateral(result)
        result = cv2.drawContours(original_image, [bounding_quadrilateral], 0, (0, 255, 0), 2)
        # Calculate and print the total execution time
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total execution time: {total_time:.4f} seconds")
        # Display the result
        cv2.imshow('Target', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('Target.jpg', result)
