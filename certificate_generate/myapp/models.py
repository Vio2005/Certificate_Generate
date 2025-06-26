from django.db import models

# Create your models here.
class Trainer(models.Model):
    trainer_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField()
    def __str__(self):
        return self.trainer_name
    
class Course(models.Model):
    course_name=models.CharField(max_length=100)
    short_name=models.CharField(max_length=50,blank=True,null=True)
    duration=models.PositiveIntegerField()
    trainer_name=models.ForeignKey(Trainer,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.course_name

class Student(models.Model):
    student_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(blank=True,null=True)
    def __str__(self):
        return self.student_name
    
    
class Enrollment(models.Model):
    student_name=models.ForeignKey(Student,on_delete=models.CASCADE)
    course_name=models.ForeignKey(Course,on_delete=models.CASCADE)
    enroll_date=models.DateField(auto_now_add=True)
    end_date=models.DateField(blank=True,null=True)
    email_date=models.DateField(blank=True,null=True)
    status=models.BooleanField(default=False)
    email_status=models.BooleanField(default=False)
    def __str__(self):
        return f'{self.student_name}......{self.course_name}'
    
class Mymodel(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    



        
    








