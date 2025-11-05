from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Student
from .forms import StudentRegistrationForm, StudentProfileForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator



def home(request):
    return render(request, 'home.html')


# -----------------------------
#  Register View
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


# -----------------------------
#  Login View
# -----------------------------
@never_cache
def login_view(request):
    # 🚫 Prevent logged-in users from seeing login page
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('student_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('admin_dashboard' if user.is_staff else 'student_dashboard')
        messages.error(request, "Invalid username or password.")
        return redirect('login')

    form = AuthenticationForm()
    return render(request, 'login.html', { 'form': form })


# -----------------------------
#  Logout View
# -----------------------------
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# -----------------------------
#  Student Dashboard
# -----------------------------
@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')  # Prevent admin from accessing student dashboard
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student_dashboard.html', {'student': student})


# -----------------------------
#  Edit Profile
# -----------------------------
@login_required
def edit_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            # Update linked User model fields
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'edit_profile.html', {'form': form, 'student': student})


 

# -----------------------------
# admin dashboard
# -----------------------------

@staff_member_required
def admin_dashboard(request):
    query = request.GET.get('q', '').strip()

    # Fetch all students with related user data
    students_qs = Student.objects.select_related('user')
    if query:
        students_qs = students_qs.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(department__icontains=query) |
            Q(year__icontains=query)
        )
    students_qs = students_qs.order_by('user__username')

    paginator = Paginator(students_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {'students': page_obj})



@staff_member_required
def add_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Error adding student. Please check the form.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'add_student.html', {'form': form})



@staff_member_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('admin_dashboard')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'edit_student.html', {'form': form, 'student': student})



@staff_member_required
def block_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request, f"{user.username} has been blocked and cannot login.")
    else:
        messages.info(request, f"{user.username} is already blocked.")
    return redirect('admin_dashboard')

@staff_member_required
def unblock_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, f"{user.username} has been unblocked and can login now.")
    else:
        messages.info(request, f"{user.username} is already active.")
    return redirect('admin_dashboard')


@staff_member_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    user.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('admin_dashboard')
