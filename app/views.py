from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from .models import User,Branch
from django import forms
from datetime import datetime
import calendar
from django.contrib import messages,auth
from .models import SignupRequest,Student,Teacher,Batch,Attendance,Course,Subject,Marks,PaymentRequest,Fees,MarksheetRequest,Fees,Wallet,Transaction,OldMarksheet,OldCourse,OldSubject,MonthlyAdmitCard,YearlyAdmitCard,Holiday
import random
from django.core.mail import send_mail
# from .serializers import StudentSerializer 
from django.core import serializers
import json
from django.db import transaction
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import date as date_filter
from rest_framework.decorators import api_view
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import json
from django.http import JsonResponse
from django.conf import settings
from weasyprint import HTML,CSS
import os
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

import threading



def home(request):
    courses= Course.objects.all()
    return render(request, 'app/index.html',{'courses':courses})


def teacherdashboardlogin(request):
     return render(request, 'app/teacherdashboard.html')

def termsandconditions(request):
     return render(request, 'app/t&c.html')

def refundpolicy(request):
     return render(request, 'app/refundpolicy.html')

def privacypolicy(request):
     return render(request, 'app/privacypolicy.html')


def holiday(request):
     return render(request, 'app/adminholiday.html')



def printmarksheet(request):
    branch_id = request.GET.get('branch_id')
    batch_id = request.GET.get('batch_id')
    student_id = request.GET.get('student_id')
    course_id = request.GET.get('course_id')

    student =  get_object_or_404(Student, Studentid=student_id)

    marksheets = Marks.objects.filter(branch_id=branch_id, batch_id=batch_id, student_id=student.id, course_id=course_id)
    print(marksheets)
    marks = []
    for i in marksheets:
        x = {'subject_id' : i.subject,"theory_marks":i.theory_marks_obtained,"theory_max_marks":i.theory_max_marks,"practical_marks":i.practical_marks_obtained,"practical_total_marks":i.practical_max_marks }
        marks.append(x)

    otherdetails = [{"branch":marksheets[0].branch,"student":marksheets[0].student,"batch":marksheets[0].batch,"course":marksheets[0].course}]
    print(marks,otherdetails)
    return render(request, 'app/printmarksheet.html', {'marks': marks,'otherdetails':otherdetails})


def attendence(request, user_id):
    teacher = get_object_or_404(Teacher, id=user_id)
    branch = teacher.branch
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    
    batches = Batch.objects.filter(branch=branch)
    students = Student.objects.filter(batches__branch=branch)

    
    return render(request, 'app/attendence.html', {'teacher': teacher, 'batches': batches, 'students': students, 'days_in_month': range(1, days_in_month + 1)})


def create_course(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)

    if request.method == 'POST':
        coursetype = request.POST.get('course_type')
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        image = request.FILES.get('image')
        document = request.FILES.get('document')
        price = request.POST.get('price')
        course = Course.objects.create(name=name,course_type=coursetype ,duration=duration, image=image, branch=branch,document =document , price= price)
        course.branch = branch  
        course.save()

        return redirect('branchdashboard',branch_id = branch.id)
    else:
        return HttpResponse("Error")
    

def admin_create_course(request, branch_id):

    if request.method == 'POST':
        coursetype = request.POST.get('course_type')
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        image = request.FILES.get('image')
        document = request.FILES.get('document')
        price = request.POST.get('price')
        course = Course.objects.create(name=name,course_type=coursetype ,duration=duration, image=image, branch=branch,document =document , price= price)
        course.branch = 'null'  
        course.save()

        return redirect('dashboard')
    else:
        return HttpResponse("Error")


def createcourse(request,branch_id):
        branch = get_object_or_404(Branch, pk=branch_id)
        courses = Course.objects.filter(branch=branch)
        return render(request, 'app/coursecreation.html', {'courses': courses,'branch':branch})


def director(request):
    return render(request, 'app/director.html')


def payment(request):
    payment_data = request.session.get('payment_data')
    print(payment_data)
    if payment_data:
        course_name = payment_data.get('course_data').get('name')
        course_price = payment_data.get('course_price')
        course_duration = payment_data.get('course_duration')

        context = {
            'course_name': course_name,
            'course_price': course_price,
            'course_duration': course_duration,
        }
        return render(request, 'app/payment.html', context)
    else:
        return HttpResponse("Payment data not found. Please complete registration first.")



def adminteachers(request):
    teachers = Teacher.objects.all()
    branches = Branch.objects.all()
    return render(request, 'app/adminteachers.html', {'teachers': teachers,'branches':branches})


def adminstudents(request):
    students = Student.objects.all()
    return render(request, 'app/adminstudents.html', {'students': students})


def adminbranch(request):
    branches = Branch.objects.all()
    return render(request, 'app/adminbranch.html', {'branches': branches})


def excellence(request):
    return render(request, 'app/Excellence.html')

def certificate(request):
    return render(request, 'app/certificate.html')

def contact(request):
    return render(request, 'app/contact.html')

def upload(request):
    return render(request, 'app/teacherupload.html')

def gallery(request):
    return render(request, 'app/gallery.html')
    
def chairman(request):
    return render(request, 'app/chairman.html')

def admitcarddownload(request):
    return render(request, 'app/admitcardownload.html')

def feespayment(request):
    return render(request, 'app/feespayement.html')

def registrationverification(request):
    return render(request, 'app/registrationverification.html')

def branchlisthome(request):
    branches = Branch.objects.all() 
    return render(request, 'app/branchlist.html',{'branches':branches})

def createsubject(request):
    courses = Course.objects.all()  
    subject_data = {}  
    for course in courses:
        subject_data[course] = Subject.objects.filter(course=course)
    return render(request, 'app/createsubject.html', {'courses': courses, 'subject_data': subject_data})



def results(request):
    return render(request, 'app/result.html')


def studentresults(request):
    return render(request, 'app/studentresults.html')



def studentfeestable(request, branch_id):
    students = Student.objects.filter(branch_id=branch_id)
    print(students)

    student_fee_data = []

    for student in students:
        print(student.id)
        try:
            fee_data = Fees.objects.get(user=student.user_id)
            fee_amount = fee_data.amount
            fee_status = fee_data.status
            
            course = Course.objects.get(id=fee_data.course_id)
            course_name = course.name
            course_fees = course.price 
        except Fees.DoesNotExist:
            fee_amount = "N/A"
            fee_status = "N/A"
            course_name = "N/A"
            course_fees = "N/A"
        student_fee_data.append({
            'id': student.id,
            'name': student.name,
            'fee_amount': fee_amount,
            'fee_status': fee_status,
            'course_name': course_name,
            'course_fees': course_fees
        })
        print(student_fee_data)

    context = {
        'student_fee_data': student_fee_data
    }

    return render(request, 'app/studentfeestable.html', context)





def createmarksheet(request):
    branches = Branch.objects.all()
    marks = Marks.objects.all()
    # batches = Batch.objects.all()
    # students = Student.objects.all()
    # courses = Course.objects.all()
    # subjects = Subject.objects.all()
    # marks = Marks.objects.all()

     
        # 'branches': branches,
        # 'marks':marks
        # 'batches': batches,
        # 'students': students,
        # 'courses': courses,
        # 'subjects': subjects,
        # 'marks': marks,
    
    return render(request, 'app/createmarksheet.html', {'branches': branches,'marks':marks})





def certificatedownload(request):
    return render(request, 'app/certificatedownload.html')


def printcertificate(request):
    # Retrieve parameters from the URL query string
    branch_id = request.GET.get('branch_id')
    batch_id = request.GET.get('batch_id')
    student_id = request.GET.get('student_id')
    course_id = request.GET.get('course_id')

    student =  get_object_or_404(Student, Studentid=student_id)

    # Fetch data from the database based on the parameters
    marksheets = Marks.objects.filter(branch_id=branch_id, batch_id=batch_id, student_id=student.id, course_id=course_id)
   

    # Pass the fetched data to the template
    return render(request, 'app/printcertificate.html', {'marksheets': marksheets})

def team(request):
    return render(request, 'app/team.html')

def vision(request):
    return render(request, 'app/vision.html')

def facilities(request):
    return render(request, 'app/facilities.html')

def pdfmaterial(request):
    return render(request, 'app/pdfmaterial.html')

def brochure(request):
    return render(request, 'app/brochure.html')

def branchlogin(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")

            branch = Branch.objects.get(email=email)
        
            if password == branch.password:
                if email == "admin@example.com":
                    return redirect('dashboard')
                else:
                    return redirect('branchdashboard', branch_id=branch.id)
            else:
                return JsonResponse({"message": "Invalid email or password"})
        
        except Branch.DoesNotExist:
            return JsonResponse({"message": "Branch not found"})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Server error"})

    return render(request, 'app/branchlogin.html')


def teacherlogin(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
        
            teacher = Teacher.objects.get(email=email)

            if teacher.password == password:
                return redirect('teacherdashboard', user_id=teacher.id)
            else:
                return JsonResponse({"message": "Invalid email or password"})
        except Teacher.DoesNotExist:
            return JsonResponse({"message": "Teacher not found"})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Server error"})
    return render(request, 'app/teacherlogin.html')




def course(request):
    return render(request, 'app/course.html')

def internationalcourse(request):
    return render(request, 'app/internationalcourse.html')

def vision(request):
    return render(request, 'app/vision.html')

def verifyotp(request):
    return render(request, 'app/verifyotp.html')

# def batchlist(request):
#     return render(request, 'app/batchlist.html')

def about(request):
    return render(request, 'app/about.html')
def login(request):
    return render(request, 'app/login.html')
# def dashboard(request):
#     return render(request, 'app/adashboard.html')
def signup(request):
    branches = Branch.objects.all()
    courses = Course.objects.all()

    return render(request, 'app/signup.html', {'branches': branches,'courses':courses})



def generate_otp():
    return str(random.randint(1000, 9999))

def register(request):
    if request.method == "POST":
        try:
            # Collecting form data
            name = request.POST.get("name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirmpassword = request.POST.get("confirmpassword")
            father_name = request.POST.get("father_name")
            mother_name = request.POST.get("mother_name")
            dob = request.POST.get("dob")
            residential_address = request.POST.get("residential_address")
            branch_id = request.POST.get("branch_id")
            mobilenumber = request.POST.get("mobilenumber")
            gaurdiannumber = request.POST.get("gaurdiannumber")
            profile_picture = request.FILES.get("profile_picture")
            course = request.POST.get("course")
            session = request.POST.get("session")
            gender = request.POST.get("gender")
            signature = request.FILES.get("signature")

            # Validation checks
            if not username:
                return JsonResponse({"error": "Username is a required field."}, status=400)

            if not email:
                return JsonResponse({"error": "Email is a required field."}, status=400)

            if not password:
                return JsonResponse({"error": "Password is a required field."}, status=400)

            if password != confirmpassword:
                return JsonResponse({"error": "Passwords do not match."}, status=400)

            # if User.objects.filter(username=username).exists():
            #     return JsonResponse({"error": "Username already exists."}, status=400)

            # if User.objects.filter(email=email).exists():
            #     return JsonResponse({"error": "Email already exists."}, status=400)

            # Additional checks for required fields
            if not name:
                return JsonResponse({"error": "Name is a required field."}, status=400)

            if not mobilenumber:
                return JsonResponse({"error": "Mobile number is a required field."}, status=400)

            if not dob:
                return JsonResponse({"error": "Date of birth is a required field."}, status=400)

            if not branch_id:
                return JsonResponse({"error": "Branch ID is a required field."}, status=400)

            if not course:
                return JsonResponse({"error": "Course is a required field."}, status=400)

            if not session:
                return JsonResponse({"error": "Session is a required field."}, status=400)

            if not gender:
                return JsonResponse({"error": "Gender is a required field."}, status=400)

            # If all checks pass, proceed with OTP generation
            otp = generate_otp()

            send_mail(
                'OTP for Email Verification',
                f'Your OTP is: {otp}',
                'akshatasthana73@gmail.com',
                [email],
                fail_silently=False,
            )

            fs = FileSystemStorage()

            # Save profile picture
            profile_picture_name = fs.save(profile_picture.name, profile_picture) if profile_picture else None

            # Save signature
            signature_name = fs.save(signature.name, signature) if signature else None

            # Store data in session for OTP verification
            request.session['name'] = name
            request.session['username'] = username
            request.session['email'] = email
            request.session['password'] = password
            request.session['mother_name'] = mother_name
            request.session['residential_address'] = residential_address
            request.session['dob'] = dob
            request.session['branch_id'] = branch_id
            request.session['profile_picture'] = profile_picture_name
            request.session['signature'] = signature_name
            request.session['gender'] = gender
            request.session['otp'] = otp
            request.session['course'] = course
            request.session['session'] = session
            request.session['father_name'] = father_name
            request.session['mobilenumber'] = mobilenumber
            request.session['gaurdiannumber'] = gaurdiannumber

            return JsonResponse({"message": "OTP sent to your email. Please verify."})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return render(request, 'app/login.html')


def verify_otp(request):
    if request.method == "POST":
        try:
            otp_entered = request.POST.get("otp")
            otp_generated = request.session.get("otp")
            
            if otp_entered != otp_generated:
                return JsonResponse({"error": "Invalid OTP."})

            session = request.session.get("session")
            name = request.session.get("name")
            username = request.session.get("username")
            email = request.session.get("email")
            password = request.session.get("password")
            father_name = request.session.get("father_name")
            mother_name = request.session.get("mother_name")
            mobilenumber = request.session.get("mobilenumber")
            gaurdiannumber = request.session.get("gaurdiannumber")
            gender = request.session.get("gender")
            dob = request.session.get("dob")
            residential_address = request.session.get("residential_address")
            branch_id = request.session.get("branch_id")
            course_id = request.session.get("course")

            profile_picture_path = request.session.get("profile_picture")
            signature_path = request.session.get("signature")


            print(profile_picture_path,signature_path)

            if not profile_picture_path or not signature_path:
                return JsonResponse({"error": "Profile picture and signature paths are required."})

            course = get_object_or_404(Course, pk=course_id)

            last_student = Student.objects.order_by('-Studentid').first()
            if last_student:
                last_student_id = int(last_student.Studentid[3:]) + 1
            else:
                last_student_id = 100 

            student_id = "SDT" + str(last_student_id)

            user = User.objects.create(username=username, email=email, password=password, name=name)

            student = Student.objects.create(
                user=user,
                name=name,
                course=course,
                email=email,
                branch_id=branch_id,
                studentsession=session,
                mother_name=mother_name,
                dob=dob,
                permanent_address=residential_address,
                upload_sign=signature_path,
                gender=gender,
                father_name=father_name,
                phone_number=mobilenumber,
                guardian_number=gaurdiannumber,
                profile_picture=profile_picture_path,
                Studentid=student_id
            )

            request.session['user_id'] = user.id

            course_data = {
                'id': course.id,
                'name': course.name
            }
            
            course_price = int(course.price)
            course_duration = int(course.duration)
            payment_data = {
                'user_id': user.id,
                'username': username,
                'email': email,
                'course_data': course_data,
                'course_price': course_price,
                'course_duration': course_duration,
                'branch_id': branch_id,
            }
            print(payment_data)
            request.session['payment_data'] = payment_data
        

            return JsonResponse({"message": "Registration successful."})

        except Exception as e:
            return JsonResponse({"error": str(e)})
    
    return render(request, 'app/payment.html')


def adminlogin(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")

            if email == "admin@example.com":
                if password =="adminpassword":
                    return redirect('dashboard')
                else:
                    return JsonResponse({"message": "Invalid email or password"})
       
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Server error"})
    return render(request, 'app/adminlogin.html')

def login(request):
     if request.method == "POST":
        try:
            rollnumber = request.POST.get("rollnumber")
            password = request.POST.get("password")
    
            student = Student.objects.get(roll_number=rollnumber)
            user = User.objects.get(id = student.user.id)
            if password == user.password:
                student, created = Student.objects.get_or_create(user=user)
                return redirect('studentdashboard', user_id=user.id)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"})
     return render(request, 'app/login.html')   



def signup_requests(request):
    signup_requests = SignupRequest.objects.all()
    context = {
        'signup_requests': signup_requests
    }
    return render(request, 'app/adashboard.html', context)


def dashboard(request):
    marksheet_requests = MarksheetRequest.objects.all()
    teachers = Teacher.objects.all()
    batches = Batch.objects.all()
    branches = Branch.objects.all()
    Transactions = Transaction.objects.all()


    context = {
        'marksheetrequests': marksheet_requests,
        'teachers': teachers,
        'batches': batches,
        'branches': branches,
        'Transactions':Transactions
    }

    return render(request, 'app/adashboard.html', context)

# def approve_signup_request(request, request_id):
#     # if not request.user.is_superuser:
#     #     return redirect('index')  

#     signup_request = SignupRequest.objects.get(pk=request_id)
#     signup_request.approved = True
#     signup_request.user.is_active = True
#     signup_request.user.save()
#     signup_request.save()
#     return redirect('dashboard')

def studentdashboard(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        student = Student.objects.get(user=user)
        fees = Fees.objects.get(user_id=user.id)
        
        branch_id = student.branch_id
        
        return render(request, 'app/studentdashboard.html', {'student': student, 'branch_id': branch_id,'fees':fees})
    
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found"})
    except Student.DoesNotExist:
        return JsonResponse({"message": "Student profile not found"})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Server error"})
    

def teacherdashboard(request, user_id):
    try:
        user = Teacher.objects.get(pk=user_id)
        teacher = Teacher.objects.get(id=user.id)
        branches = Branch.objects.all()
        return render(request, 'app/teacherdashboard.html', {'teacher': teacher,'branches':branches})
    except Teacher.DoesNotExist:
        return JsonResponse({"message": "User not found"})


# def teacherdashboard(request):
#     return render(request, 'app/teacherdashboard.html')
def branchdashboard(request, branch_id):
    try:    
        branch = get_object_or_404(Branch, pk=branch_id)
        
        
        wallet = Wallet.objects.get(branch_id=branch_id)
        Transactions = Transaction.objects.filter(branchstaticid = branch.branchstaticid)
 

        teachers = Teacher.objects.filter(branch=branch)
        courses = Course.objects.filter(branch=branch)
        students = Student.objects.filter(branch=branch)
        batches = Batch.objects.filter(branch=branch)
        payment_requests = PaymentRequest.objects.filter(branch=branch)
        print(branch_id)
        print(payment_requests)
        return render(request, 'app/branchdashboard.html', {
            'branch': branch, 
            'courses': courses, 
            'students': students, 
            'teachers': teachers, 
            'payment_requests': payment_requests,
            'batches': batches,
            'wallet': wallet,
            'Transactions':Transactions
        })
    except Branch.DoesNotExist:
        return JsonResponse({"message": "Branch not found"})


def marks(request):

    branches = Branch.objects.all()
    batches = Batch.objects.all()
    students = Student.objects.all()
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    
    # print(branches,batches,students,courses,subjects)

    return render(request, 'app/entermarks.html',{'branches': branches,'batches': batches,'students': students,'courses': courses,'subjects':subjects})



def branchtables(request,branch_id):
    branches = Branch.objects.filter(branch_id=branch_id)
    return render(request, 'app/branchtables.html', {'branches': branches})


def studentables(request,branch_id):
    students = Student.objects.filter(branch_id=branch_id)
    return render(request, 'app/studenttables.html', {'students': students})

def teachertables(request, branch_id):
    teachers = Teacher.objects.filter(branch_id=branch_id)
    branch = Branch.objects.filter(id = branch_id)
    print(branch)
    return render(request, 'app/teachertables.html',{'teachers': teachers,'branch':branch})
 
def enter_marks(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    
    branch_id = data.get('branch')
    batch_id = data.get('batch')
    student_id = data.get('student')
    course_id = data.get('course')
    subject_id_list = data.get('subject')
    theory_marks_obtained_list = data.get('theory_marks_obtained')
    theory_max_marks_list = data.get('theory_max_marks')
    practical_marks_obtained_list = data.get('practical_marks_obtained')
    practical_max_marks_list = data.get('practical_max_marks')

    # Check if all required data is provided
    if not all([branch_id, batch_id, student_id, course_id, subject_id_list,
                theory_marks_obtained_list, theory_max_marks_list,
                practical_marks_obtained_list, practical_max_marks_list]):
        return JsonResponse({'error': 'Missing required data'}, status=400)
    
    # Ensure that all lists have the same length
    if not (len(subject_id_list) == len(theory_marks_obtained_list) == len(theory_max_marks_list) == len(practical_marks_obtained_list) == len(practical_max_marks_list)):
        return JsonResponse({'error': 'Mismatch in lengths of provided lists'}, status=400)

    try:
        student = Student.objects.get(Studentid=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student does not exist.'}, status=400)
    except Student.MultipleObjectsReturned:
        return JsonResponse({'error': 'Multiple students found with the same ID.'}, status=400)

    for subject_id, theory_marks_obtained, theory_max_marks, practical_marks_obtained, practical_max_marks in zip(
            subject_id_list, theory_marks_obtained_list, theory_max_marks_list,
            practical_marks_obtained_list, practical_max_marks_list):

        try:
            marks = Marks.objects.get(
                branch_id=branch_id,
                batch_id=batch_id,
                student=student,
                course_id=course_id,
                subject_id=subject_id
            )
            # Update existing marks
            marks.theory_marks_obtained = theory_marks_obtained
            marks.theory_max_marks = theory_max_marks
            marks.practical_marks_obtained = practical_marks_obtained
            marks.practical_max_marks = practical_max_marks
            marks.save()
        except Marks.DoesNotExist:
            # Create a new entry if it does not exist
            Marks.objects.create(
                branch_id=branch_id,
                batch_id=batch_id,
                student=student,
                course_id=course_id,
                subject_id=subject_id,
                theory_marks_obtained=theory_marks_obtained,
                theory_max_marks=theory_max_marks,
                practical_marks_obtained=practical_marks_obtained,
                practical_max_marks=practical_max_marks
            )

    return JsonResponse({'message': 'Marks entered successfully.'})

def approve_user(request, signup_request_id):
    try:
        signup_request = SignupRequest.objects.get(id=signup_request_id)
        user = signup_request.user
        signup_type = signup_request.signup_type

        # Set the signup request as approved
        signup_request.approved = True
        signup_request.save()

        if signup_type == 'student':
            Student.objects.create(user=user)
        elif signup_type == 'teacher':
                Teacher.objects.create(user=user)
                pass

        return redirect('dashboard')
    except SignupRequest.DoesNotExist:
        return redirect('dashboard')
    
def reject_user(request, signup_request_id):
    try:
        signup_request = SignupRequest.objects.get(id=signup_request_id)
        signup_request.delete()
        return redirect('dashboard')  
    except SignupRequest.DoesNotExist:
        return redirect('dashboard') 
    


def add_branch(request):
    if request.method == 'POST':
        branch_name = request.POST.get('branchName')
        branch_address = request.POST.get('branchAddress')
        branch_pincode = request.POST.get('branchPincode')
        branch_capacity = request.POST.get('branchCapacity')
        branch_state = request.POST.get('branchState')
        branch_id = request.POST.get('branchid')
        branch_manager = request.POST.get('branchManager')
        branch_phone_number = request.POST.get('branchPhoneNumber')
        branch_email = request.POST.get('email')
        branch_password = request.POST.get('password')
        opening_date_str = request.POST.get('branchOpeningDate')
        picture = request.FILES.get('profile_picture')
        print(branch_name,branch_address,branch_password,branch_id,branch_email)

        opening_date = datetime.strptime(opening_date_str, '%Y-%m-%d').date() if opening_date_str else None

        branch = Branch.objects.create(
            name=branch_name,
            address=branch_address,
            pincode=branch_pincode,
            capacity=branch_capacity,
            state=branch_state,
            branchstaticid=branch_id,
            manager=branch_manager,
            phone_number=branch_phone_number,
            email=branch_email,
            password=branch_password,
            opening_date=opening_date,
            profile_picture= picture if picture else None
        )

        wallet = Wallet.objects.create(branch=branch, amount=0)

        subject = 'Your account details for SOFT Dev Tally LMS'
        message = f'Your Dashboard has been created. Email: {branch_email}, Password: {branch_password}'
        sender_email = 'akshatasthana73@gmail.com'  
        send_mail(subject, message, sender_email, [branch_email])

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def student_profile(request, user_id):
    try:
        student = Student.objects.get(user_id=user_id)
        return render(request, 'app/studentprofile.html', {'student': student,'user_id': user_id})
    except Student.DoesNotExist:
        return render(request, 'error_page.html', {'message': 'Student profile not found'})
    
def teacher_profile(request, user_id):
    try:
        teacher = Teacher.objects.get(id=user_id)
        return render(request, 'app/teacherprofile.html', {'teacher': teacher})
    except Teacher.DoesNotExist:
        # Handle the case where the student profile does not exist
        return render(request, 'error_page.html', {'message': 'Teacher profile not found'})

# @csrf_exempt
# def save_marks(request):
#     if request.method == 'POST':
#         try:
#             branch_id = request.POST.get('branch')
#             batch_id = request.POST.get('batch')
#             student_id = request.POST.get('studentId')
#             course_id = request.POST.get('course')
#             theory_marks_obtained = request.POST.getlist('theory_marks_obtained[]')
#             practical_marks_obtained = request.POST.getlist('practical_marks_obtained[]')
#             subject_ids = request.POST.getlist('subject[]')

#             theory_max_marks = request.POST.getlist('theory_max_marks[]')
#             practical_max_marks = request.POST.getlist('practical_max_marks[]')
#             print(branch_id,batch_id,student_id,course_id,theory_marks_obtained,practical_marks_obtained,theory_max_marks,practical_max_marks)

#             for subject_id, theory_marks, practical_marks, theory_max, practical_max in zip (
#                     subject_ids, theory_marks_obtained, practical_marks_obtained, theory_max_marks, practical_max_marks):
                
#                 # print(branch_id,batch_id,student_id,course_id,theory_marks,practical_marks,theory_max,practical_max)
#                 marks = Marks(
#                     branch_id=branch_id,
#                     batch_id=batch_id,
#                     student_id=student_id,
#                     course_id=course_id,
#                     subject_id=subject_id,
#                     theory_marks_obtained=theory_marks,
#                     practical_marks_obtained=practical_marks,
#                     theory_max_marks=theory_max,
#                     practical_max_marks=practical_max
#                 )
#                 marks.save()

#             return JsonResponse({'message': 'Marks saved successfully'})
#         except Exception as e:
#             print(e)
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)

def save_marks(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            branchid = data[0]["branchid"]
            batchid = data[0]["batchid"]
            studentid  =data[0]["studentid"]
            student  = Student.objects.filter(Studentid=studentid)[0]
            print(student.id)
            studentID = student.id
            course  = data[0]["course"]
            marks = data[0]["marks"]

            for i in marks:
                subject = i[0]
                theorymarksobtained = i[1]
                theorymaxmarks = i[2]
                practicalmarksobtained = i[3]
                practicalmaxmarks = i[4] 
                subject_id = i[5]
                marksdata,created = Marks.objects.update_or_create(
                    branch_id=branchid,
                    batch_id=batchid,
                    student_id=studentID,
                    course_id=course,
                    subject_id=subject_id,
                    theory_marks_obtained=theorymarksobtained,
                    practical_marks_obtained=practicalmarksobtained,
                    theory_max_marks=theorymaxmarks,
                    practical_max_marks=practicalmaxmarks
                )
                marksdata.save()
            return JsonResponse({'messa':"Marks saved Successfully"},status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Branch ID not provided'}, status=400)



def save_student_profile(request, user_id):
    if request.method == 'POST':
        try:
            student = Student.objects.get(user_id=user_id)
            student.name = request.POST.get('name')
            student.full_name = request.POST.get('full_name')
            student.dob = request.POST.get('dob')
            student.email = request.POST.get('email')
            student.permanent_address = request.POST.get('permanent_address')
            student.course_name = request.POST.get('course_name')
            student.save()
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def save_teacher_profile(request, user_id):

    teacher = get_object_or_404(Teacher, user__id=user_id)

    if request.method == 'POST':
        teacher.name = request.POST.get('name')
        teacher.email = request.POST.get('email')
        teacher.phone_number = request.POST.get('phone_number')
        teacher.qualification = request.POST.get('qualification')
        teacher.experience = request.POST.get('experience')

        teacher.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    else:

        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
def create_batch(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        branch_id = request.POST.get('branch')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        branch = Branch.objects.get(pk=branch_id)
        batch = Batch.objects.create(name=name, branch=branch, start_time=start_time, end_time=end_time)
        response_data = {'success': True, 'message': 'Batch created successfully'}
        return JsonResponse(response_data)
    else:
        response_data = {'success': False, 'message': 'Invalid request method'}
        return JsonResponse(response_data, status=400)
    
def branchlist(request):
    batches = Batch.objects.all()
    return render(request, 'app/teacherdashboard.html', {'batches': batches})

def batchlist(request, batch_id):
    students = Student.objects.filter(batches__id=batch_id)
    
    return render(request, 'app/batchlist.html', {'students': students})


def teacher_dashboard(request,user_id):
    teacher = Teacher.objects.get(id=user_id)  
    branch = teacher.branch
    print(branch)

    students = Student.objects.filter(branch=branch)
    print(students)

    batches = Batch.objects.filter(branch=branch)
    print(batches)

    # context = {
    #     'teacher': teacher,
    #     'students': students,
    #     'batches': batches,
    # }
    return render(request, 'app/batchlist.html', {'teacher': teacher,'students': students,'batches': batches})


def assign_batch(request, student_id, batch_id):
    # Get the student object based on the provided student_id
    student = get_object_or_404(Student, id=student_id)
    
    # Get the batch object based on the provided batch_id
    batch = get_object_or_404(Batch, id=batch_id)
    
    # Get the teacher object based on the provided user_id
    
    # Check if the student's branch matches the teacher's branch
        # Check if the batch belongs to the same branch as the teacher's branch
            # Assign the batch to the student
    student.batches.add(batch)
            # Return a JSON response indicating successful assignment
    return JsonResponse({'message': 'Batch assigned successfully'})


def student_batch_list(request, user_id):
    # Get the teacher object based on the provided user_id
    teacher = get_object_or_404(Teacher, id=user_id)

    # Get the branch associated with the teacher
    branch = teacher.branch

    # Get all batches belonging to the branch
    batches = Batch.objects.filter(branch=branch)

    # Get all students belonging to the branch
    students = Student.objects.filter(branch=branch)

    # Pass the teacher, batches, and students to the template
    return render(request, 'app/teacherdashboard.html', {'teacher': teacher, 'batches': batches, 'students': students})

def get_month_days():
    today = datetime.today()
    return calendar.monthrange(today.year, today.month)[1]

def allocate_batch_to_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        batch_id = request.POST.get('batch_id')
        print(teacher_id)
        print(batch_id)
        if batch_id:
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            batch = get_object_or_404(Batch, pk=batch_id)
            print(teacher,batch)

            teacher.batches.add(batch)
            
            return HttpResponse("Batch allocated successfully.")
        else:
            return HttpResponse("Please select a batch.")
    else:
        return HttpResponse("Invalid request method.")

def add_subject_to_course(request):
    if request.method == "POST":
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)
        
        subject_names = request.POST.getlist('subject_name[]')
        theory_marks_obtained = request.POST.getlist('theory_marks_obtained[]')
        theory_max_marks = request.POST.getlist('theory_max_marks[]')
        practical_marks_obtained = request.POST.getlist('practical_marks_obtained[]')
        practical_max_marks = request.POST.getlist('practical_max_marks[]')
        
        for i in range(len(subject_names)):
            subject_name = subject_names[i]
            theory_obtained = theory_marks_obtained[i]
            theory_max = theory_max_marks[i]
            practical_obtained = practical_marks_obtained[i]
            practical_max = practical_max_marks[i]
            
            subject = Subject.objects.create(
                name=subject_name,
                theory_marks_obtained=theory_obtained,
                theory_max_marks=theory_max,
                practical_marks_obtained=practical_obtained,
                practical_max_marks=practical_max
            )
            subject.save()
            
            course.subjects.add(subject)
        
        return redirect('add_subject_to_course')  
    
    courses = Course.objects.all()  
    return render(request, 'app/createsubject.html', {'courses': courses})

def entermarks(request):
    branches = Branch.objects.all()
    return render(request, 'app/entermarks.html', {"branches":branches})



def add_teacher(request):
    if request.method == 'POST':
        teacher_name = request.POST.get('teacherName')
        teacher_location = request.POST.get('teacherLocation')
        branch = request.POST.get('branchId')
        email = request.POST.get('email')
        password = request.POST.get('password')
        teacher_manager_id = request.POST.get('teacherManager')
        teacher_salary = request.POST.get('teacherSalary')
        opening_date_str = request.POST.get('teacherjoiningdate')

        joiningdate = datetime.strptime(opening_date_str, '%Y-%m-%d').date() if opening_date_str else None

        print(joiningdate)

        teacher = Teacher.objects.create(
            name=teacher_name,
            location=teacher_location,
            email=email,
            password=password,
            salary=teacher_salary,
            joining_date = joiningdate,
            branch = branch

        )

        subject = 'Your account details for SOFT DEV TALLY LMS'
        message = f'Your Dashboard has been created. Email: {email}, Password: {password}'
        sender_email = 'akshatasthana73@gmail.com'
        send_mail(subject, message, sender_email, [email])

        return redirect('branchtables')
    else:
        return render(request, 'app/branchtables.html')


def add_teacher_admin(request):
    if request.method == 'POST':
        teacher_name = request.POST.get('teacherName')
        teacher_location = request.POST.get('teacherLocation')
        branch = request.POST.get('branch')
        print(branch)
        email = request.POST.get('email')
        password = request.POST.get('password')
        phonenumber  = request.POST.get('mobilenumber')
        # teacher_manager_id = request.POST.get('teacherManager')
        teacher_salary = request.POST.get('teacherSalary')
        opening_date_str = request.POST.get('teacherOpeningDate')
        print(opening_date_str)

        joiningdate = datetime.strptime(opening_date_str, '%Y-%m-%d').date() if opening_date_str else None

        branch_data = get_object_or_404(Branch, id = branch)

        print(joiningdate)

        teacher = Teacher.objects.create(
            name=teacher_name,
            location=teacher_location,
            phone_number = phonenumber,
            email=email,
            password=password,
            salary=teacher_salary,
            joining_date = joiningdate,
            branch = branch_data

        )

        subject = 'Your account details for SOFT DEV TALLY LMS'
        message = f'Your Dashboard has been created. Email: {email}, Password: {password}'
        sender_email = 'akshatasthana73@gmail.com'
        send_mail(subject, message, sender_email, [email])

        return redirect('adminteachers')
    else:
        return render(request, 'app/adminteachers.html')

def addteacher(request,branch_id):
    if request.method == 'POST':
        teacher_name = request.POST.get('teacherName')
        teacher_location = request.POST.get('teacherLocation')
        branch = request.POST.get('branchId')
        print(branch)
        email = request.POST.get('email')
        password = request.POST.get('password')
        phonenumber  = request.POST.get('mobilenumber')
        # teacher_manager_id = request.POST.get('teacherManager')
        teacher_salary = request.POST.get('teacherSalary')
        opening_date_str = request.POST.get('teacherOpeningDate')
        print(opening_date_str)

        joiningdate = datetime.strptime(opening_date_str, '%Y-%m-%d').date() if opening_date_str else None

        branch_data = get_object_or_404(Branch, id = branch)

        print(joiningdate)

        teacher = Teacher.objects.create(
            name=teacher_name,
            location=teacher_location,
            phone_number = phonenumber,
            email=email,
            password=password,
            salary=teacher_salary,
            joining_date = joiningdate,
            branch = branch_data

        )

        subject = 'Your account details for SOFT DEV TALLY LMS'
        message = f'Your Dashboard has been created. Email: {email}, Password: {password}'
        sender_email = 'akshatasthana73@gmail.com'
        send_mail(subject, message, sender_email, [email])
        return redirect('branchdashboard',branch_id = branch_id)
    else:
        return render(request, 'app/login.html')



def payment_approval(request):
    if request.method == "POST":
        try:
            payment_amount = json.loads(request.body)['payment_amount']
            payment_data = request.session.get('payment_data') 

            print(payment_amount)
            print(payment_data)


            if payment_data:
                user_id = payment_data.get('user_id')
                email = payment_data.get('email')
                course_data = payment_data.get('course_data', {})
                course_name = course_data.get('name')
                course_price = payment_data.get('course_price')
                course_duration = payment_data.get('course_duration')
                course_id = payment_data.get('course_id')
                branch_id = payment_data.get('branch_id')   
                print(course_data['id'])           

                paymentobject = PaymentRequest.objects.create(
                    user_id=user_id,  
                    price=course_price,                                         
                    course_id=course_data['id'],
                    payment_amount=payment_amount,
                    branch_id=branch_id,
                    email=email
                )
                
                request.session.clear()
                return JsonResponse({"message": "Payment request saved successfully."})            
            else:
                return HttpResponse("Payment data not found. Please complete registration first.")
        except Exception as e:
            return JsonResponse({"error": str(e)})






def approve_payment(request, payment_request_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        roll_number = data['roll_number']
        enrollment_number = data['enrollment_number']

        payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)
        branch = payment_request.branch_id
        payment_request.approved = True
        payment_request.save()

        user_id = payment_request.user_id
        course_id = payment_request.course_id

        user = get_object_or_404(User, id=user_id)
        student, created = Student.objects.get_or_create(user=user)

        # Update roll number and enrollment number
        student.roll_number = roll_number
        student.enrollment_number = enrollment_number
        student.save()

        try:
            with transaction.atomic():
                fees, created = Fees.objects.get_or_create(user_id=user_id)
                if created:
                    fees.amount = 0

                fees.amount = payment_request.price - payment_request.payment_amount
                fees.course_id = course_id
                fees.save()

                branch_wallet = Wallet.objects.select_for_update().get(branch_id=branch)
                signup_amount = branch_wallet.signup_request

                if branch_wallet.amount < signup_amount:
                    raise ValueError("Insufficient balance in the wallet.")

                branch_wallet.amount -= signup_amount
                branch_wallet.save()

                branch_object = Branch.objects.get(id=branch)

                Transaction.objects.create(
                    wallet_id=branch_wallet.id,
                    amount=signup_amount,
                    transaction_type='Debit',
                    branchstaticid=branch_object.branchstaticid,
                    timestamp=timezone.now()
                )
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

        # Store the data in the session
        request.session['payment_request_id'] = payment_request.id
        request.session['user_id'] = user.id
        request.session['student_id'] = student.id

        return JsonResponse({
            'success': True,
            'redirect_url': reverse('registration_receipt')
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def registration_receipt(request):
    payment_request_id = request.session.get('payment_request_id')
    user_id = request.session.get('user_id')
    student_id = request.session.get('student_id')

    if payment_request_id and user_id and student_id:
        payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)
        user = get_object_or_404(User, id=user_id)
        student = get_object_or_404(Student, id=student_id)

        context = {
            'payment_request': payment_request,
            'user': user,
            'student': student,
        }
        return render(request, 'app/registrationreceipt.html', context)

    return JsonResponse({'success': False, 'error': 'Missing data in session'})
    # Redirect or respond with an error if not a POST request

def reject_payment(request, payment_request_id):
    payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)
    payment_request.status = 'rejected'
    payment_request.save()
    return redirect('branch_panel')

def fetch_branches(request):
    branches = Branch.objects.all()
    branches_data = serialize('json', branches)
    return render(request,'app/createmarksheet.html',{'branches': branches_data})

def fetch_batches(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Parse the JSON data from the request body
        try:
            data = json.loads(request.body.decode('utf-8'))
            branch_id = data.get('branch_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Branch ID not provided'}, status=400)

        if branch_id is not None:
            batches = Batch.objects.filter(branch_id=branch_id)
            batches_data = [{'id': batch.id, 'name': batch.name} for batch in batches]
            return JsonResponse({'batches': batches_data})
        else:
            return JsonResponse({'error': 'Branch ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# def fetch_students(request):
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#         batch_id = data.get('batch_id')

#         if batch_id is None:
#             return JsonResponse({'error': 'Batch ID not provided'}, status=400)

#         # batch = get_object_or_404(Batch,id=batch_id)
#         # print(batch)
#         # student = batch.all()
#         batch = Batch.objects.get(id=batch_id)
#         students = batch.student.all()
#         # students = Student.batches.all()
#         print(students)

#         students_data = [{'id': student.id, 'name': student.name} for student in students]

#         return JsonResponse({'students': students_data}, status=200)

#     except Batch.DoesNotExist:
#         return JsonResponse({'error': 'Batch does not exist'}, status=404)

#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    

def fetch_students_attendance(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        batch_id = data.get('batch_id')

        if batch_id is None:
            return JsonResponse({'error': 'Batch ID not provided'}, status=400)

        # batch = get_object_or_404(Batch,id=batch_id)
        # print(batch)
        # student = batch.all()
        batch = Batch.objects.get(id=batch_id)
        students = batch.student.all()
        attendences = Attendance.objects.filter(batch_id = batch_id)
        # students = Student.batches.all()
        print(students)

        students_data = [{'id': student.id, 'name': student.name} for student in students]
        attendance_data = [{'batch_id':attendance.batch_id,'student_id':attendance.student.id,'student_name':attendance.student.name,'date':attendance.date,'status':attendance.status} for attendance in attendences]

        return JsonResponse({'students': students_data,'attendance':attendance_data}, status=200)

    except Batch.DoesNotExist:
        return JsonResponse({'error': 'Batch does not exist'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)



def fetch_courses(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id')

        if student_id is None:
            return JsonResponse({'error': 'Student ID not provided'}, status=400)
        else:
            student = Student.objects.get(Studentid=student_id)
            print(student)
            course=student.course
            print(course)
            # courseID=[]
            # for st in student:
            #     courseID.append(st.course)
            print(course)
            course_data=[{"id":course.id,"name":course.name}]
            return JsonResponse({'courses': course_data}, status=200)
    except Course.DoesNotExist:
         return JsonResponse({'error': 'Batch does not exist'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            

# def fetch_courses(request):
#     student_id = request.GET.get('student_id')
#     courses = Course.objects.filter(student_id=student_id)
#     return JsonResponse({'courses': courses})
@csrf_exempt
def fetch_subjects_max_marks(request, course_id):
    if request.method == 'GET':
        try:
            subjects = Subject.objects.filter(course=course_id)
            subjects
            subjects_data = [{'id':subject.id,'name': subject.name, 'theory_max_marks': subject.theory_max_marks, 'practical_max_marks': subject.practical_max_marks} for subject in subjects]
            print(subjects_data)
            return JsonResponse({'subjects': subjects_data})
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Subjects not found'}, status=404)

def fetch_marks(request):
    course_id = request.GET.get('course_id')
    print(course_id)
    subjects = Course.objects.get(id=course_id).subjects.all()
    students = Student.objects.filter(course_id=course_id)
    marks_data = []
    for student in students:
        marks = [Marks.objects.get(student=student, subject=subject).marks for subject in subjects]
        marks_data.append({'student_id': student.id, 'marks': marks})
    return JsonResponse({'subjects': [{'id': subject.id, 'name': subject.name} for subject in subjects],
                         'students': marks_data})


def fetch_student_details(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        try:
            student = Student.objects.get(pk=student_id)
            serializer = StudentSerializer(student)  # Assuming you have a serializer defined
            return JsonResponse(serializer.data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def post_attendance(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        try:
            data = json.loads(request.body.decode('utf-8'))
            batch_id = data[0]["Batchid"]
            print(batch_id)
            date = data[0]["Date"]
            print(date)
            

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Branch ID not provided'}, status=400)

        if batch_id is not None:
            for i in data[1]["Attendance"]:
                student=Student.objects.get(id=i["Student_id"])
                if i["Present"]==True:
                    status="present"
                else:
                    status="absent"
                print(student)
                attendance=Attendance.objects.create(student=student,date=date,status=status,batch_id=batch_id)
                attendance.save()
            return JsonResponse({'batch_id': batch_id})
        else:
            return JsonResponse({'error': 'Batch ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def fetch_student_courses(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            student_id = data.get('student_id')

            if student_id is None:
                return JsonResponse({'error': 'Student ID not provided'}, status=400)

            student = Student.objects.get(Studentid=student_id)
            course = student.course  # Assuming student.course returns a single Course object
            
            # Construct a dictionary from the Course object
            course_data = {'id': course.id, 'name': course.name}  # Add more fields as needed

            return JsonResponse({'course_data': course_data})

        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def filter_courses(request):
    branch_id = request.GET.get('branch_id')
    course_type = request.GET.get('course_type')

    if branch_id and course_type:
        # Filter courses based on the selected branch ID and course type
        filtered_courses = Course.objects.filter(branch_id=branch_id, course_type=course_type)
        # Serialize the filtered courses
        serialized_courses = [{'id': course.id, 'name': course.name} for course in filtered_courses]
        return JsonResponse({'courses': serialized_courses}, status=200)
    elif course_type:
        # If only course type is provided, filter courses based on the course type
        filtered_courses = Course.objects.filter(course_type=course_type)
        # Serialize the filtered courses
        serialized_courses = [{'id': course.id, 'name': course.name} for course in filtered_courses]
        return JsonResponse({'courses': serialized_courses}, status=200)
    elif branch_id:
        # If only branch ID is provided, filter courses based on the branch ID
        filtered_courses = Course.objects.filter(branch_id=branch_id)
        # Serialize the filtered courses
        serialized_courses = [{'id': course.id, 'name': course.name} for course in filtered_courses]
        return JsonResponse({'courses': serialized_courses}, status=200)
    else:
        # If neither branch ID nor course type is provided, return all courses
        all_courses = Course.objects.all()
        serialized_courses = [{'id': course.id, 'name': course.name} for course in all_courses]
        return JsonResponse({'courses': serialized_courses}, status=200)


def addmoney(request):
    return render(request,"app/wallet.html")


def oldmarksheet(request):
    branches = Branch.objects.all()
    return render(request,"app/oldmarksheet.html",{'branches':branches})



@transaction.atomic
def addmoneytowallet(request):
    if request.method == 'POST':
        try:
            data = request.POST  
            branch_static_id = data.get('branch_id')
            cash = int(data.get('amount'))

            branch = Branch.objects.get(branchstaticid=branch_static_id)

            try:
                wallet_entry = branch.wallet
            except ObjectDoesNotExist:
                wallet_entry = None

            if wallet_entry is None:
                wallet_entry = Wallet.objects.create(branch=branch, amount=cash)
            elif wallet_entry.amount is None:
                wallet_entry.amount = 0

            wallet_entry.amount += cash
            wallet_entry.save()

            Transaction.objects.create(
                wallet=wallet_entry,
                amount=cash,
                transaction_type='credit',
                branchstaticid=branch_static_id
            )

            return JsonResponse({'success': True, 'message': 'Amount added to wallet successfully'})
        except (ValueError, Branch.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Invalid branch static ID or amount'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet does not exist for the branch'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def studentmarkstable(request):
    return render(request, 'app/studentmarkstable.html')

def changecosting(request):
    wallet  =  Wallet.objects.all()
    return render(request, 'app/changecosting.html',{'wallet':wallet})

@csrf_exempt
def update_branch(request):
    if request.method == "POST":
        try:
            branch_static_id = request.POST.get("BranchStaticid")
            signup_request = request.POST.get("signup_request")
            marksheet_amount = request.POST.get("marksheet_amount")

            branch = get_object_or_404(Branch, branchstaticid=branch_static_id)

            wallet = get_object_or_404(Wallet,branch = branch)

            if signup_request:
                wallet.signup_request = signup_request
            if marksheet_amount:
                wallet.marksheet_amount = marksheet_amount

            wallet.save()

            return JsonResponse({"message": "Branch updated successfully."})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Only POST requests are allowed."})


def printoldmarksheet(request):
    if request.method == 'GET':
        # Retrieve data from GET parameters
        student_name = request.GET.get('student_name')
        father_name = request.GET.get('father_name')
        mother_name = request.GET.get('mother_name')
        dob = request.GET.get('dob')
        mobile_number = request.GET.get('mobile_number')
        address = request.GET.get('address')
        branch = request.GET.get('branch')
        state = request.GET.get('state')
        pincode = request.GET.get('pincode')
        enrollment_no = request.GET.get('enrollment_no')
        session = request.GET.get('session')
        registration_date = request.GET.get('registration_date')
        course_name = request.GET.get('course')
        profile_picture = request.GET.get('profile_picture')
        serial_number = request.GET.get('serial_number')
        roll_number = request.GET.get('roll_number')

        # Find course in OldCourse table using course_name
        try:
            branchdata = Branch.objects.get(pk=branch)
            branch_code = branchdata.branchstaticid
            branch_name = branchdata.name
            branch_address = branchdata.address
            branch_state = branchdata.state
            branch_pincode = branchdata.pincode
        except Branch.DoesNotExist:
            return JsonResponse({'error': 'Branch with ID {} does not exist'.format(branch)}, status=400)

        try:
            old_course = OldCourse.objects.get(id=course_name)
        except OldCourse.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)

        try:
            old_marksheet = OldMarksheet.objects.get(enrollment_no=enrollment_no)
        except OldMarksheet.DoesNotExist:
            return JsonResponse({'error': 'Old Mark Sheet not found for the enrollment number'}, status=404)

        # Retrieve subjects associated with the marksheet
        old_subjects = OldSubject.objects.filter(student_id=old_marksheet.id)

        # Calculate total obtained marks and max marks for theory and practical
        total_obtained_theory = 0
        total_max_theory = 0
        total_obtained_practical = 0
        total_max_practical = 0

        subject_details = []

        for subject in old_subjects:
            obtained_total = subject.theory_marks + (subject.practical_marks or 0)
            max_total = subject.theory_max_marks + (subject.practical_max_marks or 0)

            subject_details.append({
                'subject_name': subject.subject_name,
                'theory_marks': subject.theory_marks,
                'theory_max_marks': subject.theory_max_marks,
                'practical_marks': subject.practical_marks,
                'practical_max_marks': subject.practical_max_marks,
                'obtained_total': obtained_total,
                'max_total': max_total
            })

            total_obtained_theory += subject.theory_marks
            total_max_theory += subject.theory_max_marks
            total_obtained_practical += subject.practical_marks
            total_max_practical += subject.practical_max_marks

        # Calculate grand total
        grand_total = total_obtained_theory + total_obtained_practical
        print(grand_total)
        grand_sum = total_max_theory + total_max_practical
        print(grand_sum)

        if total_max_theory > 0:
            percentage_theory = (total_obtained_theory / total_max_theory) * 100
        else:
            percentage_theory = 0

        if total_max_practical > 0:
            percentage_practical = (total_obtained_practical / total_max_practical) * 100
        else:
            percentage_practical = 0

        total_percentage = ((total_obtained_theory + total_obtained_practical) / (total_max_theory + total_max_practical)) * 100

        # Determine grade and division based on percentage
        if total_percentage >= 75:
            grade = 'A+'
            division = 'First Division with Distinction'
        elif total_percentage >= 70:
            grade = 'A'
            division = 'First Division'
        elif total_percentage >= 60:
            grade = 'B'
            division = 'Second Division'
        elif total_percentage >= 50:
            grade = 'C'
            division = 'Pass'
        elif total_percentage >= 40:
            grade = 'D'
            division = 'Pass'
        else:
            grade = 'F'
            division = 'Fail'

        # Prepare certificate data
        certificate_data = {
            'student_name': student_name,
            'father_name': father_name,
            'mother_name': mother_name,
            'dob': dob,
            'mobile_number': mobile_number,
            'address': address,
            'branch_address': branch_address,
            'state': state,
            'pincode': pincode,
            'enrollment_no': enrollment_no,
            'session': session,
            'registration_date': registration_date,
            'course_name': course_name,
            'branch_code': branch_code,
            'course': old_course,
            'old_subjects': subject_details,
            'branch_name': branch_name,
            'profile_picture': profile_picture,
            'serial_number': serial_number,
            'roll_number': roll_number,
            'total_obtained_theory': total_obtained_theory,
            'total_max_theory': total_max_theory,
            'total_obtained_practical': total_obtained_practical,
            'total_max_practical': total_max_practical,
            'percentage_theory': percentage_theory,
            'percentage_practical': percentage_practical,
            'total_percentage': total_percentage,
            'grand_total': grand_total,
            'grade': grade,
            'division': division,
            'grand_sum': grand_sum
        }

        return render(request, 'app/printoldmarksheet.html', {'certificate_data': certificate_data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


def printoldceetificate (request):
    if request.method == 'GET':
        student_name = request.GET.get('student_name')
        father_name = request.GET.get('father_name')
        mother_name = request.GET.get('mother_name')
        dob = request.GET.get('dob')
        mobile_number = request.GET.get('mobile_number')
        address = request.GET.get('address')
        branch = request.GET.get('branch')
        state = request.GET.get('state')
        pincode = request.GET.get('pincode')
        enrollment_no = request.GET.get('enrollment_no')
        session = request.GET.get('session')
        registration_date = request.GET.get('registration_date')
        course_name = request.GET.get('course')
        profile_picture = request.GET.get('profile_picture')
        serial_number = request.GET.get('serial_number')
        roll_number = request.GET.get('roll_number')

        # Find course in OldCourse table using course_name
        try:
            branchdata = Branch.objects.get(pk=branch)
            branch_code  =branchdata.branchstaticid
            branch_name = branchdata.name
            branch_address = branchdata.address
            branch_state = branchdata.state
            branch_pincode = branchdata.pincode
        except Branch.DoesNotExist:
            return JsonResponse({'error': 'Branch with ID {} does not exist'}, status=400)
        try:
            old_course = OldCourse.objects.get(id=course_name)
        except OldCourse.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        
        try:
            old_marksheet = OldMarksheet.objects.get(enrollment_no=enrollment_no)
        except OldMarksheet.DoesNotExist:
            return JsonResponse({'error': 'Old Mark Sheet not found for the enrollment number'}, status=404)
        

       # Retrieve subjects associated with the marksheet
        old_subjects = OldSubject.objects.filter(student_id=old_marksheet.id)

        total_obtained_theory = 0
        total_max_theory = 0
        total_obtained_practical = 0
        total_max_practical = 0

        for subject in old_subjects:
            total_obtained_theory += subject.theory_marks
            total_max_theory += subject.theory_max_marks
            total_obtained_practical += subject.practical_marks
            total_max_practical += subject.practical_max_marks

        # Calculate grand total
        grand_total = total_obtained_theory + total_obtained_practical
        print(grand_total)

        # Calculate percentage for theory and practical
        if total_max_theory > 0:
            percentage_theory = (total_obtained_theory / total_max_theory) * 100
        else:
            percentage_theory = 0

        if total_max_practical > 0:
            percentage_practical = (total_obtained_practical / total_max_practical) * 100
        else:
            percentage_practical = 0

        # Calculate overall percentage
        total_percentage = ((total_obtained_theory + total_obtained_practical) / (total_max_theory + total_max_practical)) * 100
        print(total_percentage)

        # Determine grade and division based on percentage
        if total_percentage >= 61:
            division = 'First'
        elif total_percentage >= 51:
            division = 'Second'
        elif total_percentage >= 40:
            division = 'Third'
        elif total_percentage >= 0:
            division = 'Fail'
        
        if total_percentage >= 75:
            grade = 'A+'
        elif total_percentage >= 70:
            grade = 'A'
        elif total_percentage >= 60:
            grade = 'B'
        elif total_percentage >= 50:
            grade = 'C'
        elif total_percentage >= 40:
            grade = 'D'
        else:
            grade = 'F'


        # Prepare certificate data
        certificate_data = {
            'student_name': student_name,
            'father_name': father_name,
            'mother_name': mother_name,
            'dob': dob,
            'mobile_number': mobile_number,
            'address': address,
            'branch_address': branch_address,
            'state': branch_state,
            'pincode': branch_pincode,
            'enrollment_no': enrollment_no,
            'session': session,
            'registration_date': registration_date,
            'course_name': course_name,
            'branch_code': branch_code,
            'course': old_course,
            'old_subjects':old_subjects,
            'profile_picture':studentimage(enrollment_no),
            'serial_number':serial_number,
            'roll_number':roll_number,
            'branch_name':branch_name,
            'grand_total': grand_total,
            'grade': grade,
            'division': division,
        }
        # studentimage(enrollment_no)
        return render(request, 'app/printoldcertificate.html', {'certificate_data': certificate_data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    

def studentimage(enrollment_no):
    marksheet = OldMarksheet.objects.filter(enrollment_no=enrollment_no)
    serialized_data = serialize('json', marksheet)
    data = json.loads(serialized_data)
    return data[0]["fields"]["profile_picture"]

def oldcoursecreation (request):
    course = OldCourse.objects.all()
    return render (request, 'app/oldcoursecreation.html',{'course':course})

def oldsubjectcreation (request):
    Subject = OldSubject.objects.all()
    return render (request, 'app/oldsubjectcreation.html',{'subject':Subject})

def old_create_course(request):
    if request.method == 'POST':
        try:
            coursetype = request.POST.get('course_type')
            name = request.POST.get('name')
            duration = request.POST.get('duration')
            price = request.POST.get('price')

            course = OldCourse.objects.create(
                category=coursetype,
                name=name,
                duration=duration,
                price=price
            )

            return JsonResponse({'success': True, 'message': 'Course created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def fetch_old_subjects(request):
    if request.method == 'POST':
        course_type = request.POST.get('course_type')

        if course_type:
            subjects = OldCourse.objects.filter(category=course_type).values('id', 'name')
            return JsonResponse(list(subjects), safe=False)
        else:
            return JsonResponse({'error': 'Course type not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def add_old_subjects(request):
    if request.method == 'POST':
        course_ids = request.POST.get('course')
        subject_names = request.POST.getlist('subject_name[]')
        theory_marks_obtained = request.POST.getlist('theory_marks_obtained[]')
        theory_max_marks = request.POST.getlist('theory_max_marks[]')
        practical_marks_obtained = request.POST.getlist('practical_marks_obtained[]')
        practical_max_marks = request.POST.getlist('practical_max_marks[]')

        print(course_ids)

        if course_ids and subject_names:  # Checking if both course IDs and subject names are provided
            try:
                for i in range(len(subject_names)):
                    # Extracting subject details for each index
                    subject_name = subject_names[i]
                    theory_obtained = theory_marks_obtained[i]
                    theory_max = theory_max_marks[i]
                    practical_obtained = practical_marks_obtained[i]
                    practical_max = practical_max_marks[i]

                    # Creating the subject
                    subject = OldSubject.objects.create(
                        subject_name=subject_name,
                        theory_marks=theory_obtained,
                        theory_max_marks=theory_max,
                        practical_marks=practical_obtained,
                        practical_max_marks=practical_max,
                        course_id = course_ids
                    )

                    # Adding the subject to each course
                    # for course_id in course_ids:
                    #     try:
                    #         course = OldCourse.objects.get(pk=course_id)
                    #         subject.course.add(course)
                    #     except OldCourse.DoesNotExist:
                    #         subject.delete()
                    #         return JsonResponse({'error': f'Course with ID {course_id} does not exist'}, status=400)

                return JsonResponse({'message': 'Subjects created and added to courses successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing course IDs or subject names'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def fetch_subjects(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        print(course_id)

        if course_id:
            try:
                subjects = OldSubject.objects.filter(course_id=course_id, student__isnull=True).values()
                print(subjects)
                return JsonResponse(list(subjects), safe=False)
            except OldSubject.DoesNotExist:
                return JsonResponse({'error': 'No subjects found for the given course ID'}, status=404)
        else:
            return JsonResponse({'error': 'Course ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def submit_form(request):
    if request.method == 'POST':
        # Extract form data
        student_name = request.POST.get('student_name')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        dob = request.POST.get('dob')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        state = request.POST.get('state')
        branch = request.POST.get('branch')
        pincode = request.POST.get('pincode')
        enrollment_no = request.POST.get('enrollment_no')
        session = request.POST.get('session')
        registration_date = request.POST.get('registration_date')
        course_id = request.POST.get('course')
        profile_picture = request.FILES.get('profile_picture')  # Handle file upload
        serial_number = request.POST.get('serial_number')
        roll_number  = request.POST.get('roll_number')

        print(branch)

        try:
            branchdata = Branch.objects.get(id=branch)
            print(branchdata)
            branch_code  =branchdata.branchstaticid
            branch_name = branchdata.name
            branch_address = branchdata.address
            branch_state = branchdata.state
            print(branch_state)
            branch_pincode = branchdata.pincode
        except Branch.DoesNotExist:
            return JsonResponse({'error': 'Branch with ID {} does not exist'.format(course_id)}, status=400)
        try:
            course = OldCourse.objects.get(pk=course_id)
        except OldCourse.DoesNotExist:
            return JsonResponse({'error': 'Course with ID {} does not exist'.format(course_id)}, status=400)

        marksheet, created = OldMarksheet.objects.get_or_create(
            enrollment_no=enrollment_no,
            defaults={
                'branch_code': branch_code,
                'branch_name': branch_name,
                'student_name': student_name,
                'father_name': father_name,
                'mother_name': mother_name,
                'dob': dob,
                'mobile_number': mobile_number,
                'address': address,
                'branch_address': branch_address,
                'branch_state': branch_state,
                'pincode': branch_pincode,
                'enrollment_no': enrollment_no,
                'session': session,
                'registration_date': registration_date,
                'course': course,
                'profile_picture': profile_picture,
                'serial_number': serial_number,
                'roll_number': roll_number
            }
        )

        if not created:
            marksheet.branch_code = branch_code
            marksheet.branch_name = branch_name
            marksheet.student_name = student_name
            marksheet.father_name = father_name
            marksheet.mother_name = mother_name
            marksheet.dob = dob
            marksheet.mobile_number = mobile_number
            marksheet.address = address
            marksheet.branch_address = branch_address
            marksheet.branch_state = branch_state
            marksheet.pincode = branch_pincode
            marksheet.session = session
            marksheet.registration_date = registration_date
            marksheet.course = course
            marksheet.profile_picture = profile_picture
            marksheet.serial_number = serial_number
            marksheet.roll_number = roll_number
            marksheet.save()

        subjects_data_json = request.POST.get('subject_marks')
        subjects_data = json.loads(subjects_data_json)
        print(subjects_data)

        for subject_data in subjects_data:
            subject_name = subject_data.get('subject_name')

            subject, created = OldSubject.objects.get_or_create(
                course=course,
                subject_name=subject_name,
                student=marksheet,
            )

            subject.theory_marks = subject_data.get('theory_marks')
            subject.theory_max_marks = subject_data.get('theory_max_marks')
            subject.practical_marks = subject_data.get('practical_marks')
            subject.practical_max_marks = subject_data.get('practical_max_marks')
            subject.total_obtained_marks = subject_data.get('total_obtained_marks')
            subject.total_max_marks = subject_data.get('total_max_marks')
            subject.student = marksheet 

            subject.save()

        return JsonResponse({'message': 'Form submitted successfully', 'marksheet_id': marksheet.id})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405) 
    
def print_marksheet(request):
    if request.method == 'GET':
        student_name = request.GET.get('student_name')
        father_name = request.GET.get('father_name')
        mother_name = request.GET.get('mother_name')
        dob = request.GET.get('dob')
        mobile_number = request.GET.get('mobile_number')
        address = request.GET.get('address')
        branch_address = request.GET.get('branch_address')
        state = request.GET.get('state')
        pincode = request.GET.get('pincode')
        enrollment_no = request.GET.get('enrollment_no')
        session = request.GET.get('session')
        registration_date = request.GET.get('registration_date')
        course_name = request.GET.get('course_name')
        branch_name = request.GET.get('branch_name')
        profile_picture = request.GET.get('profile_picture')
        serial_number = request.GET.get('serial_number')
        roll_number = request.GET.get('roll_number')

        certificate_data = {
            'student_name': student_name,
            'father_name': father_name,
            'mother_name': mother_name,
            'dob': dob,
            'mobile_number': mobile_number,
            'address': address,
            'branch_address': branch_address,
            'state': state,
            'pincode': pincode,
            'enrollment_no': enrollment_no,
            'session': session,
            'registration_date': registration_date,
            'course_name': course_name,
            'branch_name': branch_name,
            'profile_picture': profile_picture,
            'serial_number': serial_number,
            'roll_number': roll_number,
        }

        return render(request, 'app/printoldmarksheet.html', {'certificate_data': certificate_data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

def branchadminprofile(request, branch_id):
    branch_admin = get_object_or_404(Branch, id=branch_id)

    return render(request, "app/branchadminprofile.html", {'branch_admin': branch_admin})

def update_profile(request, branch_id):
    if request.method == 'POST':
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return JsonResponse({'error': 'Branch not found'}, status=404)
        
        branch.name = request.POST.get('name', branch.name)
        branch.address = request.POST.get('address', branch.address)
        branch.manager = request.POST.get('manager', branch.manager)
        
        if 'profile_picture' in request.FILES:
            branch.profile_picture = request.FILES['profile_picture']
        
        branch.save()
        
        branch_data = {
            'id': branch.id,
            'name': branch.name,
            'address': branch.address,
            'manager': branch.manager,
            'profile_picture': branch.profile_picture.url if branch.profile_picture else None,
        }
        
        return JsonResponse({'message': 'Branch profile updated successfully', 'branch': branch_data})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def delete_branch(request):
    if request.method == 'POST':
        branch_id = request.POST.get('id')
        try:
            branches = Branch.objects.filter(branchstaticid=branch_id)
            if branches.exists():
                branches.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'No branches found with the given ID'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def edit_branch(request):
    if request.method == 'POST':
        branch_id = request.POST.get('branchId')
        branch_name = request.POST.get('branchName')
        branch_address = request.POST.get('branchAddress')
        branch_capacity = request.POST.get('branchCapacity')
        branch_manager = request.POST.get('branchManager')
        branch_pincode = request.POST.get('branchPincode')
        branch_state = request.POST.get('branchState')
        branch_number = request.POST.get('branchPhoneNumber')   
        picture = request.FILES.get('profile_picture')     
        
        try:
            branch = Branch.objects.get(branchstaticid=branch_id)
            branch.name = branch_name
            branch.address = branch_address
            branch.capacity = branch_capacity
            branch.manager = branch_manager
            branch.pincode = branch_pincode
            branch.state = branch_state
            branch.phone_number = branch_number
            branch.profile_picture = picture

            
            branch.save()
            return JsonResponse({'success': True})
        except Branch.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Branch does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def certificate_verify(request):
    return render (request,"app/certificateverification.html")

def marksheet_verify(request):
    return render (request,"app/marksheetverification.html")

def get_course_by_enrollment(request):
    try:
        data = json.loads(request.body)
        enrollment_no = data.get('enrollment_no')
        
        if not enrollment_no:
            return JsonResponse({'error': 'Enrollment number is required'}, status=400)

        try:
            marksheet = OldMarksheet.objects.get(enrollment_no=enrollment_no)
            course_name = marksheet.course.name  
            return JsonResponse({'course': course_name}, status=200)
        except OldMarksheet.DoesNotExist:
            return JsonResponse({'error': 'Enrollment number not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
@csrf_exempt
def get_old_marksheet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        enrollment_no = data.get('enrollment_no', None)
        if enrollment_no:
            try:
                old_marksheet = OldMarksheet.objects.get(enrollment_no=enrollment_no)
                subjectdata = OldSubject.objects.filter(student=old_marksheet.id)
                marks = []
                total_obtained_marks = 0
                total_max_marks = 0

                for sd in subjectdata:
                    marksdata = {
                        "subject_name": sd.subject_name,
                        "theory_marks": sd.theory_marks,
                        "max_theory_marks": sd.theory_max_marks,
                        "max_practical_marks": sd.practical_max_marks,
                        "practical_marks": sd.practical_marks
                    }
                    marks.append(marksdata)
                    total_obtained_marks += (sd.theory_marks + sd.practical_marks)
                    total_max_marks += (sd.theory_max_marks + sd.practical_max_marks)

                # Calculate percentage
                if total_max_marks > 0:
                    total_percentage = (total_obtained_marks / total_max_marks) * 100
                else:
                    total_percentage = 0

                # Determine grade
                if total_percentage >= 75:
                    grade = 'A+'
                elif total_percentage >= 70:
                    grade = 'A'
                elif total_percentage >= 60:
                    grade = 'B'
                elif total_percentage >= 50:
                    grade = 'C'
                elif total_percentage >= 40:
                    grade = 'D'
                else:
                    grade = 'F'

                # Format dates
                dob = old_marksheet.dob.strftime('%d/%m/%Y') if old_marksheet.dob else ''
                registration_date = old_marksheet.registration_date.strftime('%d/%m/%Y') if old_marksheet.registration_date else ''

                old_marksheet_data = {
                    'branch_code': old_marksheet.branch_code,
                    'branch_name': old_marksheet.branch_name,
                    'student_name': old_marksheet.student_name,
                    'father_name': old_marksheet.father_name,
                    'mother_name': old_marksheet.mother_name,
                    'dob': dob,
                    'mobile_number': old_marksheet.mobile_number,
                    'address': old_marksheet.address,
                    'branch_address': old_marksheet.branch_address,
                    'branch_state': old_marksheet.branch_state,
                    'pincode': old_marksheet.pincode,
                    'enrollment_no': old_marksheet.enrollment_no,
                    'session': old_marksheet.session,
                    'registration_date': registration_date,
                    'course_name': old_marksheet.course.name,
                    'profile_picture': old_marksheet.profile_picture.url if old_marksheet.profile_picture else None,
                    'serial_number': old_marksheet.serial_number,
                    'roll_number': old_marksheet.roll_number
                }

                old_marksheet_data = [old_marksheet_data]
                data = {
                    'old_marksheet': old_marksheet_data,
                    'subject_data': marks,
                    'total_obtained_marks': total_obtained_marks,
                    'total_max_marks': total_max_marks,
                    'total_percentage': total_percentage,
                    'grade': grade
                }
                return JsonResponse(data, status=200)
            except OldMarksheet.DoesNotExist:
                return JsonResponse({'error': 'Old marksheet not found'}, status=404)
        else:
            return JsonResponse({'error': 'Enrollment number not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

def marksheetrequestpanel(request, branch_id):
    branch =  branch_id
    print(branch)
    marksheet = MarksheetRequest.objects.all()
    return render(request, 'app/marksheetrequestpanel.html', {"branch":branch,'marksheet':marksheet})

@csrf_exempt
def marksheet_request_api(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the JSON
            enrollment_no = data.get('enrollment_no')
            issue_date = data.get('issue_date')
            branch_id = data.get('branchId')
            course_type = data.get('course_type')
            course_name = data.get('course_name')
            print(branch_id)
            # Validate data (add your validation logic here)

            student = Student.objects.get(Studentid = enrollment_no)
            user = student.user
            branch = Branch.objects.get(id = branch_id)
            course  = Course.objects.get(id = course_name)
            # marks = Marks.objects.get(student = student)

            request = MarksheetRequest.objects.create(
                student=student,
                issuedate=issue_date,
                branch=branch,
                user = user,
                Course = course
            )

            # Return success response
            return JsonResponse({'success': True, 'message': 'Marksheet request saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def marksheethistory(request):
    data=OldMarksheet.objects.all()
    return render(request,'app/marksheethistory.html',{'data':data})

@csrf_exempt
def save_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        file_path = default_storage.save('marksheets/' + pdf_file.name, ContentFile
        (pdf_file.read()))
        pdf_url = default_storage.url(file_path)
        return JsonResponse({'pdf_url': pdf_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_marksheet(request):
 if request.method == 'POST': 
     data = json.loads(request.body)
     pdf_url = data.get('pdf_url')
     if pdf_url:
         marksheet_id = data.get('marksheet_id')
         try:
          marksheet = OldMarksheet.objects.get(id=marksheet_id)
          marksheet.pdf_url = pdf_url
          marksheet.save()
          return JsonResponse({'message': 'Marksheet updated successfully'})
         except OldMarksheet.DoesNotExist:
             return JsonResponse({'error': 'Marksheet not found'}, status=404)
     return JsonResponse({'error': 'PDF URL not provided'}, status=400)
 return JsonResponse({'error': 'Invalid request'}, status=400)


def monthlyadmitcard(request,branch_id):
    context = {
        'branch_id': branch_id,
    }
    return render(request,'app/monthlyadmitcard.html',context)

def admitcardtemplate(request):
    return render(request,'app/admitcardtemplate.html')


def issuemonthlyadmitcard(request):
    return render(request,'app/issuemonthlyadmitcard.html')

def yearlyadmitcard(request,branch_id):
    context = {
        'branch_id': branch_id,
    }
    return render(request,'app/yearlyadmitcard.html',context)


def registrationreceipt(request):
    return render(request,'app/registrationreceipt.html')


def issueyearlyadmitcard(request):
    return render(request,'app/issueyearlyadmitcard.html')
    

@csrf_exempt
def save_pdf(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        pdf_file = request.FILES['pdf']
        
        if not studentid or not pdf_file:
            return JsonResponse({'success': False, 'error': 'Missing student ID or PDF file'})

        random_number = random.randint(10000, 99999)
        
        pdf_file.name = f'registration_receipt_{studentid}_{random_number}.pdf'
        save_path = os.path.join('registration_receipts', pdf_file.name)
        path = default_storage.save(os.path.join(settings.MEDIA_ROOT, save_path), pdf_file)

        try:
            student = Student.objects.get(Studentid=studentid)
            student.receipt_path = save_path  
            student.save()
            return JsonResponse({'success': True, 'file_path': path})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def generate_admit_card(request):
    if request.method == 'POST':
        session = request.POST.get('session')
        courses = request.POST.getlist('course[]')
        semesters = request.POST.getlist('semester[]')
        paper_names = request.POST.getlist('paperName[]')
        exam_dates = request.POST.getlist('examDate[]')
        start_times = request.POST.getlist('startTime[]')
        end_times = request.POST.getlist('endTime[]')
        total_hours_list = request.POST.getlist('totalHours[]')
        exam_centres = request.POST.getlist('examCentre[]')
        branch = request.POST.get('branchId')

        print(session,courses,semesters,paper_names,exam_dates,start_times,end_times,total_hours_list,exam_centres)

        for i in range(len(courses)):
            course = get_object_or_404(Course, id=courses[i])
            branch = get_object_or_404(Branch,id = branch)
            MonthlyAdmitCard.objects.create(
                session=session,
                course=course,
                semester=semesters[i],
                paper_name=paper_names[i],
                exam_date=exam_dates[i],
                start_time=start_times[i],
                end_time=end_times[i],
                total_hours=total_hours_list[i],
                exam_centre=exam_centres[i],
                branch = branch
            )
        return JsonResponse({'message': 'Admit Cards have been successfully generated.'})
    
    return render(request, 'generate_admit_card.html')


def get_courses(request):
    branch_id = request.GET.get('branch_id')
    course_type = request.GET.get('course_type')

    if branch_id and course_type:
        courses = Course.objects.filter(branch_id=branch_id, course_type=course_type).values('id', 'name')
        course_list = list(courses)
        return JsonResponse(course_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)


def get_admit_card(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        semester = request.POST.get('semester')
        session = request.POST.get('session')

        if not all([student_id, semester, session]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        try:
            student = Student.objects.get(Studentid=student_id)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        course = student.course.id
        print(course)

        monthly_admit_card = MonthlyAdmitCard.objects.filter(course=course,semester=semester, session=session)
        print(monthly_admit_card)
        if not monthly_admit_card.exists():
            return JsonResponse({'error': 'No monthly admit card found for the student'}, status=404)

        context = {
            'student': student,
            'monthly_admit_card': monthly_admit_card.first() 
        }
        return render(request, 'app/admitcardtemplate.html', context)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
def save_admit_pdf(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        pdf_file = request.FILES['pdf']
        
        if not studentid or not pdf_file:
            return JsonResponse({'success': False, 'error': 'Missing student ID or PDF file'})

        # Generate a random 5-digit number
        random_number = random.randint(10000, 99999)
        
        pdf_file.name = f'monthlyadmitcard_{studentid}_{random_number}.pdf'
        save_path = os.path.join('monthlyadmitcards', pdf_file.name)
        path = default_storage.save(os.path.join(settings.MEDIA_ROOT, save_path), pdf_file)

        try:
            student = Student.objects.get(Studentid=studentid)
            student.monthlyAdmitCard = save_path  
            student.save()
            return JsonResponse({'success': True, 'file_path': path})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def generate_yearly_admit_card(request):
   if request.method == 'POST':
    session = request.POST.get('session')
    courses = request.POST.getlist('course[]')
    exam_dates = request.POST.getlist('examDate[]')
    paper1_start_time = request.POST.getlist('paper1startTime[]')
    paper1_end_time = request.POST.getlist('paper1endTime[]')
    paper1_total_hours = request.POST.getlist('paper1totalHours[]')
    paper2_start_time = request.POST.getlist('paper2startTime[]')
    paper2_end_time = request.POST.getlist('paper2endTime[]')
    paper2_total_hours = request.POST.getlist('paper2totalHours[]')
    exam_centres = request.POST.getlist('examCentre[]')
    branchid = request.POST.get('branchId')

    print(session,courses,exam_dates,exam_centres)

    for i in range(len(courses)):
        course = get_object_or_404(Course, id=courses[i])
        branch = get_object_or_404(Branch,id = branchid)
        YearlyAdmitCard.objects.create(
            session=session,
            course=course,
            exam_date=exam_dates[i],
            paper1_start_time=paper1_start_time[i],
            paper1_end_time=paper1_end_time[i],
            paper1_total_hours=paper1_total_hours[i],
            paper2_start_time=paper2_start_time[i],
            paper2_end_time=paper2_end_time[i],
            paper2_total_hours=paper2_total_hours[i],
            exam_centre=exam_centres[i],
            branch = branch
        )
        return JsonResponse({'message': 'Admit Cards have been successfully generated.'})
    
   return render(request, 'generate_admit_card.html')

def get_yearly_admit_card(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        session = request.POST.get('session')

        if not all([student_id, session]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        try:
            student = Student.objects.get(Studentid=student_id)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        course = student.course.id
        print(course)

        monthly_admit_card = YearlyAdmitCard.objects.filter(course=course, session=session)
        print(monthly_admit_card)
        if not monthly_admit_card.exists():
            return JsonResponse({'error': 'No monthly admit card found for the student'}, status=404)

        context = {
            'student': student,
            'monthly_admit_card': monthly_admit_card.first() 
        }
        return render(request, 'app/yearlyadmitcardtemplate.html', context)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
def save_yearly_admit_pdf(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        pdf_file = request.FILES['pdf']
        
        if not studentid or not pdf_file:
            return JsonResponse({'success': False, 'error': 'Missing student ID or PDF file'})

        # Generate a random 5-digit number
        random_number = random.randint(10000, 99999)
        
        pdf_file.name = f'Yearlyadmitcard_{studentid}_{random_number}.pdf'
        save_path = os.path.join('Yearlyadmitcards', pdf_file.name)
        path = default_storage.save(os.path.join(settings.MEDIA_ROOT, save_path), pdf_file)

        try:
            student = Student.objects.get(Studentid=studentid)
            student.YearlyAdmitCard = save_path  
            student.save()
            return JsonResponse({'success': True, 'file_path': path})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def approve_marksheet(request, marksheet_request_id):
    marksheet_request = get_object_or_404(MarksheetRequest, id=marksheet_request_id)
    branch_id = marksheet_request.branch_id
    marksheet_request.approved = True
    marksheet_request.save()

    user_id = marksheet_request.user.id
    course_id = marksheet_request.Course

    user = get_object_or_404(User, id=user_id)
    student, created = Student.objects.get_or_create(user=user)

    with transaction.atomic():
        branch_wallet = Wallet.objects.select_for_update().get(branch_id=branch_id)
        marksheetfees = branch_wallet.marksheet_amount
        if branch_wallet.amount < marksheetfees:
            raise ValueError("Insufficient balance in the wallet.")

        marks_queryset = Marks.objects.filter(student=student)

        for mark in marks_queryset:
            pass

        branch_wallet.amount -= marksheetfees
        branch_wallet.save()

        branch_object = Branch.objects.get(id=branch_id)

        Transaction.objects.create(
            wallet_id=branch_wallet.id,
            amount=marksheetfees,
            transaction_type='Debit',
            branchstaticid=branch_object.branchstaticid,
            timestamp=timezone.now()
        )

    context = {
        'marksheet_request': marksheet_request,
        'user': user,
        'student': student,
        'marks': marks_queryset, 
    }
    return render(request, 'app/automaticmarksheet.html', context)

@csrf_exempt
def save_oldcertificate_pdf(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        pdf_file = request.FILES['pdf']
        
        if not studentid or not pdf_file:
            return JsonResponse({'success': False, 'error': 'Missing student ID or PDF file'})

        # Generate a random 5-digit number
        random_number = random.randint(10000, 99999)
        
        pdf_file.name = f'ManualCertificate_{studentid}_{random_number}.pdf'
        save_path = os.path.join('ManualCertificate', pdf_file.name)
        path = default_storage.save(os.path.join(settings.MEDIA_ROOT, save_path), pdf_file)

        try:
            student = OldMarksheet.objects.get(enrollment_no=studentid)
            student.certificate_pdf_url = save_path  
            student.save()
            return JsonResponse({'success': True, 'file_path': path})
        except OldMarksheet.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def save_oldmarksheet_pdf(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        pdf_file = request.FILES['pdf']
        
        if not studentid or not pdf_file:
            return JsonResponse({'success': False, 'error': 'Missing student ID or PDF file'})

        # Generate a random 5-digit number
        random_number = random.randint(10000, 99999)
        
        pdf_file.name = f'ManualMarksheet_{studentid}_{random_number}.pdf'
        save_path = os.path.join('ManualMarksheet', pdf_file.name)
        path = default_storage.save(os.path.join(settings.MEDIA_ROOT, save_path), pdf_file)

        try:
            student = OldMarksheet.objects.get(enrollment_no=studentid)
            student.marksheet_pdf_url = save_path  
            student.save()
            return JsonResponse({'success': True, 'file_path': path})
        except OldMarksheet.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def yearlyadmitcardhistory(request,branch_id):
    yadmitcards = YearlyAdmitCard.objects.filter(branch_id = branch_id)
    return render(request, 'app/yearlyadmitcardhistory.html', {'yadmitcards':yadmitcards})

def monthlyadmitcardhistory(request,branch_id):
    Madmitcards = MonthlyAdmitCard.objects.filter(branch_id = branch_id)
    return render(request, 'app/monthlyadmitcardhistory.html',  {'Madmitcards':Madmitcards}) 

def admitcardhistory(request,branch_id):
    Students = Student.objects.filter(branch_id = branch_id)
    print(Students)
    return render(request, 'app/admitcardshistory.html',  {'Students':Students}) \
    

@csrf_exempt
def delete_subject(request, subject_id):
    try:
        subject = OldSubject.objects.get(id=subject_id)
        subject.delete()
        return JsonResponse({'success': True, 'message': 'Subject deleted successfully'})
    except OldSubject.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Subject does not exist'}, status=404)

@csrf_exempt
def delete_course(request, course_id):
    try:
        course = OldCourse.objects.get(id=course_id)
        course.delete()
        return JsonResponse({'success': True, 'message': 'Course deleted successfully'})
    except OldCourse.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Course does not exist'}, status=404)
    

def edit_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, Studentid=student_id)
        print(student)
        data = json.loads(request.body)
        print(data)

        # Update student fields with newly received values
        student.name = data.get('name', student.name)
        student.enrollment_number = data.get('enrollment_number', student.enrollment_number)
        student.roll_number = data.get('roll_number', student.roll_number)
        student.email = data.get('email', student.email)
        student.father_name = data.get('father_name', student.father_name)
        student.mother_name = data.get('mother_name', student.mother_name)
        student.permanent_address = data.get('permanent_address', student.permanent_address)
        student.dob = data.get('dob', student.dob)
        student.phone_number = data.get('phone_number', student.phone_number)
        # Save the changes
        student.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)

def get_student(request, student_id):
    student = get_object_or_404(Student, Studentid=student_id)
    student_data = {
        "Studentid": student.Studentid,
        "name": student.name,
        "enrollment_number": student.enrollment_number,
        "roll_number": student.roll_number,
        "email": student.email,
        "father_name": student.father_name,
        "mother_name": student.mother_name,
        "permanent_address": student.permanent_address,
        "phone_number": student.phone_number,  
        "dob": student.dob 
    }
    return JsonResponse(student_data)

def delete_student(request, student_id):
    if request.method == 'DELETE':
        student = get_object_or_404(Student, Studentid=student_id)
        
        user = student.user
        
        student.delete()
        user.delete()
        
        return JsonResponse({'message': 'Student and associated user deleted successfully'})
    
    return JsonResponse({'message': 'Invalid request'}, status=400)

def student_dashboard(request, studentid):
    student = get_object_or_404(Student, id=studentid)
    
    context = {
        'student': student,
    }
    return render(request, 'app/studentdownlaods.html', context)


@csrf_exempt
def save_automatic_admit_pdf(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        pdf_file = request.FILES['pdf']
        
        if not studentid or not pdf_file:
            return JsonResponse({'success': False, 'error': 'Missing student ID or PDF file'})

        # Generate a random 5-digit number
        random_number = random.randint(10000, 99999)
        
        pdf_file.name = f'Marksheet_{studentid}_{random_number}.pdf'
        save_path = os.path.join('Automaticmarksheet', pdf_file.name)
        path = default_storage.save(os.path.join(settings.MEDIA_ROOT, save_path), pdf_file)

        try:
            student = Student.objects.get(Studentid=studentid)
            marksheet = MarksheetRequest.objects.get(student=student)
            marksheet.marksheet_pdf_url = save_path  
            marksheet.save()
            return JsonResponse({'success': True, 'file_path': path})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
        except MarksheetRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Marksheet request not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def requestmarksheethistory(request):
    marksheet = MarksheetRequest.objects.all()
    return render(request,'app/marksheetrequesthistory.html',{'marksheet':marksheet})


@csrf_exempt
def fetch_student_marks(request, student_id):
    student = get_object_or_404(Student, Studentid=student_id)
    marks = Marks.objects.filter(student=student)
    
    marks_list = []
    for mark in marks:
        marks_list.append({
            'student_name': mark.student.name,
            'subject_name': mark.subject.name,
            'theory_marks': mark.theory_marks_obtained,
            'theory_max_marks': mark.theory_max_marks,
            'practical_marks': mark.practical_marks_obtained,
            'practical_max_marks':mark.practical_max_marks,
        })
    
    return JsonResponse({'marks': marks_list})



def get_teacher_allocations(teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
        return teacher.batches.all()
    except Teacher.DoesNotExist:
        return None
    

@csrf_exempt
def verify_registration(request):
    if request.method == 'POST':
        enrollment_number = request.POST.get('certificateNumber')
        dob = request.POST.get('dob')

        if not enrollment_number or not dob:
            return JsonResponse({'success': False, 'error': 'Missing enrollment number or date of birth'})

        try:
            student = Student.objects.get(enrollment_number=enrollment_number, dob=dob)
            receipt_address = student.receipt_path  
            return JsonResponse({'success': True, 'receipt_address': receipt_address})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



@api_view(['POST'])
def get_student_results(request):
    roll_number = request.data.get('rollNumber')
    dob = request.data.get('dob')


    try:
        student = Student.objects.get(roll_number=roll_number, dob=dob)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'})

    marks = Marks.objects.filter(student=student)
    if not marks.exists():
        return Response({'error': 'No marks found for this student'})

    results = []
    for mark in marks:
        result = {
            'roll_number': student.roll_number,
            'name': student.name,
            'subject': mark.subject.name,
            'practical_mark_obtained': mark.practical_marks_obtained,
            'practical_max_marks': mark.practical_max_marks,
            'theory_mark_obtained': mark.theory_marks_obtained,
            'theory_max_marks': mark.theory_max_marks
        }
        results.append(result)

    return Response({'data': results})

@csrf_exempt
def delete_record(request, record_id):
    if request.method == 'DELETE':
        record = get_object_or_404(OldMarksheet, id=record_id)
        record.delete()
        return JsonResponse({'message': 'Record deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def get_holiday_data(request):
    if request.method == 'GET':
        holidays = Holiday.objects.all().values('id','name', 'date_from', 'date_to', 'no_of_holidays', 'remarks')
        holiday_list = list(holidays)
        return JsonResponse(holiday_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def create_holiday(request):
    if request.method == 'POST':
        holiday_name = request.POST.get('holiday_name')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        number_of_holidays = request.POST.get('number_of_holidays')
        remarks = request.POST.get('remarks')

        if holiday_name and date_from and date_to and number_of_holidays:
            holiday = Holiday(
                name=holiday_name,
                date_from=date_from,
                date_to=date_to,
                no_of_holidays=number_of_holidays,
                remarks=remarks
            )
            holiday.save()
            return JsonResponse({'message': 'Holiday entry created successfully!'}, status=201)
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def delete_holiday(request, id):
    if request.method == 'DELETE':
        try:
            holiday = Holiday.objects.get(id=id)
            holiday.delete()
            return JsonResponse({'message': 'Holiday deleted successfully.'})
        except Holiday.DoesNotExist:
            return JsonResponse({'message': 'Holiday not found.'}, status=404)
    return HttpResponse(status=405)