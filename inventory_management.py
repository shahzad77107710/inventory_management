import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Initialize products in session state
if 'products' not in st.session_state:
    st.session_state.products = {
        "1": {"SNO": 1, "Product": "Smart Phone", "In Stock": 20, "Price": 200},
        "2": {"SNO": 2, "Product": "Head Phones", "In Stock": 100, "Price": 30},
        "3": {"SNO": 3, "Product": "Screen Guard", "In Stock": 200, "Price": 5},
        "4": {"SNO": 4, "Product": "Chargers", "In Stock": 100, "Price": 10},
        "5": {"SNO": 5, "Product": "Memory Cards", "In Stock": 120, "Price": 50}
    }

# PDF Generator Function using reportlab
def create_pdf(customer_name, product_name, price):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the PDF document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Python Mobile Shop")
    c.setFont("Helvetica", 12)
    c.drawCentredString(300, 730, "---------------------------------")
    
    # Add bill details
    c.drawString(100, 700, f"Bill No: 12345")
    c.drawString(100, 680, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 660, f"Customer Name: {customer_name}")
    c.drawCentredString(300, 640, "---------------------------------")
    c.drawString(100, 620, f"Product: {product_name}")
    c.drawString(100, 600, f"Amount: ${price}")
    c.drawCentredString(300, 580, "---------------------------------")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(300, 550, "Thank you for your purchase!")
    
    c.save()
    buffer.seek(0)
    return buffer

# Text Receipt Generator
def create_text_receipt(customer_name, product_name, price):
    receipt = f"""
    Python Mobile Shop
    ---------------------------------
    Bill No: 12345
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Customer Name: {customer_name}
    ---------------------------------
    Product: {product_name}
    Amount: ${price}
    ---------------------------------
    Thank you for your purchase!
    """
    return receipt

# Streamlit UI
st.title("📱 Python Mobile Shop")
st.markdown("*************************************")

option = st.sidebar.selectbox("Menu", ["Show All Products", "Buy Product", "Add Products", "Exit"])

if option == "Show All Products":
    st.subheader("📋 All Products")
    st.table([{
        "SNO": product["SNO"],
        "Product": product["Product"],
        "In Stock": product["In Stock"],
        "Price": f"${product['Price']}"
    } for product in st.session_state.products.values()])

elif option == "Buy Product":
    st.subheader("🛒 Buy Product")
    st.table([{
        "ID": pid,
        "Product": details["Product"],
        "In Stock": details["In Stock"],
        "Price": f"${details['Price']}"
    } for pid, details in st.session_state.products.items()])
    
    product_id = st.text_input("Enter Product ID to buy:")
    customer_name = st.text_input("Enter Your Name:")
    
    if st.button("Purchase"):
        if product_id in st.session_state.products:
            product = st.session_state.products[product_id]
            st.success(f"Order Summary:\nProduct: {product['Product']}\nPrice: ${product['Price']}")
            
            # Generate PDF
            pdf_buffer = create_pdf(customer_name, product['Product'], product['Price'])
            st.download_button(
                label="Download Bill as PDF",
                data=pdf_buffer,
                file_name=f"mobile_shop_bill_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            
            # Generate Text Receipt
            text_receipt = create_text_receipt(customer_name, product['Product'], product['Price'])
            st.download_button(
                label="Download Text Receipt",
                data=text_receipt,
                file_name=f"mobile_shop_receipt_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.error("Product not found")

elif option == "Add Products":
    st.subheader("➕ Add New Product (Admin Only)")
    admin = st.text_input("Admin Username:")
    password = st.text_input("Password:", type="password")
    
    if st.button("Authenticate"):
        if admin == 'admin' and password == 'pass':
            st.success("Admin authenticated")
            
            with st.form("product_form"):
                product_id = st.text_input("Product ID:")
                product_name = st.text_input("Product Name:")
                quantity = st.number_input("Quantity:", min_value=1)
                price = st.number_input("Price:", min_value=1)
                
                if st.form_submit_button("Add Product"):
                    st.session_state.products[product_id] = {
                        "SNO": len(st.session_state.products) + 1,
                        "Product": product_name,
                        "In Stock": quantity,
                        "Price": price
                    }
                    st.success("Product added successfully!")
                    st.write(st.session_state.products[product_id])
        else:
            st.error("Invalid credentials")

elif option == "Exit":
    st.success("Thank you for visiting Python Mobile Shop!")
    st.stop()