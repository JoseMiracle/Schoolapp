from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(NewUser)
admin.site.register(TeacherDetails)
admin.site.register(StudentDetails)
admin.site.register(Attendance)
admin.site.register(SubjectFile)
admin.site.register(Subjects)
admin.site.register(ClassesAndSubject)
admin.site.register(Announcement)
admin.site.register(Comments)
admin.site.register(AssignmentSolution)
admin.site.register(SessionInfo)
admin.site.register(Terms)
