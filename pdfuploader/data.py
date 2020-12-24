def analysis_sheets(dfl):
  df=dfl.copy(deep=True)
  df["date"]=pd.to_datetime(df["date"],dayfirst=True,errors='coerce')
  df['month']=df['date'].dt.month
  df['year'] = pd.DatetimeIndex(df['date']).year
  df['month']=df['month'].fillna(0)
  df['month'] = df['month'].astype(int)
  #df['month name'] = pd.to_datetime(df['month'], format='%m').dt.month_name().str.slice(stop=3)
  df['month name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
  lm=[]
  for i in range(0,(df.shape)[0]):
    x1=df["month name"][i]
    x2=df["year"][i]
    lm.append(f"{x1}{x2}")
  df['month year']=lm
  
  lm = list(dict.fromkeys(lm))
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
  for i in lm:
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    f1=newdf['balance'].iloc[-1] + newdf['debit'].iloc[-1] - newdf['credit'].iloc[-1]
    f2=(newdf["balance"][0]) + (newdf["debit"][0]) - (newdf["credit"][0]) 
    first.append(f2)
    second.append(f1)
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
  dfx["Opening"]=first 
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
    avgb.append((sum(b1)/len(b1))) 
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
  for i in lm:
    D1B1=[]
    D14B1=[]
    D30B1=[]
    newdf=df[df['month year'] == i]
    newdf.reset_index(inplace=True)
    ndg=newdf.shape
    for i in range(0,ndg[0]):
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
    for i in range(0,nnd):
      s=new_deb_df["description"][i]
      t=s.lower()
      if (t.find("self") != -1 or t.find("keshav") != -1):
        Intern_deb.append(i)  
      if (t.find("cash") != -1):
        cash_deb.append(i)
      if (t.find("self") != -1):
        self_deb.append(i)    
      if (t.find("charges") != -1 or t.find("charge") != -1):
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
    for i in range(0,sz):
      s=new_cred_df["description"][i]
      t=s.lower()
      if (t.find("self") != -1 or t.find("keshav") != -1):
        Intern_cred.append(i)  
      if (t.find("cash") != -1):
        cash_cred.append(i) 
      if (t.find("self") != -1):
        self_cred.append(i)    
      if (t.find("neft fm") != -1):
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
  dfx=dfx.T
  return dfx,"Analysis"

