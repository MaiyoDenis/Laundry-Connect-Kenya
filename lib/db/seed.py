from lib.db.models import SessionLocal, create_tables
from lib.models.customer import Customer
from lib.models.service import Service
from lib.models.location import Location
from lib.models.order import Order
from datetime import date

def seed_database():
    # Avoid circular import by importing create_tables here
    from lib.models import create_tables
    create_tables()
    session = SessionLocal()

    # Seed services
    services = [
        {"name": "Wash & Fold", "price_per_unit": 5.0, "description": "Basic wash and fold service", "unit": "kg"},
        {"name": "Dry Cleaning", "price_per_unit": 10.0, "description": "Professional dry cleaning", "unit": "item"},
        {"name": "Ironing", "price_per_unit": 3.0, "description": "Clothes ironing service", "unit": "item"},
    ]
    for s in services:
        service = Service(name=s["name"], price_per_unit=s["price_per_unit"], description=s["description"], unit=s["unit"])
        session.add(service)

    # Seed locations
    locations = [
        {"name": "Nairobi", "address": "123 Nairobi St", "phone": "0711000000", "email": "nairobi@laundry.com"},
        {"name": "Mombasa", "address": "456 Mombasa Rd", "phone": "0722000000", "email": "mombasa@laundry.com"},
        {"name": "Kisumu", "address": "789 Kisumu Ave", "phone": "0733000000", "email": "kisumu@laundry.com"},
    ]
    for l in locations:
        location = Location(name=l["name"], address=l["address"], phone=l["phone"], email=l["email"])
        session.add(location)

    # Seed customers
    customers = [
        {"name": "Alice", "phone": "0712345678", "email": "alice@example.com", "address": "Nairobi"},
        {"name": "Bob", "phone": "0723456789", "email": "bob@example.com", "address": "Mombasa"},
    ]
    for c in customers:
        customer = Customer(name=c["name"], phone=c["phone"], email=c["email"], address=c["address"])
        session.add(customer)

    session.commit()

    # Seed orders (example)
    # Assuming services and customers have been committed and have IDs
    service_wash = session.query(Service).filter_by(name="Wash & Fold").first()
    customer_alice = session.query(Customer).filter_by(name="Alice").first()

    if service_wash and customer_alice:
        order = Order(
            customer_id=customer_alice.id,
            service_id=service_wash.id,
            weight=10.0,
            total_price=service_wash.price_per_unit * 10.0,
            status="placed",
            pickup_date=date.today(),
            pickup_time="morning",
            special_instructions="Handle with care"
        )
        session.add(order)
        session.commit()

    session.close()
