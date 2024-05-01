from datetime import datetime
from django.db import models

# Create your models here.
class Telemetry(models.Model):
    token = models.CharField(max_length=128)
    ressived_time = models.DateTimeField(default=lambda: datetime.now().isoformat())
    data = models.JSONField()

class Devices(models.Model):
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    owner = models.IntegerField()
    token = models.CharField(max_length=128)