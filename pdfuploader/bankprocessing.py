import cv2
import numpy as np
import re
import pandas as pd

df=pd.DataFrame()

def myfun():
	global df
	return df["B"][0]

def bob(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	x1=re.compile("(?<=Name).*")
	y1=x1.findall(text)
	name =y1[0]
	df.loc[0,"B"]=name.strip()
	d=df.loc[0,"B"]=name.strip()
	print("rere")
	print(d)

	x2=re.compile("(?<=Account Number\s\s:\s)\d*")
	y2=x2.findall(text)
	print()
	df.loc[1,"B"]=y2[0].strip()

	df.loc[2,"B"]="Bank of Baroda"
	df.loc[3, "B"]=act_type

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].str.strip()
	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df

	
def boi(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	x1=re.compile("(?<=Name).*(?=Account)")
	y1=x1.findall(text)
	name =y1[0]
	df.loc[0,"B"]=name.strip()

	x2=re.compile("(?<=Account No\s:\s)\d*")
	y2=x2.findall(text)
	print()
	df.loc[1,"B"]=y2[0].strip()

	df.loc[2,"B"]="Bank of India"
	df.loc[3, "B"]=act_type

	x8=re.compile("(?<=IFSC\sCode\s:\s).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].str.strip()
	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df


def icici(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	x01=re.compile("(?<=Account\sName).*")
	y2=x01.findall(text)

	z2=str(y2)
	name = z2
	df.loc[0,"B"]=name
	

	x12=re.compile("(?<=Account\sNo).*")
	y12=x12.findall(text)
	listToStr = ' '.join(map(str, y12))
	acc = listToStr.split()


  


	#detail=str(acc[1])
	detail=""
	df.loc[1,"B"]=detail
	

	x2=re.compile("(?<=IFSC\sCode).*")
	y2=x2.findall(text)
	listToStr = ' '.join(map(str, y2))
	ifsc = listToStr.split()
	print(y2)
	#details=str(ifsc[1])
	details=""
	#details = y2[1].split()
	df.loc[8,"B"]=details


	df.loc[2,"B"]="ICICI Bank"
	df.loc[3, "B"]=act_type
	


	
	#df.loc[8, "B"] = details[5]

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df

def idbi(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	x1=re.compile("(?<=A/c\sName\s:\s1.\s).*")
	y2=x1.findall(text)

	z2=str(y2)
	name = z2
	df.loc[0,"B"]=name

	x2=re.compile("(?<=ACCOUNT Number:)\s*\d*")
	y2=x2.findall(text)
	print()

	df.loc[1,"B"]=y2[0].strip()

	df.loc[2,"B"]="IDBI"
	df.loc[3, "B"]=act_type

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].str.strip()
	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df
	
def kotak(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	splitted = text.split()
	second = splitted[2]+" "+splitted[3]
	

	
	
	df.loc[0,"B"]=second

	x2=re.compile("(?<=Account No.\s)\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="Kotak"
	df.loc[3, "B"]=act_type


	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df
	print(df)

def pnb(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	x1=re.compile("(?<=Account\sName)Cus*")
	y1=x1.findall(text)
	name =y1[0]
	df.loc[0,"B"]=name.strip()

	x2=re.compile("(?<=Statement\sFor\sAccount:)\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=y2[0].strip()

	df.loc[2,"B"]="Punjab National Bank"
	df.loc[3, "B"]=act_type

	x8=re.compile("(?<=IFSC\sCode:).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].str.strip()
	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df

def sbi(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	x2=re.compile("(?<=Account\sName).*")
	y2=x2.findall(text)

	z2=str(y2)
	name = z2
	df.loc[0,"B"]=name

	x4=re.compile("(?<=Account\sNumber).*\d*")
	y4=x4.findall(text)

	tmp=re.compile("(?<=IFS\sCode).*")
	ifsc=tmp.findall(text)

	df.loc[8, "B"] = str(ifsc)

	df.loc[1,"B"]=str(y4)

	df.loc[2,"B"]="State Bank of India"
	df.loc[3, "B"]=act_type

	tmp2=re.compile("(?<=Interest\sRate).*")
	interest = tmp2.findall(text)
	df.loc[9, "B"] = str(interest)


	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\([^)]*\)","", regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	df["B"]=df["B"].str.lstrip()
	return df

def unitedbank(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	x2=re.compile("(?<=Name:\s).*")
	y2=x2.findall(text)

	z2=str(y2)
	name = z2
	df.loc[0,"B"]=name

	x4=re.compile("(?<=Account Number:\s)\d*")
	y4=x4.findall(text)

	df.loc[1,"B"]=str(y4)

	df.loc[2,"B"]="United Bank of India"
	df.loc[3, "B"]=act_type

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df

def hdfc(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	x1=re.compile("(?:MR|MRS|M/S).*")
	y1=x1.findall(text)
	name =str(y1)
	df.loc[0,"B"]=name

	x2=re.compile("(?<=AccountNo\s:\s)\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="HDFC"
	df.loc[3, "B"]=act_type

	x4=re.compile("(?<=Email\s:\s).*")
	y4=x4.findall(text)
	df.loc[4, "B"] = str(y4)

	x6=re.compile("(?<=Phone No.\s:\s)\d*")
	y6=x6.findall(text)
	df.loc[6, "B"] = str(y6)


	# x7=re.compile("(?<=A/C\sOpen\sDate\s:\s)\d\d/\d\d/\d\d\d\d")
	# y7=x7.findall(text)



	
	# z7=str(y7)
	# opendate=z7
	# opendate=opendate.replace("/","")
	# opendate=opendate.replace("[","")
	# opendate=opendate.replace("]","")
	# opendate=pd.to_datetime(date,dayfirst=True,errors="coerce",format='%d%m%Y')
	# diff=end_date-opendate.date()
	# daydiff=diff.days
	# finallres=[]
	# if daydiff>=365:
	# 	result=diff/np.timedelta64(1,'Y')
	# 	finallres.append(result)
	# else:
	# 	result=diff/np.timedelta64(1,'M')
	# 	finallres.append(result)
	# finallres.append("years")
	# finallres=str(finallres)[1:-1]
	# df.loc[7,"B"]=finallres




	x8=re.compile("(?<=RTGS/NEFTIFSC:\s).*(?=MICR)")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " To :" + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df
	


def corporation(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	x1=re.compile("(?<=Name:)\Bran*")
	y2=x1.findall(text)

	z2=str(y2)
	name = z2
	df.loc[0,"B"]=name
	

	x2=re.compile("(?<=Number:\s)\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="Corporation Bank"
	df.loc[3, "B"]=act_type


	# x7=re.compile("(?<=A/C\sOpen\sDate\s:\s)\d\d/\d\d/\d\d\d\d")
	# y7=x7.findall(text)



	
	# z7=str(y7)
	# opendate=z7
	# opendate=opendate.replace("/","")
	# opendate=opendate.replace("[","")
	# opendate=opendate.replace("]","")
	# opendate=pd.to_datetime(date,dayfirst=True,errors="coerce",format='%d%m%Y')
	# diff=end_date-opendate.date()
	# daydiff=diff.days
	# finallres=[]
	# if daydiff>=365:
	# 	result=diff/np.timedelta64(1,'Y')
	# 	finallres.append(result)
	# else:
	# 	result=diff/np.timedelta64(1,'M')
	# 	finallres.append(result)
	# finallres.append("years")
	# finallres=str(finallres)[1:-1]
	# df.loc[7,"B"]=finallres




	x8=re.compile("(?<=IFSC\sCode).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df



def Central(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	
	splitted = text.split()
	second = splitted[28]+" "+splitted[29]
	


	
	df.loc[0,"B"]=second

	x2=re.compile("(?<=Account Number\s:)\s*\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="Central Bank"
	df.loc[3, "B"]=act_type

	x4=re.compile("(?<=Email\s:\s).*")
	y4=x4.findall(text)
	df.loc[4, "B"] = str(y4)

    


	x8=re.compile("(?<=IFSC\sCode).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df


def axis(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	
	splitted = text.split()
	second = splitted[28]+" "+splitted[29]
	


	
	df.loc[0,"B"]=second

	x2=re.compile("(?<=Account Number\s:)\s*\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="Central Bank"
	df.loc[3, "B"]=act_type

	x4=re.compile("(?<=Email\s:\s).*")
	y4=x4.findall(text)
	df.loc[4, "B"] = str(y4)

    


	x8=re.compile("(?<=IFSC\sCode).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df

def indian(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	
	splitted = text.split()
	second = splitted[28]+" "+splitted[29]
	


	
	df.loc[0,"B"]=second

	x2=re.compile("(?<=Account Number\s:)\s*\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="Central Bank"
	df.loc[3, "B"]=act_type

	x4=re.compile("(?<=Email\s:\s).*")
	y4=x4.findall(text)
	df.loc[4, "B"] = str(y4)

    


	x8=re.compile("(?<=IFSC\sCode).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df



def indusind(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re
	
	splitted = text.split()
	second = splitted[28]+" "+splitted[29]
	


	
	df.loc[0,"B"]=second

	x2=re.compile("(?<=Account Number\s:)\s*\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="Central Bank"
	df.loc[3, "B"]=act_type

	x4=re.compile("(?<=Email\s:\s).*")
	y4=x4.findall(text)
	df.loc[4, "B"] = str(y4)

    


	x8=re.compile("(?<=IFSC\sCode).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df

def yes(text, act_type, start_date, end_date):
	global df
	List1=["Name of the Account Holder","Account Number","Name of the Bank","Account Type","Email","PAN","Mobile Number","Tenure of Relationship with Bank","IFSC Code","Interest Rate","Statement upload","Missing Months"]
	df["A"]=List1
	import re

	x1=re.compile("(?:MR|MRS|M/S).*")
	y1=x1.findall(text)
	name =str(y1)
	df.loc[0,"B"]=name

	x2=re.compile("(?<=Account Number\s:)\s*\d*")
	y2=x2.findall(text)

	df.loc[1,"B"]=str(y2)

	df.loc[2,"B"]="Central Bank"
	df.loc[3, "B"]=act_type

	x4=re.compile("(?<=Email\s:\s).*")
	y4=x4.findall(text)
	df.loc[4, "B"] = str(y4)

    


	x8=re.compile("(?<=IFSC\sCode).*")
	y8=x8.findall(text)
	df.loc[8, "B"] = str(y8)

	df.loc[10,"B"]=str(start_date) + " to " + str(end_date)
	df.loc[11,"B"]=0

	df["B"]=df["B"].replace("]","",regex=True)
	df["B"]=df["B"].replace("\[","",regex=True)
	df["B"]=df["B"].replace(":","",regex=True)
	df["B"]=df["B"].replace("\'","",regex=True)
	return df