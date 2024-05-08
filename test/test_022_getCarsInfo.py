import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db
from server import OwnCar, Customer


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        yield app.test_client()  # Yielding testing client for your application
        

def test_get_car_infos_success(client):
    """ Test successful retrieval of car information """
    response = client.get('/getCarInfos', query_string={'car_id': '1'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['car_id'] == 1
    assert data['make'] == 'Subaru'
    assert data['model'] == 'Outback'
    assert data['color'] == 'Gray'