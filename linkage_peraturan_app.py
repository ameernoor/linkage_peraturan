import streamlit as st
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Ensure this is correct

# Function to extract images from PDF
def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
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
st.sidebar.header("Select a PDF to Process")

# Folder path containing the regulations
folder_path = r"E:\Gawean\OTL\!Potensi Inovasi OTL\Daftar Peraturan"

# List files in the folder for the user to select
pdf_files = os.listdir(folder_path)
selected_pdf = st.sidebar.selectbox("Select a PDF", pdf_files)

# Extract text from selected PDF
if selected_pdf:
    pdf_file_path = os.path.join(folder_path, selected_pdf)
    
    # Extract images from PDF and apply OCR
    images = extract_images_from_pdf(pdf_file_path)
    ocr_text = ""
    for image in images:
        ocr_text += ocr_image(image)
    
    # Display the extracted OCR text
    st.subheader(f"Extracted OCR Text from {selected_pdf}")
    st.text_area("OCR Output", ocr_text, height=400)
    
    # Optionally, save the output to a file
    output_file_path = os.path.join(folder_path, f"{selected_pdf}_ocr_output.txt")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(ocr_text)
    st.write(f"OCR output saved to: {output_file_path}")
