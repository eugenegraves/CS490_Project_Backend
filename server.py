from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_cors import CORS
from flask_mysqldb import MySQL
from sqlalchemy import text, func, and_, update
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import math
from math import ceil
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select


''' Connection '''

app = Flask(__name__)

#hello

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Westwood-18@localhost/cars_dealershipx' #Abdullah Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:great-days321@localhost/cars_dealershipx' #Dylan Connection 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:A!19lopej135@localhost/cars_dealershipx' # joan connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12340@localhost/cars_dealershipx' # Ismael connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:*_-wowza-shaw1289@localhost/cars_dealershipx' #hamza connection
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
    available = db.Column(db.Integer, nullable=False)
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

class TestDriveAppointment(db.Model):
    __tablename__ = 'test_drive_appointments'

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(45), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)

    customer = relationship('Customer', backref='test_drive_appointments')
    car = relationship('Cars', backref='test_drive_appointments')

    def __repr__(self):
        return f'<TestDriveAppointment appointment_id={self.appointment_id} appointment_date={self.appointment_date} status={self.status}>'

# NOT FINISHED -DYLAN
class AssignedServices(db.Model):
    __tablename__ = 'assigned_services'

    assigned_service_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    technicians_id = db.Column(db.Integer, db.ForeignKey('technicians.technicians_id'), nullable=False)
    service_request_id = db.Column(db.Integer, db.ForeignKey('services_request.service_request_id'), nullable=False)


    technician = relationship('Technicians', backref='assigned_services')
    service_request = relationship('ServicesRequest', backref='assigned_services')


    def __repr__(self):
        return f'<AssignedServices assigned_service_id={self.assigned_service_id} technicians_id={self.technicians_id} service_request_id={self.service_request_id}>'

class Offers(db.Model):
    __tablename__='offers'

    offer_id=db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    offer_price=db.Column(db.Float, nullable=False)
    offer_status=db.Column(db.String(45), nullable=False)
    customer_id=db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    car_id=db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)

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
    
    if 'admin_id' in data:
        admin_id = data['admin_id']
        manager_id = 1
    elif 'manager_id' in data:
        admin_id = None
        manager_id = data['manager_id']
    else:
        return jsonify({'error': 'Either admin_id or manager_id must be provided'}), 400

    technician = Technicians(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        usernames=data['username'],  # corrected 'usernames' to 'username'
        phone=data['phone'],
        password=data['password'],
        manager_id=manager_id
    )
    db.session.add(technician)
    db.session.commit()
    return jsonify({'message': 'Technician added successfully'}), 201

# adds a manager to the database
@app.route("/add_manager", methods=['POST'])
def add_manager():
    data=request.get_json()
    if 'admin_id' in data:
        manager=Managers(
            firstName=data['first_name'],
            lastName=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            admin_id=data['admin_id']
        )
    else:
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

# IN DEVELOPMENT
@app.route('/get_available_technicians', methods=['GET'])
def get_available_technicians():
    selected_date = request.args.get('date', default=datetime.today().strftime('%Y-%m-%d'), type=str)

    result = db.session.query(
        Technicians.technicians_id,
        func.count(AssignedServices.service_request_id).label('job_count')
    ).outerjoin(
        AssignedServices,
        db.and_(
            Technicians.technicians_id == AssignedServices.technicians_id,
            db.func.date(AssignedServices.proposed_datetime) == selected_date
        )
    ).group_by(
        Technicians.technicians_id
    ).having(
        func.count(AssignedServices.service_request_id) <= 7
    ).all()

    available_technicians = [
        {'technician_id': tech_id, 'job_count': count} for tech_id, count in result
    ]

    return jsonify(available_technicians)

#@app.route('/assign_technicians', methods=['POST'])
#def assign_technicians():
    

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

# DYLAN IS WORKING
@app.route('/show_assigned_services', methods=['GET'])
def show_assigned_services():
    assigned_services = db.session.query(
        AssignedServices,
        ServicesRequest,
        ServicesRequest.service_request_id,
        Customer.first_name,
        Customer.last_name,
        Customer.phone,
        ServicesOffered.name.label('service_name'),
        ServicesOffered.price.label('service_price'),
        ServicesOffered.description.label('service_description'),
    ).join(
        ServicesRequest,
        AssignedServices.service_request_id == ServicesRequest.service_request_id
    ).join(
        Customer,
        Customer.customer_id == ServicesRequest.customer_id
    ).join(
        ServicesOffered,
        ServicesOffered.services_offered_id == ServicesRequest.service_offered_id
    ).options(
        joinedload(AssignedServices.service_request)
    ).all()

    result = []

    for assigned_service, service_request, service_request_id, first_name, last_name, customer_phone, service_name, service_price, service_description in assigned_services:
        service_dict = {
            'assigned_service_id': assigned_service.assigned_service_id,
            'service_request_id': assigned_service.assigned_service_id,
            'technician_first_name': assigned_service.technician.first_name,
            'technician_last_name': assigned_service.technician.last_name,
            'technician_email': assigned_service.technician.email,
            'technician_phone': assigned_service.technician.phone,
            'service_name': service_name,
            'service_price': service_price,
            'service_description': service_description,
            'proposed_datetime': service_request.proposed_datetime.isoformat() if service_request.proposed_datetime else None,
            'status': service_request.status,
            'car_id': service_request.car_id,
            'service_offered_id': service_request.service_offered_id,
            'customer_first_name': first_name,
            'customer_last_name': last_name,
            'customer_phone': customer_phone
        }
        result.append(service_dict)

    return jsonify(result)

# @app.route('/update_assigned_service_requests/<int:service_request_id>', methods=['PATCH'])
# def update_assigned_service(service_request_id):
#     # Retrieve the service request from the database
#     service_request = ServicesRequest.query.get(service_request_id)

#     if not service_request:
#         return jsonify({'error': 'Service request not found'}), 404

#     # Parse the request body for the new status
#     data = request.json
#     new_status = data.get('status')

#     # Update the status of the service request
#     service_request.status = new_status
#     db.session.commit()

#     return jsonify({'message': 'assigned service updated successfully'}), 200


@app.route('/ServicesPackage', methods=['GET'])
def getServicePackage():
    services = ServicesPackage.query.all()

    services_list = []
    for service in services:
        services_list.append({
            'service_package_id': service.service_package_id,
            'name': service.name,
            'price': service.price,
            'description': service.description,
            'image': service.image
        })
    print(services_list)    
    return jsonify(services_list), 200

@app.route('/show_customer_service_requests/', methods=['GET'])
def show_customer_service_requests():
    service_requests = db.session.query(
        ServicesRequest, ServicesOffered.name, ServicesOffered.price,
        ServicesOffered.description, ServicesRequest.proposed_datetime,
        ServicesRequest.status, ServicesRequest.car_id,
        ServicesRequest.service_offered_id,
        Customer.customer_id,
        Customer.usernames,
        Customer.phone
    ).join(
        ServicesOffered, ServicesRequest.service_offered_id == ServicesOffered.services_offered_id
    ).join(
        Customer, Customer.customer_id == ServicesRequest.customer_id
    ).all()

    result = []
    for request, name, service_price, description, proposed_datetime, status, car_id, service_offered_id, customer_id, customer_username, customer_phone, in service_requests:

        result.append({
            'service_request_id': request.service_request_id,
            'service_name': name,
            'service_price': service_price,
            'description': description,
            'proposed_datetime': proposed_datetime.isoformat() if proposed_datetime else None,
            'status': status,
            'car_id': car_id,
            'service_offered_id': service_offered_id,
            'customer_id': customer_id,
            'customer_username': customer_username,
            'customer_phone': customer_phone
        })

    return jsonify(result)

@app.route('/update_customer_service_requests/<int:service_request_id>', methods=['PATCH'])
def update_customer_service_requests(service_request_id):
    # Retrieve the service request from the database
    service_request = ServicesRequest.query.get(service_request_id)

    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    # Parse the request body for the new status
    data = request.json
    new_status = data.get('status')

    # Update the status of the service request
    service_request.status = new_status
    db.session.commit()

    return jsonify({'message': 'Service request updated successfully'}), 200

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
            'proposed_datetime': proposed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
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

#use the carid to delete the perks and car if it is a car else use cartId
@app.route('/delete_cart_item/<int:cartId>/<int:car_id>/<int:service_package_id>/<int:customer_id>', methods=['DELETE'])
def delete_cart(cartId,car_id,service_package_id,customer_id):
    try:
        # Query for all instances matching the criteria
        if car_id != 0 and service_package_id == 0:
            carts_to_delete = Cart.query.where(and_(car_id== car_id,customer_id ==customer_id)).all()
        else:
            carts_to_delete = Cart.query.filter_by(cart_id=cartId).all()
        
        # Delete each instance
        for cart in carts_to_delete:
            db.session.delete(cart)
        
        # Commit the transaction
        db.session.commit()
        
        return jsonify(message='Carts deleted successfully'), 200
    except Exception as e:
        db.session.rollback()
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
    item_service_offered_id = data.get('service_offered_id')

    try:
        # Conditionally assign service_offered_id based on its presence in the JSON payload
        if item_service_offered_id is not None:
            new_cart_item = Cart(
                customer_id=customer_id,
                item_price=item_price,
                item_name=item_name,
                item_image=item_image,
                car_id=car_id,
                accessoire_id=None,  
                service_offered_id=item_service_offered_id,  
                service_package_id=None  
            )
        else:
            #return 409 if a car is present in the cart
            result = Cart.query.filter_by(car_id=car_id).first()
            if(result):
                return "car already present in cart", 409
            #end    
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
        print("exception    ", str(e))
        return jsonify({'error': str(e)}), 500

# Create a route to add a new car for a customer
@app.route('/add_own_car/<int:customer_id>', methods=['POST'])
def add_car(customer_id):
    data = request.get_json()
    car_id = data.get('car_id')
    make = data.get('make')
    model = data.get('model')

    # Check if the car_id already exists in the cars table
    existing_car = Cars.query.filter_by(car_id=car_id).first()
    if existing_car:
        return jsonify({'error': 'Car ID already exists'}), 400

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

# endpoint to display all cars if no filters applied, and display only filtered cars if there are filters applied. Only show cars that are available
@app.route('/cars_details', methods=['POST', 'GET'])
def cars_details():
    if request.method == 'POST':
        data = request.get_json()
        make = data.get("make", None)
        model = data.get("model", None)
        color = data.get("color", None)
        budget = data.get("budget", None)
        page = data.get('page', 1)  # Default to first page
        per_page = data.get('per_page', 12)  # Default to 12 cars per page

        filtered_cars = Cars.query.filter(Cars.available==1)

        if make:
            filtered_cars = filtered_cars.filter(Cars.make == make)
        if model:
            filtered_cars = filtered_cars.filter(Cars.model == model)
        if color:
            filtered_cars = filtered_cars.filter(Cars.color == color)
        if budget:
            # if the user selects $200000+, handle it accordingly
            if budget.endswith("+"):
                min_price = float(budget.replace('$', '').replace('+', ''))
                max_price = float('inf')  
            else:
                budget_range = budget.replace('$', '').split("-")
                min_price = float(budget_range[0]) 
                max_price = float(budget_range[1]) if len(budget_range) > 1 else float('inf') 

            # apply price range filter
            filtered_cars = filtered_cars.filter(Cars.price >= min_price)
            if max_price != float('inf'):
                filtered_cars = filtered_cars.filter(Cars.price <= max_price)

        total_filtered = filtered_cars.count()
        total_pages = ceil(total_filtered / per_page)
        filtered_cars = filtered_cars.offset((page - 1) * per_page).limit(per_page)

        cars = [{'car_id': car.car_id, 'make': car.make, 'model': car.model,
                 'year': car.year, 'price': car.price, 'color': car.color,
                 'image': car.image0} for car in filtered_cars]

        return jsonify({'cars': cars, 'total_pages': total_pages, 'current_page': page}), 200
    
    elif request.method == 'GET':
        # display all cars on their respective page
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)

        # get the relevant cars meant for each page
        offset = (page - 1) * per_page
        all_cars = Cars.query.filter(Cars.available==1).order_by(Cars.car_id).offset(offset).limit(per_page).all()

        # data to be returned
        cars = [{
            'car_id': car.car_id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'price': car.price,
            'color': car.color,
            'image': car.image0
        } for car in all_cars]

        # get the total number of cars to display
        total_cars = Cars.query.count()

        # get the number of pages
        total_pages = math.ceil(total_cars / per_page)

        return jsonify({'cars': cars, 'total_pages': total_pages, 'current_page': page}), 200

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
def accessories():
    try:
        category = request.get_json()['category']  # Use MultiDict for validation
        print("this is the recieved category: ", category )
        query = text("SELECT accessoires.accessoire_id, accessoires.name, accessoires.description, accessoires.price, accessoires.image FROM cars_dealershipx.accessoires WHERE accessoires.category = :category")
        result = db.session.execute(query, {'category': category})
        rows = result.fetchall()
        accessories_dic = [{'accessoire_id': row[0], 'name': row[1], 'description': row[2], 'price': row[3], 'image': row[4]} for row in rows]
        return jsonify(accessories_dic), 200
    except Exception as e:
        # Handle errors appropriately (log, return error response)
        return jsonify({'error': str(e)}), 500

    # Return the JSON response containing the accessories data
    #return jsonify(accessoriesDic), 200

@app.route('/remove_car', methods=['POST'])
def removeCar():
    carID = request.json.get('car_id')  # Get car_id from JSON request data
    
    if carID:
        print("Car ID received:", carID)  # Print the received car ID
        return jsonify({'message': carID}), 200  # Send back OK response if data is received
    else:
        return jsonify({'error': 'No data received'}), 400  # Send back error response if no data is received

# Delete the accessory by accessory_id
@app.route('/deleteAccessory', methods=['POST'])
def deleteAccessory():
    try:
        accessoryID = request.get_json()['accessoryID']  # Use MultiDict for validation
        print("this is the received accessory_id: ", accessoryID)
        query = text("DELETE FROM cars_dealershipx.accessoires WHERE accessoire_id = :accessoryID")
        result = db.session.execute(query, {'accessoryID': accessoryID})
        # Commit the transaction
        db.session.commit()

        # Check if any rows were affected
        if result.rowcount > 0:
            return jsonify({'message': 'Accessory deleted successfully'}), 200
        else:
            return jsonify({'error': 'Accessory not found'}), 404
    except Exception as e:
        # Handle errors appropriately (log, return error response)
        return jsonify({'error': str(e)}), 500

# Add the accessory to the database
@app.route('/addAccessory', methods=['POST'])
def addAccessory():
    try:
        if request.is_json:
            data = request.get_json()
            accessory_data = data.get('accessoryData')
            print("Received JSON data:", accessory_data)
            name = accessory_data.get('name')
            description = accessory_data.get('description')
            price = accessory_data.get('price')
            image = accessory_data.get('image')
            category = accessory_data.get('category')
            print("Received: name -", name)
            print("Received: description -", description)
            print("Received: price -", price)
            print("Received: image -", image)
            print("Received: category -", category)
            
            if name and description and price and image and category:
                query = text('''INSERT INTO cars_dealershipx.accessoires (name, description, price, image, category)
                        VALUES (:name, :description, :price, :image, :category)''')
                result = db.session.execute(query, {'name': name, 'description': description, 'price': price, 'image': image, 'category': category})
                print("Result row count:", result.rowcount)
                if result.rowcount > 0:
                    db.session.commit()
                    return jsonify({'message': 'Accessory added successfully'}), 200
                else:
                    return jsonify({'error': 'Unsuccessful execution of query'}), 400
            else:
                return jsonify({'error': 'Accessory data not provided or incomplete'}), 400
        else:
            return jsonify({'error': 'Request is not in JSON format'}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to add accessory'}), 500

# add accessory to cart
@app.route('/addAccessoryToCart', methods=['POST'])
def addAccessoryToCart():
    try:
        if request.is_json:
            data = request.get_json()
            cart_data = data.get('cartData')
            print("Received JSON data:", cart_data)
            customer_id = cart_data.get('customer_id')
            item_price = cart_data.get('item_price')
            item_image = cart_data.get('item_image')
            item_name = cart_data.get('item_name')
            accessoire_id = cart_data.get('accessoire_id')
            print("Received: csut -", customer_id)
            print("Received: price -", item_price)
            print("Received: image -", item_image)
            print("Received: name -", item_name)
            print("Received: aceID -", accessoire_id)
            
            if customer_id and item_price and item_image and item_name and accessoire_id:
                query = text('''INSERT INTO cars_dealershipx.cart (customer_id, item_price, item_image, item_name, accessoire_id)
                        VALUES (:customer_id, :item_price, :item_image, :item_name, :accessoire_id)''')
                result = db.session.execute(query, {'customer_id': customer_id, 'item_price': item_price, 'item_image': item_image, 'item_name': item_name, 'accessoire_id': accessoire_id})
                print("Result row count:", result.rowcount)
                if result.rowcount > 0:
                    db.session.commit()
                    return jsonify({'message': 'Accessory added to cart successfully'}), 200
                else:
                    return jsonify({'error': 'Unsuccessful execution of query'}), 400
            else:
                return jsonify({'error': 'cart data not provided or incomplete'}), 400
        else:
            return jsonify({'error': 'Request is not in JSON format'}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to add accessory'}), 500

@app.route('/addtoCartAndOwnedService', methods=['POST'])
def AddtoCartAndOwnedService():
    data = request.get_json()
    customer_id = data.get('customer_id')
    packages = data.get('packages')
    car_id = data.get('car_id')
    # print("id",customer_id)
    # print("packages  " ,packages)
    try:
        # Begin a transaction
        db.session.begin()

        for package in packages: 
            # Add to cart
            new_cart_item = Cart(
                customer_id=customer_id,
                item_price=package.get("price"),
                item_name=package.get("name"),
                item_image=package.get("image"),
                car_id=car_id,
                accessoire_id=None,  
                service_offered_id=None,  
                service_package_id=package.get("service_package_id")  
            )
            db.session.add(new_cart_item)

            # Add to subscribed services
            # new_subscribedService_item = SubscribedService(
            #     customer_id=customer_id,
            #     service_package_id=package.get("service_package_id")  
            # )
            # db.session.add(new_subscribedService_item)
        
        # Commit the transaction
        db.session.commit()
        
    except Exception as e:
        # Rollback the transaction in case of any exception
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Service packages added to subscribed services and cart successfully'}), 200
        
@app.route('/deleteAccessoryManager', methods=['POST'])
def deleteAccessoryManager():
    try:
        if request.is_json:
            data = request.get_json()
            accessoryData = data.get('accessoryID')
            print("Received JSON data:", accessoryData)
            accessoire_id = accessoryData.get('accessoire_id')

            print("this is the received accessory_id: ", accessoire_id)
            query = text("DELETE FROM cars_dealershipx.accessoires WHERE accessoire_id = :accessoryID")
            result = db.session.execute(query, {'accessoryID': accessoire_id})
            # Commit the transaction
            db.session.commit()

            # Check if any rows were affected
            if result.rowcount > 0:
                return jsonify({'message': 'Accessory deleted successfully'}), 200
            else:
                return jsonify({'error': 'Accessory not found'}), 404
        else:
            return jsonify({'error': 'Request is not in JSON format'}), 400
    except Exception as e:
        # Handle errors appropriately (log, return error response)
        return jsonify({'error': str(e)}), 500

@app.route('/testdrive', methods=['POST'])
def add_appointment():
    data = request.json


    appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d %H:%M:%S')
    status = data['status']
    customer_id = data['customer_id']
    car_id = data['car_id']


    new_appointment = TestDriveAppointment(
        appointment_date=appointment_date,
        status=status,
        customer_id=customer_id,
        car_id=car_id
    )

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment added successfully'}), 201

@app.route('/show_test_drive_appointments', methods=['GET', 'PATCH'])
def get_appointments():
    appointments = db.session.query(TestDriveAppointment).\
        join(Customer, TestDriveAppointment.customer_id == Customer.customer_id).all()

    appointment_list = []
    for appointment in appointments:
        appointment_dict = {
            'appointment_id': appointment.appointment_id,
            'appointment_date': appointment.appointment_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            'status': appointment.status,
            'customer_id': appointment.customer_id,
            'car_id': appointment.car_id,
            'first_name': appointment.customer.first_name,  # Accessing customer username through the relationship
            'last_name': appointment.customer.last_name,  # Accessing customer username through the relationship
            'phone': appointment.customer.phone  # Accessing customer phone through the relationship
        }
        appointment_list.append(appointment_dict)

    return jsonify(appointment_list)

@app.route('/update_test_drive_appointments/<int:appointment_id>', methods=['PATCH'])
def update_test_drive_appointments(appointment_id):
    # Retrieve the service request from the database
    service_request = TestDriveAppointment.query.get(appointment_id)

    if not service_request:
        return jsonify({'error': 'Test drive request not found'}), 404

    # Parse the request body for the new status
    data = request.json
    new_status = data.get('status')

    # Update the status of the service request
    service_request.status = new_status
    db.session.commit()

    # Return a response indicating success
    return jsonify({'message': 'Test drive request updated successfully'}), 200

@app.route('/test_drive_appointments/<int:customer_id>', methods=['GET'])
def get_appointments_by_customer(customer_id):
    appointments = TestDriveAppointment.query.filter_by(customer_id=customer_id).all()
    if not appointments:
        return jsonify({'message': 'No appointments found for this customer ID'}), 404

    appointment_list = []
    for appointment in appointments:
        car = Cars.query.get(appointment.car_id)  
        if car:
            car_name = f"{car.make} {car.model} {car.year}"  
            appointment_data = {
                'appointment_id': appointment.appointment_id,
                'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d %H:%M:%S'),
                'status': appointment.status,
                'customer_id': appointment.customer_id,
                'car_id': appointment.car_id,
                'car_name': car_name 
            }
            appointment_list.append(appointment_data)
    return jsonify(appointment_list), 200


def fetch_categories_from_database():
    """Fetches unique categories from the 'Accessoire' model."""
    categories = db.session.query(Accessoire.category).distinct().all()
    return [category[0] for category in categories]  # Extract category values

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = fetch_categories_from_database()
    categories_data = [{'value': category, 'label': category} for category in categories]
    return jsonify(categories_data), 200


@app.route('/fetchOffersManager', methods=['POST'])
def fetchOffersManager():
    data = request.get_json()
    status = data.get("category")
    try:   
        query = select(Offers,Cars).where(and_(Offers.car_id == Cars.car_id, Offers.offer_status == status))
        result = db.session.execute(query)
        offersDic = [{"car_id" : row.Cars.car_id, "offer_id":row.Offers.offer_id, "make" : row.Cars.make, "model" : row.Cars.model, "customer_id":row.Offers.customer_id,
            "car_image" :row.Cars.image0, "year" : row.Cars.year, "offer_price" : row.Offers.offer_price, "car_price" :row.Cars.price } for row in result]
            # print("dic", offersDic)
        return jsonify(offersDic), 200
    except Exception as e:
        db.session.rollback()
        print("error  ", str(e))
        return jsonify({'error': str(e)}), 500


#get the offers and car infos base on offer status
@app.route('/fetchOffers', methods=['POST'])
def fetchOffers():
    data = request.get_json()
    customer_id = data.get("customer_id")
    status = data.get("category")
    try:
      
        query = select(Offers,Cars).where(and_(Offers.car_id == Cars.car_id,Offers.customer_id == customer_id, Offers.offer_status == status))
        result = db.session.execute(query)
        offersDic = [{"car_id" : row.Cars.car_id, "offer_id":row.Offers.offer_id, "make" : row.Cars.make, "model" : row.Cars.model, "customer_id":row.Offers.customer_id,
            "car_image" :row.Cars.image0, "year" : row.Cars.year, "offer_price" : row.Offers.offer_price, "car_price" :row.Cars.price } for row in result]
            # print("dic", offersDic)
        return jsonify(offersDic), 200
    except Exception as e:
        db.session.rollback()
        print("error  ", str(e))
        return jsonify({'error': str(e)}), 500

#handle make offer and counter offers
@app.route('/makeOffer', methods=['POST'])
def makeOffer():
    result=0
    data = request.get_json()
    print(data['offer'])
    #counter offer case
    result = Offers.query.where(and_(Offers.car_id==data.get('car_id'),Offers.customer_id==data.get('customer_id'))).first()
    print(result)
    try:
        if(result):
           query = update(Offers).where(and_(Offers.customer_id == data.get('customer_id'), 
           Offers.car_id == data.get('car_id'))).values({Offers.offer_price : data['offer'], Offers.offer_status :data[ "status"]})
           result = db.session.execute(query)
           db.session.commit()   
        else:
        #first offer case 
            new_offer = Offers(
                offer_price=data['offer'],
                offer_status="pending",
                customer_id=data.get('customer_id'),
                car_id=data.get('car_id')
            )
            db.session.add(new_offer)
            db.session.commit()
    except Exception as e:
           db.session.rollback()
           print("ERRRORRR", str(e))
           return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'offer sent'}), 200
 

@app.route('/acceptOffer',methods=['POST'])
def AcceptOffer():
    data =  request.get_json()
    print("offerid:  ", data["customer_id"])
    try:
        db.session.begin()
        query = update(Offers).where(Offers.offer_id == data["offer_id"]).values({ Offers.offer_status :"accepted"})
        result = db.session.execute(query)
        #add the car to the cart with the oofer price
        new_cart_item = Cart(
                customer_id=data.get("customer_id"),
                item_price=data.get("offer_price"),
                item_name=data.get("car_name"),
                item_image=data.get("car_image"),
                car_id=data.get("car_id"),
                accessoire_id=None,  
                service_offered_id=None,  
                service_package_id=None  
            )

        db.session.add(new_cart_item)  
        db.session.commit() 
    except Exception as e:
        db.session.rollback()
        print("error", str(e))
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'offer added to cart and status updated to accepted'}), 200


#humza working
@app.route('/view_customer_service_details/<int:assigned_service_id>', methods=['GET'])
def view_customer_service_details(assigned_service_id):
    try:
        # Retrieve the service request details from the database
        query = text("SELECT aas.assigned_service_id, sr.service_request_id, c.make, c.model, ct.first_name, ct.last_name, so.name, so.price, so.description FROM cars_dealershipx.services_request sr join cars_dealershipx.cars c on sr.car_id = c.car_id join cars_dealershipx.customers ct on sr.customer_id = ct.customer_id join cars_dealershipx.services_offered so on sr.service_offered_id = so.services_offered_id join cars_dealershipx.assigned_services aas on sr.service_request_id = aas.service_request_id where aas.assigned_service_id = :serviceID")
        result = db.session.execute(query, {'serviceID': assigned_service_id})
        rows = result.fetchall()

        # Check if the service request details were found
        if not rows:
            return jsonify({'error': 'Service details not found'}), 404

        # Construct ticket details
        ticket_details = [{'assigned_service_id': row[0],
                           'service_request_id': row[1],
                           'car_make': row[2],
                           'car_model': row[3],
                           'customer_first_name': row[4],
                           'customer_last_name': row[5],
                           'service_name': row[6],
                           'service_price': row[7],
                           'service_description': row[8]}
                          for row in rows]

        return jsonify(ticket_details), 200
    except Exception as e:
        # Handle errors
        print('Error fetching service details:', e)
        return jsonify({'error': 'Failed to fetch service details'}), 500
    

@app.route('/submitReport', methods=['POST'])
def submitReport():
    try:
        if request.is_json:
            data = request.get_json()
            report = data.get('report')
            assigned_service_id = data.get('assigned_service_id')
            if report is None or assigned_service_id is None:
                return jsonify({'error': 'Missing report or assigned_service_id in JSON data'}), 400
            
            print("Received JSON data:", report)
            print("Received JSON data:", assigned_service_id)
            
            query = text('''INSERT INTO cars_dealershipx.service_report (assigned_service_id, report) 
                           VALUES (:assignedServiceId, :report)''')
            result = db.session.execute(query, {'assignedServiceId': assigned_service_id, 'report': report})
            print("Result row count:", result.rowcount)
            
            db.session.commit()
            
            if result.rowcount > 0:
                return jsonify({'message': 'Feedback added successfully'}), 200
            else:
                return jsonify({'error': 'Unsuccessful execution of query for feedback'}), 400
        else:
            return jsonify({'error': 'Request is not in JSON format'}), 400
    except Exception as e:
        # Log the error for debugging purposes
        print("An error occurred:", e)
        # Handle errors appropriately (log, return error response)
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/rejectOffer',methods=['POST'])
def RejectOffer():
    data =  request.get_json()
    # print("offerid:  ", data["offer_id"])
    try:
        query = update(Offers).where((Offers.offer_id==data["offer_id"])).values({ Offers.offer_status :"declined"})
        result = db.session.execute(query)
        db.session.commit() 
    except Exception as e:
        db.session.rollback()
        print("error", str(e))
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'offer status updated to declined'}), 200


@app.route('/getAccessoryCategoryManager', methods=['GET'])
def getAccessoryCategoryManager():
    try:
        # Use DISTINCT to get unique categories
        query = text("SELECT DISTINCT category FROM cars_dealershipx.accessoires")
        result = db.session.execute(query)
        rows = result.fetchall()
        
        # Extract categories from rows
        categories = [row[0] for row in rows]

        # Return categories as JSON response
        return jsonify(categories), 200
    except Exception as e:
        # Handle errors appropriately (log, return error response)
        return jsonify({'error': str(e)}), 500


@app.route('/receiveFinanceApp', methods=['POST'])
def receiveApplication():
    try:
        data = request.get_json()
        print(data)
        sendApplication(data)
        response = sendApplication(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'application recieved'}), 201
    print(response)
    return response
def sendApplication(data):
    url = 'http://localhost:5001/receive_finance_application'
    try:
        response = requests.post(url, json=data)
        print(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Stub has recieved application'}), 201
    return response.json()

if __name__ == "__main__":
    app.run(debug = True, host='localhost', port='5000')

