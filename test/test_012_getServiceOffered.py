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
        yield app.test_client()  # Yielding testing client for your application
        
def test_get_all_services(client):
    """Test retrieving all services offered."""
    response = client.get('/services-offered')
    assert response.status_code == 200
    services = response.get_json()
    assert len(services) == 10 # subject to chnage based on the rows we have within our databse
    assert services[0]['name'] == "Oil Change"
    assert services[1]['name'] == "Tire Rotation"
    assert services[0]['price'] == 49.99
    assert 'description' in services[0]
    assert 'image' in services[0]
    assert services[0]['image'] == "https://i.ibb.co/QQrpbYS/OIG2-Fu-BCh6f-RT.jpg"