# SECURE-FILE-SHARING-SYSTEM

Simple Django application to upload, store and share files in encrypted form.

## Overview
This project encrypts uploaded files (using Fernet symmetric encryption), saves the encrypted files to MEDIA_ROOT (under `encrypted/`), and stores file metadata in a `SecureFile` model. Users can upload files, view a list of encrypted files, and (when implemented) download/decrypt files they are allowed to access.

## Features
- File upload with server-side encryption (Fernet)
- Encrypted files saved under `MEDIA_ROOT/encrypted/`
- Metadata persisted in `SecureFile` model (filename, encrypted file path, uploader, timestamp)
- Basic user association (uploaded_by)

## Tech stack
- Python 3.12
- Django (project uses SQLite by default)
- cryptography (Fernet)

## Project layout (important files)
- core/models.py — SecureFile model
- core/views.py — upload_view, index, etc.
- core/forms.py — UploadForm
- settings.py — MEDIA_ROOT / MEDIA_URL and encryption key handling
- requirements.txt — project dependencies

## Quick setup (Windows)
1. Create and activate virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set environment variables (example):
   - In PowerShell:
     ```
     $env:DJANGO_SECRET_KEY="your_django_secret"
     $env:FERNET_KEY="your_base64_fernet_key"
     ```
   - Generate a Fernet key if needed:
     ```
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```

4. Make and apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Ensure MEDIA_ROOT exists or is configured in settings.py. Uploaded encrypted files will be stored under `MEDIA_ROOT/encrypted/`.

## Notes & troubleshooting
- If you see errors like `no such table: core_securefile` or missing columns (OperationalError), run `makemigrations` and `migrate`. If models changed after initial migrations, consider creating new migrations or resetting the DB in development.

## live project url :- https://secure-file-sharing-system-on-cloud.onrender.com/