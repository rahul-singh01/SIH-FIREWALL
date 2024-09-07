# api/models/log_models.py

from django.db import models

class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ['-timestamp']
