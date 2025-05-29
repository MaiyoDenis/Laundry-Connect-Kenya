from lib.models import create_tables
from lib.db.seed import seed_database

def init_db():
    create_tables()
    seed_database()

if __name__ == "__main__":
    init_db()
    print("Database created and seeded successfully.")
