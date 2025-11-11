# from .forms import UploadForm
# from rest_framework.authtoken.models import Token
import os
from django.shortcuts import render, redirect
from django.conf import settings
from .models import SecureFile
from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, FileUploadForm
from django.contrib.auth.models import User
from django.contrib import messages


def get_fernet():
    key = settings.FERNET_KEY
    # key = token
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

def index(request):
    files = SecureFile.objects.all()
    return render(request, "index.html", {"files": files})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            # Set a success message
            messages.success(request, 'Registration successful! You can now log in.')
            # Redirect to login page
            return redirect('login')  # Use your actual login URL name
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


from django.http import HttpResponse
from django.http import HttpResponseBadRequest, Http404
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)

from django.http import HttpResponseForbidden

@login_required
def download_decrypt(request, pk):
    try:
        # Get the file object or return 404
        obj = get_object_or_404(SecureFile, pk=pk)

        # ✅ Only allow access if the logged-in user is the receiver
        if request.user != obj.uploaded_by:
            return HttpResponseForbidden("You are not authorized to download this file.")

        # Full path to the encrypted file
        path = os.path.join(settings.MEDIA_ROOT, obj.encrypted_file.name)

        # Check if file exists
        if not os.path.exists(path):
            logger.warning(f"File not found on disk: {path}")
            return HttpResponseNotFound("Encrypted file not found.")

        # Read and decrypt file
        with open(path, "rb") as fh:
            encrypted_data = fh.read()

        try:
            decrypted_data = get_fernet().decrypt(encrypted_data)
        except Exception as e:
            logger.error(f"Decryption failed for file {obj.pk}: {e}")
            return HttpResponseBadRequest("Invalid or corrupted encryption token.")

        # Return decrypted file as download
        response = HttpResponse(decrypted_data, content_type="application/octet-stream")
        response["Content-Disposition"] = f'attachment; filename="{obj.filename}"'
        return response

    except Http404:
        return HttpResponseNotFound("Secure file not found.")
    except Exception as e:
        logger.exception(f"Unexpected error during download_decrypt: {e}")
        return HttpResponse("Internal server error.", status=500)
