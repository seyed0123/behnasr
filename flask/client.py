import requests
import json


class FlaskAppClient:
    def __init__(self, base_url, jwt_token=None):
        self.base_url = base_url+'/api'
        self.jwt_token = jwt_token

    def _get_headers(self):
        headers = {}
        if self.jwt_token:
            headers['Authorization'] = f'Token {self.jwt_token}'
        return headers

    def post_ocr(self, image_path, lang, engine, preprocessing, postprocessing):
        url = f"{self.base_url}/ocr/"

        # Prepare the JSON payload as a dictionary
        payload = {
            'lang': lang,
            'engine': engine,
            'preprocessing': preprocessing,
            'postprocessing': postprocessing
        }

        # Prepare the files
        files = {
            'inputImage': open(image_path, 'rb')
        }

        # Send the POST request with form data (payload), files, and headers
        headers = self._get_headers()
        response = requests.post(url, data=payload, files=files, headers=headers)

        # Close the file
        files['inputImage'].close()

        # Return the JSON response
        return response.json()

    def post_classify(self, image_path):
        url = f"{self.base_url}/classify/"

        # Prepare the files
        files = {
            'inputImage': open(image_path, 'rb')
        }

        # Send the POST request with headers
        headers = self._get_headers()
        response = requests.post(url, files=files, headers=headers)

        # Close the file
        files['inputImage'].close()

        # Return the JSON response
        return response.json()


# Example usage
if __name__ == "__main__":
    # Replace with the actual JWT token
    jwt_token = "a41238d9105a1e183c9469c45ca80c5bad12db91"

    client = FlaskAppClient("http://localhost:8000", jwt_token=jwt_token)
    image_pa = '12.jpg'
    # Example for OCR
    ocr_response = client.post_ocr(
        image_path=image_pa,
        lang="eng",
        engine="0",
        preprocessing="1,2,3",
        postprocessing="1,2"
    )
    print(ocr_response)

    # Example for Classification
    classify_response = client.post_classify(image_path=image_pa)
    print(classify_response)