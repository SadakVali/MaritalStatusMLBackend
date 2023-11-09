# imports from packages
import os
import sys
import faiss
import numpy as np
from tqdm import tqdm

# imporst from my own code base
from src.logger import logging
from src.exception import CustomException

# imports from the utility functions
from src.utils import face_enc_and_extract_face_coordinates_with_df_lib, save_object

# imports assets/constants
from src.constants import *


class TrainingPipeline:
    def creating_face_paths_list(self):
        self.DB_FACE_PATHS = []
        try:
            logging.info("collecting all face image paths from input dataset")
            # for each input image path 
            for person_name in os.listdir(INPUT_DATASET):
                for img_name in os.listdir(INPUT_DATASET / person_name):
                    img_path = str(INPUT_DATASET / person_name / img_name)
                    self.DB_FACE_PATHS.append(img_path)
            logging.info("collecting all face image paths completed")
            # save the DB_FACE_PATHS to be used in the prediction pipeline
            save_object(DB_FACE_PATHS_PATH, self.DB_FACE_PATHS)
            logging.info("image paths object saved to path: ", DB_FACE_PATHS_PATH)
        except Exception as e:
            raise CustomException(e, sys)

    def creating_face_encodings_and_coordinates(self):
        self.DB_FACE_ENC, DB_FACE_COORDINATES = [], []
        try:
            logging.info("Extracting the Face Bounding Box Coordinates and Face Encodings")
            # for each input face image path
            for img_path in tqdm(self.DB_FACE_PATHS):
                result = face_enc_and_extract_face_coordinates_with_df_lib(img_path)
                [encoding, coordinates] = result
                self.DB_FACE_ENC.append(encoding)
                DB_FACE_COORDINATES.append(coordinates)
            # save the DB_FACE_COORDINATES to be used in the prediction pipeline
            save_object(DB_FACE_COORDINATES_PATH, DB_FACE_COORDINATES)
            logging.info("face bounding box coordinates object saved to path: ", DB_FACE_COORDINATES_PATH)
        except Exception as e:
            raise CustomException(e, sys)

    def creating_FAISS_indexing_obj(self):
        try:
            logging.info("starting the indexing face encodings with FAISS librarry")
            embeddings = np.array(self.DB_FACE_ENC, dtype='f')
            # using cosine similarity for similarity search
            FAISS_INDEXING_OBJ = faiss.IndexFlatIP(NUM_OF_DIMS) 
            faiss.normalize_L2(embeddings)
            # adding complete database for indexing with FAISS
            FAISS_INDEXING_OBJ.add(embeddings)
            # save the FAISS object
            save_object(FAISS_INDEXING_OBJ_PATH, FAISS_INDEXING_OBJ)
            logging.info("FAISS encoding object save to the path: ", FAISS_INDEXING_OBJ_PATH)
        except Exception as e:
            raise CustomException(e, sys)



if __name__ == "__main__":
    training = TrainingPipeline()
    training.creating_face_paths_list()
    training.creating_face_encodings_and_coordinates()
    training.creating_FAISS_indexing_obj()
