# imports from the packages
from pathlib import Path

# DeepFace library constants
MODEL_NAME = "ArcFace" 
DETECTOR_BACKEND = "mtcnn" 
NORMALIZATION = "ArcFace"
TARGET_SIZE = (112, 112) 
NUM_OF_DIMS = 512 

# Given input dataset
INPUT_DATASET = Path("data/CleanData/")

# Paths to save pickel files
DB_FACE_PATHS_PATH = "artifacts/DB_FACE_PATHS.pickle"
FAISS_INDEXING_OBJ_PATH = "artifacts/FAISS_INDEXING_OBJ.pickle"
DB_FACE_COORDINATES_PATH = "artifacts/DB_FACE_COORDINATES.pickle"

# allowed image file types in our API end point 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}