import cv2
import numpy as np


def is_image_stock(image_path: str) -> bool:
    """
    Checks if a given image is stock image which could be displayed on a website. The idea is that
    such an image would have a uniform background and a single object in the foreground.
    @param image_path: The path to the image file to check
    @return: True if the image is a stock image, False otherwise
    """
    image = cv2.imread(image_path)
    upper_left_pixel = image[0, 0]
    number_same_colored_pixels: int = np.sum(np.all(image == upper_left_pixel, axis=-1))
    return (number_same_colored_pixels / image.size) > 0.2
