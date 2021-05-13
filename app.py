#!flask/bin/python
from flask import Flask, request
from resnet_classifier import ResnetClassifier

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/qure/v1.0/classify/', methods=['GET','POST'])
def classify_image():
    if 'file' not in request.files:
        return "Please attach an image", 400
    file = request.files['file']
    img_bytes = file.read()
    classifier = ResnetClassifier()
    try:
        res = classifier.classify(img_bytes=img_bytes)
        return { res[0][0] : res[0][1] }, 200
    except Exception as e:
        # TODO log the exception here
        print(e)
        return "An error occurred", 500

if __name__ == "__main__":
	print(("* Starting Flask server..."
		"please wait until server has fully started"))
	app.run(debug=True, host='0.0.0.0')
