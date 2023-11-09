from pathlib import Path

MODEL_NAME = "ArcFace" 
DETECTOR_BACKEND = "mtcnn" 
NORMALIZATION = "ArcFace"

TARGET_SIZE = (112, 112) 
NUM_OF_DIMS = 512 

DESTINATION = Path("data/CleanData/")

FAISS_INDEXING_OBJ_PATH = "artifacts/FAISS_INDEXING_OBJ.pickle"
DB_FACE_PATHS_PATH = "artifacts/DB_FACE_PATHS.pickle"
DB_FACE_COORDINATES = "artifacts/DB_FACE_COORDINATES.pickle"
