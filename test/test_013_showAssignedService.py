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
        
def test_show_assigned_services_with_results(client):
    """ Test retrieving assigned services for a technician with results """
    response = client.get('/show_assigned_services/1')  # Assuming technician_id 1 has assigned services
    assert response.status_code == 200
    services = response.get_json()
    assert len(services) > 0
    assert services[0]['service_name'] == "Oil Change"
    assert services[0]['technician_first_name'] == "Adam"

def test_show_assigned_services_no_results(client):
    """ Test retrieving assigned services for a technician with no assigned services """
    response = client.get('/show_assigned_services/999')  # Assuming technician_id 999 has no assigned services
    assert response.status_code == 200
    services = response.get_json()
    assert len(services) == 0