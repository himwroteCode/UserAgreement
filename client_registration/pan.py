# import cv2
# import pytesseract
# import re

# # Set the path to Tesseract executable (if not in PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows example

# def preprocess_image(image_path):
#     # Read image
#     img = cv2.imread(image_path)
#     # Convert to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # Apply Gaussian blur to reduce noise
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     # Thresholding using Otsu's method
#     _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     return threshold

# def extract_text(image_path):
#     processed_img = preprocess_image(image_path)
#     # Use Tesseract with custom configuration
#     text = pytesseract.image_to_string(processed_img, config='--psm 11 --oem 3')
#     return text

# def parse_pan_data(text):
#     data = {}
    
#     # PAN Number (format: ABCDE1234F)
#     pan_pattern = re.compile(r'[A-Z]{5}[0-9]{4}[A-Z]')
#     pan_match = pan_pattern.search(text)
#     if pan_match:
#         data['pan_number'] = pan_match.group()
    
#     # Date of Birth (format: DD/MM/YYYY)
#     dob_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
#     dob_match = dob_pattern.search(text)
#     if dob_match:
#         data['dob'] = dob_match.group()
    
#     # Name and Father's Name (look for "NAME" or "FATHER'S NAME" labels)
#     lines = [line.strip() for line in text.split('\n') if line.strip()]
#     name_keywords = ['name', 'father', 'mother']
#     for i, line in enumerate(lines):
#         if any(keyword in line.lower() for keyword in name_keywords):
#             # Assume the next line contains the name
#             if i + 1 < len(lines):
#                 data['name'] = lines[i + 1]
#             break  # Adjust logic if multiple matches
    
#     return data

# if __name__ == "__main__":
#     image_path = "E:\\User agreement OCR\\OCR\\PAN front.jpg"
#     extracted_text = extract_text(image_path)
#     pan_data = parse_pan_data(extracted_text)
    
#     print("Extracted PAN Data:")
#     for key, value in pan_data.items():
#         print(f"{key.upper()}: {value}")

import cv2
import pytesseract
import re

# Set the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy by converting to grayscale,
    applying Gaussian blur, and Otsu's thresholding.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold

def extract_text(image_path):
    """
    Extract text from the preprocessed image using Tesseract OCR with sparse text configuration.
    """
    processed_img = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_img, config='--psm 11 --oem 3')
    return text

def clean_lines(text):
    """
    Clean each line of the text by removing unwanted characters and preserving structure.
    """
    cleaned_lines = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        cleaned_line = re.sub(r'[^A-Za-z0-9/\- ]', '', line)
        cleaned_line = cleaned_line.strip()
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    return cleaned_lines

def extract_fields(cleaned_lines):
    """
    Extract PAN Number, DOB, Name, and Father's Name from cleaned lines using regex patterns.
    """
    fields = {
        "PAN Number": "Not Found",
        "DOB": "Not Found"
    }

    # PAN Number extraction
    pan_pattern = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b')
    pan_matches = []
    for line in cleaned_lines:
        pan_match = pan_pattern.search(line)
        if pan_match:
            pan_matches.append(pan_match.group())
    if pan_matches:
        fields["PAN Number"] = pan_matches[-1]  # Assume last occurrence is correct

    # DOB extraction
    dob_pattern = re.compile(r'\b(\d{2}[-/]\d{2}[-/]\d{4})\b')
    dob_matches = []
    for line in cleaned_lines:
        dob_match = dob_pattern.search(line)
        if dob_match:
            dob_matches.append(dob_match.group())
    if dob_matches:
        fields["DOB"] = dob_matches[0].replace('-', '/')  # Normalize to slashes

    return fields

def extract_pan_details(image_path):
    """
    Main function to extract PAN card details from the given image path.
    """
    raw_text = extract_text(image_path)
    cleaned_lines = clean_lines(raw_text)
    
    # print("=== Raw OCR Text ===")
    # print(raw_text)
    
    # print("\n=== Cleaned Lines ===")
    
    details = extract_fields(cleaned_lines)
    
    # print("\n=== Extracted Fields ===")
    for key, value in details.items():
        print(f"{key}: {value}")
    
    # return details

if __name__ == '__main__':
    image_path = "E:\\User agreement OCR\\OCR\\PAN front.jpg"  # Update with your image path
    extract_pan_details(image_path)