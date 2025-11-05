from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        return redirect('student_dashboard')
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Student':
            return view_func(request, *args, **kwargs)
        return redirect('admin_dashboard')
    return wrapper