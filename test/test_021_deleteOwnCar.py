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
        
        
@pytest.fixture
def add_car():
    car = OwnCar(car_id=130, customer_id=1, make="Toyota", model="Rav4", year=2023)
    db.session.add(car)
    db.session.commit()
    return car


def test_delete_car_success(client, add_car):
    """Test successful deletion of a car."""
    response = client.delete(f'/delete_own_car/{add_car.car_id}')
    assert response.status_code == 200
    assert 'Car with ID 130 deleted successfully' in response.get_json()['message']
    assert OwnCar.query.get(add_car.car_id) is None

def test_delete_car_not_found(client):
    """Test deletion attempt for a non-existing car."""
    response = client.delete('/delete_own_car/24')  # Assuming car ID 999 does not exist
    assert response.status_code == 404
    assert 'Car with ID 24 not found' in response.get_json()['error']

def test_delete_car_exception(client, monkeypatch):
    """Test internal error during car deletion."""
    def mock_delete(*args, **kwargs):
        raise Exception("Mock exception")

    monkeypatch.setattr(db.session, 'delete', mock_delete)
    response = client.delete('/delete_own_car/1')
    assert response.status_code == 500
    assert 'Mock exception' in response.get_json()['error']