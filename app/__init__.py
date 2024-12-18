# This file marks the app directory as a Python package
from app.database import init_db, add_product, get_all_products, update_product

__all__ = ['init_db', 'add_product', 'get_all_products', 'update_product']
