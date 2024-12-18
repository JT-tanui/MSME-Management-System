# MSME Management System

### **Overview**
The **MSME (Micro, Small, and Medium Enterprises) Management System** is a comprehensive web application designed to streamline the operations of small businesses. Built with **Flask** and integrated with tools for inventory, sales, expense, and financial reporting, the platform provides an all-in-one solution for managing day-to-day business operations.

Link: https://msme-management-system.onrender.com/

Test: https://msme-management-system.onrender.com/test-config

---

## **Features**

### **1. Dashboard**
- Quick overview of business metrics
- Daily sales summary
- Low stock alerts
- Monthly expense tracking
- Real-time business status

### **2. Inventory Management**
- Product tracking
- Stock level monitoring
- Reorder level alerts
- Product details management (name, quantity, price)
- Stock update history

### **3. Sales Management**
- Record new sales
- Daily/weekly/monthly sales tracking
- Product-wise sales history
- Transaction records
- Sales performance metrics

### **4. Expense Management**
- Expense categorization
- Expense recording
- Monthly expense tracking
- Expense type management
- Expense history

### **5. Reports & Analytics**
- Financial summaries
- Sales trends visualization
- Expense distribution charts
- Top-selling products
- Profit/loss analysis
- Excel export functionality

---

## **Technical Implementation**

### **Backend**
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Data Processing**: Pandas
- **File Handling**: Excel export with openpyxl

---

## **Project Structure**

```plaintext
msme-management-system/
|-- app/
|   |-- static/          # CSS, JS, Images
|   |-- templates/       # HTML Templates (Jinja2)
|   |-- routes.py        # Application Routes
|   |-- models.py        # Database Models
|   |-- utils.py         # Utility Functions (Excel Export, etc.)
|-- migrations/          # Database Migrations
|-- database.db          # SQLite Database
|-- requirements.txt     # Project Dependencies
|-- config.py            # Configuration File
|-- run.py               # Application Entry Point
|-- README.md            # Project Documentation
```

---

## **Database Schema**
The system uses a well-structured SQLite database with the following key tables:

- **Products**: Product details, stock levels, and price.
- **Sales**: Transaction history with timestamps and amounts.
- **Expenses**: Expense records categorized by type.
- **Reports**: Financial summaries and exportable data.

---

## **Deployment**
The MSME Management System can be deployed easily with the following steps:

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/msme-management-system.git
cd msme-management-system
```

### **2. Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the Application**
```bash
python run.py
```
- Access the app at `http://127.0.0.1:5000`

### **5. Deployment on Render**
- Set up the project on [Render](https://render.com/) for production hosting.
- Configure **Environment Variables** and **Database Initialization**.

---

## **Key Features in Detail**

### **1. Real-Time Stock Management**
- Automatic stock updates upon sales.
- Low stock notifications and history tracking.

### **2. Financial Tracking**
- Revenue and expense monitoring.
- Profit/loss calculation and monthly summaries.

### **3. Data Export**
- Export reports to Excel format using **openpyxl**.
- Supports custom date ranges for:
   - Inventory status
   - Sales history
   - Expense records

### **4. Analytics**
- Visualized data trends using **Chart.js**.
- Insights into sales, expenses, and performance.

---

## **Future Enhancements (Phase 2)**
- User authentication
- Customer and supplier management
- Advanced analytics
- Mobile optimization
- Email notifications
- PDF report generation
- Multi-currency support

---

## **Technologies Used**
| **Category**       | **Tools/Technologies** |
|---------------------|------------------------|
| **Backend**        | Flask, Python          |
| **Database**       | SQLite                |
| **Frontend**       | Bootstrap   |
| **Data Handling**  | Pandas, openpyxl       |
| **Deployment**     | Render                 |
| **Icons & Styling**| Font Awesome, CSS      |

---

## **Installation Requirements**
- Python 3.8+
- Flask
- SQLite
- Pandas
- openpyxl
- Bootstrap 5
- Chart.js

Install all dependencies with:
```bash
pip install -r requirements.txt
```


---

## **License**
This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

---

## **Contributing**
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-branch`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push to the branch: `git push origin feature-branch`.
5. Open a pull request.

---

## **Contact**
For questions or collaboration:
- **Name**: Job Kiprotich Busienei
- **Email**: tanuijobs11@gmail.com
- **GitHub**: [My github profile](https://github.com/https://github.com/JT-tanui/)

---

**Thank you for checking out the MSME Management System!** 🚀
