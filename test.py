import streamlit as st
import requests
from chat import  customer_support
import random

# Streamlit page configuration
st.set_page_config(page_title="Product Page", page_icon="🛒", layout="wide")

# Initialize session state
if 'action' not in st.session_state:
    st.session_state.action = None
if 'selected_products' not in st.session_state:
    st.session_state.selected_products = []

# Function to display customer support form
# def customer_support():
    # st.subheader("Customer Support")
    # st.write("If you need help, please contact us at support@example.com.")
    # st.text_area("Describe your issue or inquiry:")

# Function to schedule an appointment
def schedule_appointment():
    st.subheader("Schedule Appointment")
    st.write("Please select a date and time for your appointment.")
    date = st.date_input("Date")
    time = st.time_input("Time")
    if st.button("Submit"):
        st.write(f"Appointment scheduled for {date} at {time}.")

# Function to place an order
def place_order():
    response = requests.get("https://fakestoreapi.com/products")
    products = response.json()

    st.subheader("Place Order")
    
    # Show product options for order
    for i, product in enumerate(products):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image(product["image"], width=80)  # Small image
        with col2:
            if st.checkbox(f"Select {product['title']}", key=f"product_{i}"):
                if product not in st.session_state.selected_products:
                    st.session_state.selected_products.append(product)
        with col3:
            st.write(f"${product['price']}")
    
    if st.session_state.selected_products:
        st.write("Selected Products:")
        for product in st.session_state.selected_products:
            st.image(product["image"], width=100)  # Small image
            st.write(f"{product['title']} - ₦{product['price']}")
        
        if st.button("Proceed with Purchase"):
            st.session_state.action = "collect_address"
            st.experimental_rerun()  # Rerun the script to transition to the next step

# Function to collect delivery address and confirm order
def collect_address():
    st.subheader("Delivery Address")
    address = st.text_input("Enter your delivery address")
    number = st.text_input("Enter your phone number")
    
    if st.button("Proceed with Purchase"):
        if address:
            order_id = random.randint(1000, 9999)  # Simulating order ID
            st.write(f"Order purchased successfully! Your order ID is {order_id}.")
            st.session_state.selected_products = []
            st.session_state.action = None
        else:
            st.warning("Please enter a delivery address.")

# Function to generate an invoice
def generate_invoice():
    st.subheader("Generate Invoice")
    st.write("Invoice generation is not yet implemented.")

# Main content based on sidebar selection
sidebar_option = st.sidebar.radio(
    "Choose an option",
    ["Customer Support", "Schedule Appointment", "Place Order"]
    # ["Customer Support", "Schedule Appointment", "Place Order", "Generate Invoice"]
)

if sidebar_option == "Customer Support":
    customer_support()
    # print("")
elif sidebar_option == "Schedule Appointment":
    schedule_appointment()
elif sidebar_option == "Place Order":
    if st.session_state.action == 'collect_address':
        collect_address()
    else:
        place_order()
# elif sidebar_option == "Generate Invoice":
#     generate_invoice()
