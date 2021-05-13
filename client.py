import requests

def sendImage():
    files = {'file': open('images/dog.jpeg', 'rb')}
    url = 'https://flask-service.bov0er98st5ta.us-east-1.cs.amazonlightsail.com/qure/v1.0/classify/'
    #url = 'http://localhost:5000/qure/v1.0/classify/'
    response = requests.post(url, files=files)
    try:
        print (response.json())
    except:
        print(response)

sendImage()
