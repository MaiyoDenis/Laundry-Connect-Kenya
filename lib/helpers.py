import sys
from lib.models.customer import Customer
from lib.models.order import Order
from lib.models.service import Service
from lib.models.location import Location
from lib.models.order_status_history import OrderStatusHistory
from lib.db.models import SessionLocal
from datetime import datetime

def clear_screen():
    print("\033[H\033[J", end="")

def exit_program():
    print("Goodbye!")
    sys.exit()

# Customer helpers
def view_all_customers():
    session = SessionLocal()
    customers = Customer.get_all(session)
    if not customers:
        print("No customers found.")
    else:
        for c in customers:
            print(f"ID: {c.id}, Name: {c.name}, Phone: {c.phone}, Email: {c.email}, Address: {c.address}")
    input("\nPress Enter to continue...")
    session.close()

def find_customer_by_id():
    session = SessionLocal()
    try:
        id = int(input("Enter customer ID: "))
        customer = Customer.find_by_id(session, id)
        if customer:
            print(f"ID: {customer.id}, Name: {customer.name}, Phone: {customer.phone}, Email: {customer.email}, Address: {customer.address}")
        else:
            print("Customer not found.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def find_customer_by_phone():
    session = SessionLocal()
    phone = input("Enter customer phone: ")
    customer = Customer.find_by_phone(session, phone)
    if customer:
        print(f"ID: {customer.id}, Name: {customer.name}, Phone: {customer.phone}, Email: {customer.email}, Address: {customer.address}")
    else:
        print("Customer not found.")
    input("\nPress Enter to continue...")
    session.close()

def add_customer():
    session = SessionLocal()
    name = input("Enter customer name: ").strip()
    phone = input("Enter customer phone: ").strip()
    email = input("Enter customer email (optional): ").strip()
    address = input("Enter customer address (optional): ").strip()
    if not name or not phone:
        print("Name and phone are required.")
    else:
        customer = Customer.create(session, name, phone, email or None, address or None)
        print(f"Customer created with ID: {customer.id}")
    input("\nPress Enter to continue...")
    session.close()

def update_customer():
    session = SessionLocal()
    try:
        id = int(input("Enter customer ID to update: "))
        customer = Customer.find_by_id(session, id)
        if not customer:
            print("Customer not found.")
        else:
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
                print("Customer updated successfully.")
            else:
                print("Update failed.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def delete_customer():
    session = SessionLocal()
    try:
        id = int(input("Enter customer ID to delete: "))
        success = Customer.delete(session, id)
        if success:
            print("Customer deleted successfully.")
        else:
            print("Customer not found or could not be deleted.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def view_customer_orders():
    session = SessionLocal()
    try:
        id = int(input("Enter customer ID to view orders: "))
        orders = Order.find_by_customer(session, id)
        if not orders:
            print("No orders found for this customer.")
        else:
            for o in orders:
                print(f"Order ID: {o.id}, Service ID: {o.service_id}, Weight: {o.weight}, Status: {o.status}, Pickup Date: {o.pickup_date}")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

# Service helpers
def view_all_services():
    session = SessionLocal()
    services = Service.get_all(session)
    if not services:
        print("No services found.")
    else:
        for s in services:
            print(f"ID: {s.id}, Name: {s.name}, Price per Unit: {s.price_per_unit}")
    input("\nPress Enter to continue...")
    session.close()

def find_service_by_id():
    session = SessionLocal()
    try:
        id = int(input("Enter service ID: "))
        service = Service.find_by_id(session, id)
        if service:
            print(f"ID: {service.id}, Name: {service.name}, Price per Unit: {service.price_per_unit}")
        else:
            print("Service not found.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def add_service():
    session = SessionLocal()
    name = input("Enter service name: ").strip()
    try:
        price_per_unit = float(input("Enter price per unit: "))
        if not name:
            print("Service name is required.")
        else:
            service = Service.create(session, name, price_per_unit)
            print(f"Service created with ID: {service.id}")
    except ValueError:
        print("Invalid input. Price must be a number.")
    input("\nPress Enter to continue...")
    session.close()

def update_service():
    session = SessionLocal()
    try:
        id = int(input("Enter service ID to update: "))
        service = Service.find_by_id(session, id)
        if not service:
            print("Service not found.")
        else:
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
                print("Service updated successfully.")
            else:
                print("Update failed.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def delete_service():
    session = SessionLocal()
    try:
        id = int(input("Enter service ID to delete: "))
        success = Service.delete(session, id)
        if success:
            print("Service deleted successfully.")
        else:
            print("Service not found or could not be deleted.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

# Order helpers
def view_all_orders():
    session = SessionLocal()
    orders = Order.get_all(session)
    if not orders:
        print("No orders found.")
    else:
        for o in orders:
            print(f"Order ID: {o.id}, Customer ID: {o.customer_id}, Service ID: {o.service_id}, Weight: {o.weight}, Status: {o.status}, Pickup Date: {o.pickup_date}")
    input("\nPress Enter to continue...")
    session.close()

def find_order_by_id():
    session = SessionLocal()
    try:
        id = int(input("Enter order ID: "))
        order = Order.find_by_id(session, id)
        if order:
            print(f"Order ID: {order.id}, Customer ID: {order.customer_id}, Service ID: {order.service_id}, Weight: {order.weight}, Status: {order.status}, Pickup Date: {order.pickup_date}")
        else:
            print("Order not found.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def add_order():
    session = SessionLocal()
    try:
        customer_id = int(input("Enter customer ID: "))
        service_id = int(input("Enter service ID: "))
        weight = float(input("Enter weight: "))
        pickup_date = input("Enter pickup date (YYYY-MM-DD): ").strip()
        pickup_time = input("Enter pickup time (morning, afternoon, evening): ").strip()
        special_instructions = input("Enter special instructions (optional): ").strip() or None
        order = Order.create(session, customer_id, service_id, weight, pickup_date, pickup_time, special_instructions)
        print(f"Order created with ID: {order.id}")
    except ValueError as e:
        print(f"Invalid input: {e}")
    input("\nPress Enter to continue...")
    session.close()

def update_order_status():
    session = SessionLocal()
    try:
        id = int(input("Enter order ID to update status: "))
        order = Order.find_by_id(session, id)
        if not order:
            print("Order not found.")
        else:
            status = input(f"Enter new status (current: {order.status}): ").strip()
            updated_order = Order.update(session, id, status=status)
            if updated_order:
                print("Order status updated successfully.")
            else:
                print("Update failed.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def delete_order():
    session = SessionLocal()
    try:
        id = int(input("Enter order ID to delete: "))
        success = Order.delete(session, id)
        if success:
            print("Order deleted successfully.")
        else:
            print("Order not found or could not be deleted.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def view_order_history():
    session = SessionLocal()
    try:
        id = int(input("Enter order ID to view status history: "))
        histories = session.query(OrderStatusHistory).filter_by(order_id=id).all()
        if not histories:
            print("No status history found for this order.")
        else:
            for h in histories:
                print(f"Status: {h.status}, Timestamp: {h.timestamp}")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

# Location helpers
def view_all_locations():
    session = SessionLocal()
    locations = Location.get_all(session)
    if not locations:
        print("No locations found.")
    else:
        for l in locations:
            print(f"ID: {l.id}, Name: {l.name}")
    input("\nPress Enter to continue...")
    session.close()

def find_location_by_id():
    session = SessionLocal()
    try:
        id = int(input("Enter location ID: "))
        location = Location.find_by_id(session, id)
        if location:
            print(f"ID: {location.id}, Name: {location.name}")
        else:
            print("Location not found.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def add_location():
    session = SessionLocal()
    name = input("Enter location name: ").strip()
    address = input("Enter location address (optional): ").strip()
    phone = input("Enter location phone (optional): ").strip()
    email = input("Enter location email (optional): ").strip()
    if not name:
        print("Location name is required.")
    else:
        location = Location.create(session, name, address or None, phone or None, email or None)
        print(f"Location created with ID: {location.id}")
    input("\nPress Enter to continue...")
    session.close()

def update_location():
    session = SessionLocal()
    try:
        id = int(input("Enter location ID to update: "))
        location = Location.find_by_id(session, id)
        if not location:
            print("Location not found.")
        else:
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
                    print("Location updated successfully.")
                else:
                    print("Update failed.")
            else:
                print("No changes made.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

def delete_location():
    session = SessionLocal()
    try:
        id = int(input("Enter location ID to delete: "))
        success = Location.delete(session, id)
        if success:
            print("Location deleted successfully.")
        else:
            print("Location not found or could not be deleted.")
    except ValueError:
        print("Invalid input. ID must be an integer.")
    input("\nPress Enter to continue...")
    session.close()

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
