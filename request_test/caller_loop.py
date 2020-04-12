import requests, time

while True:
    r = requests.get('http://localhost:8080/')
    time.sleep(0.3)
    print(r.text)