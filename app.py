import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect("loyalty.db", check_same_thread=False)
cursor = conn.cursor()

# Title
st.title("Customer Loyalty Program")

# Customer Registration
with st.form("register_form"):
    name = st.text_input("Customer Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    submit = st.form_submit_button("Register Customer")
    
    if submit and name and email and phone:
        valid_until = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')  # 1-year validity
        cursor.execute("INSERT INTO customers (name, email, phone, valid_until) VALUES (?, ?, ?, ?)", 
                       (name, email, phone, valid_until))
        conn.commit()
        st.success(f"Customer {name} registered successfully!")

# View Customers
st.subheader("Customers List")
cursor.execute("SELECT id, name, email, phone, points, valid_until FROM customers")
customers = cursor.fetchall()
for c in customers:
    st.write(f"ID: {c[0]}, Name: {c[1]}, Email: {c[2]}, Phone: {c[3]}, Points: {c[4]}, Valid Until: {c[5]}")

# Add Points
st.subheader("Manage Points")
customer_id = st.number_input("Customer ID", min_value=1, step=1)
points = st.number_input("Points to Add", min_value=1, step=1)
if st.button("Add Points"):
    cursor.execute("UPDATE customers SET points = points + ? WHERE id = ?", (points, customer_id))
    conn.commit()
    st.success("Points added successfully!")

# Redeem Points
if st.button("Redeem Points"):
    cursor.execute("UPDATE customers SET points = 0 WHERE id = ?", (customer_id,))
    conn.commit()
    st.success("Points redeemed!")

# Close connection
conn.close()
