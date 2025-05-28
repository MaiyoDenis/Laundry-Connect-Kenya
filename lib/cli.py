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

def main():
    # Create database tables if they don't exist
    create_tables()
    
    main_menu_loop()

def main_menu_loop():
    """Main application loop"""
    while True:
        display_header()
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
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

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
