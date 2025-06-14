🛒 Sportzilla Online Retail Store
A database-backed retail management system built as part of a DBMS course project. Sportzilla simulates a real-world sports merchandise store with inventory management, customer interactions, and transaction handling.

📦 Features
🗃️ Relational schema with SQL-based product, customer, and order management
🛍️ GUI-based interface using Tkinter for customer and admin operations
🔄 Multi-phase implementation with emphasis on data integrity, normalization, and query optimization
🔐 Support for conflicting transaction detection and resolution
💾 Built-in save/load and update capabilities via SQL scripts and Python wrappers
🛠️ Tech Stack
Backend: SQLite / PostgreSQL (via SQL scripts)
Frontend: Tkinter (Python GUI)
Languages: Python, SQL
Tools: SQL DDL/DML, Procedural Scripts, ER Modeling
🗂️ Project Structure
DBMS_SportsZilla/ ├── Schema/ │ ├── create.sql │ ├── query/ ├── Phase-3/ ├── Phase-5/ │ ├── Sportzilla_pkg.py │ └── GUI using tkinter/ ├── Phase-6/ │ ├── main_app.py │ ├── conflicting transactions/ │ ├── setup.md ├── README.md

⚙️ How to Run
Setup database schema:
sqlite3 sportzilla.db < Schema/create.sql
Run the GUI app (Phase 6):

python Phase-6/main_app.py Explore transaction logic and conflict handling: See conflicting transactions/ and Phase 6 for test cases.

📚 Concepts Demonstrated Relational DB design & ER modeling

DDL, DML operations (create, insert, update, delete)

Transactions and ACID compliance

GUI integration with backend logic

Multi-user operation and conflict resolution

👨‍💻 Contributors Kshitij Gupta

Aakarsh

Pratham

📄 License Academic Project — IIIT-Delhi, DBMS Course
