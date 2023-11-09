from flask import Flask, request, jsonify 

from src.pipeline.predict_pipeline import PredictPipeline

app = Flask(__name__)

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

predict_pipeline = PredictPipeline()

@app.route("/")
def index():
    home_page_res = {
        "success": True, 
        "message": "Server is UP and Running"
    }
    return jsonify(home_page_res)

@app.route("/check-marital-status", methods=["POST"])
def check_marital_status():
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
        return jsonify(success_result_as_res) 
    faillure_result_as_res = {
        "success": False, 
        "data": []
    }
    return jsonify(faillure_result_as_res) 


if __name__ == "__main__":
    # http://127.0.0.1:5000/
    app.run(
        host = "0.0.0.0", 
        port = 5000, 
        debug = True
    ) 
