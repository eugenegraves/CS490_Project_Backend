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
        
        
def test_edit_customer_success(client):
    """Test successfully updating a customer's data."""
    customer_id = 24
    updated_data = {
        'first_name': 'Jane3',
        'last_name': 'Doe',
        'email': 'jane3@example.com',
        'phone': '987-654-3210',
        'Address': '123 Maple St',
        'password': 'newpassword',
        'usernames': 'jane3_doe'
    }
    response = client.put(f'/edit-customer/{customer_id}', json=updated_data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User data updated successfully'

def test_edit_customer_not_found(client):
    """Test updating a non-existent customer."""
    customer_id = 999  # Assuming this ID does not exist
    response = client.put(f'/edit-customer/{customer_id}', json={'first_name': 'Test'})
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Customer not found'

# def test_edit_customer_invalid_method(client):
#     """Test using an invalid HTTP method to access the endpoint."""
#     customer_id = 1
#     response = client.get(f'/edit-customer/{customer_id}')  # GET is not allowed
#     assert response.status_code == 405
#     json_data = response.get_json()
#     #assert json_data is not None  # This ensures JSON data exists
#     assert 'Invalid request method' in json_data['message']  # Correct access to JSON response