from django.db import models
from accounts.models import Myuser
# Create your models here.
class IncidentHistory(models.Model):
    user = models.ForeignKey(
       Myuser,
        on_delete=models.CASCADE,
        related_name="incidents"
    )
    incident_date = models.DateField(auto_now_add=True)
    incident_time = models.TimeField(auto_now_add=True)
    confidence = models.FloatField()
    predicted_class = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.predicted_class} ({self.confidence})"