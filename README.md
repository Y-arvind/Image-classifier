## Resnet Classifier
A residual network, or ResNet for short, is an artificiagit l neural network that helps to build a deeper neural network by utilizing skip connections or shortcuts to jump over some layers. 
It is a type of CNN network. Here we use a pretrained Resnet18 model to classify images into one of 1000 labels. 

## How to run
### Locally
To run locally, execute the app.py script : `python app.py`. The server will now be accessible on `localhost:5000`. 
Send a post request to the endpoint `resnet/v1.0/classify` along with an image attached. The response will be a json key-value pair with the classified label and it's confidence score. 
### In Docker
Build a docker image
`sudo docker build -t classifier:latest .`
Run the image
`sudo docker run -d -p 5000:5000 classifier`
The API is again available on localhost:5000


## Sample classification
<ins> Image sent </ins> 

<img src="https://github.com/Y-arvind/ResnetClassifier/blob/master/images/dog.jpeg" width="500">

<ins> Response </ins>

`{'Labrador retriever': 70.66324615478516}`
