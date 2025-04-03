# import cv2
# import pytesseract
# import numpy as np
# from PIL import Image
# import re

# # Set Tesseract path (adjust if necessary)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_image(uploaded_file):
#     """Extract text using Tesseract OCR from an uploaded image."""
#     # Read the uploaded image into a numpy array
#     image_array = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#     img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)  # Convert to OpenCV format

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
#     text = pytesseract.image_to_string(gray)
#     return text

# def extract_aadhar_details(uploaded_file):
#     """Extract Aadhar details like Name and Number."""
#     text = extract_text_from_image(uploaded_file)
    
#     # Extract Name (Assuming it's in the first line)
#     name = text.split("\n")[0].strip()
#     print(name)
    
#     # Extract Aadhar Number (Regex for 12-digit format)
#     aadhar_match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', text)
#     aadhar_number = aadhar_match.group() if aadhar_match else None
#     print(aadhar_number)
    
#     return {"name": name, "aadhar_number": aadhar_number}

def extract_pan_details(uploaded_file):
    """Extract PAN card details like Name and PAN Number."""
    text = extract_text_from_image(uploaded_file)
    
    # Extract PAN Number (Regex for standard PAN format)
    pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', text)
    pan_number = pan_match.group() if pan_match else None
    print(pan_number)
    
    return {"pan_number": pan_number}

import cv2
import pytesseract
import re
import numpy as np

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(uploaded_file):
    """Preprocess the uploaded image for better OCR accuracy."""
    # Convert InMemoryUploadedFile to OpenCV format
    image_array = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((2, 2), np.uint8)
    processed_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return processed_img

def extract_text_from_image(uploaded_file):
    """Extract text using OCR with enhanced preprocessing."""
    processed_img = preprocess_image(uploaded_file)
    
    # Resize for better OCR
    scale_factor = 2
    height, width = processed_img.shape
    resized_img = cv2.resize(processed_img, (width * scale_factor, height * scale_factor))
    
    text = pytesseract.image_to_string(resized_img, lang='eng+hin')
    return text

def extract_aadhar_details(uploaded_file):
    """Extract Aadhaar Number, Name, and DOB using refined regex."""
    text = extract_text_from_image(uploaded_file)
    
    aadhaar_pattern = r"\b\d{4} \d{4} \d{4}\b"
    dob_pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    
    # Extract Aadhaar Number
    aadhaar_match = re.search(aadhaar_pattern, text)
    aadhaar_number = aadhaar_match.group() if aadhaar_match else None
    
    # Extract DOB
    dob_match = re.search(dob_pattern, text)
    dob = dob_match.group() if dob_match else None
    
    # Extract Name
    name = "Not Found"
    name_regex = r"([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,}){1,2})"
    name_matches = re.findall(name_regex, text)

    if name_matches:
        if aadhaar_match:
            aadhaar_pos = aadhaar_match.start()
            name = min(name_matches, key=lambda x: abs(text.find(x) - aadhaar_pos))
        else:
            name = max(name_matches, key=len)

        print(name)
        print(aadhaar_number)
        print(dob)
    
    return {
        "name": name,
        "aadhar_number": aadhaar_number,
        "dob": dob
    }

