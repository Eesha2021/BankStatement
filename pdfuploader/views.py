from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser,FileUploadParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from .serializers import PdfSerializer
#from pdf2image import convert_from_bytes, convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
import pdfplumber
import pyrebase
import requests
#import pytesseract
#import cv2
import camelot
from camelot.core import TableList
import os
import io
import sys
import re
import pdfuploader
import pandas as pd
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import urllib.request
from io import BytesIO
import numpy as np
from .pdfprocessing import cleaning
from .analysis import *

from django.shortcuts import render
#from .monthly_analysis import *

from django.core.files.uploadhandler import TemporaryFileUploadHandler
from .bankprocessing import *

#pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'


Config = {
  'apiKey': "AIzaSyAzQnxOnWJboVmV81TDeTodIFqJomEDX0U",
  'authDomain': "pdfupload-e532a.firebaseapp.com",
  'databaseURL': "https://pdfupload-e532a.firebaseio.com",
  'projectId': "pdfupload-e532a",
  'storageBucket': "pdfupload-e532a.appspot.com",
  'messagingSenderId': "679349138249",
  'appId': "1:679349138249:web:847b515394d44678286098",
  'measurementId': "G-QLWMESYGT2"
};


# Create your views here.
class PdfView(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request, *args, **kwargs):
		firebase=pyrebase.initialize_app(Config)


		file_serializer = PdfSerializer(data=request.data)
		if file_serializer.is_valid():
			file_serializer.save()
			if request.method == "POST":
				if request.FILES.get("pdf", None) is not None:
					stream=request.FILES["pdf"]

					storage=firebase.storage()

					uploadTask = storage.child('pdf/' + request.FILES["pdf"].name).put(request.FILES["pdf"])
					filepath = storage.child("pdf/" +request.FILES["pdf"].name).get_url(None)
					bankname=request.POST['bankname']
					passkey=request.POST['passkey']
					act_type = request.POST['actype']

					
					dfn=cleaning(filepath,bankname,passkey,act_type)
					current_fn = [cheque_bounce, Balances, top5Credit, top5Debit, FrequentCr, FrequentDb, credit_analysis, finance_analysis, debit_analysis, chartsfrequent, statement_charts,analysis_sheets]
					saving_fn = [average_Monthy, credit, Dividend, interest_analysis, salary_analysis,analysis_sheets]
					both_fn = [loan, fund_recieved, fund_remittances, opening_bal, penalty, high_value, internal_txn, loan_analysis, Non_rev,analysis_sheets]
					#, Balances current
					#x21=average_Quaterly_analysis(dfn) #saving
					#x24=analysis(dfn)         #saving and current
					# x25=statement_charts(dfn) 
					# x26=Non_rev(dfn) 
					#x27=salary_analysis(dfn)
					final_sheets =[]
					start_date = dfn.iloc[0, 0].date()
					end_date = dfn.iloc[-1, 0].date()
					ocr_sheet = self.userDetails(filepath, bankname, passkey, act_type, start_date, end_date) 
					ocr_sheet.fillna('', inplace=True)
					lst = ocr_sheet.to_dict('records')
					lst.append('User Details')
					final_sheets.append(lst)
					
					if(act_type == 'current' or act_type == 'both'):
						for data in ocr_sheet:
							print(data)

					if(act_type == 'current' or act_type == 'both'):	
						for fn in current_fn:
							tmp = fn(dfn)
							if isinstance(tmp, list):
								for sheet in tmp:
									sheet[0].fillna('', inplace=True)
									lst = sheet[0].to_dict("records")
									lst.append(sheet[1])
									final_sheets.append(lst)
							else:	
								tmp[0].fillna('', inplace=True)
								lst = tmp[0].to_dict("records")
								lst.append(tmp[1])
								#print()
								final_sheets.append(lst)
					
					if(act_type == 'savings' or act_type == 'both'):	
						for fn in saving_fn:
							tmp = fn(dfn)
							if isinstance(tmp, list):
								for sheet in tmp:
									sheet[0].fillna('', inplace=True)
									lst = sheet[0].to_dict("records")
									lst.append(sheet[1])
									final_sheets.append(lst)
							else:	
								tmp[0].fillna('', inplace=True)
								lst = tmp[0].to_dict("records")
								lst.append(tmp[1])
								#print()
								final_sheets.append(lst)
					for fn in both_fn:
						tmp = fn(dfn)
						if isinstance(tmp, list):
							for sheet in tmp:
								sheet[0].fillna('', inplace=True)
								lst = sheet[0].to_dict("records")
								lst.append(sheet[1])
								final_sheets.append(lst)
						else:	
							tmp[0].fillna('', inplace=True)
							lst = tmp[0].to_dict("records")
							lst.append(tmp[1])
							#print()
							final_sheets.append(lst)		
					
                  #t=camelot.read_pdf(filepath,pages='1')
			return Response(final_sheets,status=status.HTTP_201_CREATED)
		else:
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	def userDetails(self, input_file, bankname, password, act_type, start_date, end_date):
		switcher = {
		  "BOB": bob,
	      "BOI": boi,
	      "ICICI": icici,
	      "KOTAK": kotak,
	      "PNB": pnb,
	      "IDBI": idbi,
	      "SBI": sbi,
	      "UBOI": unitedbank,
	      "HDFC": hdfc,
	      "CORP": corporation,
		  "CBOI":Central,
		  "AXIS":axis,
			"INDIAN":indian,
			"INDUSIND":indusind,
			"YES":yes
	    } 
		remoteFile = urllib.request.urlopen(input_file).read()
		memoryFile = BytesIO(remoteFile)
		with pdfplumber.open(memoryFile, password= password) as inp:
			page = inp.pages[0]
			print("hello")
			print(page.extract_text())
			return switcher.get(bankname, lambda x: "Invalid bank name")(page.extract_text(), act_type, start_date, end_date)
