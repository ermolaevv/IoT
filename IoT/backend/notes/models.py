from datetime import datetime
from django.db import models

# Create your models here.
class Telemetry(models.Model):
    token = models.CharField(max_length=128)
    ressived_time = models.DateTimeField(default=lambda: datetime.now().isoformat())
    data = models.JSONField()
