from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest, CustomUser
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.core.paginator import Paginator



def choice_page(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    return render(request, 'choice.html')

from django.contrib import messages

def student_login(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    if request.user.is_authenticated:
        return redirect('student_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_student:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid student credentials.')
    return render(request, 'login_student.html')


def teacher_login(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    if request.user.is_authenticated:
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_teacher:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Invalid teacher credentials.')
    return render(request, 'login_teacher.html')



@login_required
def student_dashboard(request: HttpRequest):
    if not request.user.is_student:
        return render(request, 'access_denied.html', status=403)
    
    leaves_list = LeaveRequest.objects.filter(student=request.user).order_by('-from_date')
    paginator = Paginator(leaves_list, 6)  # Show 6 leave entries per page
    page_number = request.GET.get('page')
    leaves = paginator.get_page(page_number)

    return render(request, 'dashboard_student.html', {'leaves': leaves})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import LeaveRequest, CustomUser
from django.db.models import Count


@login_required
def teacher_dashboard(request):
    teacher = request.user
    students = CustomUser.objects.filter(class_id=teacher.class_id, is_student=True)

    # Count leaves for those students
    leave_counts = LeaveRequest.objects.filter(student__in=students) \
        .values('student') \
        .annotate(total=Count('id'))

    # Build dict of student_id -> total
    count_dict = {item['student']: item['total'] for item in leave_counts}

    # Create list of (student_obj, total_leaves), even if total is 0
    leave_summary = [(student, count_dict.get(student.id, 0)) for student in students]

    return render(request, 'teacher_dashboard.html', {
        'leave_summary': leave_summary,
    })

from .forms import LeaveRequestForm

@login_required
def apply_leave(request):
    if not request.user.is_student:
        return render(request, 'access_denied.html', status=403)

    if request.method == 'POST':
        post_data = request.POST.copy()

        # Handle single_day checkbox
        if post_data.get('single_day') == 'on':
            post_data['to_date'] = post_data.get('from_date')

        form = LeaveRequestForm(post_data)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = request.user
            leave.save()
            return redirect('student_dashboard')
    else:
        form = LeaveRequestForm()

    return render(request, 'apply_leave.html', {'form': form})




from django.core.paginator import Paginator

@login_required
def manage_leave_requests(request):
    if not request.user.is_teacher:
        return render(request, 'access_denied.html', status=403)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        message = request.POST.get('review_msg')
        leave_request = LeaveRequest.objects.get(id=request_id)

        if action in ['approved', 'rejected']:
            leave_request.status = action
            leave_request.review_msg = message
            leave_request.reviewed_by = request.user
            leave_request.save()

    request_list = LeaveRequest.objects.filter(
        student__class_id=request.user.class_id,
        status='pending'
    ).order_by('-from_date')
    
    paginator = Paginator(request_list, 5)
    page_number = request.GET.get('page')
    requests = paginator.get_page(page_number)

    return render(request, 'manage_requests.html', {'requests': requests})

@login_required
def past_leave_requests(request):
    if not request.user.is_teacher:
        return render(request, 'access_denied.html', status=403)

    # ✅ Only show requests that are already reviewed (not pending)
    requests = LeaveRequest.objects.filter(
        student__class_id=request.user.class_id
    ).exclude(status='pending')

    return render(request, 'past_requests.html', {'requests': requests})



@login_required
def profile_page(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES['profile_pic']
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        return redirect('profile')
    
    if request.user.is_teacher:
        return render(request, 'update_profile_teacher.html')
    elif request.user.is_student:
        return render(request, 'profile.html')
    else:
        return render(request, 'access_denied.html')


@login_required
def dashboard(request):
    if request.user.is_teacher:
        return redirect('teacher_dashboard')
    elif request.user.is_student:
        return redirect('student_dashboard')
    return redirect('choice')

from django.contrib.auth import logout

from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.shortcuts import redirect

@require_POST
def user_logout(request):
    logout(request)
    return redirect('choice_page')  # Redirect to landing/login/choice page

from django.shortcuts import redirect

from django.views.decorators.cache import never_cache

@never_cache
def choice_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # or redirect accordingly
    return render(request, 'choice.html')





