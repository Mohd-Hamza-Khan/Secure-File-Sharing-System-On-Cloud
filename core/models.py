from django.db import models
from django.contrib.auth.models import User

class SecureFile(models.Model):
    filename = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to='encrypted/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
