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


def test_get_customer_bank_details_success(client):
    """Test retrieving bank details successfully."""
    response = client.get('/get_customer_bank_details?customer_id=1')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['bank_name'] == 'Bank of America'


def test_get_customer_bank_details_no_id(client):
    """Test response for missing customer ID."""
    response = client.get('/get_customer_bank_details')
    assert response.status_code == 400
    assert response.json['error'] == 'Customer ID is required.'


def test_get_customer_bank_details_no_data_found(client):
    """Test response when no data is found."""
    response = client.get('/get_customer_bank_details?customer_id=55')  # Assuming ID 999 has no data
    assert response.status_code == 404
    assert response.json['error'] == 'No bank details found for the specified customer.'