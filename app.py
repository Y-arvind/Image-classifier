#!flask/bin/python
from flask import Flask, request, render_template, jsonify
from resnet_classifier import ResnetClassifier

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/qure/v1.0/classify/', methods=['GET','POST'])
def classify_image():
    if 'file' not in request.files:
        return "Please attach an image", 400
    file = request.files['file']
    img_bytes = file.read()
    classifier = ResnetClassifier()
    try:
        res = classifier.classify(img_bytes=img_bytes)
        if res[0][1]<50:
            return jsonify("Sorry for the inconvenience!,The confidence index is low to classify accurately.")
        return jsonify({ res[0][0] : res[0][1] }), 200
    except Exception as e:
        # TODO log the exception here
        print(e)
        return "An error occurred", 500

if __name__ == "__main__":
	print(("* Starting Flask server..."
		"please wait until server has fully started"))
	app.run(debug=True, host='0.0.0.0')
