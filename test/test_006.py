import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime, timedelta
from server import app, db
from server import Technicians, ServicesRequest, AssignedServices

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
    # Assuming Technicians and ServicesRequest models are correctly defined and related
    technician = Technicians(
        first_name='new', 
        last_name='Taylor', 
        email='new.taylor@example.com', 
        usernames='newtaylor123', 
        phone='123-456-7890', 
        password='password123', 
        manager_id='1'
    )
    db.session.add(technician)
    db.session.commit()

    # Add service requests for today and tomorrow
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    service_today = ServicesRequest(
        technicians_id=technician.technicians_id,
        proposed_datetime=today
    )
    service_tomorrow = ServicesRequest(
        technicians_id=technician.technicians_id,
        proposed_datetime=tomorrow
    )
    db.session.add_all([service_today, service_tomorrow])
    db.session.commit()
    
def test_get_available_technicians_valid_date(client):
    """ Test retrieving available technicians on a specific valid date """
    response = client.get('/get_available_technicians?date=' + datetime.today().strftime('%Y-%m-%d'))
    assert response.status_code == 200
    technicians = response.get_json()
    assert len(technicians) > 0
    assert technicians[0]['full_name'] == 'new Taylor'

def test_get_available_technicians_invalid_date_format(client):
    """ Test date validation handling """
    response = client.get('/get_available_technicians?date=invalid-date')
    assert response.status_code == 400
    assert 'Invalid date format' in response.get_json()['error']

def test_get_available_technicians_no_technicians(client):
    """ Test no technicians available on a future date """
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    response = client.get(f'/get_available_technicians?date={future_date}')
    assert response.status_code == 200
    assert len(response.get_json()) == 0