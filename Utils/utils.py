import cv2
import os

def save_images(image_dir, count, img):
    # Create directories to save images
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    image_path = os.path.join(image_dir, f"image_{count:04d}.png")
    cv2.imwrite(image_path, img)