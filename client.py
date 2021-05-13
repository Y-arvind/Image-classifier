import requests

def sendImage():
    files = {'media': open('cat.jpeg', 'rb')}
    #url = 'https://flask-service.bov0er98st5ta.us-east-1.cs.amazonlightsail.com/qure/v1.0/classify/'
    url = 'http://localhost:5000/qure/v1.0/classify/'
    response = requests.post(url, files=files)
    print(response.json())

sendImage()
