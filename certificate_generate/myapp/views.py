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
    paginator = Paginator(course, 3) 

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

def detailstudent(request,id):
    student=Student.objects.filter(id=id)
    context={"student":student}
    return render(request,'studentdetail.html',context)



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
            return redirect('register/')
        else:
            usr=User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname)
            usr.set_password(password)
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
    
class IndexView(LoginRequire,SuperUser,View):
    def get(self,request):
        student=Student.objects.count()
        trainer=Trainer.objects.count()
        course=Course.objects.count()
        active_enrollments = Enrollment.objects.filter(status=False).count()
        courselist=Course.objects.all()
        trainer_obj=Trainer.objects.all()
        context={"student":student,"trainer":trainer,"course":course,"active_enrollments":active_enrollments,"courselist":courselist,"trainer_obj":trainer_obj}
        return render(request,'homepage.html',context)

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
    paginator = Paginator(trainer, 3) 

    page_number = request.GET.get("page")
    trainer_obj = paginator.get_page(page_number)
    context={'trainer':trainer,'trainer_obj':trainer_obj,'trainerform':trainerform}
    return render(request,'trainerlist.html',context)

def deletetrainer(request,id):
    trainer_obj=Trainer.objects.filter(id=id).delete()
    return redirect('/trainerlist')

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
    course = Course.objects.all()

    if request.method == "POST":
        uploaded_file = request.FILES.get('list')
        selected_course_name = request.POST.get('course')

        course = Course.objects.get(course_name=selected_course_name)

        data = pandas.read_excel(uploaded_file)
        for index, row in data.iterrows():
            student_name = row['name'].strip()
            email = row['email'].strip().lower()
            phone = str(row['phone']).strip()

            student, created = Student.objects.get_or_create(
                email=email,
                defaults={
                    'student_name': student_name,
                    'phone': phone
                }
            )

            if not created:
                student.student_name = student_name
                student.phone = phone
                student.save()

            Enrollment.objects.create(
                student_name=student,
                course_name=course
            )

        return redirect('/enrollinput')

    # Important: return context in GET request
    return render(request, 'enrollinput.html', {'course': course})




def email(request, id):
    # Step 1: Update email_status and email_date
    Enrollment.objects.filter(id=id).update(
        email_status=True,
        email_date=timezone.now()
    )

    # Step 2: Fetch the updated Enrollment object (with related Course and Student)
    enroll = Enrollment.objects.select_related('course_name', 'student_name').get(id=id)
    student = enroll.student_name
    receiver_email = student.email

    # Step 3: Build absolute domain for loading static files
    domain = request.build_absolute_uri('/')[:-1]

    # Step 4: Render HTML from template with the single enrollment object
    html_content = render_to_string('index2.html', {
        'enroll': enroll,
        'domain': domain,
    })

    # Step 5: Save the HTML content to a temporary file
    html_path = os.path.join(settings.BASE_DIR, 'temp_certificate.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Step 6: Convert HTML to Image
    hti = Html2Image()
    output_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
    os.makedirs(output_dir, exist_ok=True)
    image_name = f'certificate_{student.student_name}.jpg'
    hti.output_path = output_dir
    hti.screenshot(
        html_file=html_path,
        save_as=image_name,
        size=(1000, 700)
    )

    image_path = os.path.join(output_dir, image_name)

    # Step 7: Send the email with image attachment
    email = EmailMessage(
        subject='Your Certificate',
        body=f"""
Dear {student.student_name},

Congratulations! 🎉

You have successfully completed the course: {enroll.course_name.course_name}

Warm regards,  
RIG Admin  
Training Coordinator  
Realistic Infotech Group  
Consulting / Software Solutions / IT Training  
www.rig-info.com  
09256675642, 09953933826
""",
        from_email=settings.EMAIL_HOST_USER,
        to=[receiver_email],
    )
    email.attach_file(image_path)
    email.send()

    # Step 8: Cleanup temporary HTML
    os.remove(html_path)

    return redirect('enrolllist')

def enrollview(request,id=None):
    course_name = Course.objects.all()

    course = None
    enrollments = None

    if id is not None:
        course = Course.objects.get(id=id)
        enrollments = Enrollment.objects.filter(course_name=course)

    return render(request, 'enrollview.html', {
        'course_name': course_name,
        'course': course,
        'enrollments': enrollments
    })
def course_enrollments(request, id):
    course = Course.objects.get(id=id)
    enrollments = Enrollment.objects.filter(course_name=course)
    return render(request, 'enrollview.html', {
        'course': course,
        'enrollments': enrollments
    })