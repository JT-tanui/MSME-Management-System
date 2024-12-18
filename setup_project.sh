#!/bin/bash

# Create directories
mkdir -p app
mkdir -p templates
mkdir -p static/css
mkdir -p static/js
mkdir -p data
mkdir -p docs

# Create app files
touch app/__init__.py
touch app/main.py
touch app/database.py
touch app/inventory.py
touch app/sales.py
touch app/expenses.py
touch app/reports.py

# Create template files
touch templates/base.html
touch templates/inventory.html
touch templates/sales.html
touch templates/expenses.html
touch templates/reports.html

# Create static files
touch static/css/style.css
touch static/js/app.js

# Create doc files
touch docs/README.md
touch docs/user_guide.pdf

# Create root level files
touch requirements.txt
touch run_app.py

echo "Project structure created successfully!" 