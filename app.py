from flask import Flask, jsonify, render_template, request, redirect, url_for
from datetime import date
from database import Vehicle, app, fetch_vehicles, insert_vehicle, fetch_rentals, update_return_date


@app.route('/')
def index():
    vehicles = fetch_vehicles()  # This will fetch all the vehicles from the database

    return render_template('index.html', vehicles=vehicles)

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        insert_vehicle(make, model, year, price)
        return redirect(url_for('index'))
    return render_template('add_vehicle.html')

@app.route('/rent_vehicle', methods=['GET', 'POST'])
def rent_vehicle_view():
    if request.method == 'POST':
        vehicle_id = request.form['vehicle_id']
        rental_date = request.form['rental_date']
        return_date = request.form['return_date']
        # Process the rental information as needed
        return redirect(url_for('index'))  # Redirect to an appropriate route

    # Fetch the vehicles from the database
    vehicles = fetch_vehicles()  # Use fetch_vehicles directly
    return render_template('rent_vehicle.html', vehicles=vehicles)

@app.route('/rentals')
def rentals():
    rentals = fetch_rentals()
    return render_template('rentals.html', rentals=rentals)

@app.route('/update_return_date', methods=['POST'])
def update_return_date_view():
    data = request.json  # Assuming you're sending the update as JSON data
    rental_id = data.get('rental_id')
    return_date = data.get('return_date')

    try:
        update_return_date(rental_id, return_date)
        return jsonify({'message': 'Return date updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
