import requests, json, time, datetime

i = 0
kind = 'local'
while True:
    ans = input('This is a local test? [Y/n] ')
    print()
    if ans in ('y', 'Y', ''):
        url = 'http://localhost:8080/'
        print('Application address (http://example:8080/):', url)
        break
    elif ans in ('n', 'N'):
        url = ''
        kind = 'cloud'
        while url == '':
            url = input('Put the application address (https://appml.run.app/): ')
        if url[-1] != '/':
            url = url + '/'
        print('Application URL:', url)
        break

with open('example.json', 'rb') as f:
    data = json.load(f)

print('\nData:', data)
print()

i = 0
t = datetime.timedelta(0)
if kind == 'local':
    mv = 50
else:
    mv = 1
while True:
    i += 1
    r = requests.post(url+'predict', json=data)
    t += r.elapsed
    if i%mv==0:
        print(i, t/mv, json.loads(r.text), end='\r')
        t = datetime.timedelta(0)