from flask import Flask, request, jsonify
import pymysql
from datetime import datetime

app = Flask(__name__)

# Connect to MySQL using pymysql
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Yash@123',
        database='VehicleRental',
        cursorclass=pymysql.cursors.DictCursor  
    )
except pymysql.MySQLError as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

def create_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                make VARCHAR(100) NOT NULL,
                model VARCHAR(100) NOT NULL,
                year INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rental (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                rental_date DATE NOT NULL,
                return_date DATE,
                FOREIGN KEY (vehicle_id) REFERENCES vehicle(id)
            )
        """)
        connection.commit()

create_tables()

class Vehicle:
    def __init__(self, id, make, model, year, price):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.price = price


class Rental:
    def __init__(self, id, vehicle_id, rental_date, return_date):
        self.id = id
        self.vehicle_id = vehicle_id
        self.rental_date = rental_date
        self.return_date = return_date

def insert_vehicle(make, model, year, price):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO vehicle (make, model, year, price) VALUES (%s, %s, %s, %s)",
            (make, model, year, price)
        )
        connection.commit()

def fetch_vehicles():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vehicle")
        vehicles = cursor.fetchall()
        return [Vehicle(id=v['id'], make=v['make'], model=v['model'], year=v['year'], price=v['price']) for v in vehicles]

def fetch_rentals():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rental")
        rentals = cursor.fetchall()
        return [Rental(id=r['id'], vehicle_id=r['vehicle_id'], rental_date=r['rental_date'], return_date=r['return_date']) for r in rentals]


def rent_vehicle(vehicle_id, rental_date):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO rental (vehicle_id, rental_date) VALUES (%s, %s)",
            (vehicle_id, rental_date)
        )
        connection.commit()


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = fetch_vehicles()
    return jsonify([{'id': v.id, 'make': v.make, 'model': v.model, 'year': v.year, 'price': str(v.price)} for v in vehicles])

@app.route('/insert_vehicle', methods=['POST'])
def create_vehicle():
    data = request.json
    try:
        insert_vehicle(data['make'], data['model'], data['year'], data['price'])
        return jsonify({'message': 'Vehicle added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/rent', methods=['POST'])
def rent():
    data = request.json
    vehicle_id = data.get('vehicle_id')
    rental_date = datetime.strptime(data.get('rental_date'), '%Y-%m-%d').date()

    try:
        rent_vehicle(vehicle_id, rental_date)
        return jsonify({'message': 'Vehicle rented successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rentals', methods=['GET'])
def get_rentals():
    rentals = fetch_rentals()
    return jsonify([{
        'id': r.id,
        'vehicle_id': r.vehicle_id,
        'rental_date': r.rental_date.isoformat(),
        'return_date': r.return_date.isoformat() if r.return_date else None
    } for r in rentals])


def update_return_date(rental_id, return_date):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE rental SET return_date = %s WHERE id = %s",
            (return_date, rental_id)
        )
        connection.commit()

if __name__ == "__main__":
    app.run(debug=True)
