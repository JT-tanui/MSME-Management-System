import sqlite3
import os
from flask import g

def get_db_connection():
    """Create a database connection"""
    try:
        if 'db' not in g:
            # Ensure instance folder exists
            os.makedirs('instance', exist_ok=True)
            
            # Connect to database
            g.db = sqlite3.connect(
                'instance/msme.db',
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

        return g.db
    except RuntimeError:
        # Handle case when outside application context
        os.makedirs('instance', exist_ok=True)
        
        # Connect to database
        db = sqlite3.connect(
            'instance/msme.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
        return db

def close_db(e=None):
    """Close the database connection"""
    db = g.pop('db', None)
    
    if db is not None:
        db.close() 