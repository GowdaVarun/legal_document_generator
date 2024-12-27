import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
import base64
from reportlab.pdfgen import canvas

# Function to generate Sale Deed content using reportlab and PyPDF2
def generate_sale_deed(seller_name, buyer_name, property_address, state, sale_price, contract_duration, deed_date, deed_time):
    # Temporary buffer to store content
    pdf_output = BytesIO()

    # Write the content to the PDF
    c = canvas.Canvas(pdf_output)
    c.setFont("Helvetica", 12)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "SALE DEED")
    
    # Subtitle
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, f"THIS DEED OF SALE is made on the {deed_date} at {deed_time}.")
    
    # Parties (handling multiple lines)
    y_position = 730
    c.drawString(30, y_position, f"BETWEEN")
    y_position -= 15
    c.drawString(30, y_position, f"{seller_name}, hereinafter called the 'SELLER',")
    y_position -= 15
    c.drawString(30, y_position, f"AND")
    y_position -= 15
    c.drawString(30, y_position, f"{buyer_name}, hereinafter called the 'BUYER'.")
    
    # Property Details
    y_position -= 25
    c.drawString(30, y_position, f"WHEREAS the Seller is the absolute owner of the property located at {property_address}, {state}.")
    
    # Consideration Clause
    y_position -= 25
    c.drawString(30, y_position, f"NOW THIS DEED WITNESSES that in consideration of the sum of {sale_price} paid by the Buyer to the Seller,")
    y_position -= 15
    c.drawString(30, y_position, f"the receipt whereof the Seller hereby acknowledges, the Seller hereby transfers all rights, title,")
    y_position -= 15
    c.drawString(30, y_position, f"and interest in the said property to the Buyer.")
    
    # Duration
    y_position -= 25
    c.drawString(30, y_position, f"Duration of Agreement: {contract_duration}")
    
    # Signatures
    y_position -= 35
    c.drawString(30, y_position, "_________________")
    y_position -= 15
    c.drawString(30, y_position, "Seller's Signature")
    y_position -= 25
    c.drawString(30, y_position, "_________________")
    y_position -= 15
    c.drawString(30, y_position, "Buyer's Signature")
    
    # Save the PDF content
    c.save()
    
    # Move the buffer pointer to the beginning
    pdf_output.seek(0)

    # Read the content with PyPDF2 to handle it
    reader = PdfReader(pdf_output)
    writer = PdfWriter()

    # Add the first page to the PdfWriter object
    writer.add_page(reader.pages[0])

    # Create a new buffer for the output
    final_pdf_output = BytesIO()
    writer.write(final_pdf_output)

    # Return the final PDF
    final_pdf_output.seek(0)
    return final_pdf_output

# Function to generate download link for PDF
def get_pdf_download_link(pdf_output, filename="Sale_Deed.pdf"):
    # Encode as base64 for preview
    b64_pdf = base64.b64encode(pdf_output.read()).decode("utf-8")
    href = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="700" height="500" style="border:none;"></iframe>'
    return href

# Streamlit App
def main():
    st.title("Sale Deed Generator")

    # Input fields for Sale Deed
    seller_name = st.text_input("Seller's Name")
    buyer_name = st.text_input("Buyer’s Name")
    property_address = st.text_area("Property Address")
    state = st.text_input("State")
    sale_price = st.text_input("Sale Price")
    contract_duration = st.text_input("Contract Duration")
    deed_date = st.date_input("Date of Deed").strftime("%d-%m-%Y")
    deed_time = st.time_input("Time of Deed").strftime("%H:%M:%S")

    if st.button("Generate and Preview Sale Deed"):
        if all([seller_name, buyer_name, property_address, state, sale_price, contract_duration]):
            # Generate the PDF
            pdf_output = generate_sale_deed(
                seller_name, buyer_name, property_address, state,
                sale_price, contract_duration, deed_date, deed_time
            )

            # Display the PDF preview
            st.markdown("### Sale Deed Preview")
            st.markdown(get_pdf_download_link(pdf_output), unsafe_allow_html=True)

            # Add a download button
            st.download_button(
                label="Download Sale Deed PDF",
                data=pdf_output,
                file_name="Sale_Deed.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please fill out all fields to generate the Sale Deed.")

if __name__ == "__main__":
    main()
