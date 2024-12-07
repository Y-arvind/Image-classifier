from flask import Flask, request, render_template, jsonify
from resnet_classifier import ResnetClassifier
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Y-arvind:Arvind#2002@localhost/feedback_db'
db = SQLAlchemy(app)

# Ensure upload directory exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ImageTag(db.Model):
    __tablename__ = 'image_tag'
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    cropcoordinates = db.Column(db.String, nullable=False)


# Image Table
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_path = db.Column(db.String, nullable=False)

    # Relationship with tags through ImageTag
    tags = db.relationship(
        'Tag',
        secondary='image_tag',
        back_populates='images'
    )





# Tag Table
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Relationship with images through ImageTag
    images = db.relationship(
        'Image',
        secondary='image_tag',
        back_populates='tags'
    )


with app.app_context():
    db.create_all()
    print("Tables created successfully.")


# Routes
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/qure/v1.0/classify/', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return "Please attach an image", 400

    file = request.files['file']
    img_bytes = file.read()
    classifier = ResnetClassifier()

    try:
        res = classifier.classify(img_bytes=img_bytes)
        confidence = res[0][1]

        if confidence < 50:
            return jsonify({
                "message": "Confidence is too low for accurate classification. Please provide Annotate.",
            }), 400

        return jsonify({res[0][0]: confidence}), 200
    except Exception as e:
        print(e)  # Replace with a logger in production
        return "An error occurred", 500


@app.route('/feedback/image', methods=['POST'])
def upload_feedback_image():
    try:
        # Retrieve image from request
        image_file = request.files['file']
        date_path = datetime.datetime.now().strftime("%Y-%m-%d")
        upload_dir = os.path.join(UPLOAD_FOLDER, date_path)
        os.makedirs(upload_dir, exist_ok=True)

        image_path = os.path.join(upload_dir, image_file.filename)
        image_file.save(image_path)

        # Save image record to datadb.Model
        image = Image(file_path=image_path)
        db.session.add(image)
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully!", "image_id": image.id}), 200

    except Exception as e:
        db.session.rollback()
        print("Error saving feedback image:", e)
        return jsonify({"error": "An error occurred while saving the image."}), 500


@app.route('/feedback/tags', methods=['POST'])
def submit_feedback_tags():
    try:
        # Retrieve data from request
        image_id = request.form.get('image_id')
        tags = request.form.get('tags')
        crops = request.form.get('cropCoordinates')

        # Validate image existence
        image = db.session.get(Image, image_id)
        if not image:
            return jsonify({"error": "Invalid image ID."}), 400

        if not crops or not tags:
            return jsonify({"error": "Missing crop coordinates or tags."}), 400

            # Process CropCoordinates
        try:
            crops = json.loads(crops)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid crop coordinates format."}), 400
        # Process tags
        tags_list = [tag.strip() for tag in tags.split(',')]
        for tag_name in tags_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                # Create a new Tag object if it doesn't exist
                tag = Tag(name=tag_name.lower())
                db.session.add(tag)
                db.session.flush()  # Flush to assign an ID to the new Tag object without committing the entire transaction

            # Create a new ImageTag association
            image_tag = ImageTag(image_id=image.id, tag_id=tag.id, cropcoordinates=json.dumps(crops))
            db.session.add(image_tag)

        db.session.commit()  # Commit after processing all tags

        return jsonify({"message": "Tags saved successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        print("Error saving feedback tags:", e)
        return jsonify({"error": "An error occurred while saving tags."}), 500

@app.route('/tags/suggestions', methods=['GET'])
def get_tag_suggestions():
    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify([])  # Return an empty list for empty queries

    # Example: Fetch matching tags from the database
    suggestions = Tag.query.filter(Tag.name.ilike(f"%{query}%")).limit(10).all()
    suggestion_list = [tag.name for tag in suggestions]

    return jsonify(suggestion_list)
if __name__ == "__main__":
    print("* Starting Flask server... please wait until server has fully started")
    app.run(debug=True, host='0.0.0.0')
