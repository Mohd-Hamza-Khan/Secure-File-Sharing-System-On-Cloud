import os
from django.shortcuts import render, redirect
from django.conf import settings
from .models import SecureFile
from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, FileUploadForm
from django.contrib.auth.models import User
from django.contrib import messages
import re # import regX module to use search function for special character


def get_fernet():
    key = settings.FERNET_KEY
    # key = token
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

@login_required
def index(request):
    files = SecureFile.objects.all()
    return render(request, "index.html", {"files": files})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            createpassword = form.cleaned_data['password']
            confirmpassword = form.cleaned_data.get('confirm_password')

            # Password match check
            if createpassword != confirmpassword:
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html', {'form': form})
            
            # Password length check
            if len(createpassword) < 8:
                messages.error(request, "Password should be at least 8 characters long.")
                return render(request, 'register.html', {'form': form})
            
            # Password strength check (special character)
            if bool(re.search('^[a-zA-Z0-9]*$', createpassword)):
                messages.warning(request, "Very weak password — add at least one special character.")
                return render(request, 'register.html', {'form': form})
            
            # If all checks pass — create user
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=createpassword
            )
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['encrypted_file']
            receiver = form.cleaned_data['uploaded_by']
            raw_data = uploaded_file.read()

            # Encrypt the file content
            encrypted_data = get_fernet().encrypt(raw_data)

            # Create encrypted directory if it doesn't exist
            encrypted_dir = os.path.join(settings.MEDIA_ROOT, "encrypted")
            os.makedirs(encrypted_dir, exist_ok=True)

            # Generate encrypted file path
            encrypted_filename = uploaded_file.name + ".enc"
            save_path = os.path.join(encrypted_dir, encrypted_filename)

            # Write the encrypted data to a file
            with open(save_path, "wb") as out_file:
                out_file.write(encrypted_data)

            # Save the file record to the model
            relative_path = f"encrypted/{encrypted_filename}"
            SecureFile.objects.create(
                filename=uploaded_file.name,
                uploaded_by=receiver,
                encrypted_file=relative_path
            )

            return redirect("index")
    else:
        form = FileUploadForm()

    return render(request, 'file_upload.html', {'form': form})


def render_error(request, message, status=400):
    """Render a centralized error page with a custom message."""
    context = {"message": message}
    return render(request, "error.html", context, status=status)

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
import logging
from django.contrib.auth import logout


logger = logging.getLogger(__name__)


@login_required
def download_decrypt(request, pk):
    try:
        obj = get_object_or_404(SecureFile, pk=pk)

        if request.user != obj.uploaded_by:
            return render_error(request, "You are not authorized to download this file.", status=403)

        path = os.path.join(settings.MEDIA_ROOT, obj.encrypted_file.name)
        if not os.path.exists(path):
            logger.warning(f"File not found on disk: {path}")
            return render_error(request, "Encrypted file not found.", status=404)

        with open(path, "rb") as fh:
            encrypted_data = fh.read()

        try:
            decrypted_data = get_fernet().decrypt(encrypted_data)
        except Exception as e:
            logger.error(f"Decryption failed for file {obj.pk}: {e}")
            return render_error(request, "Invalid or corrupted encryption token.", status=400)

        response = HttpResponse(decrypted_data, content_type="application/octet-stream")
        response["Content-Disposition"] = f'attachment; filename="{obj.filename}"'
        return response

    except Http404:
        return render_error(request, "Secure file not found.", status=404)

    except Exception as e:
        logger.exception(f"Unexpected error during download_decrypt: {e}")
        return render_error(request, "Internal server error.", status=500)
    
def custom_404_view(request, exception):
    return render_error(request, "Page not found.", status=404)

def custom_500_view(request):
    return render_error(request, "Internal server error.", status=500)

def logout_view(request):
    if request.method in ["POST", "GET"]:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')