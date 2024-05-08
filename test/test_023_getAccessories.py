import pytest
from sqlalchemy import text
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

def test_accessories_success(client):
    """Test retrieving accessories by category successfully."""
    accessories_data = [
        (1, 'Seat Cover', 'High-quality leather seat cover', 99.99, 'image1.jpg'),
        (2, 'Steering Wheel Cover', 'Wooden finish cover', 49.99, 'image2.jpg')
    ]

    with patch('sqlalchemy.orm.Session.execute', MagicMock()) as mock_execute:
        mock_result = MagicMock()
        mock_result.fetchall.return_value = accessories_data
        mock_execute.return_value = mock_result

        response = client.post('/accessories', json={'category': 'Interior'})
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['name'] == 'Seat Cover'
        assert data[1]['name'] == 'Steering Wheel Cover'

def test_accessories_failure_no_category(client):
    """Test error handling when no category is provided."""
    response = client.post('/accessories', json={})  # Empty JSON body
    assert response.status_code == 500
    assert 'error' in response.get_json()

def test_accessories_database_error(client):
    """Test error handling during a database failure."""
    with patch('sqlalchemy.orm.Session.execute', MagicMock(side_effect=Exception("Database error"))) as mock_execute:
        response = client.post('/accessories', json={'category': 'Interior'})
        assert response.status_code == 500
        assert 'Database error' in response.get_json()['error']
