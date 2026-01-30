from django.db import models

class Myuser(models.Model):
    u_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128,)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"