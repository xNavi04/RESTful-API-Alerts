import requests

response = requests.post(url='http://127.0.0.1:5000/add', data={"name": "sm1", "description": "sm2"})

print(response.status_code)