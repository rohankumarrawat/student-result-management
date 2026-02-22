from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'admin' or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif role == 'faculty':
        return redirect('faculty_dashboard')
    elif role == 'student':
        return redirect('student_dashboard')
    else:
        logout(request)
        messages.error(request, 'Role not authorized.')
        return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    total_students = StudentProfile.objects.count()
    total_subjects = Subject.objects.count()
    total_results = Result.objects.count()
    
    students = StudentProfile.objects.all()
    recent_results = Result.objects.select_related('student', 'subject').order_by('-id')[:10]
    
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_results': total_results,
        'students': students,
        'recent_results': recent_results,
    }
    return render(request, 'admin/dashboard.html', context)

import pandas as pd
from django.db import transaction
from .models import User, StudentProfile, Subject, Result

@login_required
def admin_upload_csv(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a csv file')
            return redirect('admin_upload_csv')
            
        try:
            df = pd.read_csv(csv_file)
            # Expected columns: roll_number, student_name, subject_code, subject_name, marks
            required_cols = ['roll_number', 'student_name', 'subject_code', 'subject_name', 'marks']
            if not all(col in df.columns for col in required_cols):
                messages.error(request, f'Missing required columns. Expected: {", ".join(required_cols)}')
                return redirect('admin_upload_csv')
            
            success_count = 0
            with transaction.atomic():
                for _, row in df.iterrows():
                    # Get or Create User and Student Profile
                    username = str(row['roll_number']).strip()
                    user, created = User.objects.get_or_create(
                        username=username,
                        defaults={
                            'first_name': str(row['student_name']).strip(),
                            'role': 'student'
                        }
                    )
                    if created:
                        user.set_password(username) # default password is roll number
                        user.save()
                        
                    student_profile, _ = StudentProfile.objects.get_or_create(
                        user=user,
                        defaults={'roll_number': username}
                    )
                    
                    # Get or Create Subject
                    subj_code = str(row['subject_code']).strip()
                    subject, _ = Subject.objects.get_or_create(
                        code=subj_code,
                        defaults={'name': str(row['subject_name']).strip()}
                    )
                    
                    # Update or Create Result
                    Result.objects.update_or_create(
                        student=student_profile,
                        subject=subject,
                        defaults={'marks': int(row['marks'])}
                    )
                    success_count += 1
                    
            messages.success(request, f'Successfully uploaded/updated {success_count} records.')
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            
        return redirect('admin_upload_csv')
        
    return render(request, 'admin/upload_csv.html')

from .forms import ResultForm

@login_required
def admin_manual_entry(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            # Check if this student/subject combination already exists (handled mostly by unique_together but good to catch gracefully)
            try:
                result.save()
                messages.success(request, 'Result saved successfully.')
                return redirect('admin_manual_entry')
            except Exception as e:
                messages.error(request, f'Failed to save result. Maybe it already exists? Error: {str(e)}')
    else:
        form = ResultForm()
        
    return render(request, 'admin/manual_entry.html', {'form': form})

@login_required
def faculty_dashboard(request):
    if request.user.role != 'faculty':
        return redirect('dashboard_redirect')
        
    # Get subjects assigned to this faculty
    subjects = Subject.objects.filter(faculty=request.user)
    
    # Get all results for these subjects
    results = Result.objects.filter(subject__in=subjects).select_related('student', 'subject')
    
    # Get class average marks per subject for this faculty
    subject_avgs = results.values('subject__name').annotate(avg_marks=Avg('marks'))
    
    labels = [item['subject__name'] for item in subject_avgs]
    avgs = [round(item['avg_marks'], 2) for item in subject_avgs]
    
    top_student = results.order_by('-marks').first()
    
    context = {
        'subjects': subjects,
        'results': results,
        'chart_labels': json.dumps(labels),
        'chart_avgs': json.dumps(avgs),
        'top_student': top_student,
    }
    
    return render(request, 'faculty/dashboard.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('dashboard_redirect')
        
    try:
        profile = request.user.student_profile
        results = Result.objects.filter(student=profile).select_related('subject')
        
        labels = []
        marks = []
        total_marks = 0
        max_marks = len(results) * 100
        
        for r in results:
            labels.append(r.subject.name)
            marks.append(r.marks)
            total_marks += r.marks
            
        avg_percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
        grade = 'F'
        if avg_percentage >= 90: grade = 'A+'
        elif avg_percentage >= 80: grade = 'A'
        elif avg_percentage >= 70: grade = 'B'
        elif avg_percentage >= 60: grade = 'C'
        elif avg_percentage >= 50: grade = 'D'
        
        context = {
            'results': results,
            'labels': json.dumps(labels),
            'marks': json.dumps(marks),
            'avg_percentage': round(avg_percentage, 2),
            'grade': grade,
            'total_scored': total_marks,
            'total_max': max_marks,
        }
    except StudentProfile.DoesNotExist:
        context = {'error': 'Student profile not found. Please contact administration.'}
        
    return render(request, 'student/dashboard.html', context)

import json
import pandas as pd
from django.db.models import Avg, Max, Min

@login_required
def admin_performance(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    df_results = pd.DataFrame(list(Result.objects.all().values('subject__name', 'marks', 'student__user__first_name', 'student__roll_number')))
    
    subject_labels = []
    subject_avgs = []
    
    top_students = []
    weak_students = []
    
    if not df_results.empty:
        # Subject averages
        subject_group = df_results.groupby('subject__name')['marks'].mean().reset_index()
        subject_labels = subject_group['subject__name'].tolist()
        subject_avgs = [round(m, 2) for m in subject_group['marks'].tolist()]
        
        # Overall student averages
        student_group = df_results.groupby(['student__user__first_name', 'student__roll_number'])['marks'].mean().reset_index()
        student_group = student_group.sort_values(by='marks', ascending=False)
        
        # Top 5 students
        top_students = student_group.head(5).to_dict(orient='records')
        
        # Bottom 5 students
        weak_students = student_group.tail(5).to_dict(orient='records')
        
        # Pass / Fail based on average
        passed = len(student_group[student_group['marks'] >= 40])
        failed = len(student_group[student_group['marks'] < 40])
        pass_fail_data = [passed, failed]
    else:
        pass_fail_data = [0, 0]
        
    context = {
        'subject_labels': json.dumps(subject_labels),
        'subject_avgs': json.dumps(subject_avgs),
        'top_students': top_students,
        'weak_students': weak_students,
        'pass_fail_data': json.dumps(pass_fail_data)
    }
    
    return render(request, 'admin/performance.html', context)
