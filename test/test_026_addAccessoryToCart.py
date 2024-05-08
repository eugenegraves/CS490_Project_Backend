import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Assuming the Flask app is structured properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app, db  # Import the Flask app and db context

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()  # This ensures the test client is used within app context
        

def test_add_accessory_to_cart_success(client):
    """Test adding an accessory to the cart successfully."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock()) as mock_execute:
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_execute.return_value = mock_result
        
        response = client.post('/addAccessoryToCart', json={
            'cartData': {
                'customer_id': 1,
                'item_price': 19.99,
                'item_image': 'path/to/image.jpg',
                'item_name': 'Phone Holder',
                'accessoire_id': 1001
            }
        })
        assert response.status_code == 200
        assert 'Accessory added to cart successfully' in response.get_json()['message']

def test_add_accessory_to_cart_missing_fields(client):
    """Test adding an accessory with missing fields to the cart."""
    response = client.post('/addAccessoryToCart', json={
        'cartData': {
            'customer_id': 1,
            'item_price': 19.99,
            # Missing 'item_image', 'item_name', and 'accessoire_id'
        }
    })
    assert response.status_code == 400
    assert 'cart data not provided or incomplete' in response.get_json()['error']

def test_add_accessory_to_cart_non_json_request(client):
    """Test adding an accessory with a non-JSON formatted request."""
    response = client.post('/addAccessoryToCart', data='not-a-json')
    assert response.status_code == 400
    assert 'Request is not in JSON format' in response.get_json()['error']
