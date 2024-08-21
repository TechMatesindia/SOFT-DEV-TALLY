from django.db import models
from django.utils.crypto import get_random_string
from django.db import models 
import datetime

class User(models.Model):
    name = models.CharField(max_length=20)          
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


class SignupRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200, unique=True)
    request_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    signup_type = models.CharField(max_length=20) 
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)

    def __str__(self):
        return f"Signup Request for {self.user.username}, Approved: {self.approved}, Request Date: {self.request_date}"

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)  
    manager = models.CharField(max_length=100, blank=True, null=True)   
    capacity = models.IntegerField(default=50, blank=True, null=True)   
    opening_date = models.DateField(blank=True, null=True) 
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)   
    branchstaticid = models.CharField(max_length=20)    
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    state = models.CharField(max_length=100, blank=True, null=True)  
    pincode = models.CharField(max_length=10, blank=True, null=True)  
    profile_picture = models.ImageField(upload_to='branch_profile_pics/', blank=True, null=True)


class Batch(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    Studentid = models.CharField(max_length=20, default="RTC100")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True, null=True)
    batches = models.ManyToManyField('Batch', related_name="students", related_query_name="students", null=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)  # Added field
    guardian_number = models.IntegerField( blank=True, null=True)  # Added field
    profile_picture = models.ImageField(upload_to='signup_pictures/', blank=True, null=True)
    upload_sign = models.ImageField(upload_to='signatures/', blank=True, null=True)
    DateofAdmission = models.DateField(default=datetime.date.today)
    studentsession = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    receipt_path = models.CharField(max_length=255, blank=True, null=True)
    monthlyAdmitCard = models.CharField(max_length=255, blank=True, null=True)
    YearlyAdmitCard = models.CharField(max_length=255, blank=True, null=True)
    roll_number = models.CharField(max_length=50, blank=True, null=True)  # Add roll number field
    enrollment_number = models.CharField(max_length=50, blank=True, null=True) 




    
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    salary = models.PositiveIntegerField(null=True)
    attendance = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], blank=True, null=True)
    batches = models.ManyToManyField(Batch) 
    password = models.CharField(max_length=200)
    location = models.CharField(max_length=100,blank=True, null=True)  
    joining_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='teacher_profile_pictures/',default='default_profile_picture.jpg')





class Attendance(models.Model):
    batch_id  =models.IntegerField(blank=True,null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=10)  

class Subject(models.Model):
    name = models.CharField(max_length=100)
    theory_marks_obtained = models.IntegerField(blank=True,null=True)
    theory_max_marks = models.IntegerField(blank=True,null=True)
    practical_marks_obtained = models.IntegerField(blank=True,null=True)
    practical_max_marks = models.IntegerField(blank=True,null=True)

    


class Course(models.Model):
    COURSE_TYPES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('advanced_diploma', 'Advanced Diploma'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    document = models.ImageField(upload_to='course_documents/')
    duration = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    subjects = models.ManyToManyField(Subject)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    batch = models.ManyToManyField(Batch)
    

    
class Marks(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    theory_marks_obtained = models.IntegerField(blank=True,null=True)
    theory_max_marks = models.IntegerField(blank=True,null=True)
    practical_marks_obtained = models.IntegerField(blank=True,null=True)
    practical_max_marks = models.IntegerField(blank=True,null=True)

    
class PaymentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True)
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)  


  
class Fees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=20)


    

class MarksheetRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course,on_delete=models.CASCADE)
    # marks = models.ForeignKey(Marks,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete = models.CASCADE)
    issuedate = models.DateField(blank=True, null=True)
    approved = models.BooleanField(default=False) 
    marksheet_pdf_url = models.CharField(max_length=255, null=True, blank=True)


    

class Wallet(models.Model):
    branch = models.OneToOneField(Branch,on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(default=datetime.date.today)
    signup_request  = models.IntegerField(default=300)
    marksheet_amount = models.IntegerField(default=800.0)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateField(default=datetime.date.today)
    branchstaticid = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.transaction_type} - ₹{self.amount}"
    

class OldCourse(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    duration = models.CharField(max_length=50,default=1) 
    price = models.IntegerField(default=0)

class OldMarksheet(models.Model):
    branch_code = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    dob = models.DateField()
    mobile_number = models.CharField(max_length=10)
    address = models.TextField()
    branch_address = models.TextField()
    branch_state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    enrollment_no = models.CharField(max_length=100, unique=True)
    session = models.CharField(max_length=100)
    registration_date = models.DateField()
    course = models.ForeignKey(OldCourse, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='old_profile_pictures/',default='default_profile_picture.jpg')
    serial_number = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100)
    certificate_pdf_url = models.CharField(max_length=255, null=True, blank=True)
    marksheet_pdf_url = models.CharField(max_length=255, null=True, blank=True)


class OldSubject(models.Model):
    course = models.ForeignKey(OldCourse, on_delete=models.CASCADE)
    student = models.ForeignKey(OldMarksheet,on_delete=models.CASCADE,null=True)
    subject_name = models.CharField(max_length=100)
    theory_marks = models.IntegerField(null=True)
    theory_max_marks = models.IntegerField(null=True,default=100)
    practical_marks = models.IntegerField(null=True)
    practical_max_marks = models.IntegerField(null=True,default=100)
    total_obtained_marks = models.IntegerField(null=True)
    total_max_marks = models.IntegerField(null=True)


class MonthlyAdmitCard(models.Model):
    session = models.CharField(max_length=9) 
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    semester = models.CharField(max_length=10)
    paper_name = models.CharField(max_length=255)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.CharField(max_length=10)
    exam_centre = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)

    
class YearlyAdmitCard(models.Model):
    session = models.CharField(max_length=10)
    course_type = models.CharField(max_length=20)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    exam_date = models.DateField()
    paper1_start_time = models.TimeField()
    paper1_end_time = models.TimeField()
    paper1_total_hours = models.CharField(max_length=10)
    paper2_start_time = models.TimeField()
    paper2_end_time = models.TimeField()
    paper2_total_hours = models.CharField(max_length=10)
    exam_centre = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()
    no_of_holidays = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

