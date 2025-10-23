from django.shortcuts import render,redirect,HttpResponse
from.forms import *
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.utils import timezone
from .models import *
import pandas
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from html2image import Html2Image
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


import os

# Create your views here.
def homeview(request,id):
    enroll = Enrollment.objects.select_related('course_name').get(id=id)
    
    context={"enroll":enroll}
    return render(request,'index1.html',context)

def createcourse(request):
    course=CourseModelForm()
    if request.method=="POST":
        course=CourseModelForm(request.POST,request.FILES)
        if course.is_valid():
           
            course.save()
          
            return redirect('/courselist')
        else:
           
            return HttpResponse('Error')
    return render(request,'createcourse.html',{'course':course})

def courselist(request):
    courseform=CourseModelForm()
    if request.method=="POST":
        courseform=CourseModelForm(request.POST,request.FILES)
        if courseform.is_valid():
           
            courseform.save()
          
            return redirect('/courselist')
        else:
           
            return HttpResponse('Error')
    course=Course.objects.all()
    paginator = Paginator(course, 5) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context={'course':course,'page_obj':page_obj,'courseform':courseform}
    return render(request,'courselist.html',context)

def deletecourse(request,id):
    page_obj=Course.objects.filter(id=id).delete()
    return redirect('/courselist')



def updatecourse(request,id):
    course = Course.objects.get(id=id)
    page_obj = CourseModelForm(instance=course)
    if request.method=="POST":
        obj = CourseModelForm(request.POST, instance=course)
        if obj.is_valid():
         obj.save()
        return redirect('/courselist')
    context={"course":course,"page_obj":page_obj}
    return render(request,'updatecourse.html',context)

def enroll(request,id):
    stu = Student.objects.get(id=id)
    obj = EnrollModelForm(instance=stu)
    if request.method=="POST":
        obj = EnrollModelForm(request.POST, instance=stu)
        if obj.is_valid():
         obj.save()
        return redirect('/courselist')
    context={"stu":stu,"obj":obj}
    return render(request,'enroll.html',context)




def createstudent(request):
    student=StudentModelForm()
    if request.method=="POST":
        student=StudentModelForm(request.POST,request.FILES)
        if student.is_valid():
           
            student.save()
          
            return redirect('/studentlist')
        else:
           
            return HttpResponse('Error')
    return render(request,'createstudent.html',{'student':student})

def studentlist(request):
    student=Student.objects.all()
    context={'student':student}
    return render(request,'studentlist.html',context)

def deletestudent(request,id):
    student=Student.objects.filter(id=id).delete()
    return redirect('/studentlist')

def updatestudent(request,id):
    student = Student.objects.get(id=id)
    obj = StudentModelForm(instance=student)
    if request.method=="POST":
        obj = StudentModelForm(request.POST, instance=student)
        if obj.is_valid():
         obj.save()
        return redirect('/studentlist')
    context={"student":student,"obj":obj}
    return render(request,'updatestudent.html',context)

def detailstudent(request, id):
    student = Student.objects.get(id=id)
    context = {"student": student}
    return render(request, 'studentdetail.html', context)




def enrollment(request):
    enroll=EnrollModelForm()
    if request.method=="POST":
        enroll=EnrollModelForm(request.POST)
        
        if enroll.is_valid():
            enroll.save()
          
            return redirect('/enrolllist')
        else:
           
            return HttpResponse('Error')
    return render(request,'enroll.html',{'enroll':enroll})

def enrolllist(request):
    enroll=Enrollment.objects.all()
    paginator = Paginator(enroll, 3) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context={'enroll':enroll,'page_obj':page_obj}
    return render(request,'enrolllist.html',context)

def register_view(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        firstname=request.POST['fname']
        lastname=request.POST['lname']
        user=User.objects.filter(username=username)
        if user.exists():
            return redirect('/register')
        else:
            usr=User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname)
            usr.set_password(password)
            usr.is_superuser=True
            usr.is_staff=True
            usr.save()

            return redirect ('/login')
    else:
        return render(request,'register.html')
    
def loginview(request):
    if request.method == 'POST':
    
        usr = request.POST.get('username')
        pas = request.POST.get('password')
        usr_auth=authenticate(username=usr,password=pas)
        if usr_auth:
            login(request, usr_auth)
            return redirect('/indexview/')
        else:
            return redirect('/login')
    else:

        return render(request, 'login.html')
    
def logoutview(request):
    logout(request)
    return redirect('/login/')
    

class SuperUser(object):
     def dispatch(self,request,*arg,**kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            pass
        else:
            return redirect('/studentview')
        return super().dispatch(request,*arg,**kwargs)

class LoginRequire(object):
    def dispatch(self,request,*arg,**kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            pass
        else:
            return redirect('/login')
        return super().dispatch(request,*arg,**kwargs)
    
class IndexView(LoginRequire, SuperUser, View):
    def get(self, request):
        student = Student.objects.count()
        trainer = Trainer.objects.count()
        course = Course.objects.count()
        certificate = Enrollment.objects.filter(email_status=True).count()

        # Count total incomplete enrollments
        active_enrollments = Enrollment.objects.filter(status=False).count()

        # Filter courses that have at least one incomplete enrollment and annotate them
        courses_with_incomplete = Course.objects.filter(
            enrollment__status=False
        ).annotate(
            incomplete_count=Count(
                'enrollment',
                filter=Q(enrollment__status=False)
            )
        ).distinct()

        trainer_obj = Trainer.objects.all()

        context = {
            "student": student,
            "trainer": trainer,
            "course": course,
            "certificate":certificate,
            "active_enrollments": active_enrollments,
            "courselist": courses_with_incomplete,
            "trainer_obj": trainer_obj
        }

        return render(request, 'homepage.html', context)

def index1(request):
    return render(request,'starter-template.html')

def studentview(request):
    return render(request,'studentview.html')


def tableexample(request):
    return render(request,'tableexample.html')


def deleteenroll(request,id):
    page_obj=Enrollment.objects.get(id=id)
    page_obj.delete()
    return redirect('enrollview',id=page_obj.course_name.id)

def comstatus(request,id):
    enroll = Enrollment.objects.get(id=id)
    enroll.status = True
    enroll.end_date = timezone.now()
    enroll.save()
    return redirect('enrollview', id=enroll.course_name.id)

def complete_all_status(request, id):
    course = Course.objects.get(id=id)
    Enrollment.objects.filter(course_name=course).update(status=True, end_date=timezone.now())
    return redirect('enrollview', id=course.id)

def createtrainer(request):
    trainer=TrainerModelForm()
    if request.method=="POST":
        trainer=TrainerModelForm(request.POST,request.FILES)
        if trainer.is_valid():
           
            trainer.save()
          
            return redirect('/trainerlist')
        else:
           
            return HttpResponse('Error')
    return render(request,'trainerlist.html',{'trainer':trainer})

def trainerlist(request):
    trainerform=TrainerModelForm()
    if request.method=="POST":
        trainerform=TrainerModelForm(request.POST,request.FILES)
        if trainerform.is_valid():
           
            trainerform.save()
          
            return redirect('/trainerlist')
        else:
           
            return HttpResponse('Error')
    trainer=Trainer.objects.all()
    paginator = Paginator(trainer, 5) 

    page_number = request.GET.get("page")
    trainer_obj = paginator.get_page(page_number)
    context={'trainer':trainer,'trainer_obj':trainer_obj,'trainerform':trainerform}
    return render(request,'trainerlist.html',context)

def deletetrainer(request,id):
    trainer_obj=Trainer.objects.filter(id=id).delete()
    return redirect('/trainerlist')

def deletetrainerhome(request,id):
    trainer_obj=Trainer.objects.filter(id=id).delete()
    return redirect('/indexview')

def updatetrainer(request,id):
    obj = Trainer.objects.get(id=id)
    trainer_obj = TrainerModelForm(instance=obj)
    if request.method=="POST":
        trainer_obj = TrainerModelForm(request.POST, instance=obj)
        if trainer_obj.is_valid():
         trainer_obj.save()
        return redirect('/trainerlist')
    context={"trainer_obj":trainer_obj,"obj":obj}
    return render(request,'updatetrainer.html',context)

def homepage(request):
    student=Student.objects.count()
    trainer=Trainer.objects.count()
    course=Course.objects.count()
    context={"student":student,"trainer":trainer,"course":course}
    return render(request,"homepage.html",context)

def fileinput(request):
    if request.method=="POST":
        mydata=request.FILES['myfile']
        data=pandas.read_excel(mydata)
        for index,row in data.iterrows():
            Mymodel.objects.create(
                name=row['name'],
                address=row['address'],
                phone=row['phone'],
            )
            print(index,row)
        return render(request,'fileinput.html')

    return render(request,'fileinput.html')


def studentinput(request):
    if request.method=="POST":
        mydata=request.FILES['studentfile']
        data=pandas.read_excel(mydata)
        for index,row in data.iterrows():
            Student.objects.create(
                student_name=row['name'],
                email=row['email'],
                phone=row['phone'],
            )
            print(index,row)
        return render(request,'studentinput.html')

    return render(request,'studentinput.html')

def enrollinput(request):
    courses = Course.objects.all()
    skipped_emails = []

    if request.method == "POST":
        uploaded_file = request.FILES.get('list')
        selected_course_name = request.POST.get('course')
        start_date = request.POST.get('start_date')

        try:
            course = Course.objects.get(course_name=selected_course_name)
        except Course.DoesNotExist:
            return render(request, 'enrollinput.html', {
                'course': courses,
                'error': 'Selected course does not exist.'
            })

        data = pandas.read_excel(uploaded_file)

        for index, row in data.iterrows():
            student_name = str(row['name']).strip()
            email = str(row['email']).strip().lower()
            phone = str(row['phone']).strip()

            # Check if student exists
            try:
                student = Student.objects.get(email=email)
            except Student.DoesNotExist:
                skipped_emails.append(email)
                continue

            student.student_name = student_name
            student.phone = phone
            student.save()

            if Enrollment.objects.filter(student_name=student, course_name=course).exists():
                continue

            Enrollment.objects.create(
                student_name=student,
                course_name=course,
                start_date=start_date
            )

        # Always return to same page with skipped_emails if any
        return render(request, 'enrollinput.html', {
            'course': courses,
            'skipped_emails': skipped_emails
        })

    return render(request, 'enrollinput.html', {'course': courses})



def email(request, id):
    # 1️⃣ Update email_status and email_date
    Enrollment.objects.filter(id=id).update(
        email_status=True,
        email_date=timezone.now().date()   # Just the date, no time
    )

    # 2️⃣ Fetch the updated Enrollment object with related data
    enroll = Enrollment.objects.select_related('course_name', 'student_name').get(id=id)
    student = enroll.student_name
    receiver_email = student.email

    # 3️⃣ Build absolute domain for loading static files in HTML template
    domain = request.build_absolute_uri('/')[:-1]

    # 4️⃣ Render HTML template with enrollment data
    html_content = render_to_string('index2.html', {
        'enroll': enroll,
        'domain': domain,
    })

    # 5️⃣ Save the rendered HTML to a temporary file
    html_path = os.path.join(settings.BASE_DIR, 'temp_certificate.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 6️⃣ Convert HTML to Image
    hti = Html2Image()
    output_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
    os.makedirs(output_dir, exist_ok=True)

    # Ensure unique image name (add enrollment ID)
    image_name = f'certificate_{student.student_name}_{enroll.id}.jpg'
    hti.output_path = output_dir
    hti.screenshot(
        html_file=html_path,
        save_as=image_name,
        size=(1000, 700)
    )

    # Compute relative path for MEDIA_URL
    relative_image_path = os.path.join('certificates', image_name)

    # 7️⃣ Save certificate image path to Enrollment
    enroll.certificate_image = relative_image_path
    enroll.save()

    # 8️⃣ Send email with the image attached
    email = EmailMessage(
        subject='Your Certificate',
        body=f"""
Dear {student.student_name},

Congratulations! 🎉

You have successfully completed the course: {enroll.course_name.course_name}

Warm regards,  
RIG Admin
""",
        from_email=settings.EMAIL_HOST_USER,
        to=[receiver_email],
    )
    email.attach_file(os.path.join(settings.MEDIA_ROOT, relative_image_path))
    email.send()

    # 9️⃣ Cleanup temporary HTML file
    os.remove(html_path)

    # 10️⃣ Redirect back to enrollview for that course
    return redirect('enrollview', id=enroll.course_name.id)


def email_all(request, course_id):
    # Step 1: Get all eligible enrollments
    enrollments = Enrollment.objects.filter(
        course_name_id=course_id,
        status=True,
        email_status=False
    ).select_related('course_name', 'student_name')

    if not enrollments.exists():
        return redirect('enrollview', id=course_id)

    # Step 2: Build domain and output path
    domain = request.build_absolute_uri('/')[:-1]
    output_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
    os.makedirs(output_dir, exist_ok=True)

    # Step 3: Set up Html2Image
    hti = Html2Image()
    hti.output_path = output_dir

    # Step 4: Loop through enrollments
    for enroll in enrollments:
        student = enroll.student_name
        receiver_email = student.email

        # Render certificate HTML
        html_content = render_to_string('index2.html', {
            'enroll': enroll,
            'domain': domain,
        })

        # Save HTML temporarily
        html_path = os.path.join(settings.BASE_DIR, 'temp_certificate.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Generate image
        image_name = f'certificate_{student.student_name}_{enroll.id}.jpg'
        hti.screenshot(
            html_file=html_path,
            save_as=image_name,
            size=(1000, 700)
        )

        # Relative image path for ImageField
        relative_image_path = os.path.join('certificates', image_name)
        full_image_path = os.path.join(output_dir, image_name)

        # Update enrollment with image and email info
        enroll.certificate_image = relative_image_path
        enroll.email_status = True
        enroll.email_date = timezone.now().date()
        enroll.save()

        # Send email
        email = EmailMessage(
            subject='Your Certificate',
            body=f"""
Dear {student.student_name},

Congratulations! 🎉

You have successfully completed the course: {enroll.course_name.course_name}

Warm regards,  
RIG Admin
""",
            from_email=settings.EMAIL_HOST_USER,
            to=[receiver_email],
        )
        email.attach_file(full_image_path)
        email.send()

        # Remove temporary HTML
        os.remove(html_path)

    return redirect('enrollview', id=course_id)



def enrollview(request, id=None):
    course_name = Course.objects.all()
    course = None
    enrollments = None
    all_complete = False

    if id is not None:
        course = Course.objects.get(id=id)
        enrollments = Enrollment.objects.filter(course_name=course, email_status=False)

        # Check if all enrollments for this course have status=True
        if enrollments.exists() and not enrollments.filter(status=False).exists():
            all_complete = True

    return render(request, 'enrollview.html', {
        'course_name': course_name,
        'course': course,
        'enrollments': enrollments,
        'all_complete':all_complete
    })

def certificate_view(request, id):
    enroll = Enrollment.objects.get(id=id)
    return render(request, 'certificate_view.html', {'enroll': enroll})

def historyview(request):
    enrollments = Enrollment.objects.filter(email_status=True)

    paginator = Paginator(enrollments, 5)  # Show 5 enrollments per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'enrollments': enrollments,
        'page_obj': page_obj,
    }
    return render(request, 'history.html', context)

def course_enrollments(request, id):
    course = Course.objects.get(id=id)
    enrollments = Enrollment.objects.filter(course_name=course)
    return render(request, 'enrollview.html', {
        'course': course,
        'enrollments': enrollments
    })

def deletecoursebtn(request,id):
    course_name=Course.objects.filter(id=id).delete()
    return redirect("/enrollview")

def enroll_single_student(request):
    student_data = {}
    student_id = request.GET.get('student_id')

    if student_id:
        try:
            student = Student.objects.get(id=student_id)
            student_data = {
                'student_name': student.student_name,
                'email': student.email,
                'phone': student.phone,
            }
        except Student.DoesNotExist:
            student_data = {}

    courses = Course.objects.all()

    if request.method == "POST":
        student_name = request.POST.get('student_name').strip()
        email = request.POST.get('email').strip().lower()
        phone = request.POST.get('phone').strip()
        selected_course_name = request.POST.get('course')
        start_date = request.POST.get('start_date')

        try:
            course = Course.objects.get(course_name=selected_course_name)
        except Course.DoesNotExist:
            return render(request, 'enroll_single.html', {
                'course': courses,
                'student_data': student_data,
                'error': 'Selected course does not exist.'
            })

        # 🚨 New email check — only allow emails already in Student table
        if not Student.objects.filter(email=email).exists():
            return render(request, 'enroll_single.html', {
                'course': courses,
                'student_data': {
                    'student_name': student_name,
                    'email': email,
                    'phone': phone
                },
                'error': 'This email is not registered. Please use a registered student email.'
            })

        # ✅ Get student object (we already know it exists)
        student = Student.objects.get(email=email)
        student.student_name = student_name
        student.phone = phone
        student.save()

        # ✅ Check for existing Enrollment
        existing_enrollment = Enrollment.objects.filter(
            student_name=student,
            course_name=course
        ).first()

        if existing_enrollment:
            return render(request, 'enroll_single.html', {
                'course': courses,
                'student_data': student_data,
                'error': 'This student is already enrolled in the selected course.'
            })

        # ✅ Create new Enrollment
        Enrollment.objects.create(
            student_name=student,
            course_name=course,
            start_date=start_date
        )

        return redirect('enrollview', id=course.id)

    return render(request, 'enroll_single.html', {
        'course': courses,
        'student_data': student_data
    })


def history(request):
    enroll=Enrollment.objects.all()
    paginator = Paginator(enroll, 10) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context={'enroll':enroll,'page_obj':page_obj}
    return render(request,'history.html',context)

def myaccount(request):
    user = request.user
    return render(request, 'myaccount.html', {'user': user})



def delete_history(request, id):
    enrollment = Enrollment.objects.get (id=id)
    enrollment.delete()
    return redirect('history')

@login_required
def edit_user_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Basic validation (optional)
        if not username or not email:
            messages.error(request, 'Username and email are required.')
            return render(request, 'edit_user.html', {'user_obj': user})

        # Update user object
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('myaccount')  # reload same page

    return render(request, 'edit_user.html', {'user_obj': user})
