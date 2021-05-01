import requests

URL = 'http://localhost:8080'

text ='GIEWIVrGMTLIVrHIQS'
key_range = {'start':0,'end': 10}

data = {'key_range' : key_range,'text': text}

req = requests.post(url = URL, json= data)

print(req.json())