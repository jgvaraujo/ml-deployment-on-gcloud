import requests, json

with open('example.json', 'rb') as f:
    data = json.load(f)

print(data)

while True:
    r = requests.post('http://localhost:8080/predict', json=data)
    time.sleep(0.3)
    print(r.text)