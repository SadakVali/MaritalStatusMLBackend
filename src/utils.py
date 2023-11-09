import os
import sys
import dill
from deepface import DeepFace
from src.constants import *
import numpy as np 

from src.exception import CustomException


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


def face_enc_and_coordinates_with_df(img_path):
    representation = DeepFace.represent(
        img_path=img_path,
        model_name=MODEL_NAME,
        normalization=NORMALIZATION,
        detector_backend=DETECTOR_BACKEND,
        align=True,
        enforce_detection=True,
    )[0]
    face_coordinates = representation["facial_area"]
    face_enc = representation["embedding"]
    face_enc = np.array(face_enc, dtype="f")
    # Extracting the coordinates and dimensions
    left = face_coordinates['x']
    top = face_coordinates['y']
    right = left + face_coordinates['w']
    bottom = top + face_coordinates['h']
    return [face_enc, (top, right, bottom, left)]