from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Migrate(app, db)
CORS(app)


@app.route("/bakeries")
def get_bakeries():
    bakeries = [b.to_dict() for b in Bakery.query.all()]
    response = make_response(jsonify(bakeries), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/bakeries/<int:id>")
def get_bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    return make_response(jsonify(bakery.to_dict(include_baked_goods=True)), 200)


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    goods = [
        bg.to_dict() for bg in BakedGood.query.order_by(BakedGood.price.desc()).all()
    ]
    return make_response(jsonify(goods), 200)


@app.route("/baked_goods/most_expensive")
def most_expensive_good():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bg:
        return make_response(jsonify(bg.to_dict()), 200)
    return make_response(jsonify({"error": "No baked goods found"}), 404)
