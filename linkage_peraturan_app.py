import streamlit as st
import os
import fitz  # PyMuPDF
import easyocr  # EasyOCR as an alternative to pytesseract
from PIL import Image
from io import BytesIO

# Initialize the EasyOCR reader (with default languages)
reader = easyocr.Reader(['en'])

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

# Function to apply OCR to an image using EasyOCR
def ocr_image(image):
    # Convert PIL Image to bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Use EasyOCR to perform OCR on the image bytes
    result = reader.readtext(img_byte_arr)
    
    # Join all the detected text
    ocr_text = " ".join([text[1] for text in result])
    return ocr_text

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
    
    # Create a download link for the OCR result
    output_file_path = f"{uploaded_pdf.name}_ocr_output.txt"
    
    # Save the OCR result to a file and generate a download link
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(ocr_text)

    # Provide the download link to the user
    with open(output_file_path, "r") as file:
        btn = st.download_button(
            label="Download OCR Output",
            data=file,
            file_name=output_file_path,
            mime="text/plain"
        )

    # Optionally display some part of the output in the app
    st.subheader(f"Extracted OCR Text from {uploaded_pdf.name}")
    st.text_area("OCR Output (partial)", ocr_text[:500], height=200)  # Display first 500 characters

    # Inform the user that the result is ready for download
    st.write(f"OCR output is ready for download as {output_file_path}")
