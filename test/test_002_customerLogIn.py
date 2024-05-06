import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging
from flask import json
from server import app, db  # Importing from the server module where Flask app is defined

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create schema in the test database
        yield app.test_client()  # Yielding testing client for your application
        
        
def test_login_success(client):
    """ Test customer successful login """
    login_data = {
        'usernames': 'johndoe123',
        'password': 'password123'
    }
    response = client.post('/login_customer', json=login_data)
    assert response.status_code == 200
    assert response.json['customer_id'] == 1
    assert response.json['email'] == 'john.doe@example.com'


def test_login_failure(client):
    """ Test customer login with wrong credentials """
    login_data = {
        'usernames': 'johndoe123',
        'password': 'password223'
    }
    response = client.post('/login_customer', json=login_data)
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid username or password'


def test_login_missing_fields(client):
    """ Test customer login with missing fields """
    login_data = {
        'usernames': 'johndoe123'
        # Missing password
    }
    response = client.post('/login_customer', json=login_data)
    assert response.status_code == 400
    assert response.json['error'] == 'Username and password are required'