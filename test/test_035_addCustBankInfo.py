import pytest
import os
import sys

# Ensure the server directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from server import app  # Adjust this import according to your actual module structure

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('server.requests.post')
def test_receive_customer_bank_info_success(mock_post, client):
    # Setup mock
    mock_response = MagicMock()
    mock_response.json.return_value = {'status': 'success', 'details': 'Bank info added successfully'}
    mock_post.return_value = mock_response

    # Data to be sent in the request
    data = {
        'bank_name': 'Bank of Test',
        'account_number': '1234567890'
    }

    # Call the endpoint
    response = client.post(f'/add-customer-bank_info/123', json=data)

    # Check the response from your Flask app
    assert response.status_code == 200
    assert response.get_json() == {'status': 'success', 'details': 'Bank info added successfully'}


