import sqlite3
from datetime import datetime, timedelta

# Connect to (or create) the database
conn = sqlite3.connect("data/loyalty.db")
cursor = conn.cursor()

# Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    points INTEGER DEFAULT 0,
    valid_until DATE NOT NULL
)
""")

# Function to add a new customer
def add_customer(name, email, phone):
    valid_until = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')  # 1-year validity
    try:
        cursor.execute("INSERT INTO customers (name, email, phone, valid_until) VALUES (?, ?, ?, ?)", 
                       (name, email, phone, valid_until))
        conn.commit()
        return f"Customer '{name}' added successfully!"
    except sqlite3.IntegrityError:
        return "Error: Email or phone number already exists."

# Function to fetch all customers
def get_customers():
    cursor.execute("SELECT * FROM customers")
    return cursor.fetchall()

# Function to update loyalty points
def update_points(customer_id, points):
    cursor.execute("UPDATE customers SET points = points + ? WHERE id = ?", (points, customer_id))
    conn.commit()
    return f"Added {points} points to Customer ID {customer_id}"

# Function to redeem points
def redeem_points(customer_id):
    cursor.execute("UPDATE customers SET points = 0 WHERE id = ?", (customer_id,))
    conn.commit()
    return f"Customer ID {customer_id} redeemed all points."

# Close connection
conn.close()
