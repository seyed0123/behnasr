import requests


class ApiCaller():
    def __init__(self, token, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        self.token = token
        self.headers = {
            'Authorization': f'Token {token}'
        }
        self.url = url

    def clasify(self, image_path):
        method = 'classify'
        files = {
            'image': open(image_path, 'rb')
        }

        # Data to be sent in the POST request
        data = {
            'method': method
        }
        response = requests.post(self.url + '/api/endpoint/', headers=self.headers, files=files, data=data)
        print(response.status_code)
        print(response.json())


o = ApiCaller('de674f9463370d0e56a071dcd089279d0adda7c4', 'localhost:8000')
o.clasify('media/media/members/Wallpaper_4K3D_3293.jpg')
