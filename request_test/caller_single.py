import requests, json

with open('example.json', 'rb') as f:
    data = json.load(f)

print(data)

r = requests.post('http://localhost:8080/predict', json=data)
print(r.text)