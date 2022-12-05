from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from datetime import datetime
from django.urls import reverse


def registration(request):

    if request.method == "POST":
        firstName = request.POST['firstname']
        lastName = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        gender = request.POST['gender']
        otherName = request.POST['othername']
        position = request.POST['position']
        className = request.POST['class'].upper()
        residence = request.POST['residence']
        phone_no = request.POST['phoneno']

        #This section does authentication
        if password == password1:
            if NewUser.objects.filter(email = email).exists():
                messages.info(request,'Email exists')
                return redirect('registration')
            else:
                user = NewUser.objects.create_user(
                    first_name = firstName, 
                    last_name = lastName,
                    other_name = otherName, 
                    email = email, 
                    password = password, 
                    residence = residence, 
                    gender = gender, 
                    position = position,
                    student_class = className, 
                    phone_no = phone_no)      

                userLogin = auth.authenticate(email = email, password = password)
                auth.login(request,userLogin)
                return redirect('welcome')

        elif password != password1:
            messages.info(request,"passwords not equal")
            return redirect('registration')
        
    return render(request, 'register.html')

def login(request):

    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(email = email, password= password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('welcome')

        else:
            messages.info(request,"This details provided doesn't exist, Pls check the details provided, and login again. ")
            return redirect('login')

    return render(request,'login.html')


#This view is to Welcomes user.
def welcome(request):
    #print(ClassesAndSubject.objects.get(class_name = 'SS1').class_major_subjects.all())
    current_session = SessionInfo.objects.get(is_session_active = True)
    current_term = Terms.objects.get(active_term = True)
    email = request.user.email
    userName = NewUser.objects.get(email = email)
    unApprovedUsers = NewUser.objects.all().filter(is_staff = False, is_student = False)  
    is_class_teacher = ""
        
    if userName.is_superuser:
        is_class_teacher = None
        
    elif userName.is_staff:
        is_class_teacher = TeacherDetails.objects.get(email = email).assignedClass
        print(f"Assigned under elif condition: {is_class_teacher}")
    
    today_date = datetime.now().date()
    no_of_present_student = Attendance.objects.filter(date = today_date, is_present = True).count()
    no_of_absent_student = Attendance.objects.filter(date = today_date, is_present = False).count()
    all_available_subject = Subjects.objects.all()

    context = {
        'userName': userName, 
        'unApprovedUsers' : unApprovedUsers, 
        'is_class_teacher' : is_class_teacher,
        'no_of_present_student' : no_of_present_student,
        'no_of_absent_student' : no_of_absent_student,
        'all_available_subject' : all_available_subject, 
        'current_session' : current_session,
        'current_term' : current_term
        }
    return render(request,'welcome.html', context)

#This is used for creating session
def create_session(request):

    if request.method == 'POST':
        session = request.POST['session']
        session_starts = request.POST['session_starts']
        session_ends = request.POST['session_ends']
        no_of_terms = request.POST['no_of_terms']
        session_details = SessionInfo.objects.create(
            session = session,
            session_starts = session_starts,
            session_ends = session_ends,
            no_of_terms = no_of_terms,
        )
        return redirect('school_sessions' )

    number_of_session = SessionInfo.objects.all().count()
    context = {
        'number_of_session' : number_of_session
    }
    return render(request, 'create_session_page.html', context)
#This is used in starting session
def start_session(request, session_id):
    ##This is used in deactivating any pre-existing active term 
    def deactivation_of_active_session():
        if SessionInfo.objects.filter(is_session_active = True):
            existing_session = SessionInfo.objects.get(is_session_active = True)
            existing_session.active_session = False
            existing_session.save()
            return True

        else:
            return False
    #Then activates other session created
    if deactivation_of_active_session() == True:
        sessionId = SessionInfo.objects.get(id = session_id)
        sessionId.is_session_active = True
        sessionId.save()
        return redirect('session_full_view', sessionId)
    
    ##This activate a first or new session created on the web 
    else:
        sessionId = SessionInfo.objects.get(id = session_id)
        sessionId.is_session_active = True
        sessionId.save()
        return redirect('session_full_view', sessionId)
    
    
#This is view the whole session created
def session_info(request): 
    number_of_session = SessionInfo.objects.all().count()
    if number_of_session >= 1:
        school_sessions = SessionInfo.objects.all()
        context = {
        'school_sessions' : school_sessions,
        }
        return render(request, 'session_page.html', context)
    
    else:
        return redirect('create_session')
    
#This is to view a session in full
def session_full_view(request, session):
    current_session = SessionInfo.objects.get(session = session)
    get_session_terms = ' '
    get_session_active_term = ' '
    

    def isTermAvailable(): #This checks if term is available
        if Terms.objects.all().count() == 0:
            return False
        elif Terms.objects.all().count() > 0:
            return True
    if isTermAvailable() == True:
        session_terms = Terms.objects.filter(session = current_session).order_by("-term")
        get_session_terms = session_terms 
    else:
        get_session_terms = "None"

    #This checks if a term is active
    def isActiveTerm():
        if Terms.objects.filter(active_term = True):
            return True
        else:
            return False

    if isActiveTerm() == True:
        session_active_term = Terms.objects.get(session = current_session, active_term = True) 
        get_session_active_term = session_active_term
    else:
        get_session_active_term = "None"


    context = {
        'current_session' : current_session,
        'session_terms' : get_session_terms,
        'session_active_term' : get_session_active_term
    }
    return render(request, 'session_full_view.html', context)

def term(request): ##This is used in creating a term
    if request.method == 'POST':
        new_term = request.POST['new_term'] 
        term_starts = request.POST['term_starts']
        term_ends = request.POST['term_ends']
        session = request.POST['session']
        current_session = SessionInfo.objects.get(session = session)

        session_term = Terms.objects.create(
            session = current_session, term = new_term, 
            term_starts = term_starts, 
            term_ends = term_ends
            )
        return JsonResponse({'status' : 'saved'})

 
def start_term(request, term_id): ##This is used in starting a term

    def deactivation_of_active_term(): ##This is used in deactivating any pre-existing active term 
            if Terms.objects.filter(active_term = True):
                existing_term = Terms.objects.get(active_term = True)
                existing_term.active_term = False
                existing_term.save()
                return True
    
            else:
                return False

    if deactivation_of_active_term() == True:
        termId = Terms.objects.get(id = term_id)
        termId.active_term = True
        termId.save()
        return redirect('session_full_view', termId.session)

    ##This activate a first new term 
    else:
        termId = Terms.objects.get(id = term_id)
        termId.active_term = True
        termId.save()
        return redirect('session_full_view', termId.session)
        

def delete_term(request, term_id):
    term = Terms.objects.get(id = term_id)
    term.delete()
    return redirect('session_full_view', term.session)



#This is to approve major subjects for each classes
def classes_and_subject(request):
    if request.method == 'POST':
        class_name = request.POST['class_name']
        all_class_subjects = request.POST.getlist('class_subjects')
        
        #This checks if a class exits:
        if ClassesAndSubject.objects.filter(class_name = class_name).exists():
            messages.info(request, f'{class_name} already added.')
            return redirect('schoolclasses')
        
        else:
            school_class = ClassesAndSubject.objects.create(class_name = class_name)
            major_class_subjects = [class_subject for class_subject in all_class_subjects]
            print(major_class_subjects)
            exact_class = ClassesAndSubject.objects.get(class_name__exact = class_name)

            for each_major_subject in major_class_subjects:
                major_subject = Subjects.objects.get(all_subjects = each_major_subject)
                exact_class.class_major_subjects.add(major_subject)
            return redirect('classes_and_subject') 
    
    all_school_subjects = Subjects.objects.all()
    school_classes_and_subjects = ClassesAndSubject.objects.all()
    context = {
        'all_school_subjects': all_school_subjects,
        'school_classes_and_subjects': school_classes_and_subjects
        }
    return render(request, 'classes_and_subject.html', context)


def approve_users(request, ):
    ...
#This is allows the admin to approve unauthorized staff or student
def unapprovedusers(request):
    if request.method == 'POST':
        session = SessionInfo.objects.get(is_session_active = True)
        unapproved_id = request.POST['unapproveduser_id']
        selected_teacher_subjects = request.POST.getlist('chosensubject')  

        to_be_approveduser_id = NewUser.objects.get(pk = unapproved_id)
        to_be_approveduser_fullname = to_be_approveduser_id.first_name + " " + to_be_approveduser_id.last_name + " " + to_be_approveduser_id.other_name
        to_be_approveduser_email = to_be_approveduser_id.email
        to_be_approveduser_residence = to_be_approveduser_id.residence
        user_slug = '-'.join(to_be_approveduser_fullname.split(' ', 3)) #This is to have a slug

        #This confirm that to_be_approved user is a staff
        if to_be_approveduser_id.position == 'STAFF':
            to_be_approveduser_id.is_staff = True
            
            new_teacher = TeacherDetails.objects.create(
                session = session,
                name = to_be_approveduser_fullname,
                assignedClass = 'NONE',
                email =  to_be_approveduser_email, is_teacher = True,
                teacher_residence = to_be_approveduser_residence,
                teacher_slug = user_slug
                )
            
            teacher = TeacherDetails.objects.get(name = to_be_approveduser_fullname)
            all_subjects_for_teacher = [eachsubject for eachsubject in selected_teacher_subjects]
            for each_subject in all_subjects_for_teacher:
                each_subject_id = Subjects.objects.get(all_subjects = each_subject)
                teacher.subjects.add(each_subject_id)
            

        elif to_be_approveduser_id.position == 'STUDENT':
            student_class = to_be_approveduser_id.student_class
            #student_class_and_subject = ClassesAndSubject.objects.get(class_name = student_class)
          
           
            #This is to check if the student has a class teacher already
            def is_student_class_teacher():
                if TeacherDetails.objects.filter(assignedClass__iexact = student_class).exists():
                    student_class_teacher = TeacherDetails.objects.get(assignedClass__iexact = student_class)
                    return student_class_teacher
                
                else:
                    return None

            to_be_approveduser_id.is_student = True
            major_class_subjects = ClassesAndSubject.objects.get(class_name = student_class).class_major_subjects.all()
            #to_be_approveduser_id.save() 

            new_student = StudentDetails.objects.create(
                session = session,
                student_class = student_class,
                name = to_be_approveduser_fullname,
                email = to_be_approveduser_email,
                teacher_details = is_student_class_teacher(),
                student_residence = to_be_approveduser_residence,
                student_slug = user_slug
            )

            for each_major_class_subject in major_class_subjects:
                new_student.subjects.add(each_major_class_subject)
                           
        to_be_approveduser_id.save()
        return redirect('unapprovedusers')
    
    email = request.user.email
    userName = NewUser.objects.get(email = email)
    unApprovedUsers = NewUser.objects.all().filter(is_staff = False, is_student = False)
    all_available_subject = Subjects.objects.all()        
    number_of_sessions = SessionInfo.objects.count()

    context = {
        'all_available_subject':all_available_subject,
        'userName':userName,
        'unApprovedUsers': unApprovedUsers,
        'number_of_sessions' : number_of_sessions 
    }

    return render(request, 'unapprovedusers.html', context) 

#This moves student to their table in the DB
#className = models.ForeignKey(ClassesAndSubject, on_delete = models.CASCADE, null = True)   
#This function create or add new subject to the list of subject offered by school

def subjectlist(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        
        if Subjects.objects.filter(all_subjects = subject).exists():
            messages.info(request, f'{subject} added before')
            return redirect('subjectlist')
        
        else:
            new_subject = Subjects.objects.create(all_subjects = subject)
            messages.info(request,f'{new_subject},has been added')
            return redirect('subjectlist')
    
    all_available_subject = Subjects.objects.all()
    return render(request,'school-subjects.html',{'all_available_subject':all_available_subject})


def remove_subject(request, subject):
    if request.method =='POST':
        subject = Subjects.objects.get(id = subject)
        subject.delete()
        return redirect('subjectlist')


#This return the details of all student in a school
def allstudent(request):
    allStudent = StudentDetails.objects.all()
    return render(request,'allstudent.html',{'allStudent':allStudent})

#This return the details of all the staff in a school
def allteacher(request):
    all_teacher = TeacherDetails.objects.all()
    return render(request,'allteacher.html',{'all_teacher':all_teacher})


#This shows the page where the admin assign each teacher to a class
def assignclassteacher(request):
    staff = TeacherDetails.objects.all()
    
    if request.method == "POST":
        assignedClass = request.POST['assignedClass']
        if TeacherDetails.objects.filter(assignedClass = assignedClass).exists():
            messages.info(request,f'Class {assignedClass} already assigned to a teacher')
            return redirect ('assignclassteacher')
    
        staffId = request.POST['staffId']
        thisstaff = TeacherDetails.objects.get(pk = int(staffId))
        thisstaff.assignedClass = assignedClass
        thisstaff.save()
        return redirect('assignclassteacher')

    return render(request,'assignclassteacher.html', {'staff':staff})

#This is to allow class teacher take attendance
def attendance(request):
    email = request.user.email
    teacher_to_student = TeacherDetails.objects.get(email = email).studentdetails_set.all()
    time = datetime.now().date()
    
    if request.method == "POST":

        student_name = request.POST['studentname']
        className = request.POST['classname']
        is_present = request.POST["is_present"]
        is_student_present = True
        current_date = datetime.now().date()
         
        #This next line checks if student attendance has been taken already
        if Attendance.objects.filter(student_name = student_name, date = str(current_date) ).exists():
            messages.info(request,f'{student_name} attendance has been taken already')
            return redirect('attendance')

        else:
            if is_present == 'present':
                is_student_present = True
            else:
                is_student_present = False 
            student_attendance = Attendance.objects.create(student_name = student_name, className = className, is_present = is_student_present)
            return redirect('attendance')
    return render(request, 'attendance.html', {'teacher_to_student': teacher_to_student, 'time': time})


#This is to  allow student add or remove subjects  
def subjectreview(request):
    email = request.user.email
    student_info = StudentDetails.objects.get(email = email) ##Find a good name later
    student_class = student_info.student_class
    class_subjects = ClassesAndSubject.objects.get(class_name = student_class).class_major_subjects.all()
    student_subjects = student_info.subjects.all()
    other_subjects = []
    school_subjects = Subjects.objects.all()
    
    for each_subject in school_subjects:
        
        if each_subject in class_subjects or each_subject in student_subjects:
            continue 
        else:
            other_subjects.append(each_subject)

    if request.method == 'POST':
        #This is used in adding selected subjects
       selected_subjects = request.POST.getlist('to_be_added_subjects')
    
       for each_selected_subject in selected_subjects:
            selected_subject = Subjects.objects.get(all_subjects = each_selected_subject)
            student_info.subjects.add(selected_subject)
      
        #This is used in removing subjects
       removed_subjects = request.POST.getlist('to_be_removed_subjects')
       print(removed_subjects)
      
      #This is used in removing subjects 
       for each_removed_subject in removed_subjects:
            removed_subject = Subjects.objects.get(all_subjects = each_removed_subject)
            student_info.subjects.remove(removed_subject)
       
       return redirect('subjectreview')

    context = {
        'student_subjects' : student_subjects,
        'other_subjects' : other_subjects,
        'class_subjects' :  class_subjects
    }

    return render(request, 'subjectreview.html', context )
 

#This is to schedule important announcement
def announcement(request): #Still an unfinished business
    if request.method == 'POST':
        announcement_details = request.POST['announcement_details']
        announcement_date = request.POST['announcement_date']
        announcement_deadline = request.POST['announcement_deadline']

        scheduled_announcement = Announcement.objects.create(
            announcement_details = announcement_details,
            announcement_date = announcement_date,
            announcement_deadline = announcement_deadline
            )
        
    all_scheduled_announcements = Announcement.objects.all() 

    context = {
            'all_scheduled_announcements': all_scheduled_announcements
            }

    return render(request, 'announcement.html', context) #Still an unfinished business

#This is used to view student or staff full profile
def profile(request, slug = None):
    #Yet to be filled with more info
    return render(request, 'profile.html')


def teacher_subjects(request):
    email = request.user.email
    teacher_email = TeacherDetails.objects.get(email = email)
    teacher_subjects = teacher_email.subjects.all()

    context = {
         'teacher_subjects' :  teacher_subjects,
    }
    return render(request,'teachersubjects.html', context)

def student_subject(request):
    student_email = request.user.email
    student_subjects = StudentDetails.objects.get(email = student_email).subjects.all()

    context = {
        'student_subjects' : student_subjects
    }

    return render(request, 'student_subject.html', context)

#This is for Uploading subject materials files
def files_upload(request, teacher_subject):

    if request.method == 'POST':
        kind_of_file = request.POST['subject_file'] #Find a better name
        uploader_email = request.POST['uploader_email']
        teacher_email = TeacherDetails.objects.get(email = uploader_email)
        week = request.POST['week']
        file_title = request.POST['title']
        deadline_date = request.POST['date']
        deadline_time = request.POST['deadline_time']
        latest_session_and_term = Terms.objects.latest('session')

        if SubjectFile.objects.filter(file_title = file_title, teacher_details = teacher_email).exists():
            messages.info(request, f"File name{file_title} exists") #Use Jquery
            return redirect('subject_files', teacher_subject)

        subject = Subjects.objects.get(all_subjects = teacher_subject)
        
        subject_files = request.FILES.getlist('subject_files')
        for subject_file in subject_files:

            subject_materials = SubjectFile.objects.create(
                file_title = file_title,
                kind_of_file = kind_of_file,
                teacher_details = teacher_email, 
                week = week,
                subject = subject, 
                subject_files = subject_file,
                deadline_date = deadline_date,
                deadline_time = deadline_time,
                term = latest_session_and_term
                )
        return redirect('subject_files', teacher_subject)
            
    return render(request,'subject_file_upload.html')


#This is to show the subject file
def subject_files(request, subject):
    subject = Subjects.objects.get(all_subjects = subject)
    subject_notes = SubjectFile.objects.all().filter(subject = subject, kind_of_file = 'subject_notes')
    assignments = SubjectFile.objects.all().filter(subject = subject, kind_of_file = 'assignment')
    all_weeks = []
    subject_note_weeks = [week.week for week in subject_notes]
    assignment_weeks = [week.week for week in assignments]
    all_weeks.extend(subject_note_weeks)
    all_weeks.extend(assignment_weeks)
    non_duplicate_weeks = []
   
    for each_week in all_weeks:
        if each_week in non_duplicate_weeks:
            continue
        else:
            non_duplicate_weeks.append(each_week)

    week_with_subject_notes = []
    week_without_subject_notes = []
    for week in non_duplicate_weeks:
        for subject_note in subject_notes:
            if week in subject_note.week:
                week_with_subject_notes.append(week)
            else:
                week_without_subject_notes.append(week)
    print(week_without_subject_notes)

    week_with_ass = [] 
    week_without_ass = []
    for week in non_duplicate_weeks:
        for assignment in assignments:
            if week in assignment.week:
                week_with_ass.append(week)
            else:
                week_without_ass.append(week)

    context = {
        'subject_notes' : subject_notes,
        'non_duplicate_weeks' : non_duplicate_weeks,
        'assignments' : assignments,
        'week_with_ass' : week_with_ass,
        'week_without_ass' : week_without_ass,
        'week_with_subject_notes' : week_with_subject_notes,
        'week_without_subject_notes' : week_without_subject_notes
    }

    return render(request,'subject_files.html', context)

#This returns a full_view for either assignment file or Subject notes file, and also do receive comments from user. 
def note_full_view(request, subject, note_title):
    email = request.user.email
    subject_name = Subjects.objects.get(all_subjects = subject)
    note_details = SubjectFile.objects.get(file_title = note_title, subject = subject_name)    
    all_note_comments = Comments.objects.filter(subject_file = note_details)
    user_full_name = request.user.first_name + " " + request.user.last_name + " " + request.user.other_name
    
    context = { 
        'note_details' : note_details,
        'all_note_comments' : all_note_comments,
        'user_full_name' : user_full_name
    }
    return render(request, 'note_view.html', context)

def assignment_full_view(request, subject, assignment_title):
    email = request.user.email
    subject_name = Subjects.objects.get(all_subjects = subject)

    assignment_details = SubjectFile.objects.get(file_title = assignment_title, subject = subject_name)
    all_note_comments = Comments.objects.filter(subject_file = assignment_details)
    
    def check_if_assignment():
        is_student_assignment = AssignmentSolution.objects.filter(
            student_email = email,
            subject_file = assignment_details
            ).exists() #normally this should find the solution
        
        if is_student_assignment:
            student_assignment = AssignmentSolution.objects.get(
                student_email = email,
                subject_file = assignment_details
                )
        
        elif is_student_assignment == False:
            student_assignment = 'NONE'
            
        return student_assignment
    
    student_assignment = check_if_assignment()   
    context = {
        'assignment_details' : assignment_details,
        'student_assignment' : student_assignment,
        'time' : datetime.now().time()
    }
    return render(request, 'assignment_page.html', context)


def assignment_solution_upload(request): #This is meant for student for uploading assignment solution(s)
    student_email = request.user.email
    if request.method == 'POST':
        subject = request.POST['subject']
        assignment_title = request.POST['assignment_title']
        teacher_email = request.POST['teacher_email']
        assignment_file = request.FILES.get('assignment_file')
    
        subject_name = Subjects.objects.get(all_subjects = subject)
        note_details = SubjectFile.objects.get(file_title = assignment_title, subject = subject_name)

        is_student_assignment = AssignmentSolution.objects.filter(
            student_email = student_email,
            subject_file = note_details).exists()
        
        if is_student_assignment:
            student_assignment_details = AssignmentSolution.objects.get(
                student_email = student_email,
                subject_file = note_details
            )
            student_assignment_details.solution_file = assignment_file
            student_assignment_details.number_of_submission += 1
            student_assignment_details.save()
        
        elif is_student_assignment == False:
            assignment = AssignmentSolution.objects.create(
                    subject_file = note_details,
                    solution_file = assignment_file, 
                    student_email = student_email,
                    number_of_submission = 1
                    )
            
    
        return redirect('assignment_full_view', subject, assignment_title)
            
def delete_solution_file(request):

    if request.method == "POST":
        solution_id = request.POST['assignment_solution_id']
        solution = AssignmentSolution.objects.get(id = solution_id)
        solution.solution_file = ' '
        solution.save()
        print('OK')
        return JsonResponse({'status' : 'deleted'})
        

#This is used in deleting subject file
def delete_file(request, subject_file_id):
   subject_file = SubjectFile.objects.get(pk = subject_file_id)
   subject = subject_file.subject
   subject_file.delete()
   return redirect('subject_files', subject)


#This is for teachers to view assignment submitted by student and score it. 
def all_assignment_solution(request, subject, assignment_title):
    if request.method == 'POST':
        score = request.POST['score']
        solution_id = request.POST['solution_id']
        solution = AssignmentSolution.objects.get(id = solution_id)
   
        solution.score = int(score)
        solution.save()
        return JsonResponse({
            'status' : 'saved'
            })

    user_email = request.user.email
    teacher_email = TeacherDetails.objects.get(email= user_email)     
    no_of_student_to_teacher = StudentDetails.objects.filter(teacher_details = teacher_email).count()
    subject = Subjects.objects.get(all_subjects = subject)
    assignment_details = SubjectFile.objects.get(file_title = assignment_title, subject = subject)
    assignment_solutions = AssignmentSolution.objects.filter(subject_file =  assignment_details)
    
    context = {
        'assignment_solutions' : assignment_solutions,
        'no_of_student_to_teacher' : no_of_student_to_teacher,
        'assignment_details' : assignment_details
    }
    return render(request, 'assignment_solutions.html', context )


def comment(request):
    email = request.user.email
    
    if request.method == 'POST':
        user_full_name = request.user.first_name + " " + request.user.last_name + " " + request.user.other_name
        note_title = request.POST['note_title']
        subject = request.POST['subject']
        comments = request.POST['comment']
        
        subject_name = Subjects.objects.get(all_subjects = subject)
        note_details = SubjectFile.objects.get(file_title = note_title, subject = subject_name)        
        save_comment = Comments.objects.create(
            comment = comments,
            commenter_name = user_full_name, 
            subject_file = note_details
            )
        return JsonResponse({
            'status' : 'saved'
        })


def delete_comment(request): #AJAX is needed here.
    if request.method == 'POST':
        note_title = request.POST['note_title']
        subject = request.POST['subject']
        comment_id = request.POST['comment_id']
        
        comment = Comments.objects.get(pk = comment_id)
        comment.delete()
        return JsonResponse({'status': 'deleted'})
        #return redirect('note_full_view', subject, note_title)


   

    
