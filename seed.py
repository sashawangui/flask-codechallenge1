from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_data():
    with app.app_context():
        db.create_all()

        # Seed Restaurants
        restaurant_data = [
            {"name": "Dominion Pizza", "address": "Good Italian, Ngong Road, 5th Avenue"},
            {"name": "Pizza Hut", "address": "Westgate Mall, Mwanzi Road, Nrb 100"},
        ]

        for restaurant_info in restaurant_data:
            restaurant = Restaurant(name=restaurant_info["name"], address=restaurant_info["address"])
            db.session.add(restaurant)

        # Seed Pizzas
        pizza_data = [
            {"name": "Cheese", "ingredients": "Dough, Tomato Sauce, Cheese"},
            {"name": "Pepperoni", "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"},
        ]

        for pizza_info in pizza_data:
            pizza = Pizza(name=pizza_info["name"], ingredients=pizza_info["ingredients"])
            db.session.add(pizza)

        # Associate Pizzas with Restaurants (RestaurantPizzas)
        restaurant_pizza_data = [
            {"price": 5, "pizza_id": 1, "restaurant_id": 1},
            {"price": 7, "pizza_id": 2, "restaurant_id": 1},
            {"price": 6, "pizza_id": 1, "restaurant_id": 2},
            {"price": 8, "pizza_id": 2, "restaurant_id": 2},
        ]

        for pizza_info in restaurant_pizza_data:
            restaurant_pizza = RestaurantPizza(
                price=pizza_info["price"],
                pizza_id=pizza_info["pizza_id"],
                restaurant_id=pizza_info["restaurant_id"]
            )
            db.session.add(restaurant_pizza)

        db.session.commit()

if __name__ == '__main':
    seed_data()
