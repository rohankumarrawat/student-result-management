from django.contrib.auth import get_user_model
from student_management.models import StudentProfile, Subject, Result

User = get_user_model()

# Create Admin User
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    admin_user.role = 'admin'
    admin_user.first_name = 'Admin'
    admin_user.save()
    print("Admin user created: admin / admin123")
else:
    print("Admin user already exists: admin / admin123")

# Create Faculty User
if not User.objects.filter(username='faculty1').exists():
    faculty_user = User.objects.create_user('faculty1', 'faculty1@example.com', 'faculty123')
    faculty_user.role = 'faculty'
    faculty_user.first_name = 'Faculty One'
    faculty_user.save()
    print("Faculty user created: faculty1 / faculty123")
else:
    print("Faculty user already exists: faculty1 / faculty123")

# Create Student User
if not User.objects.filter(username='student1').exists():
    student_user = User.objects.create_user('student1', 'student1@example.com', 'student123')
    student_user.role = 'student'
    student_user.first_name = 'Student One'
    student_user.save()
    
    # Create Student Profile
    profile = StudentProfile.objects.create(user=student_user, roll_number='101')
    
    # Create a dummy Subject assigned to Faculty
    faculty_user = User.objects.get(username='faculty1')
    subject, created = Subject.objects.get_or_create(code='CS101', name='Computer Science', defaults={'faculty': faculty_user})
    
    # Assign some dummy marks
    Result.objects.create(student=profile, subject=subject, marks=85)
    
    print("Student user created: student1 / student123")
else:
    print("Student user already exists: student1 / student123")
