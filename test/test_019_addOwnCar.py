import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        #populate_test_data()
        yield app.test_client()  # Yielding testing client for your application


def test_add_car_success(client):
    response = client.post('/add_own_car/1', json={'car_id': '125','make': 'Toyota', 'model': 'Corolla', 'year': 2021})
    assert response.status_code == 201
    assert 'Car added successfully' in response.get_json()['message']

# def test_add_car_missing_data(client):
#     response = client.post('/add_own_car/1', json={'car_id': '124', 'make': 'Toyota'})
#     assert response.status_code == 201
#     assert 'Missing required car details' in response.get_json()['error']

def test_add_car_customer_not_found(client):
    response = client.post('/add_own_car/999', json={'make': 'Toyota', 'model': 'Corolla', 'year': 2021})
    assert response.status_code == 404
    assert 'Customer not found' in response.get_json()['error']