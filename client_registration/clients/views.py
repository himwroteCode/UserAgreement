from django.shortcuts import render, redirect
from .models import Client
from .forms import ClientForm
from .ocr_utils import extract_aadhar_details
from django.contrib import messages
from datetime import datetime

def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract OCR data from Aadhaar image
            aadhar_data = extract_aadhar_details(request.FILES['aadhar_image'])

            # Get input details from form
            input_name = form.cleaned_data['client_name'].strip().upper()
            input_national_id = form.cleaned_data['national_id'].strip()
            
            # ✅ Convert input DOB to string (YYYY-MM-DD)
            input_dob = form.cleaned_data['dob'].strftime("%Y-%m-%d")

            # ✅ Fix Aadhaar Number Comparison (Remove spaces)
            extracted_aadhaar_number = aadhar_data['aadhar_number'].replace(" ", "").strip()

            # ✅ Fix DOB Comparison (Convert both to YYYY-MM-DD format)
            def standardize_dob(dob_str):
                try:
                    return datetime.strptime(dob_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    return dob_str  # Return as-is if conversion fails

            extracted_dob = standardize_dob(aadhar_data['dob'])

            # Track mismatches
            errors = []

            if aadhar_data['name'].upper() != input_name:
                errors.append(f"Name does not match! (Aadhaar: {aadhar_data['name']}, Entered: {input_name})")

            if extracted_aadhaar_number != input_national_id:
                errors.append(f"Aadhaar Number does not match! (Aadhaar: {extracted_aadhaar_number}, Entered: {input_national_id})")

            if extracted_dob != input_dob:
                errors.append(f"Date of Birth does not match! (Aadhaar: {extracted_dob}, Entered: {input_dob})")

            # If all match, register client
            if not errors:
                client = form.save()
                messages.success(request, f"Client {client.client_name} registered successfully!")
                return redirect('register_client')
            else:
                for error in errors:
                    messages.error(request, error)

    else:
        form = ClientForm()

    return render(request, 'clients/register.html', {'form': form})
