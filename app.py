"""Flask app for Cupcakes"""

from re import S
from flask import Flask, jsonify, request, render_template
from models import connect_db, db, Cupcake


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()


@app.route('/')
def show_home():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


def serialize_cupcakes(cupcake):
    """Serialize a Cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


@app.route("/api/cupcakes")
def get_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcakes(d) for d in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Get data about cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcakes(cupcake)
    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=['POST'])
def create_cupcake():
    """Create a cupcake with data from the body of the request."""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcakes(new_cupcake)
    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<int:id>", methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()

    serialized = serialize_cupcakes(cupcake)
    return (jsonify(cupcake=serialized))


@app.route("/api/cupcakes/<int:id>", methods=['DELETE'])
def delete_cupcake(id):
    """Delete cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return (jsonify({'msg':  'Cupcake deleted'}))
