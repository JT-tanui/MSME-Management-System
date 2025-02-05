# This file marks the app directory as a Python package
from app.database import init_db, add_product, get_all_products, update_product
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

__all__ = ['init_db', 'add_product', 'get_all_products', 'update_product']
