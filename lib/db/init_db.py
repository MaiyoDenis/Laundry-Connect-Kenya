from lib.models import create_tables
from lib.db.seed import seed_database
from lib.db.indexes import order_customer_id_index, order_service_id_index
from lib.db.models import Base, engine

def init_db():
    create_tables()
    # Create indexes
    order_customer_id_index.create(bind=engine)
    order_service_id_index.create(bind=engine)
    seed_database()

if __name__ == "__main__":
    init_db()
    print("Database created and seeded successfully.")
