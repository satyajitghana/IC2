from rest_framework import serializers
from .models import File

"""
Serializes the uploaded file
args :: 
    file        : contains the image file
    remark      : some remark to the image, could be useful to tag images later
    timestamp   : upload timestamp, we should save this in a DB so that
                    later the image can be deleted after a specific time 
"""
class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = File
    fields = ('file', 'remark', 'timestamp')