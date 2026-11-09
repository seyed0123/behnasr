from methods.ocr import OCR
from methods.classification import classify
import base64
import os
import uuid

import cv2
from flask import Flask, request, jsonify

img_extension = "png"

app = Flask(__name__)


def encode_image(rNameF, rName=None):
    if rName:
        with open(rName, "rb") as image_file:
            base64ImgToReturn = base64.b64encode(image_file.read())
        os.remove(rName)
    os.remove(rNameF)
    return base64ImgToReturn


@app.route('/ocr', methods=['POST'])
def post_ocr():
    try:
        # Extract JSON data from the request
        json_data = request.form
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate required fields
        # required_fields = ['inputImage', 'lang', 'engine', 'preprocessing', 'postprocessing']
        # if not all(field in json_data for field in required_fields):
        #     return jsonify({"error": "Missing required fields"}), 400

        # Extract and process input data
        input_image = request.files['inputImage']
        app_lang = json_data.get('lang', 'eng+fa')
        app_engine = json_data.get('engine', 0)
        preprocessing = json_data.get('preprocessing', '1,1,1')
        postprocessing = json_data.get('postprocessing', '1,1')
        # Save the input image
        image_name = uuid.uuid4()
        image_path = os.path.join('ocr', str(image_name)+input_image.filename)
        input_image.save(image_path)

        # Process preprocessing and postprocessing parameters
        preprocessing_list = [int(x) for x in preprocessing.split(",")]
        postprocessing_list = [int(x) for x in postprocessing.split(",")]

        # Map language and engine to their respective values
        lang_map = {
            'eng': 'en',
            'ara': 'ar',
            'fas': 'fas',
            'eng+fas': 'en+fas'
        }
        a_lang = lang_map.get(app_lang, 'fas')  # Default to 'fas' if not found

        engine_map = {
            '0': 'tesseract',
            '1': 'easyocr'
        }
        a_engine = engine_map.get(app_engine, 'easyocr')  # Default to 'easyocr' if not found

        # Perform OCR
        total_text, avg_confidence, _, output_img = OCR(
            image_path,
            lang=a_lang,
            EngineName=a_engine,
            ConfigurationNumber=2,
            preprocessing=preprocessing_list,
            postprocessing=postprocessing_list
        )

        # Save the output image
        res_image_path = os.path.join('ocr', str(image_name)+"02" + input_image.filename)
        cv2.imwrite(res_image_path, output_img)

        # Encode the output image to base64
        base64_img = encode_image(image_path, res_image_path)

        # Prepare the result
        result = {
            "text": total_text,
            "score": avg_confidence,
            "outputImage": base64_img.decode("utf-8")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/classify', methods=['POST'])
def classification():
    if 'inputImage' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['inputImage']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_path = os.path.join('classify', str(uuid.uuid4())+ file.filename)
    file.save(file_path)
    result = classify(file_path)

    os.remove(file_path)

    return jsonify({"class": result})


@app.route('/')
def hello_world():
    return 'Hello this is Home.'


if __name__ == '__main__':
    app.run()
