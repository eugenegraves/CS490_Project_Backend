import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db
from server import ServicesRequest
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Create schema in the test database
        populate_test_data()
        yield app.test_client()  # Yielding testing client for your application

def populate_test_data():
    service_request = ServicesRequest(
        service_offered_id=1,
        customer_id=1,
        proposed_datetime=datetime.now(),
        status='pending',
        car_id=10
    )
    db.session.add(service_request)
    db.session.commit()
    
    
def test_show_customer_service_requests_with_results(client):
    """Test retrieving pending service requests successfully."""
    response = client.get('/show_customer_service_requests/')
    assert response.status_code == 200
    requests = response.get_json()
    assert len(requests) == 1
    assert requests[0]['service_name'] == "Oil Change"
    assert requests[0]['status'] == "pending"

def test_show_customer_service_requests_no_pending(client):
    """Test retrieving service requests when none are pending."""
    # Mark existing service requests as completed
    ServicesRequest.query.update({ServicesRequest.status: 'completed'})
    db.session.commit()

    response = client.get('/show_customer_service_requests/')
    assert response.status_code == 200
    requests = response.get_json()
    assert len(requests) == 0