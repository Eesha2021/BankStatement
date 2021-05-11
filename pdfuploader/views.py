#!/usr/bin/python -tt
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
import tabula
import urllib.request
from io import BytesIO
import numpy as np
from .pdfprocessing import cleaning
from .analysis import *
import pickle
from django.shortcuts import render
#from .monthly_analysis import *

from django.core.files.uploadhandler import TemporaryFileUploadHandler
from .bankprocessing import *
import redis
from .analysis import cheque_bounce
from .bankprocessing import myfun
#pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
import json

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

#Create your views here.
class RedisView(APIView):
    def post(self,request):
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

                    cleaned_dict=dfn.to_dict()
                    p_mydict = pickle.dumps(cleaned_dict)
                    conn = redis.Redis('localhost')
                    conn.set('mydict',p_mydict)
                    #read_dict = conn.get('mydict')
                    #yourdict = pickle.loads(read_dict)
                     
                    #new_df = pd.DataFrame.from_dict(yourdict)
                    #print(new_df)
                    #credit=high_value(new_df)
                    #cheque=cheque_bounce(new_df)
                    #print("##########from redis cache#################################")
                    #print(credit)
                    #print(yourdict)
                    return Response('stored successfully in redis database',status=status.HTTP_201_CREATED)
                    #return Response(,status=status.HTTP_201_CREATED)    



class ChequeBounce(APIView):
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
					
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					cheq=cheque_bounce(new_df)
					result=cheq.to_dict("Records")
		return Response(result, status.HTTP_201_CREATED)



class Top5Credit(APIView):
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
					
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					topc=top5Credit(new_df)
					#print(topc)
					topc=topc.fillna("")
					topc_arrange=topc.T.unstack().reset_index(level=1, name='c1').rename(columns={'level_1':'c2'})[['c1','c2']]
					#print(topc_arrange.groupby("c2"))
					print("###########")
					grouped_df = topc_arrange.groupby("c2")

					grouped_lists = grouped_df["c1"].apply(list)

					grouped_lists = grouped_lists.reset_index()
					#print(grouped_lists)
					result=grouped_lists.to_dict("Records")
					#print(result)
					json_object = json.dumps(result, indent = 4)  
					print(json_object) 
		return Response(result, status.HTTP_201_CREATED)
		
		
		
class Top5Debit(APIView):
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
					
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					print(new_df)
					topd=top5Debit(new_df)
					print(topd)
					topd=topd.fillna("")
					result=topd.to_dict("Records")
		return Response(result, status.HTTP_201_CREATED)


class balances(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					bal=Balances(new_df)
					#result=bal.to_dict("records")

					#x="Eesha"
		return Response(bal,status=status.HTTP_201_CREATED)


class Loan(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					lon=loan(new_df)
					#result=lon.to_dict("records")

					#x="Eesha"
		return Response(lon,status=status.HTTP_201_CREATED)
		
		
class FundRecieved(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	
	def userDetails(self,filepath, bankname, password, act_type, start_date, end_date):
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
		remoteFile = urllib.request.urlopen(filepath).read()
		memoryFile = BytesIO(remoteFile)
		with pdfplumber.open(memoryFile, password= password) as inp:
			page = inp.pages[0]
			print("hello")
			print(page.extract_text())
			return switcher.get(bankname, lambda x: "Invalid bank name")(page.extract_text(), act_type, start_date, end_date)
	

	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					start_date = new_df.iloc[0, 0].date()
					end_date = new_df.iloc[-1, 0].date()
					print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
					print(passkey)
					print(end_date)
					print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
					user_df=self.userDetails(filepath, bankname, passkey, act_type, start_date, end_date)
					fundrec=fund_recieved(new_df,user_df)
					result=fundrec.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
	

class FundRemittances(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def userDetails(self,filepath, bankname, password, act_type, start_date, end_date):
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
		remoteFile = urllib.request.urlopen(filepath).read()
		memoryFile = BytesIO(remoteFile)
		with pdfplumber.open(memoryFile, password= password) as inp:
			page = inp.pages[0]
			print("hello")
			print(page.extract_text())
			return switcher.get(bankname, lambda x: "Invalid bank name")(page.extract_text(), act_type, start_date, end_date)
	
	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					start_date = new_df.iloc[0, 0].date()
					end_date = new_df.iloc[-1, 0].date()
					
					user_df=self.userDetails(filepath, bankname, passkey, act_type, start_date, end_date)
					fundrem=fund_remittances(new_df,user_df)
					result=fundrem.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)


class AnalysisSheets(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def userDetails(self,filepath, bankname, password, act_type, start_date, end_date):
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
		remoteFile = urllib.request.urlopen(filepath).read()
		memoryFile = BytesIO(remoteFile)
		with pdfplumber.open(memoryFile, password= password) as inp:
			page = inp.pages[0]
			print("hello")
			print(page.extract_text())
			return switcher.get(bankname, lambda x: "Invalid bank name")(page.extract_text(), act_type, start_date, end_date)
	
	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					start_date = new_df.iloc[0, 0].date()
					end_date = new_df.iloc[-1, 0].date()
					user_df=self.userDetails(filepath, bankname, passkey, act_type, start_date, end_date)
					ansheet=analysis_sheets(new_df,user_df)
					ansheet=ansheet.fillna(' ')
					result=ansheet.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
	
class Frequent_Cr(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					freqcr=FrequentCr(new_df)
					result=freqcr.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
		

class Frequent_db(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					frdb=FrequentDb(new_df)
					result=frdb.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class AverageMonthly(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					avgmon=average_Monthy(new_df)
					avgmon=avgmon.fillna("")
					result=avgmon.to_dict("records")
					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class OpeningBal(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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

					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					opbal=opening_bal(new_df)
					result=opbal.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class Penalty(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					pen=penalty(new_df)
					result=pen.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)

class Credit(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					cdt=credit(new_df)
					result=cdt.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class dividend(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
  					
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
					 
					new_df = pd.DataFrame.from_dict(yourdict)
					div=Dividend(new_df)
					result=div.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)

class HighValue(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					higval=high_value(new_df)
					result=higval.to_dict("records")
					pd.set_option('display.max_columns', None)
					#print(dfn)
					print("888888888888888888888888888888888888888888888888888888888888888888888")
					print(higval)
					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class CreditAnalysis(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					cran=credit_analysis(new_df)
					result=cran.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class DebitAnalysis(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					deban=debit_analysis(new_df)
					result=deban.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)

class FinancialAnalysis(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
   					
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
					 
					new_df = pd.DataFrame.from_dict(yourdict)
					finan=finance_analysis(new_df)
					result=finan.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)

class InternalTxn(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					intxn=internal_txn(new_df)
					result=intxn.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)

class InterestAnalysis(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					intan=interest_analysis(new_df)
					result=intan.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class AverageQAnalysis(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					aqan=average_Quaterly_analysis(new_df)
					
					result=aqan.to_dict("records")
					
					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)
		
class LoanAnalysis(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					loan=loan_analysis(new_df)
					result=loan.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)

class ChartsFrequent(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					chfreq=chartsfrequent(new_df)
					result=chfreq.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)


class StatementCharts(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					stmtc=statement_charts(new_df)
					result=stmtc.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)

class NonRev(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					nonrev=Non_rev(new_df)
					result=nonrev.to_dict("records")

					#x="Eesha"
		return Response(result,status=status.HTTP_201_CREATED)


class SalaryAnalysis(APIView):
	parser_classes = (MultiPartParser, FormParser,JSONParser)
	def post(self, request):
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
    	            
					conn = redis.Redis('localhost')
					#dfn=cleaning(filepath,bankname,passkey,act_type)
					read_dict = conn.get('mydict')
					yourdict = pickle.loads(read_dict)
                     
					new_df = pd.DataFrame.from_dict(yourdict)
					salan=salary_analysis(new_df)
					#result=salan.to_dict("records")

					#x="Eesha"
		return Response(salan,status=status.HTTP_201_CREATED)
        
class pdfCheck(APIView):
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    def post(self, request, *args, **kwargs):
        filepath=request.FILES["pdf"]
        path=request.FILES["pdf"].name
        final_msg=self.pdfcheck(path, filepath)
        return Response(final_msg, status.HTTP_201_CREATED)
    def pdfcheck(self, path, filepath):
        if path.endswith('.pdf'):
            msg= True
            return msg
        else:
            msg= False
            return msg


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
						print('eeeeeeeeeeeeeeeeeeeeeeesssssssssssssssshhhhhhhhhhaaaaaaaaaaaaaaaaaaaa')
						print(tmp)
						try:
							
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
								final_sheets.append(lst)
						except:
							pass		
	
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

















			
			

