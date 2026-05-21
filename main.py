import cv2 as cv
import os
from constants import FUNDUS_IMAGES_PATH, VESSEL_STRUCTURE_PATH




if __name__ == "__main__":
    retina_files = os.listdir(FUNDUS_IMAGES_PATH)
    vessel_files = os.listdir(VESSEL_STRUCTURE_PATH)


    

