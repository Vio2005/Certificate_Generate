from .models import *
from django import forms
from django.forms import DateInput


class CourseModelForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['course_name','short_name','duration','trainer_name']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter short name'}),            
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration '}),
            'trainer_name' :forms.Select(attrs={'class': 'form-select'}),
            
        }

class StudentModelForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['student_name','email','phone']
        widgets={
            'student_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student name'}),
            'email' :forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone' :forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone no.'}),
        }

class EnrollModelForm(forms.ModelForm):
    class Meta:
        model=Enrollment
        fields=['student_name','course_name']
        widgets={
            'student_name' : forms.Select(attrs={'class': 'form-select'}),
            'course_name' :forms.Select(attrs={'class': 'form-select'}),
        }



class TrainerModelForm(forms.ModelForm):
    class Meta:
        model=Trainer
        fields=['trainer_name','email','phone']
        widgets={
            'trainer_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Trainer name'}),
            'email' :forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone' :forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone no.'}),
        }
        


