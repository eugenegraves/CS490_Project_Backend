import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging
from flask import json
from server import app, db  # Importing from the server module where Flask app is defined
from server import Customer, Technicians  # Import Customer model from the server module

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create schema in the test database
        yield app.test_client()  # Yielding testing client for your application
def test_add_customer(client):
     """Test adding a new customer successfully."""
     customer_data = {
         "first_name": "haa",
         "last_name": "pnaa",
         "email": "hqaa",
         "phone": "31aa1-456-780",
         "Address": "22a3a grand trneqt",
         "password": "sea2uraepsnqord123",
         "usernames": "haaqnap",
         "social_security": "143a30980"
     }

     response = client.post('/add_customer', data=json.dumps(customer_data), content_type='application/json')

     assert response.status_code == 201
     assert response.get_json()['message'] == 'Customer added successfully'

     # Ensure customer was added to the database
     added_customer = Customer.query.filter_by(email="hqaa").first()
     assert added_customer is not None
     assert added_customer.first_name == "haa"  # Updated to match the correct customer
    
    
def test_add_technician(client):
     """Test adding a technician with proper manager id."""
     technician_data = {
         "firstName": "Teac",
         "lastName": "Ncaaian",
         "email": "tecaa@example.com",
         "username": "tacahnician1",
         "phone": "810-521-1234",
         "password": "stronaagpassword",
         "manager_id": 2
     }

     response = client.post('/add_technician', data=json.dumps(technician_data), content_type='application/json')
     assert response.status_code == 201
     assert response.get_json()['message'] == 'Technician added successfully'

     # Check if the technician was added to the database
     added_technician = Technicians.query.filter_by(email="tecaa@example.com").first()
     assert added_technician is not None
     assert added_technician.first_name == "Teac"

     # Test without required fields
     # response = client.post('/add_technician', data=json.dumps({}), content_type='application/json')
     # assert response.status_code == 400
    

def test_add_manager_with_admin_id(client):
    """Test adding a manager with admin_id."""
    manager_data = {
        "firstName": "hum",
        "lastName": "za",
        "email": "za.doe@example.com",
        "username": "za",
        "phone": "552-1234",
        "password": "za",
        "admin_id": 1
    }

    response = client.post('/add_manager', json=manager_data)
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Manager added successfully'
