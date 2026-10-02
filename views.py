from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Student
from .forms import StudentRegisterForm, StudentAdminForm, StudentCreateByAdminForm


def home(request):
    return render(request, 'students/home.html')


# ---------------------------------------------------------------------------
# Auth: registration / login / logout
# ---------------------------------------------------------------------------

def register_view(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data.get('last_name', ''),
            )
            Student.objects.create(
                user=user,
                roll_number=data['roll_number'],
                phone=data.get('phone', ''),
                course=data['course'],
                address=data.get('address', ''),
                date_of_birth=data.get('date_of_birth'),
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'students/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------------------------------------------------------------------
# Student-facing views
# ---------------------------------------------------------------------------

@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'students/student_dashboard.html', {'student': student})


# ---------------------------------------------------------------------------
# Admin-facing views (staff only)
# ---------------------------------------------------------------------------

def staff_required(user):
    return user.is_authenticated and user.is_staff


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view the admin dashboard.")

    query = request.GET.get('q', '').strip()
    students = Student.objects.select_related('user').all()
    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(course__icontains=query)
        )

    return render(request, 'students/admin_dashboard.html', {
        'students': students,
        'query': query,
        'total_count': Student.objects.count(),
    })


@login_required
def add_student(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        form = StudentCreateByAdminForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data.get('last_name', ''),
            )
            Student.objects.create(
                user=user,
                roll_number=data['roll_number'],
                phone=data.get('phone', ''),
                course=data['course'],
                address=data.get('address', ''),
                date_of_birth=data.get('date_of_birth'),
            )
            messages.success(request, 'Student added successfully.')
            return redirect('admin_dashboard')
    else:
        form = StudentCreateByAdminForm()
    return render(request, 'students/add_student.html', {'form': form})


@login_required
def edit_student(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentAdminForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = StudentAdminForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})


@login_required
def delete_student(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.user.delete()  # cascades to Student
        messages.success(request, 'Student deleted successfully.')
        return redirect('admin_dashboard')
    return render(request, 'students/confirm_delete.html', {'student': student})


@login_required
def view_student(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/view_student.html', {'student': student})
