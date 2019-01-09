from django.db import models

# Create your models here.

from django.db import models

# File model contains a file, a remark and a timestamp
class File(models.Model):
  file = models.FileField(blank=False, null=False)
  remark = models.CharField(max_length=20)
  timestamp = models.DateTimeField(auto_now_add=True)