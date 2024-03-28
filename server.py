from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_cors import CORS
from flask_mysqldb import MySQL
from sqlalchemy import text, func
from datetime import datetime
import math


''' Connection '''

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Westwood-18@localhost/cars_dealershipx' #Abdullah Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Westwood-18@localhost/cars_dealershipx' #Abdullah Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:great-days321@localhost/cars_dealershipx' #Dylan Connection 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:A!19lopej135@localhost/cars_dealershipx' # joan connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12340@localhost/cars_dealershipx' # Ismael connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:A!19lopej135@localhost/cars_dealershipx' # joan connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12340@localhost/cars_dealershipx' # Ismael connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:*_-wowza-shaw1289@localhost/cars_dealershipx' #hamza connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:42Drm400$!@localhost/cars_dealershipx'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


''' Data base models '''

class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    Address = db.Column(db.String(45), nullable=True)
    password = db.Column(db.String(45), nullable=False)
    usernames = db.Column(db.String(45), nullable=True, unique=True)

    def __init__(self, first_name, last_name, email, phone, password, Address=None, usernames=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.Address = Address
        self.password = password
        self.usernames = usernames

class Technicians(db.Model):
    __tablename__ = 'technicians'

    technicians_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), nullable=True, default=None)
    usernames = db.Column(db.String(255), nullable=False, default=None)
    phone = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.manager_id'), nullable=False)

    manager = relationship('Managers', backref='technicians')

    def __repr__(self):
        return f'<Technician {self.first_name} {self.last_name}>'
    
class Managers(db.Model):
    __tablename__ = 'managers'

    manager_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)
    usernames = db.Column(db.String(45), nullable=True, unique=True)

    admin = relationship('Admin', backref='managers')

    def __repr__(self):
        return f'<Manager {self.first_name} {self.last_name}>'

class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    usernames = db.Column(db.String(45), nullable=True, unique=True)
    phone = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<Admin {self.usernames}>'
    
class ItemSold(db.Model):
    __tablename__ = 'items_sold'

    item_sold_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    item_type = db.Column(db.String(45), nullable=False)
    date = db.Column(db.DateTime(6), nullable=False, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    method_of_payment = db.Column(db.String(45), default=None)

    def __init__(self, customer_id, item_type, date, price, item_id, method_of_payment=None):
        self.customer_id = customer_id
        self.item_type = item_type
        self.date = date
        self.price = price
        self.item_id = item_id
        self.method_of_payment = method_of_payment

    def __repr__(self):
        return f'<ItemSold {self.item_sold_id}>'


class ServicesRequest(db.Model):
    __tablename__ = 'services_request'
    service_request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    service_offered_id = db.Column(db.Integer, nullable=False)
    car_id = db.Column(db.Integer, nullable=False)
    proposed_datetime = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    customer_index = db.Index('fk_Service_request_Customers1_idx', customer_id)
    service_offered_index = db.Index('fk_Services_request_services_offered1_idx', service_offered_id)
    car_index = db.Index('fk_Services_request_Cars1_idx', car_id)

    __table_args__ = (
        db.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], name='fk_Service_request_Customers1'),
        db.ForeignKeyConstraint(['car_id'], ['cars.car_id'], name='fk_Services_request_Cars1'),
        db.ForeignKeyConstraint(['service_offered_id'], ['services_offered.services_offered_id'], name='fk_Services_request_services_offered1'),
        {'mysql_engine': 'InnoDB', 'mysql_auto_increment': 6, 'mysql_charset': 'utf8mb3'}
    )

class OwnCar(db.Model):
    __tablename__ = 'own_car'

    car_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))

    def __init__(self, car_id, customer_id, make, model):
        self.car_id = car_id
        self.customer_id = customer_id
        self.make = make
        self.model = model

class Cars(db.Model):
    __tablename__ = 'cars'
    car_id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.manager_id'))
    make = db.Column(db.String(45), nullable=False)
    model = db.Column(db.String(45), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(45), nullable=False)
    engine = db.Column(db.String(45), nullable=False)
    transmission = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image0 = db.Column(db.String(1000), nullable=False)
    image1 = db.Column(db.String(1000), nullable=False)
    image2 = db.Column(db.String(1000), nullable=False)
    image3 = db.Column(db.String(1000), nullable=False)
    image4 = db.Column(db.String(1000), nullable=False)
    cart_items = db.relationship('Cart', backref='car', lazy=True)

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    item_price = db.Column(db.Float, nullable=False)
    item_image = db.Column(db.String(1000), nullable=False)
    item_name = db.Column(db.String(45), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'))
    accessoire_id = db.Column(db.Integer, db.ForeignKey('accessoires.accessoire_id'))
    service_offered_id = db.Column(db.Integer, db.ForeignKey('services_offered.services_offered_id'))
    service_package_id = db.Column(db.Integer, db.ForeignKey('services_package.service_package_id'))

class Accessoire(db.Model):
    __tablename__ = 'accessoires'
    accessoire_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(45), nullable=False)
    cart_items = db.relationship('Cart', backref='accessoire', lazy=True)

class ServicesOffered(db.Model):
    __tablename__ = 'services_offered'
    services_offered_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(1000), nullable=False)
    cart_items = db.relationship('Cart', backref='service_offered', lazy=True)

class ServicesPackage(db.Model):
    __tablename__ = 'services_package'
    service_package_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(1000), nullable=False)
    cart_items = db.relationship('Cart', backref='service_package', lazy=True)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        Address=data.get('Address', None),
        password=data['password'],
        usernames=data['usernames']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 201

# adds a technician to the database
@app.route("/add_technician", methods=['POST'])
def add_technician():
    data = request.get_json()
    technician = Technicians(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        usernames=data['username'],
        phone=data['phone'],
        password=data['password'],
        manager_id = data['manager_id']
    )
    db.session.add(technician)
    db.session.commit()
    return jsonify({'message': 'Technician added sucessfully'}), 201

# adds a manager to the database
@app.route("/add_manager", methods=['POST'])
def add_manager():
    data=request.get_json()
    manager=Managers(
        firstName=data['first_name'],
        lastName=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    db.session.add(manager)
    db.session.commit()
    return jsonify({'message': 'Manager added successfully'}), 201

@app.route('/login_customer', methods=['POST'])
def login():
    data = request.get_json()
    if 'usernames' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    
    usernames = data['usernames']
    password = data['password']
    
    customer = Customer.query.filter_by(usernames=usernames, password=password).first()
    if customer:
        return jsonify({
            'customer_id': customer.customer_id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone': customer.phone,
            'Address': customer.Address,
            'password': customer.password,
            'usernames': customer.usernames
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/login_technicians', methods=['POST'])
def login_technicians():
    data = request.get_json()
    if 'usernames' not in data or 'password' not in data :
        return jsonify({'error': 'Technician ID, password, and first name are required'}), 400


    usernames = data['usernames']
    password = data['password']
    technician = Technicians.query.filter_by(usernames=usernames, password=password).first()
    if technician:

        return jsonify({
            'technicians_id': technician.technicians_id,
            'first_name': technician.first_name,
            'last_name': technician.last_name,
            'email': technician.email,
            'phone': technician.phone,
            'manager_id': technician.manager_id,
            'usernames': technician.usernames
        }), 200
    else:
        return jsonify({'error': 'Invalid technician ID, password, or first name'}), 401

@app.route('/login_managers', methods=['POST'])
def login_managers():
    data = request.get_json()
    if 'usernames' not in data or 'password' not in data :
        return jsonify({'error': 'Technician ID, password, and first name are required'}), 400


    usernames = data['usernames']
    password = data['password']

    manager = Managers.query.filter_by(usernames=usernames, password=password).first()
    if manager :
        return jsonify({
            'manager_id': manager.manager_id,
            'first_name': manager.first_name,
            'last_name': manager.last_name,
            'email': manager.email,
            'phone': manager.phone,
            'admin_id': manager.admin_id,
            'usernames': manager.usernames
        }), 200
    else:
        return jsonify({'error': 'Invalid manager ID, password, or first name'}), 401

@app.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()

    if 'usernames' not in data or 'password' not in data :
        return jsonify({'error': 'Technician ID, password, and first name are required'}), 400


    usernames = data['usernames']
    password = data['password']

    admin = Admin.query.filter_by(usernames=usernames, password=password).first()
    if admin:
        return jsonify({
            'admin_id': admin.admin_id,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
            'usernames': admin.usernames,
            'phone': admin.phone
        }), 200
    else:
        return jsonify({'error': 'Invalid admin ID, password, or first name'}), 401

@app.route('/edit-customer/<int:customer_id>', methods=['PUT'])
def edit_customer(customer_id):
    if request.method == 'PUT':
        # Get the JSON data sent from the frontend
        edited_data = request.get_json()

        customer = Customer.query.get(customer_id)

        if customer:
            # Update customer's data
            customer.first_name = edited_data.get('first_name', customer.first_name)
            customer.last_name = edited_data.get('last_name', customer.last_name)
            customer.email = edited_data.get('email', customer.email)
            customer.phone = edited_data.get('phone', customer.phone)
            customer.Address = edited_data.get('Address', customer.Address)
            customer.password = edited_data.get('password', customer.password)
            customer.usernames= edited_data.get('usernames', customer.usernames)

            db.session.commit()
            return jsonify({'message': 'User data updated successfully'})
        else:
            return jsonify({'message': 'Customer not found'}), 404

    return jsonify({'message': 'Invalid request method'}), 405

@app.route('/items-sold/<int:customer_id>', methods=['GET'])
def get_items_sold(customer_id):
    
    items = ItemSold.query.filter_by(customer_id=customer_id).all()

    
    if not items:
        return jsonify({'message': 'No items found for the given customer ID'}), 404

   
    items_sold = []
    for item in items:
        item_data = {
            'item_sold_id': item.item_sold_id,
            'customer_id': item.customer_id,
            'item_type': item.item_type,
            'date': item.date.isoformat(),  
            'price': item.price,
            'item_id': item.item_id,
            'method_of_payment': item.method_of_payment
        }
        items_sold.append(item_data)

    # Return the list of items sold as JSON
    return jsonify(items_sold), 200

@app.route('/services-offered', methods=['GET'])
def get_all_services():
    services = ServicesOffered.query.all()
    services_list = []
    for service in services:
        services_list.append({
            'services_offered_id': service.services_offered_id,
            'name': service.name,
            'price': service.price,
            'description': service.description,
            'image': service.image
        })
    return jsonify(services_list)

@app.route('/ServicesPackage', methods=['POST'])
def getServicePackage():
    services = ServicesPackage.query.all()
    services_list = []
    for service in services:
        services_list.append({
            'services_offered_id': service.services_offered_id,
            'name': service.name,
            'price': service.price,
            'description': service.description,
            'image': service.image
        })
    return jsonify(services_list)


@app.route('/service-request', methods=['POST'])
def create_service_request():
    if request.method == 'POST':
        # Get form data from request
        data = request.json

        # Extract form data
        customer_id = data.get('customer_ID')
        service_offered_id = data.get('service_offered')
        car_id = data.get('car_id')
        proposed_datetime = data.get('proposed_datetime')

        # Create a new service request object
        new_request = ServicesRequest(
            customer_id=customer_id,
            service_offered_id=service_offered_id,
            car_id=car_id,
            proposed_datetime=proposed_datetime,
            status='Pending' 
        )

        # Add the new service request to the database
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Service request created successfully'}), 201
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/car_sold/<int:customer_id>', methods=['GET'])
def get_car_sold(customer_id):
    items_sold = ItemSold.query.filter_by(customer_id=customer_id, item_type='car').all()

    if not items_sold:
        return jsonify({'message': 'No items sold found for this customer ID and item type.'}), 404

    # Serialize the items_sold data for response
    serialized_items_sold = []
    for item in items_sold:
        serialized_item = {
            'item_sold_id': item.item_sold_id,
            'customer_id': item.customer_id,
            'item_type': item.item_type,
            'date': item.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
            'price': item.price,
            'item_id': item.item_id,
            'method_of_payment': item.method_of_payment
        }
        serialized_items_sold.append(serialized_item)

    return jsonify(serialized_items_sold), 200

@app.route('/customer_service_requests/<int:customer_id>', methods=['GET'])
def get_customer_service_requests(customer_id):
   
    service_requests = db.session.query(
        ServicesRequest, ServicesOffered.name, ServicesOffered.price,
        ServicesOffered.description, ServicesRequest.proposed_datetime,
        ServicesRequest.status, ServicesRequest.car_id,
        ServicesRequest.service_offered_id
    ).join(
        ServicesOffered, ServicesRequest.service_offered_id == ServicesOffered.services_offered_id
    ).filter(
        ServicesRequest.customer_id == customer_id
    ).all()

    
    result = []
    for request, service_name, price, description, proposed_datetime, status, car_id, service_offered_id in service_requests:
        result.append({
            'service_request_id': request.service_request_id,
            'service_name': service_name,
            'price': price,
            'description': description,
            'proposed_datetime': proposed_datetime.isoformat() if proposed_datetime else None,
            'status': status,
            'car_id': car_id,
            'service_offered_id': service_offered_id
        })

    return jsonify(result)

@app.route('/get_cart_items/<int:customer_id>', methods=['GET'])
def get_cart_items(customer_id):
    # Query the database to get the cart items for the given customer ID
    cart_items = Cart.query.filter_by(customer_id=customer_id).all()

    if not cart_items:
        return jsonify({'message': 'No items found in the cart for this customer.'}), 404

    # Prepare the response data
    items_data = []
    for cart_item in cart_items:
        item_data = {
            'cart_id': cart_item.cart_id,
            'item_name': cart_item.item_name,
            'item_price': cart_item.item_price,
            'item_image': cart_item.item_image,
            'item_name' : cart_item.item_name,
            'car_id': cart_item.car_id,
            'accessoire_id': cart_item.accessoire_id,
            'service_package_id' : cart_item.service_package_id
        }
        items_data.append(item_data)

    return jsonify({'cart_items': items_data}), 200

@app.route('/delete_cart_item/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    try:
        cart = Cart.query.get(cart_id)  # Retrieve the cart by cart_id
        if cart:
            db.session.delete(cart)  # Delete the cart
            db.session.commit()  # Commit the transaction
            return jsonify(message='Cart deleted successfully'), 200
        else:
            return jsonify(message='Cart not found'), 404
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of an error
        return jsonify(message=str(e)), 500

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()

    # Extract data from the JSON payload
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    item_price = data.get('item_price')
    item_name = data.get('item_name')
    item_image = data.get('item_image')

    try:
        new_cart_item = Cart(
            customer_id=customer_id,
            item_price=item_price,
            item_name=item_name,
            item_image=item_image,
            car_id=car_id,
            accessoire_id=None,  
            service_offered_id=None,  
            service_package_id=None  
        )

        db.session.add(new_cart_item)
        db.session.commit()

        return jsonify({'message': 'Car added to cart successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# Create a route to add a new car for a customer
@app.route('/add_car/<int:customer_id>', methods=['POST'])
def add_car(customer_id):
    data = request.get_json()
    car_id = data.get('car_id')
    make = data.get('make')
    model = data.get('model')

    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    new_car = OwnCar(car_id=car_id, customer_id=customer_id, make=make, model=model)

    db.session.add(new_car)
    db.session.commit()

    return jsonify({'message': 'Car added successfully'}), 201

# adds cars to the database based on a file read 
@app.route('/add_cars_to_site', methods=['POST'])
def add_cars_to_site():
    data = request.get_json()
    cars_data = data.get('cars')     # converts to proper format in order for backend to read the info correctly

    for car_data in cars_data:
        manager_id = car_data.get('manager_id')
        make = car_data.get('make')
        model = car_data.get('model')
        year = car_data.get('year')
        color = car_data.get('color')
        engine = car_data.get('engine')
        transmission = car_data.get('transmission')
        price = car_data.get('price')
        image0 = car_data.get('image0')
        image1 = car_data.get('image1')
        image2 = car_data.get('image2')
        image3 = car_data.get('image3')
        image4 = car_data.get('image4')
        
        car = Cars(manager_id=manager_id, make=make, model=model, year=year, color=color, engine=engine, transmission=transmission, price=price,
                   image0=image0, image1=image1, image2=image2, image3=image3, image4=image4)
        
        db.session.add(car)

    db.session.commit()
    
    return jsonify({'message': 'Cars added successfully to the dealership'}), 201

@app.route('/own_cars/<int:customer_id>', methods=['GET'])
def get_cars(customer_id):
    cars = OwnCar.query.filter_by(customer_id=customer_id).all()

    cars_list = []
    for car in cars:
        cars_list.append({
            'car_id': car.car_id,
            'make': car.make,
            'model': car.model
        })

    return jsonify({'cars': cars_list})

@app.route('/delete_own_car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    try:
        car = OwnCar.query.get(car_id)
        if car:
            db.session.delete(car)
            db.session.commit()
            return jsonify({'message': f'Car with ID {car_id} deleted successfully'}), 200
        else:
            return jsonify({'error': f'Car with ID {car_id} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# handles returning filtered cars that the user selected
@app.route('/cars_details', methods=['POST'])
def cars_details():
    data = request.get_json()
    make = f'%{data["make"]}%' if data.get("make") else '%'
    model = f'%{data["model"]}%' if data.get("model") else '%'
    color = f'%{data["color"]}%' if data.get("color") else '%'

    # if budget filter is applied, split in min and max price to select appropriate cars from the db
    budget = data.get('budget')
    if budget:
        budget = budget.replace('$', '').split("-")
        min_price = budget[0]
        max_price = budget[1] if len(budget) > 1 else None
    else:
        min_price = None
        max_price = None

    query = text('''select cars.car_id,cars.make, cars.model, cars.price, cars.image0, cars.year from cars where cars.make like :make and 
    cars.model like :model and cars.color like :color and (:min_price is null or cars.price >= :min_price) 
    and (:max_price is null or cars.price <= :max_price);
    ''')
    
    result = db.session.execute(query, {
                                        'make': make,
                                        'model': model,
                                        'color': color,
                                        'min_price': min_price,
                                        'max_price': max_price})
    cars = [{'car_id':row[0],'make': row[1], 'model': row[2], 'price': row[3], 'image': row[4], 'year': row[5]} for row in result.fetchall()]
    return jsonify(cars), 200

# this will grab every car in the db in order from car_id=1 to the last car in the table. This also ensures 6 cars are grabbed per page
@app.route('/get_cars_to_display', methods=['GET'])
def get_cars_to_display():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=12, type=int)

    # calculate from where to start grabbing the next item based on the current page
    offset = (page - 1) * per_page
    
    # returns cars as a list, and order them based on car_id
    all_cars = Cars.query.order_by(Cars.car_id).offset(offset).limit(per_page).all()

    # gets the total number of cars in the table
    total_cars = Cars.query.count()

    # gets the total number of pages
    total_pages = math.ceil(total_cars / per_page)

    cars = [{
        'car_id': car.car_id,
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'price': car.price,
        'image': car.image0
    } for car in all_cars]

    # return the list of cars, total pages, and current page
    return jsonify({'cars': cars, 'total_pages': total_pages, 'current_page': page})

#fetch the selected car infos
@app.route('/getCarInfos', methods=['POST', 'GET'])
def getCarInfos():
    car_id = request.args.get('car_id')
    carInfos = Cars.query.filter_by(car_id=car_id).first()
    carInfosDict = {
    'car_id': carInfos.car_id,
    'make': carInfos.make,
    'model': carInfos.model,
    'year': carInfos.year,
    'color': carInfos.color,
    'engine': carInfos.engine,
    'transmission': carInfos.transmission,
    'price': carInfos.price,
    'image0': carInfos.image0,
    'image1': carInfos.image1,
    'image2': carInfos.image2,
    'image3': carInfos.image3,
    'image4': carInfos.image4
}
    return jsonify(carInfosDict), 200

#Retrieve the accesories by categories
@app.route('/accessories', methods=['POST'])
def accesories():
    category = request.get_json()
    acessories = Accessoire.query.filter_by(category=category).all()
    accesoriesDic = [{
        'accesoire_id' : row.accesoire_id,
        'name' : row.name,
        'description' : row.description,
        'price' : row.price,
        'image' : row.image
    } for row in acessories]
    return jsonify(accesoriesDic),200

'''IN HALT, make offer system'''
@app.route('/make_offer', methods=['POST'])
def make_offer():
    data = request.get_json()
    query_insert = ''' insert into offers values(:offer_id, :offer_price, :offer_status, :customer_id, :car_id)
    '''
    query_update = ''' update offers set offer.offer_price = :offer_price, offer.status = :offer_status 
                      where offers.customer_id = :'''
    result = db.engine.execute(query_insert, offer_id=data['offer_id'], offer_price=data['offer_status'], customer_id=data['customer_id'], car_id=data['car_id'])

if __name__ == "__main__":
    app.run(debug = True, host='localhost', port='5000')