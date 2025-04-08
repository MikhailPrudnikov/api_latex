import requests
import os

url = "http://localhost:8000/convert-to-latex"
file_path = "/Users/mihailprudnikov/Documents/uni/SecondYear/курсач/api_bot/git/api_latex/data/test/2025-04-08 17.09.49.jpg"

try:
    with open(file_path, 'rb') as f:
        response = requests.post(url, files={'image': (
            os.path.basename(file_path), f, 'image/png')})
        print(f"Status code: {response.status_code}")
        print(f"Raw response: {response.text}")
        print(response.json())
except Exception as e:
    print(f"Error: {str(e)}")
