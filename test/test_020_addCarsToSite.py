import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db
from server import Cars


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        #populate_test_data()
        yield app.test_client()  # Yielding testing client for your application
        
        
@pytest.fixture
def sample_car_data():
    return [
        {
            "manager_id": 1, "make": "Toyota", "model": "Corolla", "year": 2020,
            "color": "Red", "engine": "1.8L", "transmission": "Automatic",
            "price": 20000, "image0": "path/to/image0.jpg", "image1": "path/to/image1.jpg",
            "image2": "path/to/image2.jpg", "image3": "path/to/image3.jpg", "image4": "path/to/image4.jpg", "available": 1
        },
        {
            "manager_id": 1, "make": "Honda", "model": "Civic", "year": 2019,
            "color": "Blue", "engine": "2.0L", "transmission": "Manual",
            "price": 18000, "image0": "path/to/image1.jpg", "image1": "path/to/image1.jpg",
            "image2": "path/to/image2.jpg", "image3": "path/to/image3.jpg", "image4": "path/to/image4.jpg", "available": 1
        }
    ]
    

def test_add_cars_to_site_success(client, sample_car_data):
    """Test adding multiple cars successfully."""
    response = client.post('/add_cars_to_site', json={'cars': sample_car_data})
    assert response.status_code == 201
    assert 'Cars added successfully to the dealership' in response.get_json()['message']
    assert db.session.query(Cars).count() >= 2  

def test_add_cars_to_site_incomplete_data(client):
    """Test adding cars with incomplete data."""
    incomplete_data = [
        {
            "manager_id": 1, "make": "Toyota",  # Missing 'model' and other required fields
        }
    ]
    response = client.post('/add_cars_to_site', json={'cars': incomplete_data})
    assert response.status_code == 400
    assert 'Missing required car information' in response.get_json()['error']
    assert db.session.query(Cars).count() == 0  # Ensure no data was committed

def test_add_cars_to_site_database_error(client, sample_car_data, monkeypatch):
    """Simulate a database error during car addition."""
    # Use monkeypatch to simulate a database error on commit
    def mock_commit():
        raise Exception("Simulated database failure")
    
    monkeypatch.setattr(db.session, "commit", mock_commit)
    
    response = client.post('/add_cars_to_site', json={'cars': sample_car_data})
    assert response.status_code == 500
    assert 'Failed to add cars to the database' in response.get_json()['error']
    assert db.session.query(Cars).count() == 0  # Ensure rollback was effective