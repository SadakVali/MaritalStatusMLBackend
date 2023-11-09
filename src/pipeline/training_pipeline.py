import os
from tqdm import tqdm
from src.exception import CustomException
import pickle 
from src.utils import face_enc_and_coordinates_with_df
from src.constants import *
import numpy as np
import faiss


class TrainingPipeline:
    def __init__(self):
        pass

    def creating_face_paths_list(self):
        self.DB_FACE_PATHS = []
        for person_name in os.listdir(DESTINATION):
            for img_name in os.listdir(DESTINATION / person_name):
                self.DB_FACE_PATHS.append(str(DESTINATION / person_name / img_name))
        with open("artifacts/DB_FACE_PATHS.pickle", 'wb') as handle:
            pickle.dump(self.DB_FACE_PATHS, handle, protocol = pickle.HIGHEST_PROTOCOL) 

    def creating_face_encodings_and_coordinates(self):
        self.DB_FACE_ENC = []
        DB_FACE_COORDINATES = []
        for img_path in tqdm(self.DB_FACE_PATHS):
            [encoding, coordinates] = face_enc_and_coordinates_with_df(img_path)
            self.DB_FACE_ENC.append(encoding)
            DB_FACE_COORDINATES.append(coordinates)
        with open("artifacts/DB_FACE_ENC.pickle", "wb") as handle:
            pickle.dump(self.DB_FACE_ENC, handle, protocol = pickle.HIGHEST_PROTOCOL)
        with open("artifacts/DB_FACE_COORDINATES.pickle", "wb") as handle:
            pickle.dump(DB_FACE_COORDINATES, handle, protocol = pickle.HIGHEST_PROTOCOL)

    def creating_FAISS_indexing_obj(self):
        embeddings = np.array(self.DB_FACE_ENC, dtype='f')
        FAISS_INDEXING_OBJ = faiss.IndexFlatIP(NUM_OF_DIMS) # cosine
        faiss.normalize_L2(embeddings)
        FAISS_INDEXING_OBJ.add(embeddings)
        with open(f'artifacts/FAISS_INDEXING_OBJ.pickle', 'wb') as handle:
            pickle.dump(FAISS_INDEXING_OBJ, handle, protocol = pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    obj = TrainingPipeline()
    obj.creating_face_paths_list()
    print("creating_face_paths_list ===> completed")
    obj.creating_face_encodings_and_coordinates()
    print("creating_face_encodings_and_coordinates ===> completed")
    obj.creating_FAISS_indexing_obj()
    print("creating_FAISS_indexing_obj ===> completed")
