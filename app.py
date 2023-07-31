"""Flask app for Cupcakes"""

import os

from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, Cupcake, db

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///adopt")

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get('/api/cupcakes')
def list_all_cupcakes():
    """Show data about all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [ cupcake.serialize() for cupcake in cupcakes ]

    return jsonify(cupcakes=serialized)