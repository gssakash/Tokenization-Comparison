import requests

def test_upload_and_benchmark():
    url = 'http://localhost:5000/upload_and_benchmark'
    files = {'file': open('./synthetic_dataset.txt', 'rb')}
    response = requests.post(url, files=files)
    print(response.json())

test_upload_and_benchmark()

