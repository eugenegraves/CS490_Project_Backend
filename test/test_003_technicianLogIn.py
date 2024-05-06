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
        
        
def test_login_success(client):
    """ Test technician successful login """
    login_data = {
        'usernames': 'adamtaylor123',
        'password': 'password123'
    }
    response = client.post('/login_technicians', json=login_data)
    assert response.status_code == 200
    assert response.json['technicians_id'] == 1
    assert response.json['email'] == 'adam.taylor@example.com'
    
    
def test_login_failure(client):
    """ Test technician login with wrong credentials """
    login_data = {
        'usernames': 'adamtaylor123',
        'password': 'password223'
    }
    response = client.post('/login_technicians', json=login_data)
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid technician ID, password, or first name'
    
    
def test_login_missing_fields(client):
    """ Test technician login with missing fields """
    login_data = {
        'usernames': 'adamtaylor123'
        # Missing password
    }
    response = client.post('/login_technicians', json=login_data)
    assert response.status_code == 400
    assert response.json['error'] == 'Technician ID, password, and first name are required'