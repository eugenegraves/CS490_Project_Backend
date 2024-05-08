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
        

def test_login_manager_success(client):
    """ Test manager login successfully. """
    login_data = {
        'usernames': 'johnsmith123',
        'password': 'password123'
    }
    response = client.post('/login_managers', json=login_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['first_name'] == 'John'


def test_login_manager_failure(client):
    """ Test login failure due to incorrect credentials. """
    login_data = {
        'usernames': 'johnsmith123',
        'password': 'password223'
    }
    response = client.post('/login_managers', json=login_data)
    assert response.status_code == 401
    assert 'Invalid manager ID, password, or first name' in response.get_json()['error']


def test_login_manager_missing_fields(client):
    """ Test response for missing usernames or password. """
    login_data = {
        'usernames': 'johnsmith123'
        # missing 'password'
    }
    response = client.post('/login_managers', json=login_data)
    assert response.status_code == 400
    assert 'Technician ID, password, and first name are required' in response.get_json()['error']