import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime, timedelta
from server import app, db
from server import Technicians, ServicesRequest, AssignedServices

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        yield app.test_client()  # Yielding testing client for your application
        
    
def test_assign_technicians_successfully(client):
    """ Test assigning a technician to a service request without time conflicts """
    data = {
        'technician_id': 1,
        'service_request_id': 1
    }
    response = client.post('/assign_technicians', json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Technician assigned successfully'


def test_assign_technicians_nonexistent_request(client):
    """ Test assigning a technician to a non-existent service request """
    data = {
        'technician_id': 1,
        'service_request_id': 999  # Non-existent request ID
    }
    response = client.post('/assign_technicians', json=data)
    assert response.status_code == 404
    assert 'Service request not found' in response.get_json()['error']