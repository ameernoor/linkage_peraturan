import streamlit as st
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Ensure this is correct

# Function to extract images from PDF
def extract_images_from_pdf(pdf_file):
    # Open the in-memory PDF file using BytesIO
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]  # The xref for the image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes))
            images.append(image)
    
    return images

# Function to apply OCR to an image
def ocr_image(image):
    return pytesseract.image_to_string(image)

# Streamlit UI setup
st.title("Regulation Document OCR Processor")
st.sidebar.header("Upload a PDF to Process")

# Streamlit file uploader to allow file upload
uploaded_pdf = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

# Extract text from the uploaded PDF
if uploaded_pdf is not None:
    # Extract images from the uploaded PDF and apply OCR
    images = extract_images_from_pdf(uploaded_pdf)
    ocr_text = ""
    for image in images:
        ocr_text += ocr_image(image)
    
    # Display the extracted OCR text
    st.subheader(f"Extracted OCR Text from {uploaded_pdf.name}")
    st.text_area("OCR Output", ocr_text, height=400)
    
    # Optionally, save the output to a file
    output_file_path = os.path.join("output", f"{uploaded_pdf.name}_ocr_output.txt")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(ocr_text)
    st.write(f"OCR output saved to: {output_file_path}")
