from django.urls import path
from .views import *

urlpatterns = [
    path('homeview/<int:id>/', homeview,name='homeview'),
    path('createcourse/', createcourse,name='createcourse'),
    path('courselist/', courselist,name='courselist'),
    path('deletecourse/<int:id>/', deletecourse,name='deletecourse'),
    path('updatecourse/<int:id>/', updatecourse,name='updatecourse'),
    path('createstudent/', createstudent,name='createstudent'),
    path('studentlist/', studentlist,name='studentlist'),
    path('deletestudent/<int:id>/', deletestudent,name='deletestudent'),
    path('updatestudent/<int:id>/', updatestudent,name='updatestudent'),
    path('enrollment/', enrollment,name='enrollment'),
    path('enrolllist/', enrolllist,name='enrolllist'),
    path('register/',register_view,name='register'),
    path('login/',loginview,name='login'),
    path('register/',register_view,name='register'),
    path('homepage/',homepage,name='homepage'),
    path('logout/',logoutview,name='logout'),
    path('indexview/', IndexView.as_view(), name='indexview'),
    path('index/',index1,name='index.html'),
    path('studentview/',studentview,name='studentview'),
    path('tableexample/',tableexample,name='tableexample'),
    path('deleteenroll/<int:id>/', deleteenroll,name='deleteenroll'),
    path('comstatus/<int:id>/', comstatus,name='comstatus'),
    path('trainerlist/', trainerlist,name='trainerlist'),
    path('deletetrainer/<int:id>/', deletetrainer,name='deletetrainer'),
    path('updatetrainer/<int:id>/', updatetrainer,name='updatetrainer'),
    path('createtrainer/', createtrainer,name='createtrainer'),
    path('detailstudent/<int:id>/', detailstudent,name='detailstudent'),
    path('fileinput/',fileinput,name='fileinput'),
    path('studentinput/',studentinput,name='studentinput'),
    path('email/<int:id>/', email, name='email'),
    path('enrollinput/', enrollinput, name='enrollinput'),
    path('enrollview/', enrollview, name='enrollview'),
    path('enrollview/<int:id>/', enrollview, name='enrollview'),
    path('complete_status/<int:id>/',complete_all_status, name='complete_all_status'),
    path('deletecoursebtn/<int:id>/',deletecoursebtn, name='deletecoursebtn'),
    path('email_all/<int:course_id>/',email_all, name='email_all'),
    path('deletetrainerhome/<int:id>/',deletetrainerhome, name='deletetrainerhome'),
    path('enroll_single_student/',enroll_single_student, name='enroll_single_student'),
    path('history/', historyview, name='history'),
    path('myaccount/', myaccount, name='myaccount'),
    path('certificate/<int:id>/', certificate_view, name='certificate_view'),
    path('delete_history/<int:id>/', delete_history, name='delete_history'),

 


   
]