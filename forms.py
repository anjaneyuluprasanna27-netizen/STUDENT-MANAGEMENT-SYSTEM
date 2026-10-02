from django import forms
from django.contrib.auth.models import User
from .models import Student


class StudentRegisterForm(forms.Form):
    """Used for self-registration by a student (creates User + Student)."""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    roll_number = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=15, required=False)
    course = forms.ChoiceField(choices=Student.COURSE_CHOICES)
    address = forms.CharField(widget=forms.Textarea, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_roll_number(self):
        roll_number = self.cleaned_data['roll_number']
        if Student.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError("A student with this roll number already exists.")
        return roll_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class StudentAdminForm(forms.ModelForm):
    """Used by the admin to add/edit a student's profile fields."""
    class Meta:
        model = Student
        fields = ['roll_number', 'phone', 'course', 'address', 'date_of_birth']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class StudentCreateByAdminForm(forms.Form):
    """Used by the admin to create a brand new student (User + Student)."""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    roll_number = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=15, required=False)
    course = forms.ChoiceField(choices=Student.COURSE_CHOICES)
    address = forms.CharField(widget=forms.Textarea, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_roll_number(self):
        roll_number = self.cleaned_data['roll_number']
        if Student.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError("A student with this roll number already exists.")
        return roll_number
