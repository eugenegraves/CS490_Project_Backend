import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db
from server import ServicesRequest
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        #populate_test_data()
        yield app.test_client()  # Yielding testing client for your application

# def populate_test_data():
#     service_request = ServicesRequest(
#         customer_id=1,  
#         proposed_datetime=datetime.now(),
#         status='pending',  # Initial status is 'pending'
#         car_id=1,  
#         service_offered_id=1  
#     )
#     db.session.add(service_request)
#     db.session.commit()
    
    
def test_update_customer_service_requests_success(client):
    """Test successfully updating the status of an existing service request."""
    response = client.patch('/update_customer_service_requests/23', json={'status': 'completed'})
    assert response.status_code == 200
    # Verify that the status has been updated in the database
    updated_request = ServicesRequest.query.get(1)
    assert updated_request.status == 'completed'

def test_update_customer_service_requests_not_found(client):
    """Test updating a service request that does not exist."""
    response = client.patch('/update_customer_service_requests/999', json={'status': 'completed'})  # Non-existent ID
    assert response.status_code == 404
    assert 'Service request not found' in response.get_json()['error']