import google.generativeai as genai
from datetime import datetime
import random

# Initialize the Gemini API client
genai.configure(api_key="AIzaSyADAMRi3OSq5CkfT1uESjk4EKbU47ybBTE")

# Dummy data for orders, appointments, and products
appointments = []
orders = []
products = {"Laptop": 1200, "Headphones": 150, "Smartphone": 900}

def get_gemini_response(prompt):
    # Generate a response using the Gemini model
    response = genai.generate_text(
        response = genai.generate_text(
    model="gemini-1.5-flash",
    prompt="Your prompt here"
)
    )
    return response.generations[0].text.strip()

def schedule_appointment():
    name = input("Enter your name: ")
    date = input("Enter the appointment date (YYYY-MM-DD): ")
    time = input("Enter the appointment time (HH:MM): ")
    appointment = {
        "name": name,
        "datetime": datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    }
    appointments.append(appointment)
    print("Appointment scheduled successfully!")

def place_order():
    print("Available products:")
    for product, price in products.items():
        print(f"- {product}: ${price}")
    
    product_name = input("Enter the product name you want to order: ")
    if product_name in products:
        order_id = random.randint(1000, 9999)
        orders.append({"id": order_id, "product": product_name, "status": "Processing"})
        print(f"Order placed successfully! Your order ID is {order_id}.")
    else:
        print("Sorry, that product is not available.")

def generate_invoice(order_id):
    for order in orders:
        if order['id'] == order_id:
            product = order['product']
            price = products[product]
            print(f"--- Invoice ---\nOrder ID: {order_id}\nProduct: {product}\nPrice: ${price}\nStatus: {order['status']}")
            return
    print("Order ID not found.")

def main():
    print("Welcome to the AI-Powered Business Center!")
    
    while True:
        print("\nSelect a service:")
        print("1. Customer Support")
        print("2. Schedule Appointment")
        print("3. Place Order")
        print("4. Generate Invoice")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            user_query = input("You: ")
            gemini_response = get_gemini_response(user_query)
            print(f"AI: {gemini_response}")
        elif choice == '2':
            schedule_appointment()
        elif choice == '3':
            place_order()
        elif choice == '4':
            order_id = int(input("Enter your order ID: "))
            generate_invoice(order_id)
        elif choice == '5':
            print("Thank you for using the AI-Powered Business Center. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

