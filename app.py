from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurant_list = []

    restaurants = Restaurant.query.all()
    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
        restaurant_list.append(restaurant_data)

    response = make_response(
        jsonify(restaurant_list),
        201
    )

    return response

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404

    pizzas = []
    for restaurant_pizza in restaurant.pizzas:
        pizza = restaurant_pizza.pizza
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizzas.append(pizza_data)

    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'pizzas': pizzas
    }

    return jsonify(restaurant_data)

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def remove_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404

    # Delete associated RestaurantPizzas
    RestaurantPizza.query.filter_by(restaurant_id=id).delete()

    db.session.delete(restaurant)
    db.session.commit()

    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []

    for pizza in pizzas:
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizza_list.append(pizza_data)

    return jsonify(pizza_list), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not price or not pizza_id or not restaurant_id:
        return jsonify({'errors': ['Missing required data']}), 400

    # Check if the Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({'error': 'Validation errors'}), 404

    # Create a new RestaurantPizza
    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return jsonify({
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }), 201

if __name__ == '__main__':
    app.run(port=5555)


