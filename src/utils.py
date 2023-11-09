# imports from the packages
import os
import sys
import dill
import numpy as np 
from src.constants import *
from deepface import DeepFace

# imports from my own code base
from src.exception import CustomException

# importing the assets/constants
from src.constants import *

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def process_face_coordinates_for_face_rec_lib(face_coordinates):
    # Extracting the coordinates
    left = face_coordinates['x']
    top = face_coordinates['y']
    right = left + face_coordinates['w']
    bottom = top + face_coordinates['h']
    return (top, right, bottom, left)


def face_enc_and_extract_face_coordinates_with_df_lib(img_path):
    representation = DeepFace.represent(
        img_path=img_path,
        model_name=MODEL_NAME,
        normalization=NORMALIZATION,
        detector_backend=DETECTOR_BACKEND,
        align=True,
        enforce_detection=True)[0]
    # extracting the face encoding
    face_enc = np.array(representation["embedding"], dtype="f")
    # extracting the face bounding box coordinates
    face_coordinates = process_face_coordinates_for_face_rec_lib(
        representation["facial_area"])
    return [face_enc, face_coordinates]


def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
