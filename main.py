import cv2 as cv
import os
from constants import FUNDUS_IMAGES_PATH, VESSEL_STRUCTURE_PATH
from processing import main_process
from calculation import calculate_eclidean_error

if __name__ == "__main__":

    # Resize image is for testing when we want to display the image for testig
    RESIZE = 1

    retina_files = os.listdir(FUNDUS_IMAGES_PATH)
    vessel_files = os.listdir(VESSEL_STRUCTURE_PATH)

    for retina_file, vessel_file in zip(retina_files, vessel_files):
        img, cx, cy = main_process(retina_file, vessel_file, RESIZE)
        calculate_eclidean_error(retina_file, cx, cy)
        cv.imshow("image",img)
        cv.waitKey()
    

