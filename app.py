import streamlit as st
import sqlite3
from database_setup import add_customer, get_customers, update_points, redeem_points

# Connect to database
conn = sqlite3.connect("data/loyalty.db", check_same_thread=False)
cursor = conn.cursor()

st.title("Customer Loyalty Program 🎉")

# Customer Registration
with st.form("register_form"):
    name = st.text_input("Customer Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    submit = st.form_submit_button("Register Customer")
    
    if submit and name and email and phone:
        result = add_customer(name, email, phone)
        st.success(result)

# Display Customers
st.subheader("Registered Customers")
customers = get_customers()
for c in customers:
    st.write(f"ID: {c[0]}, Name: {c[1]}, Email: {c[2]}, Phone: {c[3]}, Points: {c[4]}, Valid Until: {c[5]}")

# Add Points
st.subheader("Manage Points")
customer_id = st.number_input("Customer ID", min_value=1, step=1)
points = st.number_input("Points to Add", min_value=1, step=1)
if st.button("Add Points"):
    result = update_points(customer_id, points)
    st.success(result)

# Redeem Points
if st.button("Redeem Points"):
    result = redeem_points(customer_id)
    st.success(result)

# Close connection
conn.close()
