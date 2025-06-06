from sqlalchemy import Index
from lib.models.order import Order

# Define indexes to improve query performance
order_customer_id_index = Index('ix_orders_customer_id', Order.customer_id)
order_service_id_index = Index('ix_orders_service_id', Order.service_id)

# Note: To apply these indexes, you need to integrate them into your database schema creation or migration process.
# For example, if using Alembic, create a migration script to add these indexes.
