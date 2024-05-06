import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging
from flask import json
from datetime import datetime, timedelta
from server import app, db  # Importing from the server module where Flask app is defined
from server import ServicesRequest, ServicesOffered, Technicians, OwnCar, AssignedServices  


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
    # Add test data to the database
    service_offered = ServicesOffered(name='Oil Change', price='49.99', description='Includes oil change and replacement of oil filter', image='https://i.ibb.co/QQrpbYS/OIG2-Fu-BCh6f-RT.jpg')
    technician = Technicians(first_name='awais', last_name='Taylor', email='awais.taylor@example.com', usernames='awaisaataylor123', phone='123-456-7890', password='password123', manager_id='1')
    car = OwnCar(car_id='4', customer_id='21', make='Toyota', model='Corolla', year=2020)
    service_request = ServicesRequest(
        customer_id='1',
        proposed_datetime=datetime.now() + timedelta(days=3),
        status='accepted',
        service_offered_id=1,
        car_id=1
    )
    db.session.add_all([service_offered, technician, car, service_request])
    db.session.commit()
        
def test_get_upcoming_week_requests_success(client):
    """Test successful retrieval of service requests."""
    response = client.get('/get_upcoming_week_requests')
    assert response.status_code == 200
    data = response.get_json()
    assert 'accepted_service_requests' in data
    assert 'assigned_service_requests' in data
    assert len(data['accepted_service_requests']) > 0  # Ensure data is being returned
