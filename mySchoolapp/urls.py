from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('registration', views.registration, name ='registration'),
    path('login', views.login, name ='login'),
    path('welcome', views.welcome, name = 'welcome'),
    path('unapprovedusers', views.unapprovedusers, name = 'unapprovedusers'),
    path('school-sessions', views.session_info, name = 'session_info'),
    path('session-full-view/<session>', views.session_full_view, name = 'session_full_view'),
    path('term', views.term, name = 'term' ),
    #path('term_processes/<term_id>', views.term_processes, name='term_processes'),
    path('start_term/<term_id>', views.start_term, name = 'start_term'),
    path('delete-term/<term_id>', views.delete_term, name = 'delete-term'),
    path('create_session', views.create_session, name = 'create_session'),
    path('start_session/ <session>', views.start_session, name= "start_session" ),
    path('subjectlist', views.subjectlist, name ="subjectlist"),
    path('allstudent', views.allstudent, name = 'allstudent'),
    path('allteacher', views.allteacher, name = 'allteacher'),
    path('assignclassteacher', views.assignclassteacher, name = 'assignclassteacher'),
    path('attendance', views.attendance, name = 'attendance'),
    path('classes-subject', views.classes_and_subject, name = 'classes_and_subject'),
    path('subjectreview', views.subjectreview, name = 'subjectreview' ),
    path('announcement', views.announcement, name= 'announcement'),
    path('profile/<slug>', views.profile, name = 'profile'),
    path('teachersubjects', views.teacher_subjects, name = 'teacher_subjects' ),
    path('<teacher_subject>/files_upload', views.files_upload, name = 'files_upload'),
    path('<subject>/subject_files', views.subject_files, name = 'subject_files'),
    path('note_view/<subject>/<note_title>', views.note_full_view, name = 'note_full_view' ),
    path('student_subject', views.student_subject, name = 'student_subject'),
    path('delete-file/<subject_file_id>', views.delete_file, name = 'delete_file'),
    path('comment', views.comment, name = 'comment'),
    path('delete_comment', views.delete_comment, name = 'delete_comment'),
    path('assignment_solution_upload', views.assignment_solution_upload, name = 'assignment_solution_upload'),
    path('assignment_solutions/<subject>/<assignment_title>', views.all_assignment_solution, name = 'assignment_solutions'),
    path('delete-solution-file', views.delete_solution_file, name = 'delete_solution_file'),
    path('<subject>/assignment-page/<assignment_title>', views.assignment_full_view, name = 'assignment_full_view'),
    

    #path('<subject>/assignmentfiles', views.assignment_files, name = 'assignment_files') bfr 
    #path('<subject>/student_subject_files', views.student_subject_files, name = 'student_subject_files'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
