from django.db import models

class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Aligning with 'created_at' in SQL
    level = models.CharField(max_length=50)  # Matches 'level VARCHAR(50) NOT NULL'
    message = models.TextField()  # Matches 'message TEXT NOT NULL'

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ['-created_at']  # Matches 'created_at TIMESTAMP'
