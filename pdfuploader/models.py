# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Create your models here.
class Pdfupload(models.Model):
	pdf=models.FileField(blank=False)
	bankname=models.CharField(max_length=50)
	actype=models.CharField(max_length=50)
	