import os
import sys
import numpy as np
import face_recognition
from deepface import DeepFace
import cv2
import pickle

from src.constants import *
from src.exception import CustomException

from src.utils import face_enc_and_coordinates_with_df, load_object

class PredictPipeline:
    def __init__(self):
        self.FAISS_INDEXING_OBJ = load_object(FAISS_INDEXING_OBJ_PATH)
        self.DB_FACE_PATHS = load_object(DB_FACE_PATHS_PATH)
        self.DB_FACE_COORDINATES = load_object(DB_FACE_COORDINATES)

    def read_img_bgr_mode(self, file):
        file = file.read()
        nparr = np.fromstring(file, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img_bgr
    
    def face_encodings(self, image_arr, known_face_locations):
        img_enc = face_recognition.face_encodings(
            face_image = image_arr, 
            known_face_locations = known_face_locations, 
            num_jitters = 1, 
            model = 'large', 
        )[0]
        return img_enc 

    def path_dis_processing(self, neighbour_idxs, distances):
        neighbour_idx_dis_dic = dict(zip(neighbour_idxs, distances))
        neighbour_idx_dis_pairs_sorted_in_asc_ord = list(sorted(
            neighbour_idx_dis_dic.items(), 
            key = lambda idx_dis: idx_dis[1],
            reverse = False  
        )) 
        neighbour_img_path_dis_pairs_sorted_in_asc_ord = [
            [self.DB_FACE_PATHS[idx_dis_pair[0]], idx_dis_pair[-1]]
            for idx_dis_pair in neighbour_idx_dis_pairs_sorted_in_asc_ord
        ]
        return neighbour_img_path_dis_pairs_sorted_in_asc_ord[1:] 

    def top_4_matching_faces(self, neighbour_img_path_dis_pairs_sorted_in_asc_ord):
        entry_flag_dic = dict()
        result = []
        for neigh_img_path, dis in neighbour_img_path_dis_pairs_sorted_in_asc_ord:
            if os.path.dirname(neigh_img_path).split("/")[-1] not in entry_flag_dic:
                entry_flag_dic[neigh_img_path.split("/")[-2]] = True
                # result.append([neigh_img_path, dis])
                result.append(neigh_img_path)
        return result[:4] 

    def face_enc_with_fr(self, img_path, known_face_locations):
        image_arr = face_recognition.load_image_file(img_path)
        img_enc = face_recognition.face_encodings(
            model='large', 
            face_image=image_arr, 
            known_face_locations=[known_face_locations], 
            num_jitters=1, 
        )[0]
        return img_enc 

    def gathering_the_surrounding_known_faces(self, neighbour_idxs):
        known_faces = []
        for neigh_idx in neighbour_idxs:
            neigh_img_path = self.DB_FACE_PATHS[neigh_idx]
            known_face_locations = self.DB_FACE_COORDINATES[neigh_idx]
            neigh_img_enc = self.face_enc_with_fr(
                neigh_img_path, 
                known_face_locations=known_face_locations
            )
            known_faces.append(neigh_img_enc)
        return known_faces

    def predict(self, file, k = 10):
        try:
            target_bgr = self.read_img_bgr_mode(file)
            # embedding the face
            [tar_enc, tar_coordinates] = face_enc_and_coordinates_with_df(target_bgr) 
            tar_enc = np.expand_dims(tar_enc, axis=0)
            # extracting the closest k embedding indexes
            distances, neighbour_idxs = self.FAISS_INDEXING_OBJ.search(tar_enc, k)
            neighbour_idxs, distances = neighbour_idxs[0], distances[0]
            # gather the surrounding known faces
            known_faces = self.gathering_the_surrounding_known_faces(neighbour_idxs)
            # calculating the distance between the target face and the closest k faces
            tar_enc = self.face_enc_with_fr(
                file, 
                known_face_locations=tar_coordinates
            )
            distances = face_recognition.face_distance(
                face_encodings=known_faces, 
                face_to_compare=tar_enc
            )
            # processing the image path and distance from target in ascending order
            neighbour_img_path_dis_pairs_sorted_in_asc_ord = self.path_dis_processing(
                neighbour_idxs, 
                distances
            )
            return self.top_4_matching_faces(neighbour_img_path_dis_pairs_sorted_in_asc_ord)
        except Exception as e:
            raise CustomException(e, sys)
        