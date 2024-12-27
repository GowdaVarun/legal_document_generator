import streamlit as st
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

# Function to generate the final Sale Deed PDF based on reference template
def generate_document_from_template(input_data, document_type):
    # Path to reference directory
    reference_dir = 'reference'  # Specify your directory path here
    template_txt_path = os.path.join(reference_dir, f"{document_type}.txt")

    # Read the reference template text file
    try:
        with open(template_txt_path, 'r') as file:
            template_text = file.read()
    except Exception as e:
        st.error(f"Error reading template: {e}")
        return None

    # Replace placeholders in the template text with actual input data
    for placeholder, value in input_data.items():
        template_text = template_text.replace(f"{{{placeholder}}}", value)

    # Create PDF from the modified text
    pdf_output = BytesIO()
    c = canvas.Canvas(pdf_output, pagesize=letter)

    # Configure text starting position
    width, height = letter
    margin = 40
    line_height = 14
    x_pos = margin
    y_pos = height - margin

    # Write text with line wrapping and pagination
    lines = template_text.split('\n')
    for line in lines:
        wrapped_lines = utils.simpleSplit(line, "Helvetica", 12, width - 2 * margin)
        for wrapped_line in wrapped_lines:
            if y_pos <= margin:  # Check if the text exceeds the page
                c.showPage()
                y_pos = height - margin
                c.setFont("Helvetica", 12)
            c.drawString(x_pos, y_pos, wrapped_line)
            y_pos -= line_height

    # Finalize the PDF
    c.save()

    pdf_output.seek(0)
    return pdf_output

# Function to generate download link for PDF
def get_pdf_download_link(pdf_output, filename="Generated_Document.pdf"):
    b64_pdf = base64.b64encode(pdf_output.read()).decode("utf-8")
    href = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="700" height="500" style="border:none;"></iframe>'
    return href

# Streamlit App for input and PDF generation
def main():
    st.title("Legal Document Generator")

    # Select document type
    document_type = st.selectbox("Select Document Type", ["Sale Deed", "Will", "Power of Attorney"])

    # Input fields for Sale Deed
    input_data = {}
    if document_type == "Sale Deed":
        # Basic date and identification
        input_data["day"] = st.text_input("Day of Execution")
        input_data["month"] = st.text_input("Month of Execution")
        input_data["year"] = st.text_input("Year of Execution")
        
        # Seller details
        st.subheader("Seller Details")
        input_data["seller_name"] = st.text_input("Seller's Name")
        input_data["seller_parent_name"] = st.text_input("Seller's Father/Spouse Name")
        input_data["seller_occupation"] = st.text_input("Seller's Occupation")
        input_data["seller_age"] = st.text_input("Seller's Age")
        input_data["seller_address_line1"] = st.text_input("Seller's Address Line 1")
        input_data["seller_address_line2"] = st.text_input("Seller's Address Line 2")

        # Purchaser details
        st.subheader("Purchaser Details")
        input_data["purchaser_name"] = st.text_input("Purchaser's Name")
        input_data["purchaser_parent_name"] = st.text_input("Purchaser's Father/Spouse Name")
        input_data["purchaser_occupation"] = st.text_input("Purchaser's Occupation")
        input_data["purchaser_age"] = st.text_input("Purchaser's Age")
        input_data["purchaser_address_line1"] = st.text_input("Purchaser's Address Line 1")
        input_data["purchaser_address_line2"] = st.text_input("Purchaser's Address Line 2")

        # Property details
        st.subheader("Property Details")
        input_data["property_number"] = st.text_input("Property Number")
        input_data["property_name"] = st.text_input("Property Name")
        input_data["property_location"] = st.text_input("Property Location")
        input_data["ownership_type"] = st.text_input("Type of Ownership")
        input_data["sale_reason"] = st.selectbox("Reason for Sale", 
            ["To clear of the debt", "For higher education of children", 
             "To defray medical expenses", "Domestic necessities"])

        # Payment details
        st.subheader("Payment Details")
        input_data["total_amount"] = st.text_input("Total Sale Amount (in Rs.)")
        input_data["total_amount_words"] = st.text_input("Total Amount in Words")
        input_data["cheque_number"] = st.text_input("Cheque Number")
        input_data["payment_date"] = st.text_input("Payment Date")
        input_data["amount_paid"] = st.text_input("Amount Paid")
        input_data["remaining_amount"] = st.text_input("Remaining Amount")

        # Schedule property details
        st.subheader("Schedule Property Details")
        input_data["schedule_property_number"] = st.text_input("Schedule Property Number")
        input_data["property_measurement"] = st.text_input("Property Measurement")
        input_data["east_boundary"] = st.text_input("Eastern Boundary")
        input_data["west_boundary"] = st.text_input("Western Boundary")
        input_data["south_boundary"] = st.text_input("Southern Boundary")
        input_data["north_boundary"] = st.text_input("Northern Boundary")
        input_data["market_value"] = st.text_input("Market Value of Property")
        input_data["market_value_words"] = st.text_input("Market Value in Words")

        # Witness and execution details
        st.subheader("Witness Details")
        input_data["deed_place"] = st.text_input("Place of Execution")
        input_data["deed_day"] = st.text_input("Day of Signing")
        input_data["deed_month"] = st.text_input("Month of Signing")
        input_data["witness1_name"] = st.text_input("Witness 1 Name")
        input_data["witness2_name"] = st.text_input("Witness 2 Name")

        # Registration details
        st.subheader("Registration Details (if applicable)")
        input_data["previous_owner"] = st.text_input("Previous Owner's Name")
        input_data["document_number"] = st.text_input("Document Number")
        input_data["book_number"] = st.text_input("Book Number")
        input_data["volume_number"] = st.text_input("Volume Number")
        input_data["page_number"] = st.text_input("Page Number")


    elif document_type == "Will":
        input_data["TESTATOR_NAME"] = st.text_input("Testator's Name")
        input_data["BENEFICIARY_NAME"] = st.text_input("Beneficiary's Name")
        input_data["ASSETS"] = st.text_area("Assets Details")
        input_data["EXECUTION_DATE"] = st.date_input("Date of Will").strftime("%d-%m-%Y")

    elif document_type == "Power of Attorney":
        input_data["PRINCIPAL_NAME"] = st.text_input("Principal's Name")
        input_data["ATTORNEY_NAME"] = st.text_input("Attorney's Name")
        input_data["AUTHORITY"] = st.text_area("Powers Given")
        input_data["EXECUTION_DATE"] = st.date_input("Date of Execution").strftime("%d-%m-%Y")

    if st.button("Generate and Preview Document"):
        if all(input_data.values()):
            # Generate the PDF document from template
            pdf_output = generate_document_from_template(input_data, document_type)

            if pdf_output:
                # Display the PDF preview
                st.markdown("### Document Preview")
                st.markdown(get_pdf_download_link(pdf_output), unsafe_allow_html=True)

                # Add a download button
                st.download_button(
                    label="Download Document PDF",
                    data=pdf_output,
                    file_name=f"{document_type}.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Please fill out all fields to generate the document.")

if __name__ == "__main__":
    main()
