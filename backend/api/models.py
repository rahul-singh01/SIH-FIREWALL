from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Policy(models.Model):
    application = models.ForeignKey(Application, related_name='policies', on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)
    protocol = models.CharField(max_length=50)
    action = models.CharField(max_length=50)  # e.g., ALLOW or DENY
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.domain} - {self.protocol} - {self.action}"

class Log(models.Model):
    application = models.ForeignKey(Application, related_name='logs', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.message}"

class Alert(models.Model):
    application = models.ForeignKey(Application, related_name='alerts', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(max_length=100)  # e.g., SECURITY, PERFORMANCE
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.alert_type} - {self.message}"
