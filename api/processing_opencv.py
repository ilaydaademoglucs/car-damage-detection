import cv2
import imutils
import numpy as np


def process_images(image1: np.ndarray, image2: np.ndarray) -> np.ndarray:
    # Resize images if necessary
    img1 = cv2.resize(image1, (600, 360))
    img2 = cv2.resize(image2, (600, 360))

    img_height = img1.shape[0]

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate absolute difference
    diff = cv2.absdiff(gray1, gray2)

    # Apply threshold
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Dilation
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Calculate contours
    contours = cv2.findContours(
        dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = imutils.grab_contours(contours)

    # Draw bounding boxes around differences
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Concatenate the images with differences marked
    x = np.zeros((img_height, 10, 3), np.uint8)
    result = np.hstack((img1, x, img2))

    return result
