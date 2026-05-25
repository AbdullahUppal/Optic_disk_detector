from dotenv import load_dotenv
import os

load_dotenv()

FUNDUS_IMAGES_PATH=os.getenv("FUNDUS_IMAGES_PATH")
VESSEL_STRUCTURE_PATH=os.getenv("VESSEL_STRUCTURE_PATH")
RESULT_CSV_PATH=os.getenv("RESULT_CSV_PATH")
RESULT_PATH = os.getenv("RESULT_PATH")