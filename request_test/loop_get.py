import requests, time

i = 0
while True:
    i += 1
    r = requests.get('http://localhost:8080/')
    time.sleep(0.3)
    print(i, r.elapsed, r.text)