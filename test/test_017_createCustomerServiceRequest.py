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
        
        
# def test_create_service_request_success(client):
#     """Test creating a service request successfully."""
#     response = client.post('/service-request', json={
#         'customer_ID': 1,
#         'service_offered': 1,
#         'car_id': 1,
#         'proposed_datetime': '2023-12-25T14:00:00'
#     })
#     assert response.status_code == 201
#     assert 'Service request created successfully' in response.get_json()['message']

# modifications needed to backend to handle this test
# def test_create_service_request_missing_fields(client):
#     """Test creating a service request with missing fields."""
#     response = client.post('/service-request', json={
#         'customer_ID': 1
#         # Missing other necessary fields
#         })
#     assert response.status_code == 400 
#     assert 'Service request created successfully' in response.get_json()['message']
#     assert 'error' in response.get_json()

#check again
def test_create_service_request_wrong_method(client):
    """Test accessing the create service request endpoint with a wrong method."""
    response = client.get('/service-request')  # GET method is not allowed
    assert response.status_code == 405
    assert 'error' in response.get_json()