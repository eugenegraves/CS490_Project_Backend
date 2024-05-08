import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Assuming the Flask app is structured properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app, db  # Import the Flask app and db context

class Accessoire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()  # Create all tables for the database
        yield app.test_client()  # This ensures the test client is used within app context

def test_get_categories(client):
    """Test fetching categories from the database using mocked database calls."""
    # Create a list of mock categories as they would be returned from the database
    mock_categories = [('Wheels',), ('Seats',)]

    # Patch the query to return mock categories
    with patch('sqlalchemy.orm.Query.all', MagicMock(return_value=mock_categories)):
        # Test the GET categories endpoint
        response = client.get('/categories')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2  # Check that two categories are returned
        assert data == [
            {'value': 'Wheels', 'label': 'Wheels'},
            {'value': 'Seats', 'label': 'Seats'}
        ]
