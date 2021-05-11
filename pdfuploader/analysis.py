import pandas as pd
import numpy as np
import re
import calendar
from .bankprocessing import myfun


def cheque_bounce(dfl):
  df=dfl.copy(deep=True)

  ls=["WRONGLY DELIVERED / NOT DRAWN ON US","FUNDS INSUFFICIENT","INSTRUMENT OUTDATED / STALE","INSTRUMENT POST DATED","EXCEEDS ARRANGEMENT","OTHER REASONS - CONNECTIVITY FAILURE","TITLE OF ACCOUNT REQUIRED","OTHER REASONS","EFFECT NOT CLEAR, PRESENT AGAIN","DRAWERS SIGNATURE DIFFER","REFER TO DRAWER","ALTERATION REQUIRED DRAWERS AUTHENT","PAYMENT STOPPED BY DRAWER","CHQ IRREGULARLY DRAWN/AMT IN WORD"]
  ls = list(dict.fromkeys(ls))

  new=[]
  for i in range (0,(df.shape)[0]):
    for j in range(0,len(ls)):
      num=(df["description"][i]).find(ls[j])
      if num != -1:
        new.append(i)    
  dte=[]
  des=[]
  cat=[]
  deb=[]
  cred=[]
  bal=[]
  for i in new:
    dte.append(df["date"][i])
    des.append(df["description"][i])
    cat.append(df["cat"][i])
    deb.append(df["debit"][i])
    cred.append(df["credit"][i])
    bal.append(df["balance"][i])        
  dit={}

  dit["date"]=dte
  dit["description"]=des 
  dit["category"]=cat
  dit["debit"]=deb
  dit["credit"]=cred
  dit["balance"]=deb
  #we have created a dataframe from dictionary
  #print(dict)
  df_bank=pd.DataFrame(dit)
  return df_bank


def top5Credit(dfl):
  df=dfl.copy(deep=True)
  df['month']=df['date'].dt.month
  df['day']=df['date'].dt.day
  m=df["month"]
  m = list(dict.fromkeys(m))
  #print(m)
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
  mn=df["month name"]
  mn= list(dict.fromkeys(mn)) 
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1} {x2}")
  abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
  lm = list(dict.fromkeys(lm)) 

  lst9=[]
  for my in lm:
    my = my.split()
    x5=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    y5=x5.sort_values(by=["credit"],ascending=False)
    z5=y5.head(5)
    k=z5["credit"].values
    lst9.append(k)
  if(len(lst9) > 0):
    maxLength = max(len(x) for x in lst9 )
  else:
    maxLength = 0
  ds=pd.DataFrame(index=np.arange(maxLength), columns=lm)
  for i in range(0,len(lm)):
    ds[lm[i]]=pd.Series(lst9[i][0:])
  print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
  print(ds)
  #ds = ds.fillna('')  
  return ds

def top5Debit(dfl):
  df=dfl.copy(deep=True)
  df['month']=df['date'].dt.month
  df['day']=df['date'].dt.day
  m=df["month"]
  m = list(dict.fromkeys(m))
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
  mn=df["month name"]
  mn= list(dict.fromkeys(mn))

  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1} {x2}")
  abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
  lm = list(dict.fromkeys(lm)) 

  lst10=[]
  for my in lm:
    my = my.split()
    x5=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    y5=x5.sort_values(by=["debit"],ascending=False)
    z5=y5.head(5)
    k=z5["debit"].values
    lst10.append(k)
  if(len(lst10) > 0):
    maxLength = max(len(x) for x in lst10 )
  else:
    maxLength = 0
  dp=pd.DataFrame(index=np.arange(maxLength), columns=lm)
  for i in range(0,len(lm)):
    dp[lm[i]]=pd.Series(lst10[i][0:])  
  return dp  

def Balances(dfl):
  df=dfl.copy(deep=True)
  f=[]
  df['month']=df['date'].dt.month
  df['day']=df['date'].dt.day
  m=df["month"]
  m = list(dict.fromkeys(m))
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
  mn=df["month name"]
  mn= list(dict.fromkeys(mn))
  day1=[]
  day14=[]
  day30=[]
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1} {x2}")
  abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
  lm = list(dict.fromkeys(lm))
  for my in lm:
    D1B1=[]
    D14B1=[]
    D30B1=[]
    my = my.split()
    newdf=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    newdf.reset_index(inplace=True)
    ndg=(newdf.shape)[0]
    data=[]

    
    for i in range(0,ndg):
      if(newdf["day"][i] <= 1):
        D1B1.append(newdf["balance"][i])
      if(newdf["day"][i] <= 14):
        D14B1.append(newdf["balance"][i])
    D30B1.append(newdf["balance"][i])
    if(len(D1B1)!=0):
      d1b=D1B1[-1]
    else:
      d1b=0
    if(len(D14B1)!=0):
      d14b=D14B1[-1]
    else:
      d14b=0
    if(len(D30B1)!=0):
      d30b=D30B1[-1]
    else:
      d30b=0
    day1.append(d1b) 
    day14.append(d14b) 
    day30.append(d30b)  

  lst3=[]
  for my in lm:
    my = my.split()
    x7=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    y7=x7.sort_values(by=["debit"])
    z7=y7[y7["debit"]!=0.0]
    lst3.append(z7["debit"].shape[0])
  lst4=[]
  for my in lm:
    my = my.split()
    x2=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    y2=x2.sort_values(by=["credit"])
    z2=y2[y2["credit"]!=0.0]
    lst4.append(z2["credit"].shape[0])
    
  lst5=[]
  for my in lm:
    my = my.split()
    x7=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    y7=x7["credit"].sum(skipna=True)
    lst5.append(y7)
  lst6=[]
  for my in lm:
    my = my.split()
    x8=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    y8=x8["debit"].sum(skipna=True)
    lst6.append(y8)
 
  
  dit={}
  dit["Month Year"]=lm
  dit["Monthly net credits"]=lst5
  dit["Monthly net debits"]=lst6
  dit["No. of Net Debits"]=lst3
  dit["No. of Net Credits"]=lst4
  dit["DAY 1 Balance"]=day1
  dit["DAY 14 Balance"]=day14
  dit["DAY 30 Balance"]=day30
  dfx=pd.DataFrame(dit) 
  f.append((dfx, "Banking Detail")) 
  dh={}
  dh["MONTH"]=mn
  dh["Monthly Average Debits"]=np.nan
  dh["Monthly Average Credits"]=np.nan
  dh["Monthly Average Balance"]=np.nan  
  month=pd.DataFrame(dh)
  for i, my in enumerate(lm):
    my = my.split()
    newdf=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    month['Monthly Average Debits'][i]=lst6[i]
    month['Monthly Average Credits'][i]=lst5[i]
    month['Monthly Average Balance'][i]=df['balance'][newdf.shape[0]] 
  f.append((month, "Banking Detail"))
  return f

def loan(dfl):
  df=dfl.copy(deep=True)
  for i in range(0,(df.shape)[0]):
    df["description"][i]=(df["description"][i])
  df["description"]=df["description"].astype(str)
  desc_colname = "description"
  c=['loan','finance','loan repayment']

  df = df[df[desc_colname].str.contains("|".join(c), case = False)]   
  dt=[]
  dsc=[]
  cta=[]
  dbt=[]
  crt=[]
  blc=[]
  for i, row in df.iterrows():
    dt.append(row["date"])
    dsc.append(row["description"])
    dbt.append(row["debit"])
    crt.append(row["credit"])
    blc.append(row["balance"])
    tmp = str(row['debit']).lower
    if(tmp == 'nan' or tmp == ""):   
         cta.append("Loan")
    else:
         cta.append("Loan Repayment")
  di={}
  di["Date"]=dt
  di["Description"]=dsc
  di["Category"]=cta
  di["Credit"]=crt
  di["Debit"]=dbt
  di["Balance"]=blc

  dfk=pd.DataFrame(di)
  dfk.to_csv (r'loanAna.csv', index = False, header=True)
  return dfk, "Loan Analysis"
    
def fund_recieved(dfl,user_df):
  df=dfl.copy(deep=True)
  for i in range(0,len(df["credit"].isnull())):
    if (df["credit"].isnull())[i]==True:
        df.drop(i,inplace=True)
  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True) 
  df['month']=df['date'].dt.month  
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])        
  mtn=df["month name"]
  df.to_csv (r'dataaa.csv', index = False, header=True)
  mtn = list(dict.fromkeys(mtn))
  mn=df["month"]
  mn = list(dict.fromkeys(mn))
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1} {x2}")
  abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
  lm = list(dict.fromkeys(lm))
  for i in range(0,len(df["description"])):
    (df["description"][i])=(df["description"][i]).lower()
  NEFT=[]
  RTGS=[]
  CASH=[]
  CHEQUE=[]
  IMPS=[]
  ONLINE=[]
  DEMAND_DRAFT=[]
  INTERNAL_TRANSCT=[]
  OTHERS=[]
  for my in lm:
    my = my.split()
    newdf=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    newdf.reset_index(inplace=True)
    neft=[]
    rtgs=[]
    cash=[]
    cheque=[]
    imps=[]
    online_transfer=[]
    Demand_Draft=[]
    Internal_Transactions=[]         
    Others=[]
    Ac_hol=user_df["B"][0]
    for i in range(0,len(newdf["description"])):
       if(newdf["description"][i].find("neft") != -1 ):
         neft.append(i)
       elif(newdf["description"][i].find("rtgs") != -1):
         rtgs.append(i)
       elif(newdf["description"][i].find("imps") != -1):
         imps.append(i)
       elif(newdf["description"][i].find("cash") != -1):
         cash.append(i)    
       elif(newdf["description"][i].find("cheque") != -1):
         cheque.append(i) 
        
       elif(newdf["description"][i].find("online") != -1 or newdf["description"][i].find("upi") != -1 or newdf["description"][i].find("netbanking") != -1):
         online_transfer.append(i)
       elif(newdf["description"][i].find("demand draft") != -1):
         Demand_Draft.append(i)
       elif(newdf["description"][i].find("self") != -1 or newdf["description"][i].find(Ac_hol) != -1):#Ac_hol=myfun()
         Internal_Transactions.append(i)
       else:
         Others.append(i)
    neftamt=[]
    for i in neft:
      neftamt.append(newdf["credit"][i])   
    rtgsamt=[]
    for i in rtgs:
      rtgsamt.append(newdf["credit"][i])   
    cashamt=[]
    for i in cash:
      cashamt.append(newdf["credit"][i]) 
    chequeamt=[]
    for i in cheque:
      chequeamt.append(newdf["credit"][i]) 
    impsamt=[]
    for i in imps:
      impsamt.append(newdf["credit"][i])
    online_transferamt=[]
    for i in online_transfer:      
      online_transferamt.append(newdf["credit"][i]) 
    demand_Draftamt=[] 
    for i in Demand_Draft:
      demand_Draftamt.append(newdf["credit"][i]) 
    internal_transactionamt=[] 
    for i in Internal_Transactions:
      internal_transactionamt.append(newdf["credit"][i])
    Others_amt=[] 
    for i in Others:
      Others_amt.append(newdf["credit"][i])
    print("its others data =========",Others)
    NEFT.append(sum(neftamt))
    RTGS.append(sum(rtgsamt))
    CASH.append(sum(cashamt))
    CHEQUE.append(sum(chequeamt))
    IMPS.append(sum(impsamt))
    ONLINE.append(sum(online_transferamt))
    DEMAND_DRAFT.append(sum(demand_Draftamt))
    INTERNAL_TRANSCT.append(sum(internal_transactionamt))
    OTHERS.append(sum(Others_amt))    
    dict1={}
#interbank transfer is not defined
  dict1["Months"]=lm
  dict1["NEFT"]=NEFT
  dict1["RTGS"]=RTGS
  dict1["IMPS"]=IMPS
  dict1["Cheque"]=CHEQUE
  dict1["Cash"]=CASH
  dict1["Online Transfers"]=ONLINE
  #dict1["Inter Bank Transfer"]=np.nan
  dict1["Demand Draft" ]=DEMAND_DRAFT
  dict1["Internal Transactions" ]=INTERNAL_TRANSCT
  dict1["Others"]=OTHERS
  dict1["Total"]=np.nan
  df_b=pd.DataFrame(dict1)
  for i in range(0,len(lm)):
    df_b["Total"][i]= df_b["Cash"][i]+ df_b["Cheque"][i]+ df_b["NEFT"][i]+ df_b["RTGS"][i] + df_b["IMPS"][i]+ df_b["Demand Draft"][i]+df_b["Internal Transactions"][i]+df_b["Others"][i]+df_b["Online Transfers"][i]
  df_b.to_csv (r'fundrecived.csv', index = False, header=True)
  print('my data',df[(df['date'].dt.month==1) & (df['description'].str.contains('imps')) & (df['credit']!=0.0) ]['credit'].head(15))
  return df_b
  
def fund_remittances(dfl,user_df):
  df=dfl.copy(deep=True)
  for i in range(0,len(df["debit"].isnull())):
    if (df["debit"].isnull())[i]==True:
        df.drop(i,inplace=True)
  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True) 
  df['month']=df['date'].dt.month  
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])        
  mtn=df["month name"]
  mtn = list(dict.fromkeys(mtn))
  mn=df["month"]
  mn = list(dict.fromkeys(mn))
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1} {x2}")
  abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
  lm = list(dict.fromkeys(lm))
  for i in range(0,len(df["description"])):
    (df["description"][i])=(df["description"][i]).lower()
  NEFT=[]
  RTGS=[]
  CASH=[]
  CHEQUE=[]
  IMPS=[]
  ONLINE=[]
  DEMAND_DRAFT=[]
  INTERNAL_TRANSCT=[]
  OTHERS=[]
  for my in lm:
    my = my.split()
    newdf=df[(df['month'] == abbr_to_num[my[0]]) & (df['year'] == int(my[1]))]
    newdf.reset_index(inplace=True)
    neft=[]
    rtgs=[]
    cash=[]
    data=[]
    cheque=[]
    imps=[]
    online_transfer=[]
    Demand_Draft=[]
    Internal_Transactions=[]         
    Others=[]
    for i in range(0,len(newdf["description"])):
      if(newdf["description"][i].find("neft") != -1 or newdf["description"][i].find("neft") != -1):
        data.append(i)
    print("data",data)
    Ac_hol=user_df["B"][0]
    for i in range(0,len(newdf["description"])):
       if(newdf["description"][i].find("neft") != -1):
          neft.append(i)
       elif(newdf["description"][i].find("rtgs") != -1):
          rtgs.append(i)
       elif(newdf["description"][i].find("cash") != -1):
          cash.append(i)    
       elif(newdf["description"][i].find("cheque") != -1):
          cheque.append(i) 
       elif(newdf["description"][i].find("imps") != -1):
          imps.append(i) 
       elif(newdf["description"][i].find("online") != -1 or newdf["description"][i].find("upi") != -1 or newdf["description"][i].find("netbanking") != -1):
          online_transfer.append(i)
       elif(newdf["description"][i].find("demand draft") != -1):
          Demand_Draft.append(i)
       elif(newdf["description"][i].find("self") != -1 or newdf["description"][i].find(Ac_hol) != -1 ):#Ac_hol=()myfun()
          Internal_Transactions.append(i)
       else:
          Others.append(i)
  
    neftamt=[]
    data1=[]
    for i in data:
      data1.append(newdf['debit'][i])

    for i in neft:
      neftamt.append(newdf["debit"][i])   
    rtgsamt=[]
    for i in rtgs:
      rtgsamt.append(newdf["debit"][i])   
    cashamt=[]
    for i in cash:
      cashamt.append(newdf["debit"][i]) 
    chequeamt=[]
    for i in cheque:
      chequeamt.append(newdf["debit"][i]) 
    impsamt=[]
    for i in imps:
      impsamt.append(newdf["debit"][i])
    online_transferamt=[]
    for i in online_transfer:
      online_transferamt.append(newdf["debit"][i]) 
    demand_Draftamt=[] 
    for i in Demand_Draft:
      demand_Draftamt.append(newdf["debit"][i]) 
    internal_transactionamt=[] 
    for i in Internal_Transactions:
      internal_transactionamt.append(newdf["debit"][i])
    Others_amt=[] 
    for i in Others:
      Others_amt.append(newdf["debit"][i])
    print("=======================interfhhjbjbjbjbjbjbhjkjjjkk",internal_transactionamt)
    NEFT.append(sum(neftamt))
    RTGS.append(sum(rtgsamt))
    CASH.append(sum(cashamt))
    CHEQUE.append(sum(chequeamt))
    IMPS.append(sum(impsamt))
    ONLINE.append(sum(online_transferamt))
    DEMAND_DRAFT.append(sum(demand_Draftamt))
    INTERNAL_TRANSCT.append(sum(internal_transactionamt))
    OTHERS.append(sum(Others_amt)) 

  print("================***********************------------------")
  print(NEFT)   
 
  dict2={}
#interbank transfer is not defined
  dict2["Months"]=lm
  dict2["NEFT"]=NEFT
  dict2["RTGS"]=RTGS
  dict2["IMPS"]=IMPS
  dict2["Cheque"]=CHEQUE
  dict2["Cash"]=CASH
  dict2["Online Transfers"]=ONLINE
  #dict2["Inter Bank Transfer"]=np.nan
  dict2["Demand Draft" ]=DEMAND_DRAFT
  dict2["Internal Transactions" ]=INTERNAL_TRANSCT
  dict2["Others"]=OTHERS
  dict2["Total"]=np.nan
  df_b=pd.DataFrame(dict2)
  for i in range(0,len(lm)):
    df_b["Total"][i]= df_b["Cash"][i]+ df_b["Cheque"][i]+ df_b["NEFT"][i]+ df_b["RTGS"][i] + df_b["Demand Draft"][i]+df_b["Internal Transactions"][i]+df_b["Others"][i]+df_b["IMPS"][i]+df_b["Online Transfers"][i]
    df_b.to_csv (r'fundreminatnce.csv', index = False, header=True)
  return df_b
  
def analysis_sheets(dfl,user_df):
  df=dfl.copy(deep=True)
  df["date"]=pd.to_datetime(df["date"],dayfirst=True,errors='coerce')
  df['month']=df['date'].dt.month
  df['year'] = pd.DatetimeIndex(df['date']).year
  df['month']=df['month'].fillna(0)
  df['month'] = df['month'].astype(int)
  Ac_hol=user_df['B'][0]
  #df['month name'] = pd.to_datetime(df['month'], format='%m').dt.month_name().str.slice(stop=3)
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  df['month year']=lm
  
  lm = list(dict.fromkeys(lm))
  print("########################################################")
  print(lm)
  mn=df["month"]
  mn = list(dict.fromkeys(mn))  
  
  dit={}
  dit["Particulars"]=lm
  dit["Opening"]=np.nan
  dit["Total Amount Of Debit Transactions"]=np.nan
  dit["Total Amount Of Credit Transactions"]=np.nan
  dit["Closing Balance"]=np.nan
  dit["Total No. of I/W Cheques Bounced: Insufficient Funds"]=np.nan
  dit["Sum of I/W Bounced Cheque: Insufficient Funds"]=np.nan
  dit["Total Number of Outward Cheque Bounces"]=np.nan
  dit["Inward Cheque Bounced %"]=np.nan
  dit["Total Number of Debit Transactions"]=np.nan
  dit["Total Number of Credit Transactions"]=np.nan
  dit["Minumum Balance"]=np.nan
  dit["Maximum Balance"]=np.nan
  dit["Monthly Average Balance"]=np.nan
  dit["Total Amount of Cash Deposit"]=np.nan
  dit["Total Amount of Cash Withdrawal"]=np.nan
  dit["Total Amount of Loan Credit"]=np.nan
  dit["Total Number of Cash deposit"]=np.nan
  dit["Total Number of Cash Withdraw"]=np.nan
  dit["Total Number of Cheque Deposit"]=np.nan
  dit["Total Amount of Cheque Deposit"]=np.nan
  dit["Total Number of Cheque Issues"]=np.nan  
  dit["Total Amount of Cheque Issues"]=np.nan
  dit["Total Number of Debit Internal Transactions"]=np.nan  
  dit["Total Number of Credit Internal Transactions"]=np.nan
  dit["Total Amount of Debit Internal Transactions"]=np.nan
  dit["Total Amount of Credit Internal Transactions"]=np.nan
  dit["Peak Utilization Limit"]=np.nan
  dit["Total Net Debit Amount"]=np.nan
  dit["Total Net Credit Amount"]=np.nan
  dit["Total Interest Paid"]=np.nan
  dit["Total Interest Received"]=np.nan
  dit["Min EOD Balance"]=np.nan
  dit["Max EOD Balance"]=np.nan
  dit["Average EOD Balance"]=np.nan
  dit["Self Withdraw"]=np.nan
  dit["Self Deposit"]=np.nan
  dit["Total No of Net Debit Transactions"]=np.nan
  dit["Total No of Net Credit Transactions"]=np.nan
  dit["Avg Utilization of OD/CC %"]=np.nan
  dit["Overdrawn Days"]=np.nan
  dit["NEFT Return"]=np.nan
  dit["Sanction Limit"]=np.nan
  dit["Balance on 1st"]=np.nan
  dit["Balance on 14th"]=np.nan
  dit["Balance on 30th/Last Day"]=np.nan
  dit["ABB on 1st,14th, 30th/Last Day"]=np.nan
  dit["Total No. of ECS/NACH Issued"]=np.nan
  dit["Total Amount of ECS/NACH Issued"]=np.nan
  dit["No. of EMI / loan payments"]=np.nan
  dit["Total Amount of EMI / loan Payments"]=np.nan
  dit["No.of Penalty Charges"]=np.nan
  dit["Total Amount of Penalty charges"]=np.nan
  dit["Interest Service Delay"]=np.nan
  dit["No. of Bank Charges"]=np.nan
  dit["Amount of Bank Charges"]=np.nan

  #we have created a dataframe from dictionary
  #print(dict)
  dfx=pd.DataFrame(dit)
  


  first=[]
  second=[]
  temp=[]
  for i in lm:
    print(i,"jkjkjkj")
  
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    f1=newdf['balance'].iloc[-1] 
    #f2=newdf['balance'][0]
    f3=newdf['balance'][0]
    #f1=newdf['balance'].iloc[-1] + newdf['debit'].iloc[-1] - newdf['credit'].iloc[-1]
    f2=newdf['balance'].iloc[-1]
   
  
    #print(df['credit'][0])
      
    #f2=(newdf["balance"][0] + (newdf["debit"][0]) - (newdf["credit"][0]) 
    first.append(f2)
    second.append(f1)
    temp.append(f3)
    print('============')
  print(first)
  print(second)
  print(temp)
  first1=first[:-1]
  print(type(first1))
    #print(temp[0])
  data=[]
  for i in range(len(first)):
    if i == 0:
      first1.insert(0,temp[0])

      
  print(first1,"update")
      
      
 
  nd=[]
  nc=[]
  
  for i in lm:
    c1=0
    c2=0
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    n1=newdf["credit"]
    n2=newdf["debit"]
    for i in n1:
      if(i != 0.0):
        c1=c1+1
    nc.append(c1)  
    for i in n2:
      if(i != 0.0):
        c2=c2+1 
    nd.append(c2)
  dfx["Opening"]=first1 
  dfx["Closing Balance"]=second 
  dfx["Total No of Net Credit Transactions"]=nc
  dfx["Total No of Net Debit Transactions"]=nd
  dfx["Total Number of Debit Transactions"]=nd
  dfx["Total Number of Credit Transactions"]=nc
  ad=[]
  ac=[]  
  for i in lm:
    s1=[]
    s2=[]
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    s1=newdf["debit"]
    s2=newdf["credit"]
    ad.append(s1.sum())
    ac.append(s2.sum())
  dfx["Total Amount Of Debit Transactions"]=ad
  dfx["Total Amount Of Credit Transactions"]=ac
  minb=[]
  maxb=[]
  avgb=[]
  for i in lm:
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    b1=newdf["balance"]

    minb.append(min(b1)) 
    maxb.append(max(b1)) 
    avgb.append((sum(b1)//len(b1))) 
  dfx["Minumum Balance"]=minb
  dfx["Maximum Balance"]=maxb  
  dfx["Monthly Average Balance"]=avgb
  minbal=[] 
  maxbal=[]
  avgbal=[]
  for i in lm:
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    eod=newdf["balance"]
    minbal.append(min(eod))
    maxbal.append(max(eod)) 
    avgbal.append((sum(eod)/len(eod)))   
  dfx["Min EOD Balance"]=minbal 	
  dfx["Max EOD Balance"]=maxbal 	
  dfx["Average EOD Balance"]=avgbal
  df['day']=df['date'].dt.day
  day1=[]
  day14=[]
  day30=[]
  
  da=[]
  for i in lm:
    D1B1=[]
    D14B1=[]
    D30B1=[]
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    ndg=newdf.shape
    print(df)
    
    for i in range(0,ndg[0]):
      limit=newdf['day'][0]
   
    for i in range(0,ndg[0]):
     
      if(newdf["day"][i]==limit):
        D1B1.append(newdf["balance"][i])
      if(newdf["day"][i] >=14 and newdf["day"][i] <=29):
        D14B1.append(newdf["balance"][i])

      D30B1.append(newdf["balance"][i])
    print("------")
    print(da)  
    if(len(D1B1)!=0):
      d1b=D1B1[0]
    else:
      d1b=0   
    if(len(D14B1)!=0):
      d14b=D14B1[0]
    else:
      d14b=0
    if(len(D30B1)!=0):
      d30b=D30B1[-1]
    else:
      d30b=0  
    day1.append(d1b) 
    day14.append(d14b) 
    day30.append(d30b)
  print(day1) 
  print("=====================================")
  dfx["Balance on 1st"]=day1
  dfx["Balance on 14th"]=day14
  dfx["Balance on 30th/Last Day"]=day30  


  deb_df=df.copy()
  d=deb_df.shape
  f=d[0]
  for i in range(0,f):
    if (deb_df["debit"][i]) == 0.0:
      deb_df.drop(i,inplace=True)
  deb_df.reset_index(inplace=True)
  deb_df.drop("index",axis=1,inplace=True)
  x1=[]
  x2=[]
  x3=[]
  x4=[]
  x5=[]
  x6=[]
  x7=[]
  x8=[]
  ndit=[]
  ncw=[]
  #nci=[]
  nbc=[]
  necs=[]
  tip=[]
  sw=[]
  npc=[]
  nelp=[]    
  for i in lm:
    self_deb=[]
    cash_deb=[]
    #cheq_deb=[]
    Intern_deb=[]
    ec_na_d=[]
    charges=[]
    penalty=[]
    interest_deb=[]
    loan_repay=[]
    new_deb_df=deb_df[deb_df['month year'] == i]
    new_deb_df.reset_index(inplace=True)
    nds=new_deb_df.shape
    nnd=nds[0]
    Ac_hol=user_df["B"][0]
    for i in range(0,nnd):
      s=new_deb_df["description"][i]
      t=s.lower()
      if (t.find("self") != -1 or t.find(Ac_hol) != -1):
        Intern_deb.append(i)  
      if (t.find("cash") != -1):
        cash_deb.append(i)
      if (t.find("self") != -1):
        self_deb.append(i)    
      if (t.find("charges") != -1 or t.find("chrgs") != -1 or t.find("dataahghadjgjgjagdj") != -1):
        charges.append(i)  
      if (t.find("penalty") != -1):
        penalty.append(i)      
      if (t.find("ecs") != -1 or t.find("nach") != -1):
        ec_na_d.append(i)      
      if (t.find("interest") != -1):
        interest_deb.append(i)  
      if (t.find("finance") != -1 or t.find("loan") != -1 or t.find("loan repayment") != -1):
        loan_repay.append(i) 
    ndit.append(len(Intern_deb))
    ncw.append(len(cash_deb))
    #nci.append(len(cheq_deb))       
    nbc.append(len(charges))
    necs.append(len(ec_na_d))
    tip.append(len(interest_deb))
    sw.append(len(self_deb))
    npc.append(len(penalty))
    nelp.append(len(loan_repay)) 
    tintern=[]
    for i in Intern_deb:
      tintern.append(new_deb_df["debit"][i])
    cash_w=[]
    for i in cash_deb:
      cash_w.append(new_deb_df["debit"][i])  
    bank_charges=[]
    for i in charges:
      bank_charges.append(new_deb_df["debit"][i])    
    penl=[]
    for i in penalty:
      penl.append(new_deb_df["debit"][i])
    Total_interest=[] 
    for i in interest_deb:
      Total_interest.append(new_deb_df["debit"][i])
    loan_payment=[] 
    for i in loan_repay:
      loan_payment.append(new_deb_df["debit"][i]) 
    Ecs_pay=[] 
    for i in ec_na_d:
      Ecs_pay.append(new_deb_df["debit"][i])  
    x1.append(sum(tintern))
    x2.append(sum(cash_w))
    x3.append(sum(bank_charges))
    x4.append(sum(penl))
    x5.append(sum(Total_interest))
    x6.append(sum(loan_payment))
    x7.append(sum(Ecs_pay))
  dfx["Total Number of Debit Internal Transactions"]=ndit
  dfx["Total Number of Cash Withdraw"]= ncw
  #dfx["Total Number of Cheque Issues"]=nci
  dfx["No. of Bank Charges"]=nbc
  dfx["Total No. of ECS/NACH Issued"]=necs
  dfx["Total Interest Paid"]=tip
  dfx["Self Withdraw"]=sw
  dfx["No.of Penalty Charges"]=npc
  dfx["No. of EMI / loan payments"]=nelp
  dfx["Total Amount of Cash Withdrawal"]=x2
  dfx["Total Amount of Penalty charges"]=x4
  dfx["Amount of Bank Charges"]=x3
  dfx["Total Amount of EMI / loan Payments"]=x6
  dfx["Total Amount of ECS/NACH Issued"]=x7
  dfx["Total Interest Paid"]=x5
  dfx["Total Amount of Debit Internal Transactions"]=x1  
  dfx["Total Net Debit Amount"]=ad
  dfx["Total Net Credit Amount"]=ac  
  

  ms=["cheque","I/W","O/W","WRONGLY DELIVERED / NOT DRAWN ON US","Outward Cheque Bounce","FUNDS INSUFFICIENT","INSTRUMENT OUTDATED / STALE","INSTRUMENT POST DATED","EXCEEDS ARRANGEMENT","OTHER REASONS - CONNECTIVITY FAILURE","TITLE OF ACCOUNT REQUIRED","OTHER REASONS","EFFECT NOT CLEAR, PRESENT AGAIN","DRAWERS SIGNATURE DIFFER","REFER TO DRAWER","ALTERATION REQUIRED DRAWERS AUTHENT","PAYMENT STOPPED BY DRAWER","CHQ IRREGULARLY DRAWN/AMT IN WORD"]
  ls=[]
  for i in ms:
    ls.append(i.lower())
  ls = list(dict.fromkeys(ls))
  n=len(ls)
  x=df.shape
  m=x[0]
  new=[]
  for i in range (0,m):
    y=df["description"][i]
    y=y.lower()
    for j in ls:
      if((y.find(j)) != -1):
        new.append(i)
        break
  aiw=[]
  now=[]
  niwf=[]
  iwprcnt=[]
  for i in lm:
    count=0
    ow=[]
    iw=[]
    iwF=[]
    cdf=df[df['month year'] == i]
    #print("ccccccccccccccccccccddddddddddddddddddddddddddddddddddddddddddddddddddffffffffffffffffffffffffffffffffffffffffffffff")
    #print(cdf)
    cdf["ind"]=cdf.index
    #cdf.reset_index(inplace=True)
    x=cdf["ind"]  
    #cdf.reset_index(inplace=True)
    #x=list(range(0,cdf.shape[0]))
    for j in new:
      if(j in x):
        jl=(cdf["description"][j]).lower()
        if(jl.find("o/w") != -1):
          ow.append(df["debit"][j])
        if(jl.find("i/w") != -1) and (jl.find("insufficient funds") != -1):  
          iwF.append(df["credit"][j])
        if(jl.find("i/w") != -1):
          iw.append(df["debit"][j]) 
    now.append(len(ow)) 
    niwf.append(len(iwF))
    aiw.append(sum(iwF))
    count=count+1   
    if (count==0):
      iwprcnt.append(0)
    else:
      iwprcnt.append((len(iw)/count)*100)
  dfx["Total No. of I/W Cheques Bounced: Insufficient Funds"]=niwf
  dfx["Total Number of Outward Cheque Bounces"]=now
  dfx["Sum of I/W Bounced Cheque: Insufficient Funds"]=aiw
  dfx["Inward Cheque Bounced %"]=iwprcnt  
  tcd=[]
  acd=[]
  acc=[]
  tcc=[]
  for i in lm:
    count=0
    oww=[]
    iww=[]
    chq_df=df[df['month year'] == i]
    chq_df.reset_index(inplace=True)
    rn=chq_df.shape
    for j in range(0,rn[0]):
      jl=(df["description"][j]).lower()
      if(jl.find("o/w") != -1):
        oww.append(chq_df["debit"][j])
      if(jl.find("i/w") != -1):
        iww.append(chq_df["credit"][j])  
    acc.append(sum(iww))
    acd.append(sum(oww))
    tcc.append(len(iww))
    tcd.append(len(oww))   
  dfx["Total Number of Cheque Issues "]=tcc
  dfx["Total Number of Cheque Deposit"]=tcd
  dfx["Total Amount of Cheque Deposit "]=acc
  dfx["Total Amount of Cheque Issues"]=acd  
  

  cred_df=df.copy()
  f1=(cred_df.shape)[0]
  for i in range(0,f1):
    if (cred_df["credit"][i]) == 0.0:
      cred_df.drop(i,inplace=True)
  cred_df.reset_index(inplace=True)
  cred_df.drop("index",axis=1,inplace=True)
  x1=[]
  x2=[]
  x3=[] 
  x4=[]
  x5=[]
  x6=[]
  x7=[]
  x8=[]
  for i in lm:
    self_cred=[]
    cash_cred=[]
    #cheq_deb=[]
    Intern_cred=[]
    Interest_rec=[]
    neft_return=[]
    loan_cred=[]
    new_cred_df=cred_df[cred_df['month year'] == i]
    new_cred_df.reset_index(inplace=True)
    shp=new_cred_df.shape
    sz=shp[0]
    Ac_hol=myfun()
    for i in range(0,sz):
      s=new_cred_df["description"][i]
      t=s.lower()
      
      
      
      if (t.find("self") != -1 or t.find(Ac_hol) != -1):
        Intern_cred.append(i)  
      if (t.find("cash") != -1):
        cash_cred.append(i) 
      if (t.find("self") != -1):
        self_cred.append(i)    
      if (t.find("neft") != -1):
        neft_return.append(i)      
      if (t.find("interest") != -1):
        Interest_rec.append(i)  
      if (t.find("finance") != -1 or t.find("loan") != -1 or t.find("loan repayment") != -1):
        loan_cred.append(i)   
    x1.append(len(Intern_cred))
    x2.append(len(cash_cred))
    #nci.append(len(cheq_deb))       
    tintern_cred=[]
    for i in Intern_cred:
      tintern_cred.append(new_cred_df["credit"][i])    
    cash_dep=[]
    for i in cash_cred:
      cash_dep.append(new_cred_df["credit"][i])
    Total_interest_cred=[] 
    for i in Interest_rec:
      Total_interest_cred.append(new_cred_df["credit"][i])
    Tloan_rec=[] 
    for i in loan_cred:
      Tloan_rec.append(new_cred_df["credit"][i]) 
    neft_cred=[] 
    for i in neft_return:
      neft_cred.append(new_cred_df["credit"][i])  
    Tself_cred=[] 
    for i in self_cred:
      Tself_cred.append(new_cred_df["credit"][i])
    x3.append(sum(tintern_cred))
    x4.append(sum(cash_dep))
    x5.append(sum(Total_interest_cred))
    x6.append(sum(Tloan_rec))
    x7.append(sum(neft_cred))
    x8.append(sum(Tself_cred)) 
  dfx["Total Number of Credit Internal Transactions"]=x1
  dfx["Total Amount of Credit Internal Transactions"]=x3 
  dfx["Total Amount of Loan Credit"]=x6
  dfx["Total Number of Cash deposit"]=x2
  dfx["Total Interest Received"]=x5
  dfx["Self Deposit"]=x8
  dfx["NEFT Return"]=x7
  dfx["Total Amount of Cash Deposit"]=x4  
  dfx=dfx
  dfx.to_csv (r'imonthly.csv', index = False, header=True)
  #print(dfx)
  return dfx

def FrequentCr(dfl):
  df=dfl.copy(deep=True)
  u=[]
  for i in range(0,len(df["credit"].isnull())):
      if (df["credit"].isnull())[i]==True:
          df.drop(i,inplace=True)
  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True) 
  df["Description"] = df["description"]
  for i in range(0,(df.shape)[0]):
    d=df["description"][i]
    x=d.replace("[","")
    y=x.replace("]","")
    z=y.replace("'","")
    df["description"][i]=z  
  df['description'] = df['description'].replace("[A-Za-z]\w+/\d+/[A-Z]\w+","",regex=True)
  df['description'] = df['description'].replace("[A-Za-z]\w+/\d+/\d+/+","",regex=True)  
  for i in range(0,(df.shape)[0]):
    d=df["description"][i]
    x=d.replace("/","")
    df["description"][i]=x
  ind=[]
  for i in range(0,(df.shape)[0]):
    count=0
    for j in range(0,(df.shape)[0]):
      if(df["description"][j]==(df["description"][i])):
        count=count+1
    if count >= 2:
        ind.append(i)
  dte=[]
  des=[]
  tt=[]
  deb=[]
  for i in ind:
    dte.append(df["date"][i])
    des.append(df["Description"][i])
    tt.append(df["description"][i])
    deb.append(df["credit"][i])  
  dict={}
  dict["Date"]=dte
  dict["Description"]=des
  dict["Transfer To"]=tt
  dict["Amount"]=deb
  df_banking2=pd.DataFrame(dict)
  df_banking2=df_banking2.sort_values(by=['Transfer To'])
  u.append((df_banking2, "Freq Cr"))
  df_banking2["Amount"]=df_banking2["Amount"].astype(str)
  df_banking2['Amount'] = df_banking2['Amount'].str.replace(r'\D', '')
  df_banking2['Amount']=pd.to_numeric(df_banking2['Amount'], errors='coerce')
  df_banking2['Amount']=df_banking2['Amount'].apply(lambda x: x/10)
  TotalAmt=[]
  for i in range(0,(df_banking2.shape)[0]):
    total=0
    for j in range(0,(df_banking2.shape)[0]):
      if(df_banking2["Transfer To"][j]==(df_banking2["Transfer To"][i])):
        total=total+(df_banking2["Amount"][j])
    TotalAmt.append(total)
  countl=df_banking2["Transfer To"]
  cl=[]
  dcl=[]
  for i in countl:
    count=0
    for j in countl:
        if(j==i):
          count=count+1
    cl.append(count)
    dcl.append(i)      
  dicn={}
  dicn["Description"]=dcl
  dicn["count"]=cl
  dicn["Amount"]=TotalAmt
  df_bank=pd.DataFrame(dicn)  
  df_bank.drop_duplicates(subset ="Description",keep = "first", inplace = True)
  u.append((df_bank, "Freq Cr"))
  df_bank=df_bank.fillna('')
  return df_bank
  
  
def FrequentDb(dfl):
  df=dfl.copy(deep=True)
  g=[]
  for i in range(0,len(df["debit"].isnull())):
    if (df["debit"].isnull())[i]==True:
      df.drop(i,inplace=True)  
  df.reset_index(inplace=True)  
  df.drop("index",axis=1,inplace=True) 
  df["Description"] = df["description"] 
  df['description'] = df['description'].replace("[A-Za-z]\w+/\d+/[A-Z]\w+","",regex=True)
  df['description'] = df['description'].replace("[A-Za-z]\w+/\d+/\d+/+","",regex=True)
  for i in range(0,(df.shape)[0]):
    d=df["description"][i]
    x=d.replace("/","")
    df["description"][i]=x 
  ind=[]
  for i in range(0,(df.shape)[0]):
    count=0
    for j in range(0,(df.shape)[0]):
      if(df["description"][j]==(df["description"][i])):
        count=count+1  
    if count >= 2:
      ind.append(i)  
  dte=[]
  des=[]
  tt=[]
  deb=[]
  for i in ind:
    dte.append(df["date"][i])
    des.append(df["Description"][i])
    tt.append(df["description"][i])
    deb.append(df["debit"][i])    
  dict={}
  dict["Date"]=dte
  dict["Description"]=des
  dict["Transfer To"]=tt
  dict["Amount"]=deb
  df_banking2=pd.DataFrame(dict)
  df_banking2=df_banking2.sort_values(by=['Transfer To'])  
  g.append((df_banking2, "Freq Dr"))  
  df_banking2["Amount"]=df_banking2["Amount"].astype(str)
  df_banking2['Amount'] = df_banking2['Amount'].str.replace(r'\D', '')
  df_banking2['Amount']=pd.to_numeric(df_banking2['Amount'], errors='coerce')
  df_banking2['Amount']=df_banking2['Amount'].apply(lambda x: x/10)
  TotalAmt=[]
  for i in range(0,(df_banking2.shape[0])):
    total=0
    for j in range(0,(df_banking2.shape[0])):
      if(df_banking2["Transfer To"][j]==(df_banking2["Transfer To"][i])):
           total=total+(df_banking2["Amount"][j])
    TotalAmt.append(total) 
  countl=df_banking2["Transfer To"]
  cl=[]
  dcl=[]
  for i in countl:
    count=0       
    for j in countl:
      if(j==i):
        count=count+1
    cl.append(count)
    dcl.append(i)
  dicn={}
  dicn["Description"]=dcl
  dicn["count"]=cl
  dicn["Amount"]=TotalAmt
  df_bank=pd.DataFrame(dicn)
  df_bank.drop_duplicates(subset ="Description",keep = "first", inplace = True)
  g.append((df_bank, "Freq Dr"))
  return df_bank 

def average_Monthy(dfl):
  df=dfl.copy(deep=True)
  df['month']=df['date'].dt.month
  df["day"]=df["date"].dt.day
 
  df["day"]=df["day"].astype(str)
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])        
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  df["month year"]=lm
  lm = list(dict.fromkeys(lm))
  
  l=lm                           
  l= list(dict.fromkeys(l))
  
  l1=[]
  l5=[]  
  l10=[]
  l15=[]
  l20=[]
  l25=[]
  l30=[]
  cl=[]
  for i in range(0,len(l)):
    m1=[]
    f=[]
    for j in range(0,(df.shape)[0]):
      if (df["month year"][j] == l[i]):
        f.append(j)
    for j in f:
      if (df["month year"][j] == l[0]):
        m1.append(0)
      else:
        kl=[]    
        for k in range(0,(df.shape)[0]):
          if(df["month year"][k]==l[i-1]):
            kl.append(k) 
        m1.append(df["balance"][kl[-1]])       
    l1.append(m1[-1])
  for i in l:
    m1=[]
    f=[]
    for j in range(0,(df.shape)[0]):  
      if (df["month year"][j] == i):
        f.append(j)
    for j in f:
      if ((df["day"][j]) == "5"):
        m1.append(df["balance"][j])    
    if len(m1) == 0:
      m1.append(0)
   
    l5.append(m1[-1])    
    m1=[]
    f=[]
    for j in range(0,(df.shape)[0]):
        if (df["month year"][j] == i):
          f.append(j)
    for j in f:
      if ((df["day"][j]) == "10"):
        m1.append(df["balance"][j])
    if len(m1) == 0:
      m1.append(0)      
    l10.append(m1[-1])   
     
    m1=[]
    f=[]
    for j in range(0,(df.shape)[0]):
      if (df["month year"][j] == i):
        f.append(j) 
    for j in f:
      if ((df["day"][j]) == "15"):
        m1.append(df["balance"][j])
    if len(m1) == 0:
        m1.append(0) 
    l15.append(m1[-1])     
    m1=[]
    f=[]
    for j in range(0,(df.shape)[0]):
      if (df["month year"][j] == i):
        f.append(j)
    for j in f:
      if ((df["day"][j]) == "20"):
        m1.append(df["balance"][j])
    if len(m1) == 0:
      m1.append(0)    
    l20.append(m1[-1]) 
    
    m1=[]
    f=[]
    for j in range(0,(df.shape)[0]):
      if (df["month year"][j] == i):
        f.append(j)
    for j in f:
      if ((df["day"][j]) == "25"):
        m1.append(df["balance"][j])
    if len(m1) == 0:
      m1.append(0)
    l25.append(m1[-1]) 

    m1=[]
    f=[]
    for j in range(0,(df.shape)[0]):
      if (df["month year"][j] == i):
        f.append(j)  
    for j in f:
      if ((df["day"][j]) == "30"):
        m1.append(df["balance"][j])
    if len(m1) == 0:
      m1.append(0)    
    l30.append(m1[-1]) 
  dict2={}
  dict2["Month"]=lm
  dict2["1st"]=l1
  dict2["5th"]=l5
  dict2["10th"]=l10
  dict2["15th"]=l15
  dict2["20th"]=l20
  dict2["25th"]=l25
  dict2["30th"]=l30
  dict2["Monthly"]=np.nan
  #we have created a dataframe from dictionary
  #print(dict)
  df_bank=pd.DataFrame(dict2)        
  return df_bank

def opening_bal(dfl):
  df=dfl.copy(deep=True)
  lsa=[]
  lsa=df["balance"]+df["debit"]-df["credit"]
  
  c=df["balance"]
  dt=[]
  for i in range(0,(df.shape)[0]):
    dt.append(df["date"][i])
  dn={}
  dn["Date"]=dt
  dn["Opening Balance"]=lsa
  dn["Closing Balance"]=c
#we have created a dataframe from dictionary
#print(dict)
  dfx=pd.DataFrame(dn)
  return dfx

def penalty(dfl):
  df=dfl.copy(deep=True)
  df.columns = df.columns.str.lower()
  debit_colname = "debit"
  desc_colname = "description"
  df[desc_colname] = df[desc_colname].astype(str)
  df = df[df[debit_colname].notna()]  
  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True)
  c=['penalty']
  penalty_total = df[df[desc_colname].str.contains("|".join(c), case = False)]  
  lp=[]
  dt=[]
  des=[]
  deb=[]
  bal=[]
  for i, row in penalty_total.iterrows():
    dt.append(df["date"][i])
    des.append(df["description"][i])
    deb.append(df["debit"][i])
    bal.append(df["balance"][i])
    tmp = str(row[desc_colname]).lower()
    if(tmp.find("penalty for minimum balance") != -1):
        lp.append("penalty for minimum Balance")
    else:
        lp.append("Others")

  dict3={}
  dict3["Date"]=dt
  dict3["Description"]=des
  dict3["Category"]=lp
  dict3["Debit"]=deb
  dict3["Balance"]=bal
#we have created a dataframe from dictionary
#print(dict)
  dfx=pd.DataFrame(dict3)
  return dfx

def credit(dfl):
  df=dfl.copy(deep=True)
  df['month']=df['date'].dt.month
  l=df["month"]
  l= list(dict.fromkeys(l))
  df["Day"]=df["date"].dt.day
  df.columns = df.columns.str.lower()
  debit_colname = "debit"
  desc_colname = "description"
  df[desc_colname] = df[desc_colname].astype(str)

  df = df[df[debit_colname].notna()]      

  c = ["credit card"]
  credit_total = df[df[desc_colname].str.contains("|".join(c), case = False)]

  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True)
  mn=df['month']
  mn= list(dict.fromkeys(mn))
  nk=[]
  month = []
  for i in mn:
    month.append(calendar.month_name[i])
    nk.append(credit_total[credit_total["month"] == i]["debit"].sum())

  d={}

  d["Month"]=month
  d["Amount"]=nk
  #we have created a dataframe from dictionary
  #print(dict)
  df_bank=pd.DataFrame(d)
  return df_bank

def Dividend(dfl):
  df=dfl.copy(deep=True)  
  df.columns = df.columns.str.lower()
  desc_colname = "description"
  df[desc_colname] = df[desc_colname].astype(str)
  credit_colname = 'credit'

  df = df[df[credit_colname].notna()]       
  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True)
  c=['zerodha brokin','dividend']
  dividend_total = df.index[df[desc_colname].str.contains("|".join(c), case = False)].tolist()            
  lp = []
  dt=[]
  des=[]
  cred=[]
  bal=[]
  for i in dividend_total:
    dt.append(df["date"][i])
    des.append(df["description"][i])
    cred.append(df["credit"][i])
    bal.append(df["balance"][i])
    lp.append("DIVIDEND")
  dx={}
  dx["Date"]=dt
  dx["Description"]=des
  dx["Category"]=lp
  dx["Credit"]=cred
  dx["Balance"]=bal
  #print(dict)
  dfx=pd.DataFrame(dx)
  return dfx

def high_value(dfl):
  df=dfl.copy(deep=True)
  scred=df.sort_values(by=(["credit"]),ascending=False)
  highcred=scred.head(5)
  sdeb=df.sort_values(by=(["debit"]),ascending=False)
  highdeb=sdeb.head(5)
  finalhigh=highdeb.append(highcred)
  finalhigh.sort_values(by=(["date"]),ascending=False)
  return highdeb
  #return finalhigh, "Saving Analysis"

def credit_analysis(df):
  df = df.copy(deep=True)
  for i in range(0,len(df["credit"].isnull())):
    if (df["credit"].isnull())[i]==True:
        df.drop(i,inplace=True)
  df.reset_index(inplace=True)       
  df.drop("index",axis=1,inplace=True)
  df["credit"]=df["credit"].astype(str)
  df['credit'] = df['credit'].str.replace(r'\D', '')
  df['credit']=pd.to_numeric(df['credit'], errors='coerce')
  df['credit']=df['credit'].apply(lambda x: x/100)
  df["month"]=df["date"].dt.month
  ml=df["month"]
  ml = list(dict.fromkeys(ml))
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])        
  mtn=df["month name"]
  mtn = list(dict.fromkeys(mtn))
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  df["month year"]=lm
  lm = list(dict.fromkeys(lm))
  df['year'] = pd.DatetimeIndex(df['date']).year
  
  NEFT=[]
  ECS=[]
  OTHERS=[]
  CASH=[]
  CHEQUE=[]
  for i in lm:                 #for iterating months
    neft=[]
    ecs=[]
    cheque=[]
    cash=[]
    Others=[]
    dfn=df[df['month year'] == i]
    dfn.reset_index(inplace=True)
    for q in range(0,(dfn.shape)[0]):
      k=(dfn["description"][q]).upper()
      if((k.find("NEFT FM")) != -1 or k.find("RTGS FM") != -1):
        neft.append(dfn["credit"][q])
      elif((k.find("ECS")) != -1 or k.find("NACH") != -1):
        ecs.append(dfn["credit"][q])
      elif((k.find("CASH")) != -1 ):
        cash.append(dfn["credit"][q])    
      elif((k.find("I/W")) != -1 ):
        cheque.append(dfn["credit"][q])  
      else:
        Others.append(dfn["credit"][q])
    NEFT.append(sum(neft))
    ECS.append(sum(ecs))       
    CASH.append(sum(cash))
    CHEQUE.append(sum(cheque))
    OTHERS.append(sum(Others))
  df_dict={}
  df_dict["Month"]=lm
  df_dict["Cash Recieved"]=CASH
  df_dict["Cheque Recieved"]=CHEQUE
  df_dict["NEFT/RTGS"]=NEFT
  df_dict["ECS/NACH"]=ECS
  df_dict["Non-Identified"]=OTHERS
  #we have created a dataframe from dictionary
  df_b=pd.DataFrame(df_dict)
  return df_b

def debit_analysis(df):
  df = df.copy(deep=True)
  for i in range(0,len(df["debit"].isnull())):
    if (df["debit"].isnull())[i]==True:
        df.drop(i,inplace=True)
  df.reset_index(inplace=True)       
  df.drop("index",axis=1,inplace=True)
  df["debit"]=df["debit"].astype(str)
  df['debit'] = df['debit'].str.replace(r'\D', '')
  df['debit']=pd.to_numeric(df['debit'], errors='coerce')
  df['debit']=df['debit'].apply(lambda x: x/100)
  df["month"]=df["date"].dt.month
  ml=df["month"]
  ml = list(dict.fromkeys(ml))
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])        
  mtn=df["month name"]
  mtn = list(dict.fromkeys(mtn))
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  df["month year"]=lm
  lm = list(dict.fromkeys(lm))
  df['year'] = pd.DatetimeIndex(df['date']).year
  
  NEFT=[]
  ECS=[]
  OTHERS=[]
  CASH=[]
  CHEQUE=[]
  for i in lm:                #for iterating in years
    neft=[]
    ecs=[]
    cheque=[]
    cash=[]
    Others=[]
    dfn=df[df['month year'] == i]
    dfn.reset_index(inplace=True)
    f1=dfn.shape
    hj=f1[0]
    for q in range(0,hj):
      s=dfn["description"][q]
      k=s.upper()
      if((k.find("NEFT TO")) != -1 or k.find("RTGS TO") != -1):
        neft.append(dfn["debit"][q])
      elif((k.find("ECS")) != -1 or k.find("NACH") != -1):
        ecs.append(dfn["debit"][q])
      elif((k.find("CASH")) != -1 ):
        cash.append(dfn["debit"][q])    
      elif((k.find("O/W")) != -1 ):
        cheque.append(dfn["debit"][q])  
      else:
        Others.append(dfn["debit"][q])
    NEFT.append(sum(neft))
    ECS.append(sum(ecs))       
    CASH.append(sum(cash))
    CHEQUE.append(sum(cheque))
    OTHERS.append(sum(Others))

  df_dict={}

  df_dict["Month"]=lm
  df_dict["Cash Recieved"]=CASH
  df_dict["Cheque Recieved"]=CHEQUE
  df_dict["NEFT/RTGS"]=NEFT
  df_dict["ECS/NACH"]=ECS
  df_dict["Non-Identified"]=OTHERS
  #we have created a dataframe from dictionary
  #print(dict)
  df_b=pd.DataFrame.from_dict(df_dict)
  return df_b

def finance_analysis(df):
  df = df.copy(deep=True)
  h=["Allahabad Bank","American Express","Andhra Bank","Axis Bank","Bandhan Bank","Bank of Baroda","Bank of India","Bank of Maharashtra","Canara Bank","Catholic Syrian Bank Ltd.","Central Bank of India","Citibank","City Union Bank","Corporation Bank","DCB Bank","Dena Bank","Deutsche Bank","Dhanlaxmi Bank","DBS Bank","Federal Bank","HDFC Bank","HSBC Bank","ICICI Bank","IDBI Bank","IDFC Bank","Indian Bank","Indian Overseas Bank","IndusInd Bank","J&K Bank","Karnataka Bank","Karur Vysya Bank","Kotak Mahindra Bank","Lakshmi Vilas Bank","Nainital Bank","Oriental Bank of Commerce","Punjab & Sind Bank","Punjab National Bank","RBL Bank","South Indian Bank","Standard Chartered Bank","State Bank of India","Syndicate Bank","Tamilnad Mercantile Bank","UCO Bank","Union Bank of India","United Bank of India","Vijaya Bank  YES Bank","Bajaj Finserv","Capital First","Citicorp Finance (India) Limited","Credila","DHFL","India Infoline Finance Limited","Indiabulls","LIC Housing Finance Limited","Manappuram Finance","Muthoot Finance","PNB Housing","Tata Capital","Reliance Home Finance","Shriram Housing Finance","Sundaram Finance","AU Small Finance Bank","Capital Small Finance Bank","ESAF Small Finance Bank","Equitas Small Finance Bank","Fincare Small Finance Bank","Jana Small Finance Bank","North East Small Finance Bank","Suryoday Small Finance Bank","Ujjivan Small Finance Bank","Utkarsh Small Finance Bank"]

  h = [x.upper() for x in h] 


  df["description"]=df["description"].astype(str)
  desc_colname = "description"
  x0=['Particular']
  df.drop(df[df[desc_colname].str.contains("|".join(x0), case = False)].index, inplace = True)

  df["month"]=df["date"].dt.month

  df["debit"]=df["debit"].astype(str)
  df["credit"]=df["credit"].astype(str)

  df['debit'] = df['debit'].str.replace(r'\D', '')
  df['credit'] = df['credit'].str.replace(r'\D', '')

  df['debit']=pd.to_numeric(df['debit'], errors='coerce')
  df['credit']=pd.to_numeric(df['credit'], errors='coerce')

  df['credit']=df['credit'].apply(lambda x: x/100)
  df['debit']=df['debit'].apply(lambda x: x/100)

  df['debit']=df['debit'].fillna(0) 
  df['credit']=df['credit'].fillna(0) 

  mn=df["month"]
  months = []
  mn = list(dict.fromkeys(mn))
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])        
  mtn=df["month name"]
  mtn = list(dict.fromkeys(mtn))
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  df["month year"]=lm
  lm = list(dict.fromkeys(lm))
  df['year'] = pd.DatetimeIndex(df['date']).year
  
  debf=[]
  credf=[]
  debcount=[]
  credcount=[]
  for month in lm:
    db=[] 
    
    cd=[]

    dfn=df[df['month year'] == month]
    dfn.reset_index(inplace=True)
    
    dfn = dfn[dfn[desc_colname].str.contains("|".join(h), case = False)]
    for i,row in dfn.iterrows():
          if(row['credit'] != 0):
              cd.append(row['credit'])
          if(row["debit"] != 0):
              db.append(row["debit"])
    debf.append(sum(db))
    credf.append(sum(cd))
    debcount.append(len(db)) 
    credcount.append(len(cd))
    #months.append(calendar.month_name["month"])
  df_dict={}
  df_dict["Month"]=lm
  df_dict["Debit"]=debf
  df_dict["Debit Transaction"]=debcount
  df_dict["Credit"]=credf
  df_dict["Credit Transaction"]=credcount
  #we have created a dataframe from dictionary
  #print(dict)
  df_b=pd.DataFrame(df_dict)
  return df_b

def internal_txn(df):
  df = df.copy(deep=True)
  desc_colname = "description"
  df[desc_colname] = df[desc_colname].astype(str)
  c=['arrowline','self']
  internal_total = df.index[df[desc_colname].str.contains("|".join(c), case = False)].tolist()            
  lp=[]

  dt=[]
  dsc=[]
  dbt=[]
  crt=[]
  blc=[]
  for i in internal_total:
      lp.append("Internal Transaction")
      dt.append(df["date"][i])
      dsc.append(df["description"][i])
      dbt.append(df["debit"][i])
      crt.append(df["credit"][i])
      blc.append(df["balance"][i])
  df_dict={}
  df_dict["Date"]=dt
  df_dict["Description"]=dsc
  df_dict["Category"]=lp
  df_dict["Debit"]=dbt
  df_dict["Credit"]=crt
  df_dict["Balance"]=blc
  #we have created a dataframe from dictionary
  #print(dict)
  dfx=pd.DataFrame(df_dict)
  return dfx

def interest_analysis(df):
  df = df.copy(deep=True)
  desc_colname="description"
  cred_colname="credit"
  df[desc_colname] = df[desc_colname].astype(str)
  df = df[df[cred_colname].notna()]
  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True)
  rows = df.shape[0]
  c = ['interest']
  interest_total = df.index[df[desc_colname].str.contains('|'.join(c), case = False)].tolist()
  dt=[]
  des=[]
  cred=[]
  bal=[]
  categories = []
  for i in interest_total:
      dt.append(df["date"][i])
      des.append(df["description"][i])
      cred.append(df["credit"][i])
      bal.append(df["balance"][i])
      categories.append("INTEREST")

  df_dict={}
  df_dict["Date"]=dt
  df_dict["Description"]=des
  df_dict["Category"]=categories
  df_dict["Credit"]=cred
  df_dict["Balance"]=bal
  dfx=pd.DataFrame(df_dict)
  return dfx

def average_Quaterly_analysis(dfn):
  #df["date"]=pd.to_datetime(df["Date"],dayfirst=True,errors='coerce')
  df = dfn.copy(deep=True)
  df["month"]=df["date"].dt.month
  df['year'] = pd.DatetimeIndex(df['date']).year
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
  mtn=df["month name"]
  mtn = list(dict.fromkeys(mtn))
  mn=df["month"]
  mn = list(dict.fromkeys(mn))
  df['year'] = pd.DatetimeIndex(df['date']).year
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  df["month year"]=lm
  lm = list(dict.fromkeys(lm))
  
  Mon=lm
  #print("Print Mon")
  #print(Mon)
  Mon2=Mon[2:len(Mon):3]
  #print("print Mon2")
  #print(Mon2)
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  lm = list(dict.fromkeys(lm))
  f=[]
  for j in range(0,len(lm)):
      if(j<=(len(lm)-3)):
          x=f"{lm[j]}-{lm[j+2]}"
          f.append(x)
  df['balance']= df['balance'].astype(str)
  df['balance'] = df['balance'].str.replace(r'\D', '')
  df['balance']=pd.to_numeric(df['balance'], errors='coerce')
  df['balance']=df['balance'].apply(lambda x: x/100) 
  fl=[]
  for i in Mon2:
      g = []
      cb = 0
      for j in range(0,(df.shape)[0]):
      		
          
          if df["month year"][j] <= i:
          		
          	  #print("ssssssssssssssss")
          	  #print(df["month year"][j])
          	  g.append(df["balance"][j])
      for j in g:
      	  cb = cb + j
      fl.append(cb)
  print(fl)    
  f1x = list(map(lambda x:x/3,fl))
  df_dict={}
  df_dict["Month"]=f
  df_dict["Amount"]=f1x
  #we have created a dataframe from dictionary
  #print(dict)
  #print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
  #print(df_dict)
  #df_bank=pd.DataFrame(df_dict)        
  dfx = pd.DataFrame.from_dict(df_dict, orient='index')
  dfx = dfx.transpose()
  #dfx=pd.DataFrame(df_dict)
  #print(df_dict)    
  return dfx 
  #return df_bank

def loan_analysis(df):
  df = df.copy(deep=True)
  desc_colname="description"
  debit_colname="debit"
  df[desc_colname] = df[desc_colname].astype(str)
  df = df[df[debit_colname].notna()]      
  df.reset_index(inplace=True)
  df.drop("index",axis=1,inplace=True)
  c=['loan','finance','loan repayment']
  loan_total = df.index[df[desc_colname].str.contains("|".join(c), case = False)].tolist()
  dt=[]
  des=[]
  deb=[]
  bal=[]
  categories = []
  for i in loan_total:
      dt.append(df["date"][i])
      des.append(df["description"][i])
      deb.append(df["debit"][i])
      bal.append(df["balance"][i])
      categories.append("Loan Repayment")
  df_dict={}
  df_dict["Date"]=dt
  df_dict["Description"]=des
  df_dict["Category"]=categories
  df_dict["credit"]=deb
  df_dict["Balance"]=bal
  
  dfx=pd.DataFrame(df_dict)
  print(df_dict)    
  return dfx 

def chartsfrequent(df):
  df = df.copy(deep = True)
  df['description'] = df['description'].replace("[A-Za-z]\w+/\d+/[A-Z]\w+","",regex=True)
  df['description'] = df['description'].replace("[A-Za-z]\w+/\d+/\d+/+","",regex=True)
  w=df.shape
  s=w[0]
  for i in range(0,s):
    d=df["description"][i]
    x=d.replace("/","")
    df["description"][i]=x

  x=df.shape
  m=x[0]

  ind=[]
  for i in range(0,m):
      count=0
      x=df["description"][i]
      for j in range(0,m):
          if(df["description"][j]==x):
              count=count+1
      if count >= 2:
          ind.append(i)
          
    
  result=pd.DataFrame()
  for i in ind:
      x=df.iloc[i]
      result=result.append(x)
  result.reset_index(inplace=True)
  result["credit"]=result["credit"].replace("\s",np.nan).astype(float)
  result["debit"]=result["debit"].replace("\s",np.nan).astype(float)
  result["credit"].fillna(0,inplace=True)
  result["debit"].fillna(0,inplace=True)
  for i in range(0,result.shape[0]):
      if result["credit"][i]==0:
          am=result["debit"][i]
          result.loc[i,"amount"]=am
          result.loc[i,"type"]="debit"
      else:
          am=result["credit"][i]
          result.loc[i,"amount"]=am
          result.loc[i,"type"]="credit"
      
  result.drop("description",axis=1,inplace=True)
  #result.drop("Unnamed: 0",axis=1,inplace=True)
  result.drop("debit",axis=1,inplace=True)
  result.drop("balance",axis=1,inplace=True)
  result.drop("index",axis=1,inplace=True)
  result.drop("credit",axis=1,inplace=True)
  return result



def statement_charts(df):
  df = df.copy(deep = True)
  result = df.groupby([df['date'].dt.year, df['date'].dt.month]).agg({'debit':['count', 'sum'], 'credit':['count', 'sum'], 'balance': lambda x: x.iloc[-1]})
  result.columns = result.columns.droplevel(0)
  result.columns = ['No. of debits', 'debit_amount', 'No. of credits', 'Credit_amount', 'Closing Balance']
  result.index.names = ['year', 'months']
  result.reset_index(level =['year', 'months'], inplace = True) 
  result.drop("year",axis=1,inplace=True)
  result['months'] = result['months'].apply(lambda x: calendar.month_name[x])
  return result

def Non_rev(dfl):
  df = dfl.copy(deep = True)
  print("nonrev",df.head(5))
  for i in range(0,(df.shape)[0]):
    f=df["description"][i]
    f=f.replace("\n"," ")
    df["description"][i]=f
  nonrevenue=["Charges","TO CLG VT TDS","TAX","Chq Deposited And Return","FUNDS INSUFFICIENT","chrg:","charge","charges","CHQ","CHARGES","Chrg"]
  lst=[]
  for i in df["description"]:
    for j in nonrevenue:
      if j in i:
        lst.append(i)
        break
  result=pd.DataFrame()
  for i in lst:
    x=df[df["description"]==i]
    result=result.append(x) 
    result.to_csv (r'non.csv', index = False, header=True)
  print("nonrevene ka result-",result)
  return result

def salary_analysis(df):
  df = df.copy(deep = True)
  result_final = []
  df["date"]=pd.to_datetime(df["date"],dayfirst=True,errors="coerce")
  df["description"]=df["description"].str.replace("[","",regex=True)
  df["description"]=df["description"].str.replace(",","",regex=True)
  df["description"]=df["description"].str.replace("]","",regex=True)
  df["description"]=df["description"].str.replace("nan","",regex=True)
  df["description"]=df["description"].str.replace("\'","",regex=True)
  salary=["SAL","SALARY","BONUS","sal","Salary"]
  df["description"]=df["description"].str.replace("\n","",regex=True)
  df["description"]=df["description"].str.replace("\\","",regex=True)
  df[df["description"]==" Charge Tran: Minimum Balance charges"]
  df['balance']=df['balance'].astype(float)
  result3=df[df["balance"]<500]
  result3.reset_index(inplace=True)
  result3.drop("index",axis=1,inplace=True)
  result_final.append((result3, "Saving Analysis"))
  #result3.to_excel("minmumbalance.xlsx",index=False)
  lst=[]
  lst2=[]
  result1=pd.DataFrame()
  result2=pd.DataFrame()
  result1 = df[df["description"].str.contains("|".join(salary), case = False)]
  result2 = df[~df["description"].str.contains("|".join(salary), case = False)]

  df["credit"]=df["credit"].replace("\s",np.nan,regex=True)
  df["credit"]=df["credit"].astype(float)
  df["credit"].fillna(0,inplace=True)
  df["debit"]=df["debit"].replace("\s",np.nan,regex=True)

  df["debit"]=df["debit"].astype(float)

  df["debit"].fillna(0,inplace=True)
  df[df["credit"]==np.nan]

  result2.reset_index(inplace=True)
  result2.drop("index",axis=1,inplace=True)
  result1.reset_index(inplace=True)
  result1.drop("index",axis=1,inplace=True)

  refund=["CASHBACK","REV"]
  result2["description"]=result2["description"].astype(str)
  lst5=[]
  for i in df["description"]:
      if "CSH" in i:
          lst5.append(i)
      elif "CASH" in i:
          lst5.append(i)
      elif "DEPOSIT" in i:
          lst5.append(i)
      elif "CD" in i:
          lst5.append(i)
      elif "CDS" in i:
          lst5.append(i)   

  result4=pd.DataFrame()
  for i in lst5:
      x=df[(df["description"]==i) &(df["debit"]==0)]
      result4=result4.append(x)     
  df["description"]=df["description"].str.upper()
  lst6=[]
  for i in df["description"]:
      if "ZERODHA" in i:
          lst6.append(i)
      elif ("LIC" in i) & ("LOAN" not in i) :
          lst6.append(i)
      elif "UPSTOX" in i:
          lst6.append(i)
      elif "ANGELBROKING" in i:
          lst6.append(i)
      elif ("FUND" in i) & ("INSUFFICIENT" not in i) :
          lst6.append(i)  
      elif "TRADE" in i:
          lst6.append(i)

  result6=pd.DataFrame()
  for i in lst6:
      x=df[(df["description"]==i) &(df["credit"]==0)]
      result6=result6.append(x)   

  for i,j in result2["description"].iteritems():
      if "INTEREST" in j:
          result2.loc[i,"category"]="INTEREST"
      elif ("CASHBACK" in j) |("REV" in j):
          result2.loc[i,"category"]="REFUND"
      elif ("IMPS" in j ):
          result2.loc[i,"category"]="IMPS"
      elif ("UPI" in j ) & ("REV" not in j):
          result2.loc[i,"category"]="UNIFIED_PAYMENT"
      elif ("TRTR") in j :
          result2.loc[i,"category"]="IMPS/MOBILE_BANKING/OTHER"
      elif ("NEFT") in j:
          result2.loc[i,"category"]="NEFT"
      elif  ("CTS" in j) & (("OW" in j) |  ("CLG" in j)):
          result2.loc[i,"category"]="CHEQUE"
      elif "TRF" in j:
          result2.loc[i,"category"]="TRANSFER"
      else:
          result2.loc[i,"category"]="OTHER"
  result1.reset_index(inplace=True)
  result1.drop("index",axis=1,inplace=True)
  lstt1=[]
  for i in result1["description"]:
      for j in salary:
          if j in i:
              lstt1.append("salary")
              break
  #print("")
  #print(lsst1)
  result1["category"]=lstt1
  index=result1.index
  index.name = "salary analysis"

  result3["description"]=result3["description"].str.upper()
  for i,j in result3["description"].iteritems():  
      if "INTEREST" in j:
          result2.loc[i,"category"]="INTEREST"
      elif ("CASHBACK" in j) |("REV" in j):
          result3.loc[i,"category"]="REFUND"
      elif ("IMPS" in j ):
          result3.loc[i,"category"]="IMPS"
      elif ("UPI" in j ) & ("REV" not in j):
          result3.loc[i,"category"]="UNIFIED_PAYMENT"
      elif ("TRTR") in j :
          result3.loc[i,"category"]="IMPS/MOBILE_BANKING/OTHER"
      elif ("NEFT") in j:
          result3.loc[i,"category"]="NEFT"
      elif  ("CTS" in j) & (("OW" in j) |  ("CLG" in j)):
          result3.loc[i,"category"]="CHEQUE"
      elif "TRF" in j:
          result3.loc[i,"category"]="TRANSFER"
      elif "CHARGE" in j:
          result3.loc[i,"category"]="CHARGES" 
      elif "CHRG" in j:
          result3.loc[i,"category"]="CHARGES"             
      else:
          result3.loc[i,"category"]="OTHER"
  result_final.append((result1, "Saving Analysis"))
  result_final.append((result2, "Saving Analysis"))
  result_final.append((result3, "Saving Analysis"))
  result_final.append((result4, "Saving Analysis"))
  result_final.append((result6, "Saving Analysis"))
  return result_final
  
