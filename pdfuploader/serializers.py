from rest_framework import serializers
from .models import Pdfupload

class PdfSerializer(serializers.ModelSerializer):
	class Meta():
	    model = Pdfupload
	    fields = '__all__'