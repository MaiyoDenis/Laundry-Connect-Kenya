# LaundryConnect Kenya CLI Project

This project is a Command Line Interface (CLI) application built using Python, SQLAlchemy ORM, Alembic for database migrations, and Pipenv for environment management. It is designed to manage a laundry service in Kenya where customers can register, place orders, and track their laundry services.

## Project Structure

```
.
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib
    ├── cli.py
    ├── helpers.py
    ├── db
    │   ├── models.py
    │   └── seed.py
    ├── models
    │   ├── __init__.py
    │   ├── base.py
    │   ├── customer.py
    │   ├── order.py
    │   ├── service.py
    │   ├── location.py
    │   └── order_status_history.py
    └── debug.py
```

## Setup Instructions

1. Install Pipenv if you don't have it:
   ```
   pip install pipenv
   ```

2. Install dependencies and activate the virtual environment:
   ```
   pipenv install
   pipenv shell
   ```

3. Initialize Alembic migrations:
   ```
   cd lib/db
   alembic init migrations
   ```

4. Modify Alembic configuration as needed and start development.

## Usage

Run the CLI application:
```
python lib/cli.py
```

Follow the on-screen menus to manage customers, orders, services, locations, and generate reports.

## Features

- Customer registration and management
- Order creation, status updates, and history tracking
- Service management with pricing
- Location management
- Reports on orders, revenue, and top customers

## Technologies Used

- Python 3.8
- SQLAlchemy ORM
- Alembic for migrations
- Pipenv for environment management

## Author

LaundryConnect Kenya Team
