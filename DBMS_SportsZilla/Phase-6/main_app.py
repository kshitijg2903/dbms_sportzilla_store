import streamlit as st
import mysql.connector
from datetime import date


class SportszillaManagementSystem:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor()

    def execute_transaction(self, operations):
        try:
            self.db.start_transaction()

            for operation in operations:
                operation()

            self.db.commit()
        except mysql.connector.Error as e:
            self.db.rollback()

    def customer_login(self, customer_name, customer_password):
        self.cursor.execute("SELECT customer_id FROM customer WHERE username=%s", (customer_name,))
        customer_id_temp = self.cursor.fetchone()
        customer_id = customer_id_temp[0]
        self.cursor.execute("SELECT password FROM customer WHERE username=%s", (customer_name,))
        result = self.cursor.fetchone()
        if result:
            password = result[0]
            if customer_password == password:
                return True
            else:
                return False
        else:
            return False

    def customer_analysis_sql_total_amount(self, customer_id):
        total_spent = 0
        self.cursor.execute("SELECT total_amount FROM orders WHERE customer_id=%s", (customer_id,))
        rows = self.cursor.fetchall()

        for row in rows:
            total_spent += int(row[0])
        return total_spent

    def customer_analysis_sql_last_date(self, customer_id):
        self.cursor.execute("SELECT MAX(order_date) FROM orders WHERE customer_id=%s", (customer_id,))
        row = self.cursor.fetchone()
        return str(row[0])

    def write_review_sql(self, message, rating, order_id):
        def operation():
            self.cursor.execute("SELECT MAX(review_id) FROM review")
            review_temp = self.cursor.fetchone()
            if review_temp != None:
                review_id = int(review_temp[0]) + 1
            else:
                review_id = 1

            self.cursor.execute("INSERT INTO review(review_ID,order_id,rating,comments) VALUES(%s,%s,%s,%s) ",
                                (review_id, order_id, rating, message))

        self.execute_transaction([operation])

    def update_quantity(self, product_id, quantity):
        def operation():
            self.cursor.execute("SELECT quantity FROM products WHERE product_id=%s", (product_id,))
            temp1 = self.cursor.fetchone()
            temp2 = int(temp1[0])
            self.cursor.execute("UPDATE products SET quantity=%s WHERE product_id=%s",
                                ((temp2 - int(quantity)), product_id))

        self.execute_transaction([operation])

    def create_an_order(self, customer_id, total_amount):
        def operation():
            self.cursor.execute("SELECT MAX(order_id) FROM orders")
            order_id_temp = self.cursor.fetchone()
            order_id = int(order_id_temp[0]) + 1
            date1 = date.today()

            self.cursor.execute("INSERT INTO orders(order_id,customer_id,order_date,total_amount) VALUES(%s,%s,%s,%s) ",
                                (order_id, customer_id, date1, total_amount))

        self.execute_transaction([operation])

    def place_order_sql(self, customer_id, product_id, quantity):
        self.update_quantity(product_id, quantity)
        self.cursor.execute("SELECT price FROM products WHERE product_id=%s", (product_id,))
        temp1 = self.cursor.fetchone()
        price_product = int(temp1[0])
        total_price = int(quantity) * int(price_product)
        self.create_an_order(customer_id, total_price)

    def view_order_history(self, customer_name):
        self.cursor.execute('SELECT customer_id FROM customer WHERE username=%s', (customer_name,))
        result = self.cursor.fetchone()
        result1 = result[0]
        self.cursor.execute("SELECT order_date,total_amount FROM orders WHERE customer_id=%s ", (result1,))
        order_history = self.cursor.fetchall()
        if order_history:
            order_history_message = "Order history for  " + customer_name + ":\n"
            for order in order_history:
                order_history_message += str(order) + "\n"
        else:
            order_history_message = "No order history found for" + customer_name

        return order_history_message

    def register_vendor(self, vendor_id, organisation_name, contact_person, phone_number, email):
        def operation():
            self.cursor.execute("INSERT INTO vendor(vendor_id,organisation_name,contact_person,phone_number,email) "
                                "VALUES(%s,%s,%s,%s,%s)",
                                (vendor_id, organisation_name, contact_person, phone_number, email, "YES"))

        self.execute_transaction([operation])

    def register_distributors(self, distributor_id, name):
        def operation():
            self.cursor.execute("INSERT INTO distributors(Distributor_ID,Name) VALUES(%s,%s)",
                                (distributor_id, name))

        self.execute_transaction([operation])

    def update_product_catalog(self, vendor_id, product_name, price, quantity):
        def operation():
            self.cursor.execute("SELECT MAX(product_id) FROM products ")
            product_temp = self.cursor.fetchone()
            product_id = int(product_temp[0]) + 1

            self.cursor.execute("INSERT INTO products(product_id,vendor_id,product_name,price,quantity) "
                                "VALUES(%s,%s,%s,%s,%s)",
                                (product_id, vendor_id, product_name, price, quantity))

        self.execute_transaction([operation])

    def remove_products(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        self.db.commit()

    def delete_customer_account(self, customer_id):
        self.cursor.execute("DELETE FROM customer WHERE customer_id=%s", (customer_id,))
        self.db.commit()

    def customer_registration(self, customer_name, customer_email, customer_address, customer_password):
        def operation():
            self.cursor.execute("SELECT MAX(customer_id) FROM customer")
            customer_id_temp = self.cursor.fetchone()
            customer_id = int(customer_id_temp[0]) + 1
            self.cursor.execute(
                "INSERT INTO customer(customer_id,username,password,address,email,user_type) "
                "VALUES(%s,%s,%s,%s,%s,%s) ",
                (customer_id, customer_name, customer_password, customer_address, customer_email, "customer"))

        self.execute_transaction([operation])


class AdminDashboard:
    def __init__(self, system):
        self.view_order_placeholder = st.empty()
        self.customer_analysis_placeholder = st.empty()
        self.remove_placeholder = st.empty()
        self.system = system

    def display(self):
        admin_options = st.sidebar.selectbox('Select Option',
                                             ['Customer Analysis', 'Register', 'Remove', 'Order History',
                                              'Update Catalog', 'Logout'])

        if admin_options == 'Customer Analysis':
            self.customer_analysis()
        elif admin_options == 'Register':
            self.register()
        elif admin_options == 'Remove':
            self.remove()
        elif admin_options == 'Order History':
            self.view_orders()
        elif admin_options == 'Update Catalog':
            self.update_catalog()

    def customer_analysis(self):
        with self.customer_analysis_placeholder.container():
            st.title('Customer Analysis')
            customer_id = st.text_input("Enter customer id")
            but1 = st.button('analyze customer last data')
            but2 = st.button('analyze customer total amount')
        if but1:
            analysis = self.system.customer_analysis_sql_total_amount(customer_id)
            st.write(f"Customer Analysis for id-{customer_id}: ", analysis)
            self.customer_analysis_placeholder.empty()
        elif but2:
            analysis = self.system.customer_analysis_sql_last_date(customer_id)
            st.write(f"Customer Analysis for id-{customer_id}: ", analysis)
            self.customer_analysis_placeholder.empty()

    def register(self):
        registration_option = st.radio('Select Registration Type', ['Vendor', 'Customer', 'Distributor'])

        if registration_option == 'Vendor':
            self.register_vendor()
        elif registration_option == 'Customer':
            self.register_customer()
        elif registration_option == 'Distributor':
            self.register_distributor()

    def register_vendor(self):
        st.title('Vendor Registration')
        vendor_id = st.text_input('Vendor ID')
        organisation_name = st.text_input('Organisation Name')
        contact_person = st.text_input('Contact Person')
        phone_number = st.text_input('Phone Number')
        email = st.text_input('Email')

        if st.button('Register Vendor'):
            self.system.register_vendor(vendor_id, organisation_name, contact_person, phone_number, email)
            st.success('Vendor Registered Successfully!')

    def register_customer(self):
        st.title('Customer Registration')
        customer_name = st.text_input('Customer Name')
        customer_email = st.text_input('Email')
        customer_address = st.text_input('Address')
        customer_password = st.text_input('Password', type='password')

        if st.button('Register Customer'):
            self.system.customer_registration(customer_name, customer_email, customer_address, customer_password)
            st.success('Customer Registered Successfully!')

    def register_distributor(self):
        st.title('Distributor Registration')
        distributor_id = st.text_input('Distributor ID')
        name = st.text_input('Name')

        if st.button('Register Distributor'):
            self.system.register_distributors(distributor_id, name)
            st.success('Distributor Registered Successfully!')

    def remove(self):
        removal_option = st.radio('Select Removal Type', ['Product', 'Customer'])

        if removal_option == 'Product':
            self.remove_product()
        elif removal_option == 'Customer':
            self.remove_customer()

    def remove_product(self):
        st.title('Remove Product')
        product_id = st.text_input('Product ID')

        if st.button('Remove Product'):
            self.system.remove_products(product_id)
            st.success('Product Removed Successfully!')

    def remove_customer(self):
        st.title('Remove Customer')
        customer_id = st.text_input('Customer ID')

        if st.button('Remove Customer'):
            self.system.delete_customer_account(customer_id)
            st.success('Customer Removed Successfully!')

    def view_orders(self):
        with self.view_order_placeholder.container():
            st.title('View Orders')
            customer_name = st.text_input('Customer Name')
        if st.button('View Orders'):
            self.view_order_placeholder.empty()
            try:
                order_history = self.system.view_order_history(customer_name)
                st.write(order_history)
            except:
                st.write("Error")

    def update_catalog(self):
        st.title('Update Catalog')
        vendor_id = st.text_input('Vendor ID')
        product_name = st.text_input('Product Name')
        price = st.number_input('Price', value=0.0)
        quantity = st.number_input('Quantity', value=0)

        if st.button('Update Catalog'):
            self.system.update_product_catalog(vendor_id, product_name, price, quantity)
            st.success('Catalog Updated Successfully!')


class CustomerDashboard:
    def __init__(self, system, userid=None, name=None):
        self.system = system
        self.userid = userid
        self.name = name
        self.view_order_placeholder = st.empty()
        self.place_order_placeholder = st.empty()

    def display(self):
        st.sidebar.title('Customer Dashboard')

        customer_options = st.sidebar.selectbox('Select Option',
                                                ['Select an option', 'View Orders', 'Write a review', 'Place Order',
                                                 'Logout'])

        if customer_options == 'Place Order':
            self.place_order()
        elif customer_options == 'Write a review':
            self.write_review()

    def place_order(self):
        st.title('Place Order')
        customer_id = self.name
        product_id = st.text_input('Product ID')
        quantity = st.number_input('Quantity', value=1)
        if st.button('Place Order'):
            self.system.place_order_sql(customer_id, product_id, quantity)
            st.success('Order Placed Successfully!')

    def write_review(self):
        st.title('Write a Review')
        order_id = st.text_input('Order ID')
        rating = st.number_input('Rating')
        message = st.text_area('Message')

        if st.button('Submit Review'):
            self.system.write_review_sql(message, rating, order_id)
            st.success('Review Submitted Successfully!')


# Initialize the SportszillaManagementSystem
# Assuming SportszillaManagementSystem is defined elsewhere
system = SportszillaManagementSystem(
    host='localhost',
    user='root',
    password='',
    database='sportszilla'
)

# Login Page


# Create session states for admin and customer logins
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False
if 'customer_logged_in' not in st.session_state:
    st.session_state['customer_logged_in'] = False

if not st.session_state['admin_logged_in'] and not st.session_state['customer_logged_in']:
    login_placeholder = st.empty()

    with login_placeholder.container():
        st.title('Sportszilla Management System')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        login_button = st.button('Login')

    if login_button:
        if username == 'admin' and password == 'admin':
            # Clear the login GUI
            login_placeholder.empty()
            st.success('Logged in as Admin')
            admin_dashboard = AdminDashboard(system)
            admin_dashboard.display()
            st.session_state['admin_logged_in'] = True
        elif system.customer_login(username, password):  # Assuming some validation for customer login
            # Clear the login GUI
            login_placeholder.empty()
            st.success('Logged in as Customer')
            customer_dashboard = CustomerDashboard(system, userid=username)
            # Removed automatic display of view orders
            customer_dashboard.display()
            st.session_state['customer_logged_in'] = True
else:
    # User is already logged in, display the dashboard directly
    if st.session_state['admin_logged_in']:
        admin_dashboard = AdminDashboard(system)
        admin_dashboard.display()
    elif st.session_state['customer_logged_in']:
        customer_dashboard = CustomerDashboard(system)
        customer_dashboard.display()
