from lib.helpers import (
    clear_screen,
    exit_program,
    # Customer helpers
    view_all_customers,
    find_customer_by_id,
    find_customer_by_phone,
    add_customer,
    update_customer,
    delete_customer,
    view_customer_orders,
    # Service helpers
    view_all_services,
    find_service_by_id,
    add_service,
    update_service,
    delete_service,
    # Order helpers
    view_all_orders,
    find_order_by_id,
    add_order,
    update_order_status,
    delete_order,
    view_order_history,
    # Location helpers
    view_all_locations,
    find_location_by_id,
    add_location,
    update_location,
    delete_location,
    # Report helpers
    generate_daily_orders_report,
    generate_customer_report,
    generate_revenue_report,
    view_upcoming_pickups,
    view_top_customers
)

from lib.models import create_tables
from lib.db.seed import seed_database

def display_header():
    """Display the application header"""
    clear_screen()
    print("=" * 60)
    print("                  LAUNDRYCONNECT KENYA")
    print("                Laundry Management System")
    print("=" * 60)
    print()

from lib.models.user import User
from lib.models.customer import Customer

current_user = None

def register():
    print("\n===== User Registration =====")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (customer/manager): ").strip().lower()
    is_customer = role == "customer"
    is_manager = role == "manager"
    
    from lib.db import get_session
    session = get_session()
    
    if User.find_by_username(session, username):
        print("Username already exists. Please try again.")
        return
    
    user = User.create(session, username, password, is_customer=is_customer, is_manager=is_manager)
    
    if is_customer:
        name = input("Enter your full name: ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email (optional): ")
        address = input("Enter your address (optional): ")
        Customer.create(session, name, phone, email, address, user_id=user.id)
    
    print("Registration successful! You can now log in.")

def login():
    global current_user
    print("\n===== User Login =====")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    from lib.db import get_session
    session = get_session()
    
    user = User.find_by_username(session, username)
    if not user or not user.check_password(password):
        print("Invalid username or password.")
        return
    
    current_user = user
    print(f"Welcome, {user.username}!")

def logout():
    global current_user
    current_user = None
    print("You have been logged out.")

def main():
    # Create database tables if they don't exist
    create_tables()
    
    while True:
        if current_user is None:
            print("\n===== Welcome to LaundryConnect =====")
            print("1. Register")
            print("2. Login")
            print("0. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                register()
            elif choice == "2":
                login()
            elif choice == "0":
                exit_program()
            else:
                print("Invalid choice. Please try again.")
        else:
            main_menu_loop()

def main_menu_loop():
    """Main application loop"""
    while True:
        display_header()
        # Show different menus based on user role
        if current_user.is_manager:
            main_menu()
            choice = input("\nEnter your choice: ")
            
            if choice == "0":
                exit_program()
            elif choice == "1":
                customer_menu()
            elif choice == "2":
                order_menu()
            elif choice == "3":
                service_menu()
            elif choice == "4":
                location_menu()
            elif choice == "5":
                report_menu()
            else:
                print("\nInvalid choice. Please try again.")
                input("\nPress Enter to continue...")
        elif current_user.is_customer:
            customer_order_menu()
        else:
            print("Unknown user role. Exiting.")
            exit_program()

def main_menu():
    print("\n===== Main Menu =====")
    print("1. Customer Management")
    print("2. Order Management")
    print("3. Service Management")
    print("4. Location Management")
    print("5. Reports")
    print("0. Exit")

def customer_order_menu():
    while True:
        display_header()
        print("\n===== Customer Order Menu =====")
        print("1. Place New Order")
        print("2. View My Orders")
        print("0. Logout")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            logout()
            return
        elif choice == "1":
            place_order()
        elif choice == "2":
            view_my_orders()
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

def place_order():
    from lib.db import get_session
    from lib.models import Service, Order
    session = get_session()
    
    print("\nAvailable Services:")
    services = session.query(Service).all()
    for service in services:
        print(f"{service.id}. {service.name} - {service.price_per_unit} per {service.unit}")
    
    service_id = input("Enter service ID to select: ")
    try:
        service_id = int(service_id)
    except ValueError:
        print("Invalid service ID.")
        return
    
    weight = input("Enter approximate weight (kgs): ")
    try:
        weight = float(weight)
        if weight <= 0:
            raise ValueError()
    except ValueError:
        print("Invalid weight.")
        return
    
    # Calculate approximate price
    service = session.query(Service).filter_by(id=service_id).first()
    if not service:
        print("Service not found.")
        return
    approx_price = service.price_per_unit * weight
    print(f"Approximate price: {approx_price}")
    
    pickup_date = input("Enter pickup date (YYYY-MM-DD): ")
    pickup_time = input("Enter pickup time (morning/afternoon/evening): ")
    special_instructions = input("Any special instructions? (optional): ")
    
    try:
        order = Order.create(
            session=session,
            customer_id=current_user.customer.id,
            service_id=service_id,
            weight=weight,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            special_instructions=special_instructions
        )
        print(f"Order placed successfully! Order ID: {order.id}")
    except Exception as e:
        print(f"Error placing order: {e}")

def view_my_orders():
    from lib.db import get_session
    from lib.models import Order
    session = get_session()
    
    orders = session.query(Order).filter_by(customer_id=current_user.customer.id).all()
    if not orders:
        print("You have no orders.")
        return
    
    for order in orders:
        print(f"Order ID: {order.id}, Service: {order.service.name}, Weight: {order.weight} kgs, Total Price: {order.total_price}, Status: {order.status}")
        print("Status History:")
        for status in order.status_history:
            print(f" - {status.status} at {status.timestamp}")
        print("-" * 40)


def main_menu():
    print("\n===== Main Menu =====")
    print("1. Customer Management")
    print("2. Order Management")
    print("3. Service Management")
    print("4. Location Management")
    print("5. Reports")
    print("0. Exit")

def customer_menu():
    while True:
        display_header()
        print("\n===== Customer Management =====")
        print("1. View All Customers")
        print("2. Find Customer by ID")
        print("3. Find Customer by Phone")
        print("4. Add New Customer")
        print("5. Update Customer")
        print("6. Delete Customer")
        print("7. View Customer Orders")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
        elif choice == "1":
            view_all_customers()
        elif choice == "2":
            find_customer_by_id()
        elif choice == "3":
            find_customer_by_phone()
        elif choice == "4":
            add_customer()
        elif choice == "5":
            update_customer()
        elif choice == "6":
            delete_customer()
        elif choice == "7":
            view_customer_orders()
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

def order_menu():
    while True:
        display_header()
        print("\n===== Order Management =====")
        print("1. View All Orders")
        print("2. Find Order by ID")
        print("3. Create New Order")
        print("4. Update Order Status")
        print("5. Delete Order")
        print("6. View Order Status History")
        print("7. Tick Order Status Stage")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
        elif choice == "1":
            view_all_orders()
        elif choice == "2":
            find_order_by_id()
        elif choice == "3":
            add_order()
        elif choice == "4":
            update_order_status()
        elif choice == "5":
            delete_order()
        elif choice == "6":
            view_order_history()
        elif choice == "7":
            tick_order_status_stage()
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

def tick_order_status_stage():
    from lib.db import get_session
    session = get_session()
    
    order_id = input("Enter Order ID to update status: ")
    try:
        order_id = int(order_id)
    except ValueError:
        print("Invalid Order ID.")
        return
    
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        print("Order not found.")
        return
    
    print(f"Current status: {order.status}")
    print("Available status stages:")
    stages = ["picked", "washed", "ironed", "drying", "awaits delivery", "delivered"]
    for i, stage in enumerate(stages, 1):
        print(f"{i}. {stage}")
    
    choice = input("Select status stage to tick: ")
    try:
        choice = int(choice)
        if choice < 1 or choice > len(stages):
            raise ValueError()
    except ValueError:
        print("Invalid choice.")
        return
    
    new_status = stages[choice - 1]
    if new_status == order.status:
        print("Order already at this status.")
        return
    
    # Update order status
    order.status = new_status
    session.commit()
    
    # Add to status history
    from lib.models.order_status_history import OrderStatusHistory
    history_entry = OrderStatusHistory(
        order_id=order.id,
        status=new_status,
        timestamp=datetime.utcnow()
    )
    session.add(history_entry)
    session.commit()
    
    print(f"Order status updated to '{new_status}'.")

def service_menu():
    while True:
        display_header()
        print("\n===== Service Management =====")
        print("1. View All Services")
        print("2. Find Service by ID")
        print("3. Add New Service")
        print("4. Update Service")
        print("5. Delete Service")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
        elif choice == "1":
            view_all_services()
        elif choice == "2":
            find_service_by_id()
        elif choice == "3":
            add_service()
        elif choice == "4":
            update_service()
        elif choice == "5":
            delete_service()
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

def location_menu():
    while True:
        display_header()
        print("\n===== Location Management =====")
        print("1. View All Locations")
        print("2. Find Location by ID")
        print("3. Add New Location")
        print("4. Update Location")
        print("5. Delete Location")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
        elif choice == "1":
            view_all_locations()
        elif choice == "2":
            find_location_by_id()
        elif choice == "3":
            add_location()
        elif choice == "4":
            update_location()
        elif choice == "5":
            delete_location()
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

def report_menu():
    while True:
        display_header()
        print("\n===== Reports =====")
        print("1. Daily Orders Report")
        print("2. Customer Report")
        print("3. Revenue Report")
        print("4. Upcoming Pickups")
        print("5. Top Customers")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
        elif choice == "1":
            generate_daily_orders_report()
        elif choice == "2":
            generate_customer_report()
        elif choice == "3":
            generate_revenue_report()
        elif choice == "4":
            view_upcoming_pickups()
        elif choice == "5":
            view_top_customers()
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
