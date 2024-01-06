# imports from packages
from flask import Flask, request, jsonify 
from flask_cors import CORS

# imports from my own code base
from src.pipeline.predict_pipeline import PredictPipeline

# importing the utility functions
from src.utils import allowed_file

# initializing app
app = Flask(__name__)
CORS(app)

# initilizing the predict pipeline
predict_pipeline = PredictPipeline()

# home route
@app.route("/")
def index():
    home_page_res = {
        "success": True, 
        "message": "Server is UP and Running"
    }
    return jsonify(home_page_res)


# main open route to return marriage photos of the person in the picture
# make sure there is only one frontal image of the person in the pic sent
@app.route("/check-marital-status", methods=["POST"])
def check_marital_status():
    # print(request.files.keys())
    if 'file' not in request.files:
        no_input_res = {
            "success": False, 
            "message": "Input Image was not delivered"
        }
        return jsonify(no_input_res)
    file = request.files["file"]
    if file.filename == '':
        no_input_res = {
            "success": False, 
            "message": "Invalid filename"
        }
        return jsonify(no_input_res)
    if file and allowed_file(file.filename):
        results = predict_pipeline.predict(file)
        success_result_as_res = {
            "success": True, 
            "data": results
        }
        return success_result_as_res 
    faillure_result_as_res = {
        "success": False, 
        "data": []
    }
    return jsonify(faillure_result_as_res) 


# if __name__ == "__main__":
#     # http://127.0.0.1:5000/
#     app.run(
#         host = "0.0.0.0", 
#         port = 5000, 
#         debug = True
#     )
