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


def test_add_accessory_success(client):
    """Test adding an accessory successfully."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock()) as mock_execute:
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_execute.return_value = mock_result
        
        response = client.post('/addAccessory', json={
            'accessoryData': {
                'name': 'Windshield Wiper',
                'description': 'Clear view windshield wiper',
                'price': 25.99,
                'image': 'image.jpg',
                'category': 'Windshield'
            }
        })
        assert response.status_code == 200
        assert 'Accessory added successfully' in response.get_json()['message']

def test_add_accessory_missing_fields(client):
    """Test adding an accessory with missing fields."""
    response = client.post('/addAccessory', json={
        'accessoryData': {
            'name': 'Windshield Wiper',
            'description': 'Clear view windshield wiper',
            # missing price, image, and category
        }
    })
    assert response.status_code == 400
    assert 'Accessory data not provided or incomplete' in response.get_json()['error']

def test_add_accessory_non_json_request(client):
    """Test adding an accessory with non-JSON formatted request."""
    response = client.post('/addAccessory', data='not-a-json')
    assert response.status_code == 400
    assert 'Request is not in JSON format' in response.get_json()['error']