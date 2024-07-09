import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, params=(), fetchone=False, commit=False):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                if fetchone:
                    return cursor.fetchone()
                return cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")

class OrderManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def place_order(self, customer_id, product_id, order_date, total_amount):
        # Inserting a new order
        order_id = self.db_manager.execute_query(
            "INSERT INTO Orders (customer_id, order_date, total_amount) VALUES (?, ?, ?)",
            (customer_id, order_date, total_amount),
            commit=True
        )
        # Updating product quantity
        self.db_manager.execute_query(
            "UPDATE products SET quantity = quantity - 1 WHERE product_id = ?",
            (product_id,),
            commit=True
        )
        print(f"Order placed successfully. Order ID: {order_id}")

    def customer_analysis(self, customer_id):
        total_spent = self.db_manager.execute_query(
            "SELECT SUM(total_amount) FROM Orders WHERE customer_id = ?",
            (customer_id,),
            fetchone=True
        )[0]
        print(f"Total amount spent by Customer {customer_id}: ${total_spent}")


# Example usage
db_manager = DatabaseManager('sportszilla.db')
order_manager = OrderManager(db_manager)

# Place an order
order_manager.place_order(1, 1, '2024-03-24', 150.00)

# Perform customer analysis
order_manager.customer_analysis(1)
