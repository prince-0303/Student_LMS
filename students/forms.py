from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
from django.core.mail import send_mail
from django.conf import settings

# -------------------------------
#  Student Registration Form
# -------------------------------
class StudentRegistrationForm(UserCreationForm):
    roll_number = forms.CharField(max_length=20, required=False)
    department = forms.CharField(max_length=50, required=False)
    year = forms.CharField(max_length=10, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'username',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'given-name',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'family-name',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'autocomplete': 'email',
                'placeholder': 'Email address'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Confirm password'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Student.objects.create(
                user=user,
                roll_number=self.cleaned_data.get('roll_number'),
                department=self.cleaned_data.get('department'),
                year=self.cleaned_data.get('year'),
                profile_picture=self.cleaned_data.get('profile_picture')
            )

            subject = "Welcome to Student LMS 🎓"
            message = f"Hello {user.first_name},\n\nWelcome to Student LMS! Your account has been successfully created.\n\nYou can now log in and start exploring your dashboard.\n\nBest regards,\nStudent LMS Team"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return user


# -------------------------------
#  Student Profile Form
# -------------------------------
class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ['roll_number', 'department', 'year', 'profile_picture']
        widgets = {
            'roll_number': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Roll number'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'organization',
                'placeholder': 'Department'
            }),
            'year': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Year'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


# -------------------------------
#  Password Reset Form
# -------------------------------
class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'placeholder': 'Enter new password'
        }),
        min_length=8
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'placeholder': 'Confirm new password'
        }),
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data