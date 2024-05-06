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
        
def test_get_items_sold_success(client):
    """Test retrieving items sold successfully for an existing customer."""
    response = client.get('/items-sold/1')
    assert response.status_code == 200
    items = response.get_json()
    assert len(items) == 1
    assert items[0]['item_type'] == "Oil Change"
    assert items[0]['price'] == 49.99

def test_get_items_sold_no_items_found(client):
    """Test retrieving items for a customer ID with no items sold."""
    response = client.get('/items-sold/50')  # Assuming customer ID 50 has no items
    assert response.status_code == 404
    assert 'No items found for the given customer ID' in response.get_json()['message']