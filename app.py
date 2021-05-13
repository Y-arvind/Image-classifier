#!flask/bin/python
import os
from flask import Flask, request
from resnet_classifier import ResnetClassifier

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World! Deployed classifier"

@app.route('/qure/v1.0/classify/', methods=['GET','POST'])
def classify_image():
    if 'media' not in request.files:
        print("No file in request")
    file = request.files['media']
    file.save(os.path.join('', 'upload.jpeg'))
    classifier = ResnetClassifier("upload.jpeg")
    res = classifier.classify()
    return { res[0][0] : res[0][1] }, 200

if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	app.run(debug=True, host='0.0.0.0')
