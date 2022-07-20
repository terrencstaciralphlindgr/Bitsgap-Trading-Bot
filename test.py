import requests
from datetime import datetime
from time import sleep

api = 'http://rick26754.pythonanywhere.com/'

while True:
    r = requests.get(api)
    print(datetime.now())
    print(r.json())

    sleep(10)
