from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from datetime import datetime
from django import forms


#from django.dispatch import receiver
# Create your models here.

class CustomManager(BaseUserManager):
    def create_user(self, email, first_name, gender, password = None, **other_fields):
        
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            gender = gender,
            **other_fields
            )
        user.is_active = True
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, first_name, gender, password = None , **other_fields):
        
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True'
            )
        
        return self.create_user(email, first_name, gender, password, **other_fields)

#MY CUSTOM MODEL
class NewUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField('Email Address', unique = True) 
    first_name = models.CharField(max_length = 150, blank = False)
    last_name = models.CharField(max_length = 150)
    other_name = models.CharField(max_length = 150)
    gender = models.CharField(max_length = 8, blank = False)
    position = models.CharField(max_length = 150)
    residence = models.CharField(max_length = 150)
    phone_no = models.IntegerField(blank = True, null = True)
    student_class = models.CharField(max_length = 10)
    is_staff = models.BooleanField(default = False)
    is_student = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)

    objects = CustomManager()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','gender']
    
    def __str__(self):
        return self.email

class SessionInfo(models.Model):
    session = models.CharField(max_length = 9)
    session_starts = models.DateTimeField()
    session_ends = models.DateTimeField()
    no_of_terms = models.IntegerField()
    current_term = models.IntegerField(null = True, blank = True)
    is_session_active = models.BooleanField(default = False)

    def __str__(self):
        return self.session

class Terms(models.Model):
    session = models.ForeignKey(SessionInfo, on_delete = models.CASCADE)
    term = models.IntegerField()
    term_starts = models.DateTimeField()
    term_ends = models.DateTimeField()
    active_term = models.BooleanField(default = False)

    def __str__(self):
        return str(self.term)

class Subjects(models.Model):
    all_subjects = models.CharField(max_length = 30)

    def __str__(self):
        return self.all_subjects

class TeacherDetails(models.Model):
    session = models.ForeignKey(SessionInfo, on_delete = models.CASCADE)
    is_teacher = models.BooleanField(default = False)
    name = models.CharField(max_length = 100)
    subjects = models.ManyToManyField(Subjects)
    assignedClass = models.CharField(max_length = 20, null = True , blank = True)
    email = models.EmailField(max_length = 300, unique = True)
    teacher_residence = models.CharField(max_length = 250)
    teacher_slug = models.SlugField(max_length = 250)

    def __str__(self):
        return self.email
        
class ClassesAndSubject(models.Model):
    class_name = models.CharField(max_length = 30)
    class_major_subjects = models.ManyToManyField(Subjects)

    def __str__(self):
        return self.class_name

class StudentDetails(models.Model):
    #subject = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    session = models.ForeignKey(SessionInfo, on_delete = models.CASCADE)
    student_class = models.CharField(max_length = 10)
    teacher_details = models.ForeignKey(TeacherDetails, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 300 , unique = True)
    subjects = models.ManyToManyField(Subjects, null = True, blank = True)
    student_residence = models.CharField(max_length = 250)
    student_slug = models.SlugField(max_length = 200)

    def __str__(self): 
        return self.name

    
class Attendance(models.Model):
    student_name = models.CharField(max_length = 100 )
    className = models.CharField(max_length = 10)
    is_present = models.BooleanField(default = False)
    date = models.DateTimeField(default = datetime.now().date())

    def __str__(self):
        return self.student_name

class Announcement(models.Model):#YYet to be completed
    announcement_details = models.TextField(max_length = 1000 )
    announcement_date = models.DateTimeField()
    announcement_deadline = models.DateTimeField()

    def __str__(self):
        return self.announcement_details


class SubjectFile(models.Model):
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    teacher_details = models.ForeignKey(TeacherDetails, on_delete=models.CASCADE, to_field = 'email')
    file_title = models.CharField(max_length = 200)
    kind_of_file = models.CharField(max_length = 20)
    week = models.CharField(max_length = 10)
    subject_files = models.FileField()
    date_uploaded = models.DateTimeField(default = datetime.now())
    deadline_date = models.DateTimeField(default = datetime.now(), null = True, blank = True)
    deadline_time = models.TimeField(default = datetime.now() ,null = True, blank = True)
    term = models.ForeignKey(Terms, on_delete = models.CASCADE)

    def __str__(self):
        return self.file_title

    def delete(self, *args, **kwargs):
        self.subject_files.delete()
        super().delete(*args, **kwargs)

class Comments(models.Model):
    subject_file = models.ForeignKey(SubjectFile, on_delete = models.CASCADE)
    comment = models.CharField(max_length = 1000)
    commenter_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.comment
class AssignmentSolution(models.Model):
    subject_file = models.ForeignKey(SubjectFile, on_delete = models.CASCADE)
    student_email = models.CharField(max_length = 100)
    solution_file = models.FileField()
    score = models.IntegerField(null = True, blank = True)
    number_of_submission = models.IntegerField(null = True, default = 0)
    def __str__(self):
        return self.student_email


#@receiver(post_save, sender = User)
#def create_profile(sender, instance, created, **kwargs):
    
 #   if created:
  #      #userProfile = Profile.objects.create(gender = gender, position = position, residence = residence, phoneno = phoneno)
   #     Profile.objects.create(user=instance)
    #    print('Profile created')
#post_save.connect(create_profile, sender=User)

#def update_profile(sender, instance, created, **kwargs):
 #   if created == False:
  #      instance.profile.save()
   #     print('profile updated')
#post_save.connect(update_profile, sender = User)

