from .models import SessionLocal as Session

def get_session():
    return Session()
