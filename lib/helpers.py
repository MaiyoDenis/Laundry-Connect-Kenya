import sys
import logging
from lib.models.customer import Customer
from lib.models.order import Order
from lib.models.service import Service
from lib.models.location import Location
from lib.models.order_status_history import OrderStatusHistory
from lib.db.models import SessionLocal
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_screen():
    print("\033[H\033[J", end="")

def exit_program():
    print("Goodbye!")
    sys.exit()

# Customer helpers
def view_all_customers():
    with SessionLocal() as session:
        customers = Customer.get_all(session)
        if not customers:
            print("No customers found.")
        else:
            for c in customers:
                print(f"ID: {c.id}, Name: {c.name}, Phone: {c.phone}, Email: {c.email}, Address: {c.address}")
    input("\nPress Enter to continue...")

def find_customer_by_id():
    try:
        id = int(input("Enter customer ID: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        customer = Customer.find_by_id(session, id)
        if customer:
            print(f"ID: {customer.id}, Name: {customer.name}, Phone: {customer.phone}, Email: {customer.email}, Address: {customer.address}")
        else:
            print("Customer not found.")
    input("\nPress Enter to continue...")

def find_customer_by_phone():
    phone = input("Enter customer phone: ")
    with SessionLocal() as session:
        customer = Customer.find_by_phone(session, phone)
        if customer:
            print(f"ID: {customer.id}, Name: {customer.name}, Phone: {customer.phone}, Email: {customer.email}, Address: {customer.address}")
        else:
            print("Customer not found.")
    input("\nPress Enter to continue...")

def add_customer():
    name = input("Enter customer name: ").strip()
    phone = input("Enter customer phone: ").strip()
    email = input("Enter customer email (optional): ").strip()
    address = input("Enter customer address (optional): ").strip()
    if not name or not phone:
        print("Name and phone are required.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        customer = Customer.create(session, name, phone, email or None, address or None)
        logger.info(f"Customer created with ID: {customer.id}")
        print(f"Customer created with ID: {customer.id}")
    input("\nPress Enter to continue...")

def update_customer():
    try:
        id = int(input("Enter customer ID to update: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        customer = Customer.find_by_id(session, id)
        if not customer:
            print("Customer not found.")
            input("\nPress Enter to continue...")
            return
        name = input(f"Enter new name (current: {customer.name}): ").strip()
        phone = input(f"Enter new phone (current: {customer.phone}): ").strip()
        email = input(f"Enter new email (current: {customer.email}): ").strip()
        address = input(f"Enter new address (current: {customer.address}): ").strip()
        updates = {}
        if name:
            updates['name'] = name
        if phone:
            updates['phone'] = phone
        if email:
            updates['email'] = email
        if address:
            updates['address'] = address
        updated_customer = Customer.update(session, id, **updates)
        if updated_customer:
            logger.info(f"Customer updated with ID: {id}")
            print("Customer updated successfully.")
        else:
            print("Update failed.")
    input("\nPress Enter to continue...")

def delete_customer():
    try:
        id = int(input("Enter customer ID to delete: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        success = Customer.delete(session, id)
        if success:
            logger.info(f"Customer deleted with ID: {id}")
            print("Customer deleted successfully.")
        else:
            print("Customer not found or could not be deleted.")
    input("\nPress Enter to continue...")

def view_customer_orders():
    try:
        id = int(input("Enter customer ID to view orders: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        orders = Order.find_by_customer(session, id)
        if not orders:
            print("No orders found for this customer.")
        else:
            for o in orders:
                print(f"Order ID: {o.id}, Service ID: {o.service_id}, Weight: {o.weight}, Status: {o.status}, Pickup Date: {o.pickup_date}")
    input("\nPress Enter to continue...")

# Service helpers
def view_all_services():
    with SessionLocal() as session:
        services = Service.get_all(session)
        if not services:
            print("No services found.")
        else:
            for s in services:
                print(f"ID: {s.id}, Name: {s.name}, Price per Unit: {s.price_per_unit}")
    input("\nPress Enter to continue...")

def find_service_by_id():
    try:
        id = int(input("Enter service ID: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        service = Service.find_by_id(session, id)
        if service:
            print(f"ID: {service.id}, Name: {service.name}, Price per Unit: {service.price_per_unit}")
        else:
            print("Service not found.")
    input("\nPress Enter to continue...")

def add_service():
    name = input("Enter service name: ").strip()
    try:
        price_per_unit = float(input("Enter price per unit: "))
    except ValueError:
        print("Invalid input. Price must be a number.")
        input("\nPress Enter to continue...")
        return
    if not name:
        print("Service name is required.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        service = Service.create(session, name, price_per_unit)
        logger.info(f"Service created with ID: {service.id}")
        print(f"Service created with ID: {service.id}")
    input("\nPress Enter to continue...")

def update_service():
    try:
        id = int(input("Enter service ID to update: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        service = Service.find_by_id(session, id)
        if not service:
            print("Service not found.")
            input("\nPress Enter to continue...")
            return
        name = input(f"Enter new name (current: {service.name}): ").strip()
        price_input = input(f"Enter new price per unit (current: {service.price_per_unit}): ").strip()
        updates = {}
        if name:
            updates['name'] = name
        if price_input:
            try:
                updates['price_per_unit'] = float(price_input)
            except ValueError:
                print("Invalid price input. Skipping price update.")
        updated_service = Service.update(session, id, **updates)
        if updated_service:
            logger.info(f"Service updated with ID: {id}")
            print("Service updated successfully.")
        else:
            print("Update failed.")
    input("\nPress Enter to continue...")

def delete_service():
    try:
        id = int(input("Enter service ID to delete: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        success = Service.delete(session, id)
        if success:
            logger.info(f"Service deleted with ID: {id}")
            print("Service deleted successfully.")
        else:
            print("Service not found or could not be deleted.")
    input("\nPress Enter to continue...")

# Order helpers
def view_all_orders():
    with SessionLocal() as session:
        orders = Order.get_all(session)
        if not orders:
            print("No orders found.")
        else:
            for o in orders:
                print(f"Order ID: {o.id}, Customer ID: {o.customer_id}, Service ID: {o.service_id}, Weight: {o.weight}, Status: {o.status}, Pickup Date: {o.pickup_date}")
    input("\nPress Enter to continue...")

def find_order_by_id():
    try:
        id = int(input("Enter order ID: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        order = Order.find_by_id(session, id)
        if order:
            print(f"Order ID: {order.id}, Customer ID: {order.customer_id}, Service ID: {order.service_id}, Weight: {order.weight}, Status: {order.status}, Pickup Date: {order.pickup_date}")
        else:
            print("Order not found.")
    input("\nPress Enter to continue...")

def add_order():
    try:
        customer_id = int(input("Enter customer ID: "))
        service_id = int(input("Enter service ID: "))
        weight = float(input("Enter weight: "))
    except ValueError as e:
        print(f"Invalid input: {e}")
        input("\nPress Enter to continue...")
        return
    pickup_date_str = input("Enter pickup date (YYYY-MM-DD): ").strip()
    pickup_time = input("Enter pickup time (morning, afternoon, evening): ").strip()
    special_instructions = input("Enter special instructions (optional): ").strip() or None

    try:
        pickup_date = datetime.strptime(pickup_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        input("\nPress Enter to continue...")
        return

    with SessionLocal() as session:
        service = Service.find_by_id(session, service_id)
        if not service:
            print("Service not found.")
            input("\nPress Enter to continue...")
            return

        total_price = weight * service.price_per_unit

        order = Order.create(session, customer_id, service_id, weight, total_price, pickup_date, pickup_time, special_instructions)
        logger.info(f"Order created with ID: {order.id}")
        print(f"Order created with ID: {order.id}")
    input("\nPress Enter to continue...")

def update_order_status():
    try:
        id = int(input("Enter order ID to update status: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        order = Order.find_by_id(session, id)
        if not order:
            print("Order not found.")
            input("\nPress Enter to continue...")
            return
        status = input(f"Enter new status (current: {order.status}): ").strip()
        updated_order = Order.update(session, id, status=status)
        if updated_order:
            logger.info(f"Order status updated for ID: {id}")
            print("Order status updated successfully.")
        else:
            print("Update failed.")
    input("\nPress Enter to continue...")

def delete_order():
    try:
        id = int(input("Enter order ID to delete: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        success = Order.delete(session, id)
        if success:
            logger.info(f"Order deleted with ID: {id}")
            print("Order deleted successfully.")
        else:
            print("Order not found or could not be deleted.")
    input("\nPress Enter to continue...")

def view_order_history():
    try:
        id = int(input("Enter order ID to view status history: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        histories = session.query(OrderStatusHistory).filter_by(order_id=id).all()
        if not histories:
            print("No status history found for this order.")
        else:
            for h in histories:
                print(f"Status: {h.status}, Timestamp: {h.timestamp}")
    input("\nPress Enter to continue...")

# Location helpers
def view_all_locations():
    with SessionLocal() as session:
        locations = Location.get_all(session)
        if not locations:
            print("No locations found.")
        else:
            for l in locations:
                print(f"ID: {l.id}, Name: {l.name}")
    input("\nPress Enter to continue...")

def find_location_by_id():
    try:
        id = int(input("Enter location ID: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        location = Location.find_by_id(session, id)
        if location:
            print(f"ID: {location.id}, Name: {location.name}")
        else:
            print("Location not found.")
    input("\nPress Enter to continue...")

def add_location():
    name = input("Enter location name: ").strip()
    address = input("Enter location address (optional): ").strip()
    phone = input("Enter location phone (optional): ").strip()
    email = input("Enter location email (optional): ").strip()
    if not name:
        print("Location name is required.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        location = Location.create(session, name, address or None, phone or None, email or None)
        logger.info(f"Location created with ID: {location.id}")
        print(f"Location created with ID: {location.id}")
    input("\nPress Enter to continue...")

def update_location():
    try:
        id = int(input("Enter location ID to update: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        location = Location.find_by_id(session, id)
        if not location:
            print("Location not found.")
            input("\nPress Enter to continue...")
            return
        name = input(f"Enter new name (current: {location.name}): ").strip()
        address = input(f"Enter new address (current: {location.address}): ").strip()
        phone = input(f"Enter new phone (current: {location.phone}): ").strip()
        email = input(f"Enter new email (current: {location.email}): ").strip()
        updates = {}
        if name:
            updates['name'] = name
        if address:
            updates['address'] = address
        if phone:
            updates['phone'] = phone
        if email:
            updates['email'] = email
        if updates:
            updated_location = Location.update(session, id, **updates)
            if updated_location:
                logger.info(f"Location updated with ID: {id}")
                print("Location updated successfully.")
            else:
                print("Update failed.")
        else:
            print("No changes made.")
    input("\nPress Enter to continue...")

def delete_location():
    try:
        id = int(input("Enter location ID to delete: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        input("\nPress Enter to continue...")
        return
    with SessionLocal() as session:
        success = Location.delete(session, id)
        if success:
            logger.info(f"Location deleted with ID: {id}")
            print("Location deleted successfully.")
        else:
            print("Location not found or could not be deleted.")
    input("\nPress Enter to continue...")

# Report helpers
def generate_daily_orders_report():
    print("Daily Orders Report - Not yet implemented.")
    input("\nPress Enter to continue...")

def generate_customer_report():
    print("Customer Report - Not yet implemented.")
    input("\nPress Enter to continue...")

def generate_revenue_report():
    print("Revenue Report - Not yet implemented.")
    input("\nPress Enter to continue...")

def view_upcoming_pickups():
    print("Upcoming Pickups - Not yet implemented.")
    input("\nPress Enter to continue...")

def view_top_customers():
    print("Top Customers - Not yet implemented.")
    input("\nPress Enter to continue...")
