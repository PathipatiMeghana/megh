
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from user.models import Bacteria, Antibiotic, Patient, CustomUser, Test

def seed():
    # Create Bacteria
    bacteria_names = ['E. coli', 'Staphylococcus aureus', 'Klebsiella pneumoniae', 'Pseudomonas aeruginosa']
    for name in bacteria_names:
        Bacteria.objects.get_or_create(name=name)
    
    # Create Antibiotics
    antibiotic_names = ['Amoxicillin', 'Ciprofloxacin', 'Gentamicin', 'Meropenem', 'Vancomycin']
    for name in antibiotic_names:
        Antibiotic.objects.get_or_create(name=name)

    # Ensure we have a default doctor for patients
    doctor, created = CustomUser.objects.get_or_create(
        username='doctor',
        defaults={'email': 'doctor@example.com', 'role': 'doctor'}
    )
    if created:
        doctor.set_password('password123')
        doctor.save()

    # Create some patients
    patients_data = [
        {'name': 'John Doe', 'age': 45, 'gender': 'Male', 'doctor': doctor},
        {'name': 'Jane Smith', 'age': 32, 'gender': 'Female', 'doctor': doctor},
        {'name': 'Sarah Connor', 'age': 28, 'gender': 'Female', 'doctor': doctor},
    ]
    for p_data in patients_data:
        Patient.objects.get_or_create(name=p_data['name'], defaults=p_data)

    # Create some test results for statistical engine
    Test.objects.get_or_create(
        doctor=doctor,
        bacteria_name='E. coli',
        antibiotic_name='Amoxicillin',
        result='R'
    )
    Test.objects.get_or_create(
        doctor=doctor,
        bacteria_name='E. coli',
        antibiotic_name='Ciprofloxacin',
        result='S'
    )

    print("Seeding complete!")

if __name__ == '__main__':
    seed()
