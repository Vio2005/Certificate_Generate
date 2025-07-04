from django.db import models
from django.utils import timezone
from django.db import transaction



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
    trainer_name=models.ForeignKey(Trainer,on_delete=models.SET_NULL,blank=True,null=True)
    
    def __str__(self):
        return self.course_name

class Student(models.Model):
    student_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(blank=True,null=True)
    def __str__(self):
        return self.student_name
    
    
class Enrollment(models.Model):
    enroll_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course, on_delete=models.SET_NULL,blank=True,null=True)
    enroll_date = models.DateField(auto_now_add=True)
    start_date=models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True, null=True)
    email_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    email_status = models.BooleanField(default=False)
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.enroll_id:
            with transaction.atomic():
                now = timezone.now()
                year_str = now.strftime("%Y")
            
                last = Enrollment.objects.filter(enroll_id__startswith=year_str).order_by('-enroll_id').first()
                
                if last and last.enroll_id:
                    last_seq = int(last.enroll_id[-5:])
                    sequence = last_seq + 1
                else:
                    sequence = 1

                sequence_str = str(sequence).zfill(5)
                self.enroll_id = f"{year_str}{sequence_str}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student_name}......{self.course_name}'
    
class Mymodel(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    



        
    








