from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import SecureFile



class FileUploadForm(forms.ModelForm):
    uploaded_by = forms.ModelChoiceField(queryset=User.objects.all(), label="Select Receiver")

    class Meta:
        model = SecureFile
        fields = ['encrypted_file', 'uploaded_by']


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  # Remove help text

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data
