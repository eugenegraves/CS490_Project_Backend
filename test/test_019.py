import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, db
from server import Cart
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
    cart_item = Cart(customer_id=3,
                     item_price=24.99,
                     item_image="http-image",
                     item_name="part", 
                     car_id=10, 
                     service_package_id=0)
    db.session.add(cart_item)
    db.session.commit()
    

def test_delete_cart_item_by_car_id(client):
    """Test deleting cart items by car ID."""
    response = client.delete('/delete_cart_item?carId=10&customerId=3')
    assert response.status_code == 200
    assert Cart.query.count() == 0  # All related carts should be deleted

# def test_delete_cart_item_failure(client):
#     """Test failure when trying to delete a non-existent cart item."""
#     response = client.delete('/delete_cart_item?cartId=20')
#     assert response.status_code == 200  # Expect success message because no action is needed
#     assert 'Carts deleted successfully' in response.get_json()['message']