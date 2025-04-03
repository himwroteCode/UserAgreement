from django.db import models

class Client(models.Model):
    # Personal Details
    client_id = models.CharField(max_length=20, unique=True, blank=True)  # Auto-generated
    client_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    marital_status = models.CharField(max_length=15, choices=[('Single', 'Single'), ('Married', 'Married')])
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    nationality = models.CharField(max_length=50)
    national_id = models.CharField(max_length=50, unique=True)
    emergency_contact_person = models.CharField(max_length=100)
    emergency_contact_relation = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=15)

    # Residential Information
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    ward = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    postal_address = models.TextField()
    postal_code = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        # Generate client_id (First 4 letters of name + City + '01')
        if not self.client_id:
            self.client_id = f"{self.client_name[:4].upper()}{self.city[:3].upper()}01"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.client_name
