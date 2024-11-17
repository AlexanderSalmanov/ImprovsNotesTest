from django.db import models
from django.conf import settings


class Notes(models.Model):
    title = models.CharField(max_length=128, null=False)
    content = models.TextField(default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes"
    )

    def __str__(self):
        return f"<Note {self.id}>"

    def __repr__(self):
        return f"<Note {self.id}>"
    