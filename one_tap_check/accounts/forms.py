from django import forms
from django.contrib.auth import get_user_model


class LogInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "type": "text",
        'id': 'email',
        'placeholder': 'email',
    }), label='')

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': "password",
        'id': 'password',
        'placeholder': 'password',
        'label': ''
    }), label='')

    CHOICES = (
        ('ADMIN', "Admin"),
        ('TEACHER', "Teacher"),
        ('STAFF', 'Staff')
    )

    role = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={
        "id": 'role',
        'name': 'role',
        'label': ''
    }), label='')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_model = get_user_model()

        if not user_model.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not associated with any account.")
        return email
