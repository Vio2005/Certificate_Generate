from django.shortcuts import render,redirect,HttpResponse
from.forms import *
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.utils import timezone
from .models import *


# Create your views here.
def homeview(request,id):
    enroll = Enrollment.objects.filter(id=id)
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
    course=Course.objects.all()
    paginator = Paginator(course, 3) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context={'course':course,'page_obj':page_obj}
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
    page_obj=Enrollment.objects.filter(id=id).delete()
    return redirect('/enrolllist')

def comstatus(request,id):
    page_obj=Enrollment.objects.filter(id=id).update(status=True,end_date=timezone.now())
    return redirect('/enrolllist')

def createtrainer(request):
    trainer=TrainerModelForm()
    if request.method=="POST":
        trainer=TrainerModelForm(request.POST,request.FILES)
        if trainer.is_valid():
           
            trainer.save()
          
            return redirect('/trainerlist')
        else:
           
            return HttpResponse('Error')
    return render(request,'createtrainer.html',{'trainer':trainer})

def trainerlist(request):
    trainer=Trainer.objects.all()
    paginator = Paginator(trainer, 3) 

    page_number = request.GET.get("page")
    trainer_obj = paginator.get_page(page_number)
    context={'trainer':trainer,'trainer_obj':trainer_obj}
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


