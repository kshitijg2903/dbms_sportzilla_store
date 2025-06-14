# 🛒 Sportzilla Online Retail Store

A database-backed retail management system built as part of a DBMS course project. Sportzilla simulates a real-world sports merchandise store with features like inventory control, customer interaction, order processing, and transaction handling.

---

## 📦 Features

- 🗃️ Relational schema with SQL-based product, customer, and order management  
- 🛍️ GUI interface using **Tkinter** for customer and admin operations  
- 🔄 Multi-phase implementation emphasizing normalization and query optimization  
- 🔐 Support for **conflicting transaction detection and resolution**  
- 💾 Built-in save/load capabilities using **SQL scripts and Python wrappers**

---

## 🛠️ Tech Stack

- **Backend:** SQLite / PostgreSQL (via raw SQL scripts)  
- **Frontend:** Tkinter (Python GUI)  
- **Languages:** Python, SQL  
- **Tools:** SQL DDL/DML, ER Modeling, Procedural Scripting

---

## 🗂️ Project Structure

DBMS_SportsZilla/
├── Schema/
│   ├── create.sql
│   └── query/
├── Phase-3/
├── Phase-5/
│   ├── Sportzilla_pkg.py
│   └── GUI using tkinter/
├── Phase-6/
│   ├── main_app.py
│   ├── conflicting transactions/
│   └── setup.md
├── README.md
⚙️ How to Run
Set up the database schema:

sqlite3 sportzilla.db < Schema/create.sql
Run the GUI application:


python Phase-6/main_app.py
Test transaction conflicts:

Check Phase-6/conflicting transactions/ for test cases and handling logic.

📚 Concepts Demonstrated
ER Modeling & Relational Database Design

DDL & DML operations: CREATE, INSERT, UPDATE, DELETE

Transaction management & ACID compliance

GUI ↔ DB integration

Multi-user concurrency & conflict resolution

👨‍💻 Contributors
Kshitij Gupta

Aakarsh

Pratham

📄 License
This is an academic project submitted to IIIT-Delhi as part of the DBMS course curriculum.
