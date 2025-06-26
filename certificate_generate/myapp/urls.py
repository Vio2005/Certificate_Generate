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
    
    


   
]