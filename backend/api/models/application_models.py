# models/application_models.py

from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ['name']
