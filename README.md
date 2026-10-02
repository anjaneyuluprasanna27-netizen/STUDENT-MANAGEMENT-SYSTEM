# Student Management System

A full-stack Student Management System built with **Django**, **MySQL** (SQLite by default for
instant setup), and plain **HTML/CSS/JS** — built as a fresher interview portfolio project.

## Features

- **Student registration** — students self-register with roll number, course, phone, address, DOB
- **Student login** — session-based auth using Django's built-in auth system
- **Student dashboard** — logged-in students can view their own profile and course
- **Admin dashboard** — staff users can:
  - View all students in a table
  - **Search** students by name, email, roll number, or course
  - **Add** a new student
  - **View** full details of a student
  - **Update** a student's profile
  - **Delete** a student
- Django's built-in `/admin-panel/` is also wired up for the raw Django admin, separate from the
  custom-built admin dashboard at `/admin-dashboard/`.

## Tech Stack

- Backend: Python, Django
- Database: MySQL (SQLite pre-configured as a zero-setup fallback)
- Frontend: Django templates + HTML/CSS/JavaScript (no frontend framework)
- Auth: Django's built-in `User` model, extended with a `Student` profile (`OneToOneField`)

## Project Structure

```
student_management_system/
├── manage.py
├── requirements.txt
├── student_management_system/      # project settings, urls
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── students/                       # the main app
    ├── models.py                   # Student model
    ├── forms.py                    # registration & admin forms
    ├── views.py                    # all views (student + admin)
    ├── urls.py
    ├── admin.py                    # Django admin registration
    ├── templates/students/         # all HTML templates
    └── static/students/            # CSS & JS
```

## Setup Instructions

### 1. Install dependencies
```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Database
The project runs out of the box on **SQLite** — no extra setup needed. To switch to **MySQL**
(recommended if the interview specifically asks for MySQL):

1. Create a database:
   ```sql
   CREATE DATABASE student_management_db;
   ```
2. In `student_management_system/settings.py`, comment out the SQLite `DATABASES` block and
   uncomment the MySQL block, filling in your MySQL username/password.
3. Make sure `mysqlclient` is installed (`pip install mysqlclient`).

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create an admin (staff) user
```bash
python manage.py createsuperuser
```
This user will automatically be treated as an **admin** (because `is_staff=True`) and will be
redirected to the admin dashboard on login instead of the student dashboard.

### 5. Run the server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/`

## How the roles work

- Any user registered through the **public registration form** is a normal student
  (`is_staff=False`) → after login, lands on `/dashboard/` (their own profile).
- Any user created via `createsuperuser` or the Django admin with `is_staff=True` → after login,
  lands on `/admin-dashboard/` and can manage all students.
- There's a single login page (`/login/`) for both — the redirect after login is based on the
  `is_staff` flag, which is a common, clean way to implement role-based dashboards in Django.

## Possible Interview Talking Points

- Why `OneToOneField` from `Student` to Django's `User`: reuses Django's built-in, secure
  password hashing and auth system instead of storing raw passwords yourself.
- `select_related('user')` used in the admin dashboard query to avoid the N+1 query problem when
  displaying student names/emails that live on the related `User` row.
- Search uses Django's `Q` objects to filter across multiple fields with `OR` logic.
- `@login_required` + an `is_staff` check inside the view protects admin-only routes; could also
  be refactored into a custom decorator or `UserPassesTestMixin` for class-based views.
- Deleting a `Student` is done by deleting the related `User` (`on_delete=models.CASCADE`),
  keeping a single source of truth instead of two disconnected delete operations.

## Possible Extensions

- Add pagination to the admin student list
- Add a "Courses" model instead of a fixed choices list, so courses can be managed dynamically
- Add profile photo upload
- Add email verification on registration
- Convert to Django REST Framework + a JS frontend calling APIs (if the role wants API skills)
