from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade='all, delete-orphan')

class Pizza(db.Model):
    __tablename__ = 'pizza'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurants = db.relationship('RestaurantPizza', backref='pizza', cascade='all, delete-orphan')

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)

    def validate_prices(self, value):
        if not (1 <= value <= 30):
            raise ValueError("Price must range between 1 and 30")
