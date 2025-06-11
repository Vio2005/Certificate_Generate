# Certificate_Generate
student=Student.objects.count()
        trainer=Trainer.objects.count()
        course=Course.objects.count()
        active_enrollments = Enrollment.objects.filter(status=True).count()
        courselist=Course.objects.all()
        trainer_obj=Trainer.objects.all()
        context={"student":student,"trainer":trainer,"course":course,"active_enrollments":active_enrollments,"courselist":courselist,"trainer_obj":trainer_obj}
        return render(request,'homepage.html',context)