import requests, json, time

with open('example.json', 'rb') as f:
    data = json.load(f)

print(data)

i = 0
while True:
    i += 1
    r = requests.post('http://localhost:8080/predict', json=data)
    time.sleep(0.3)
    print(i, r.elapsed, r.text)