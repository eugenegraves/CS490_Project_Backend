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
        

def test_delete_accessory_manager_success(client):
    """Test successfully deleting an accessory."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock()) as mock_execute:
        mock_result = MagicMock()
        mock_result.rowcount = 1  # Simulate one row being affected
        mock_execute.return_value = mock_result

        response = client.post('/deleteAccessoryManager', json={'accessoryID': {'accessoire_id': 1}})
        assert response.status_code == 200
        assert 'Accessory deleted successfully' in response.get_json()['message']

def test_delete_accessory_manager_not_found(client):
    """Test attempting to delete an accessory that does not exist."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock()) as mock_execute:
        mock_result = MagicMock()
        mock_result.rowcount = 0  # Simulate no rows being affected
        mock_execute.return_value = mock_result

        response = client.post('/deleteAccessoryManager', json={'accessoryID': {'accessoire_id': 999}})
        assert response.status_code == 404
        assert 'Accessory not found' in response.get_json()['error']

def test_delete_accessory_manager_non_json_request(client):
    """Test deleting an accessory with a request that isn't in JSON format."""
    response = client.post('/deleteAccessoryManager', data='not-a-json')
    assert response.status_code == 400
    assert 'Request is not in JSON format' in response.get_json()['error']
