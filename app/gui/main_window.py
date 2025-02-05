from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QSpinBox, QMessageBox)
from app.sales import SalesManager
from app.inventory import InventoryManager

class MSMEWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sales_manager = SalesManager()
        self.inventory = InventoryManager()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("MSME Sales Manager")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Product ID input
        self.product_id = QSpinBox()
        layout.addWidget(QLabel("Product ID:"))
        layout.addWidget(self.product_id)

        # Quantity input
        self.quantity = QSpinBox()
        self.quantity.setMaximum(1000)
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.quantity)

        # Price input
        self.price = QLineEdit()
        layout.addWidget(QLabel("Unit Price:"))
        layout.addWidget(self.price)

        # Submit button
        submit_btn = QPushButton("Record Sale")
        submit_btn.clicked.connect(self.record_sale)
        layout.addWidget(submit_btn)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def record_sale(self):
        try:
            success = self.sales_manager.record_sale(
                product_id=self.product_id.value(),
                quantity_sold=self.quantity.value(),
                unit_price=float(self.price.text() or 0)
            )
            if success:
                QMessageBox.information(self, "Success", "Sale recorded successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to record sale")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))