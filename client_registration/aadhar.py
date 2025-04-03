import cv2
import pytesseract
import re
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """Preprocess the image for better OCR accuracy."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((2,2), np.uint8)
    processed_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return processed_img

def extract_text_from_image(image_path):
    """Extract text using OCR with enhanced preprocessing."""
    processed_img = preprocess_image(image_path)
    scale_factor = 2
    height, width = processed_img.shape
    resized_img = cv2.resize(processed_img, (width * scale_factor, height * scale_factor))
    text = pytesseract.image_to_string(resized_img, lang='eng+hin')
    return text

def extract_aadhaar_info(text):
    """Extract Aadhaar Number, Name, and DOB using refined regex."""
    aadhaar_pattern = r"\b\d{4} \d{4} \d{4}\b"
    dob_pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    
    # Extract Aadhaar Number
    aadhaar_match = re.search(aadhaar_pattern, text)
    aadhaar_number = aadhaar_match.group() if aadhaar_match else "Not Found"
    
    # Extract DOB
    dob_match = re.search(dob_pattern, text)
    dob = dob_match.group() if dob_match else "Not Found"
    
    # **Name Extraction with Custom Regex**
    name = "Not Found"
    name_regex = r"([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,}){1,2})"
    name_matches = re.findall(name_regex, text)
    
    if name_matches:
        # Prioritize matches near Aadhaar number (if available)
        if aadhaar_match:
            aadhaar_pos = aadhaar_match.start()
            # Find the name closest to the Aadhaar number
            name = min(
                name_matches,
                key=lambda x: abs(text.find(x) - aadhaar_pos)
            )
        else:
            # Fallback: Use the longest match
            name = max(name_matches, key=len)
    
    return {"Aadhaar Number": aadhaar_number, "Name": name, "DOB": dob}
    
def main(image_path):
    extracted_text = extract_text_from_image(image_path)
    aadhaar_details = extract_aadhaar_info(extracted_text)
    
    print("\nExtracted Aadhaar Details:")
    print(f"Name: {aadhaar_details['Name']}")
    print(f"Aadhaar Number: {aadhaar_details['Aadhaar Number']}")
    print(f"Date of Birth (DOB): {aadhaar_details['DOB']}")
    return aadhaar_details

# Example Usage
image_path = r'E:\User agreement OCR\OCR\Aadhar front.jpg'
data = main(image_path)
