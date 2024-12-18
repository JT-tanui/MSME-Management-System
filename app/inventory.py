from typing import Dict, List, Optional, Union
from app.database import (
    add_product, 
    get_all_products, 
    update_product, 
    delete_product,
    search_products,
    get_low_stock_products
)

class InventoryManager:
    @staticmethod
    def add_new_product(
        product_name: str, 
        quantity: int, 
        unit_price: float, 
        reorder_level: int = 10
    ) -> bool:
        """Add a new product to inventory"""
        try:
            add_product(product_name, quantity, unit_price, reorder_level)
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False

    @staticmethod
    def get_inventory() -> List[Dict]:
        """Get all products in inventory"""
        try:
            return get_all_products()
        except Exception as e:
            print(f"Error retrieving inventory: {e}")
            return []

    @staticmethod
    def update_product_details(
        product_id: int, 
        **updates: Dict[str, Union[str, int, float]]
    ) -> bool:
        """Update product details"""
        try:
            return update_product(product_id, **updates)
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    @staticmethod
    def remove_product(product_id: int) -> bool:
        """Remove a product from inventory"""
        try:
            return delete_product(product_id)
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    @staticmethod
    def search_inventory(search_term: str) -> List[Dict]:
        """Search for products in inventory"""
        try:
            return search_products(search_term)
        except Exception as e:
            print(f"Error searching inventory: {e}")
            return []

    @staticmethod
    def check_low_stock(threshold: Optional[int] = None) -> List[Dict]:
        """Get products with low stock"""
        try:
            return get_low_stock_products(threshold)
        except Exception as e:
            print(f"Error checking low stock: {e}")
            return []

    @staticmethod
    def adjust_stock(product_id: int, quantity_change: int) -> bool:
        """
        Adjust stock levels (positive for addition, negative for reduction)
        """
        try:
            products = get_all_products()
            product = next((p for p in products if p['id'] == product_id), None)
            
            if not product:
                return False
                
            new_quantity = product['quantity'] + quantity_change
            if new_quantity < 0:
                return False
                
            return update_product(product_id, quantity=new_quantity)
        except Exception as e:
            print(f"Error adjusting stock: {e}")
            return False
