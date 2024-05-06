import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db
from server import ItemSold
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        populate_test_data()
        yield app.test_client()  # Yielding testing client for your application

def populate_test_data():
    # Sample data of cars sold
    item_sold1 = ItemSold(
        #item_sold_id is generated
        customer_id=1,
        item_type='car',
        name='car',
        date=datetime.utcnow(),
        price=20000,
        item_id=101,
        method_of_payment='bank account'
    )
    item_sold2 = ItemSold(
        #item_sold_id is generated
        customer_id=1,
        item_type='car',
        name='car',
        date=datetime.utcnow(),
        price=15000,
        item_id=102,
        method_of_payment='bank account'
    )
    db.session.add_all([item_sold1, item_sold2])
    db.session.commit()
    
    
def test_get_car_sold_success(client):
    """Test successfully retrieving cars sold to a specific customer."""
    response = client.get('/car_sold/1')
    assert response.status_code == 200
    cars_sold = response.get_json()
    assert len(cars_sold) >= 2  # Assuming customer 1 bought 2 cars
    assert cars_sold[0]['price'] == 20000
    assert cars_sold[1]['method_of_payment'] == 'bank account'

def test_get_car_sold_no_items_found(client):
    """Test retrieving cars sold when no cars have been sold to the customer."""
    response = client.get('/car_sold/999')  # Assuming customer 999 has no cars sold
    assert response.status_code == 404
    assert 'No items sold found' in response.get_json()['message']