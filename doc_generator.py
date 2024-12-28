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
    # Create a BytesIO buffer to store PDF data
    pdf_output = BytesIO()
    
    # Define PDF document layout
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter
    margin = 40
    line_height = 14
    x_pos = margin
    y_pos = height - margin
    
    # Set the font for the document
    c.setFont("Helvetica", 12)

    # Read the reference template text file for the document
    reference_dir = 'reference'  # Directory where your template text files are stored
    template_txt_path = os.path.join(reference_dir, f"{document_type}.txt")
    
    try:
        with open(template_txt_path, 'r') as file:
            template_text = file.read()
    except Exception as e:
        st.error(f"Error reading template: {e}")
        return None

    # Replace placeholders in the template with actual input data
    for placeholder, value in input_data.items():
        template_text = template_text.replace(f"{{{placeholder}}}", value)
    
    # Split the template text into lines and handle text wrapping
    lines = template_text.split('\n')
    for line in lines:
        # Wrap text to ensure it doesn't overflow the page
        wrapped_lines = wrap_text(c, line, width - 2 * margin)  # Wrap within page width
        for wrapped_line in wrapped_lines:
            # Check if text exceeds the page and if so, add a new page
            if y_pos <= margin:
                c.showPage()
                y_pos = height - margin
                c.setFont("Helvetica", 12)
            
            c.drawString(x_pos, y_pos, wrapped_line)
            y_pos -= line_height  # Move down for the next line

    # Finalize the PDF
    c.save()

    # Move the buffer pointer to the start
    pdf_output.seek(0)
    
    return pdf_output

# Function to wrap text within a given width (to prevent overflow)
def wrap_text(c, text, max_width):
    # Break text into lines that fit within the max_width
    from reportlab.lib.pagesizes import letter
    width, height = letter
    lines = []
    line = ''
    
    # Split the text into words
    for word in text.split(' '):
        test_line = line + word + ' '
        if c.stringWidth(test_line, "Helvetica", 12) < max_width:
            line = test_line
        else:
            if line:
                lines.append(line)
            line = word + ' '
    
    if line:
        lines.append(line)  # Add the last line
    
    return lines

# Function to generate a download link for the PDF
def get_pdf_download_link(pdf_output, filename="Generated_Document.pdf"):
    b64_pdf = base64.b64encode(pdf_output.read()).decode("utf-8")
    href = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="700" height="500" style="border:none;"></iframe>'
    return href

def add_custom_css():
    st.markdown("""
        <style>

            /* Main container and background */
            .stApp {
                background: linear-gradient(180deg, #EEF2FF 0%, #FFFFFF 100%);
            }

            /* Make text inputs visible with proper contrast */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div,
            .stTextArea > div > div > textarea {
                color: #111827 !important;
                background-color: white !important;
                border: 1px solid #d1d5db !important;
                border-radius: 8px !important;
                font-size: 1rem !important;
                line-height: 1.5 !important;
            }

            /* Input focus states */
            .stTextInput > div > div > input:focus,
            .stSelectbox > div > div > div:focus,
            .stTextArea > div > div > textarea:focus {
                border-color: #2563EB !important ;
                box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
            }

            /* Labels */
            .stTextInput > label,
            .stSelectbox > label,
            .stTextArea > label {
                color: #374151 !important;
                font-size: 1rem !important;
                font-weight: 500 !important;
                margin-bottom: 0.5rem !important;
            }

            /* Header styling */
            .header {
                background-color: #2563EB;
                color: white;
                padding: 2rem;
                border-radius: 0 0 1rem 1rem;
                margin-bottom: 2rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(37, 99, 235, 0.1);
            }

            .header h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: bold;
            }

            /* Subheaders */
            .stMarkdown h3 {
                color: #000000 !important;
                font-size: 1.5rem;
                font-weight: 600;
                margin-top: 2rem;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #E5E7EB;
            }

            /* Button styling */
            .stButton > button ,
            st.download_button {
                background-color: #2563EB !important;
                color: white !important;
                border: none !important;
                padding: 0.75rem 2rem !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
                width: auto !important;
            }

            .stButton > button:hover {
                background-color: #1D4ED8 !important;
                box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
            }

            /* Container styling */
            .content-container {
                background-color: white;
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 2rem auto;
            }

            /* Error messages */
            .stAlert {
                background-color: #FEE2E2 !important;
                color: #991B1B !important;
                padding: 1rem !important;
                border-radius: 8px !important;
                border: 1px solid #FCA5A5 !important;
            }

            /* Footer styling */
            # .footer {
            #     background-color: #2563EB;
            #     color: white;
            #     padding: 1rem;
            #     text-align: center;
            #     position: fixed;
            #     bottom: 0;
            #     width: 100%;
            #     left: 0;
            #     font-size: 0.875rem;
            # }

            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            /* Spacing for footer */
            .main-content {
                margin-bottom: 5rem;
            }

            /* Date input styling */
            .stDateInput > div > div > input {
                color: #111827 !important;
                background-color: white !important;
                border: 1px solid #d1d5db !important;
                padding: 0.75rem !important;
                border-radius: 8px !important;
                font-size: 1rem !important;
            }

            /* PDF preview container */
            .pdf-preview {
                margin-top: 2rem;
                padding: 1rem;
                border-radius: 8px;
                background-color: #F9FAFB;
            }

            /* Selectbox styling */
            .stSelectbox > div > div > div {
                background-color: white !important;
            }

            # /* Make sure text is visible in all inputs */
            # input, select, textarea {
            #     color: #111827 !important;
            # }
        </style>
        
        
    """, unsafe_allow_html=True)

# Streamlit App for input and PDF generation
def main():
    add_custom_css()

    st.markdown('<div class="header"><h1>Legal Document Generator</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    #st.title("Legal Document Generator")

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
        #st.subheader("Seller Details")
        input_data["seller_name"] = st.text_input("Seller's Name")
        input_data["seller_parent_name"] = st.text_input("Seller's Father/Spouse Name")
        input_data["seller_occupation"] = st.text_input("Seller's Occupation")
        input_data["seller_age"] = st.text_input("Seller's Age")
        input_data["seller_address_line1"] = st.text_input("Seller's Address Line 1")
        input_data["seller_address_line2"] = st.text_input("Seller's Address Line 2")

        # Purchaser details
        #st.subheader("Purchaser Details")
        input_data["purchaser_name"] = st.text_input("Purchaser's Name")
        input_data["purchaser_parent_name"] = st.text_input("Purchaser's Father/Spouse Name")
        input_data["purchaser_occupation"] = st.text_input("Purchaser's Occupation")
        input_data["purchaser_age"] = st.text_input("Purchaser's Age")
        input_data["purchaser_address_line1"] = st.text_input("Purchaser's Address Line 1")
        input_data["purchaser_address_line2"] = st.text_input("Purchaser's Address Line 2")

        # Property details
        #st.subheader("Property Details")
        input_data["property_number"] = st.text_input("Property Number")
        input_data["property_name"] = st.text_input("Property Name")
        input_data["property_location"] = st.text_input("Property Location")
        input_data["ownership_type"] = st.text_input("Type of Ownership")
        input_data["sale_reason"] = st.selectbox("Reason for Sale", 
            ["To clear of the debt", "For higher education of children", 
             "To defray medical expenses", "Domestic necessities"])

        # Payment details
        #st.subheader("Payment Details")
        input_data["total_amount"] = st.text_input("Total Sale Amount (in Rs.)")
        input_data["total_amount_words"] = st.text_input("Total Amount in Words")
        input_data["cheque_number"] = st.text_input("Cheque Number")
        input_data["payment_date"] = st.text_input("Payment Date")
        input_data["amount_paid"] = st.text_input("Amount Paid")
        input_data["remaining_amount"] = st.text_input("Remaining Amount")

        # Schedule property details
        #st.subheader("Schedule Property Details")
        input_data["schedule_property_number"] = st.text_input("Schedule Property Number")
        input_data["property_measurement"] = st.text_input("Property Measurement")
        input_data["east_boundary"] = st.text_input("Eastern Boundary")
        input_data["west_boundary"] = st.text_input("Western Boundary")
        input_data["south_boundary"] = st.text_input("Southern Boundary")
        input_data["north_boundary"] = st.text_input("Northern Boundary")
        input_data["market_value"] = st.text_input("Market Value of Property")
        input_data["market_value_words"] = st.text_input("Market Value in Words")

        # Witness and execution details
        #st.subheader("Witness Details")
        input_data["deed_place"] = st.text_input("Place of Execution")
        input_data["deed_day"] = st.text_input("Day of Signing")
        input_data["deed_month"] = st.text_input("Month of Signing")
        input_data["witness1_name"] = st.text_input("Witness 1 Name")
        input_data["witness2_name"] = st.text_input("Witness 2 Name")

        # Registration details
        #st.subheader("Registration Details (if applicable)")
        input_data["previous_owner"] = st.text_input("Previous Owner's Name")
        input_data["document_number"] = st.text_input("Document Number")
        input_data["book_number"] = st.text_input("Book Number")
        input_data["volume_number"] = st.text_input("Volume Number")
        input_data["page_number"] = st.text_input("Page Number")

    
    elif document_type == "Will":
        input_data["testator_name"] = st.text_input("Testator's Full Name")
        input_data["testator_parent_name"] = st.text_input("Testator's Parent's Name")
        input_data["testator_address"] = st.text_area("Testator's Address")
        input_data["testator_age"] = st.text_input("Testator's Age")
        input_data["testator_religion"] = st.text_input("Testator's Religion")
        input_data["testator_occupation"] = st.text_input("Testator's Occupation")
        
        input_data["executor1_name"] = st.text_input("Executor 1 Full Name")
        input_data["executor1_parent_name"] = st.text_input("Executor 1 Parent's Name")
        input_data["executor1_address"] = st.text_area("Executor 1 Address")
        input_data["executor1_age"] = st.text_input("Executor 1 Age")
        input_data["executor1_religion"] = st.text_input("Executor 1 Religion")
        input_data["executor1_occupation"] = st.text_input("Executor 1 Occupation")
        
        input_data["executor2_name"] = st.text_input("Executor 2 Full Name")
        input_data["executor2_parent_name"] = st.text_input("Executor 2 Parent's Name")
        input_data["executor2_address"] = st.text_area("Executor 2 Address")
        input_data["executor2_age"] = st.text_input("Executor 2 Age")
        input_data["executor2_religion"] = st.text_input("Executor 2 Religion")
        input_data["executor2_occupation"] = st.text_input("Executor 2 Occupation")

        input_data["executor3_name"] = st.text_input("Executor 3 Full Name")
        input_data["executor3_parent_name"] = st.text_input("Executor 3 Parent's Name")
        input_data["executor3_address"] = st.text_area("Executor 3 Address")
        input_data["executor3_age"] = st.text_input("Executor 3 Age")
        input_data["executor3_religion"] = st.text_input("Executor 3 Religion")
        input_data["executor3_occupation"] = st.text_input("Executor 3 Occupation")
        
        input_data["family_details"] = st.text_area("Family Details")
        input_data["assets"] = st.text_area("Assets Details")
        input_data["beneficiary_name"] = st.text_input("Beneficiary's Name")
        input_data["execution_date"] = st.date_input("Date of Will").strftime("%d-%m-%Y")

        
    elif document_type == "Power of Attorney":
        input_data["executant_name"] = st.text_input("Testator's Name")
        input_data["executant_relation"] = st.text_input("Testator's Relationship")
        input_data["executant_age"] = st.text_input("Testator's Age")
        input_data["executant_address"] = st.text_input("Testator's Address")

        input_data["attorney_name"] = st.text_input("Attorney's Name")
        input_data["attorney_relation"] = st.text_input("Attorney's Relationship")
        input_data["attorney_age"] = st.text_input("Attorney's Age")
        input_data["attorney_address"] = st.text_input("Attorney's Address")

        input_data["property_no"] = st.text_input("Property Number")
        input_data["property_measurements"] = st.text_input("Property Measurements")
        input_data["boundary_east"] = st.text_input("East Boundary")
        input_data["boundary_west"] = st.text_input("West Boundary")
        input_data["boundary_south"] = st.text_input("South Boundary")
        input_data["boundary_north"] = st.text_input("North Boundary")

        input_data["execution_day"] = st.text_input("Day of Execution")
        input_data["execution_month"] = st.text_input("Month of Execution")
        input_data["execution_year"] = st.text_input("Year of Execution")

        input_data["witness_1"] = st.text_input("First Witness")
        input_data["witness_2"] = st.text_input("Second Witness")

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
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer"><p>&copy; 2024 Legal Document Generator</p></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
