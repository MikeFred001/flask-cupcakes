"""Flask app for Cupcakes"""

import os

from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, Cupcake, db, DEFAULT_IMAGE_URL

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get('/')
def display_cupcakes_and_form():
    """Displays list of cupcakes and a form to add more."""

    return render_template("index.html")


@app.get('/api/cupcakes')
def list_all_cupcakes():
    """Show data about all cupcakes
    {"cupcakes": [{id, flavor, size, rating, image_url},
    {id, flavor, size, rating, image_url}]}
   """

    cupcakes = Cupcake.query.all()
    serialized = [ cupcake.serialize() for cupcake in cupcakes ]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """Show information on one single cupcake.
    Returns JSON {"cupcake": {id, flavor, size, rating, image_url}}
    """


    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """Make a new cupcake.
    Post body should look like this:
    {"flavor": flavor, "size": size, "rating": rating, "image_url": ""}

     Returns JSON {"cupcake": {id, flavor, size, rating, image_url}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"] or None

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url=image_url
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Updates information on a single cupcake.
    Body should be a JSON object containing changed values.
    Example: {"flavor": "chocolate", "size": "medium", "rating": "5"}

    Returns JSON: {
        "cupcake": {
            "id": "1",
            "flavor": "chocolate",
            "size": "medium",
            "rating": "5",
            "image_url":
            "example.com"
        }"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)

    if not request.json.get("image_url") == "":
        cupcake.image_url = request.json.get("image_url")
    else:
        cupcake.image_url = DEFAULT_IMAGE_URL


    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Delete's a cupcake
    Returns JSON: {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=[cupcake.id])

