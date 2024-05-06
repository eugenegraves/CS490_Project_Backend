import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db
from server import ServicesPackage

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        yield app.test_client()  # Yielding testing client for your application
        
        
def test_get_service_packages(client):
    """Test retrieving all service packages."""
    response = client.get('/ServicesPackage')
    assert response.status_code == 200
    packages = response.get_json()
    assert len(packages) == 6  # Ensure two packages are returned
    assert packages[0]['name'] == "Lifetime Oil Change"
    assert packages[1]['name'] == "Lifetime Tire Rotation"
    assert packages[0]['price'] == 499.9
    assert 'description' in packages[0]
    assert 'image' in packages[0]
    assert packages[0]['image'] == "https://i.ibb.co/ckgNHNK/OIG2.jpg"
