from django.shortcuts import render

# Create your views here

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    # GRAB the POST request and process the data

    def post(self, request, *args, **kwargs):
        import matplotlib.pyplot as plt
        from PIL import Image
        import os

        file_serializer = FileSerializer(data=request.data)
        image = request.data['file']

        try :
            img = Image.open(image)
            img.verify()

            #plt.imshow(img.)
            #plt.show()
        except:
            raise IOError("Unsupported Image Type")

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
