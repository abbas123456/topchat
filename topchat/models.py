from django.db import models

class HoldingPageNotification(models.Model):
    email_address = models.EmailField()
    
