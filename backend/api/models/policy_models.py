# models/policy_models.py

from django.db import models

class Policy(models.Model):
    ACTION_CHOICES = [
        ('ALLOW', 'Allow'),
        ('DENY', 'Deny'),
        ('RESTRICT', 'Restrict'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='DENY')
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    protocol = models.CharField(max_length=10, blank=True)
    port = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.action})"

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
        ordering = ['-created_at']
