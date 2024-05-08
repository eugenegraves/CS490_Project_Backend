import pytest
import os
import sys

# Ensure the server directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app, db  # Importing Flask app and db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        
        
from unittest.mock import patch, MagicMock

def test_delete_accessory_success(client):
    """Test successful deletion of an existing accessory."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock()) as mock_execute:
        mock_result = MagicMock()
        mock_result.rowcount = 1  # Simulate one row affected
        mock_execute.return_value = mock_result

        response = client.post('/deleteAccessory', json={'accessoryID': 1})
        assert response.status_code == 200
        assert 'Accessory deleted successfully' in response.get_json()['message']

def test_delete_accessory_not_found(client):
    """Test deletion attempt for a non-existent accessory."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock()) as mock_execute:
        mock_result = MagicMock()
        mock_result.rowcount = 0  # Simulate no rows affected
        mock_execute.return_value = mock_result

        response = client.post('/deleteAccessory', json={'accessoryID': 999})
        assert response.status_code == 404
        assert 'Accessory not found' in response.get_json()['error']

def test_delete_accessory_database_error(client):
    """Test handling of database errors during deletion."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock(side_effect=Exception("Database error"))) as mock_execute:
        response = client.post('/deleteAccessory', json={'accessoryID': 1})
        assert response.status_code == 500
        assert 'Database error' in response.get_json()['error']