import PyPDF2
import pandas as pd
import camelot
import re
from collections import OrderedDict
import numpy as np


from datetime import datetime



def cleaning(filepath,bankname,passkey,act_type)  : 
    print(filepath)
    '''with open(filepath, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        n=reader.getNumPages()'''
    if act_type=="SAVING":
        rt=2
        flavor = 'lattice'
        if passkey==""  :
            passkey=None

        if(bankname == 'IDBI' or bankname == 'KOTAK' or bankname=='HDFC' or bankname=='YES'):
            flavor = 'stream'

        if flavor=='stream':
            if(bankname=="HDFC"):
                tables = camelot.read_pdf(filepath,flavor='stream',strip_text=False,row_tol=10,table_regions=['23,570,637,83'],columns=['67,271,358,400,482,565'])
            elif(bankname=="KOTAK"):
                tables=camelot.read_pdf(filepath, pages='all',flavor=flavor,password=passkey,row_tol=10,columns=['82,200,360,499,605,687,784'])
            elif(bankname=="IDBI"):
                tables=camelot.read_pdf(filepath,pages='all',password=passkey,flavor='stream',row_tol=10,edge_tol=500,split_text = True)
            elif(bankname=="YES"):
                tables=camelot.read_pdf(filepath, pages='all',flavor='stream',row_tol=10,password=passkey,edge_tol=500,split_text = True)
            else:
                tables=camelot.read_pdf(filepath, pages='all',flavor=flavor, password=passkey, split_text = True,row_tol=rt)

        else:
            if(bankname=="INDUSIND"):
                tables=camelot.read_pdf(filepath, pages='all',flavor=flavor, password=passkey, split_text = True,process_background=True)
            else:
                tables=camelot.read_pdf(filepath, pages='all',flavor=flavor, password=passkey, split_text = True)
        
        dfs = pd.DataFrame()
        
    

        if(bankname == 'IC' or bankname == 'SI'):
            tables = tables[:1]
        
    
        

        


        for table in tables:
            dfs = dfs.append(table.df)
        print('section2')
        print(dfs)
        print(dfs.head(10))

        if (bankname=="HDFC"):
            df=dfs
            df=df.reset_index(drop=True)
            df.columns=df.loc[0]
            df=df.drop(index=0)
            df=df.replace("",np.nan)
            blocks = df[['Date','Chq./Ref.No.']].notna().all(axis=1).cumsum()
            df=df.replace(np.nan,'')
            
            dfs = (df.groupby(blocks, as_index=False)
                .agg({'Date' : 'first',
                    'Narration' : ' '.join,
                    'Chq./Ref.No.': 'first',
                    'Value Dt':'first',
                    'Withdrawal Amt.':'first',
                    'Deposit Amt.':'first',
                    'Closing Balance':'first'}))
            dfs['Date'] = pd.to_datetime(dfs['Date'], errors='coerce')
            dfs =dfs.dropna(subset=['Date'])
            dfs.columns=range(0,len(dfs.columns))

        if (bankname=="KOTAK"):
            df=dfs
            df=df.reset_index(drop=True)
            df=df.drop_duplicates(keep='first')
            df[[0,1]]=df[[0,1]].replace('',np.nan)
            blocks=df[[0,1]].notna().all(axis=1).cumsum()
            dfs=(df.groupby(blocks,as_index=False).agg(
                {1:'first',2:' '.join,3:'first',4:'first',5:'first',6:'first'}))
            dfs[1] = pd.to_datetime(dfs[1], errors='coerce')
            dfs =dfs.dropna(subset=[1])
            dfs.columns=range(0,len(dfs.columns))

        if (bankname=="YES"):
            df=dfs
            df=df.drop(index=0)
            df=df.drop(columns=0)
            df=df.reset_index(drop=True)
            df=df.replace("",np.nan)
            blocks=df[[1]].notna().all(axis=1).cumsum()
            df=df.replace(np.nan,'')
            dfs=(df.groupby(blocks,as_index=False).agg({1:'first',2:' '.join,3:'first',4:'first',5:'first'}))
            dfs.columns = range(dfs.shape[1])
        
        if (bankname=="INDUSIND"):
            df=dfs
            df=df.replace("",np.nan)
            blocks=df[[0]].notna().all(axis=1).cumsum()
            df=df.replace(np.nan,'')
            dfs=(df.groupby(blocks,as_index=False).agg({0:'first',1:' '.join,2:'first',3:'first',4:'first',5:'first'}))
        
        if(bankname=="SBI"):
            dfs=dfs.reset_index(drop=True)

        if(bankname=='CBOI'):
            dfs=dfs.dropna()
            dfs.drop(index=0,inplace=True)
            dfs.reset_index(inplace=True,drop=True)
            
        if(bankname=="INDIAN"):
            dfs.drop(index=0,inplace=True)
            dfs=dfs.reset_index(drop=True)
            dfs[1] = dfs[1].str.replace('\n','')
            dfs.drop(index=0,inplace=True)
            dfs=dfs.reset_index(drop=True)



        dfs.to_csv (r'dat.csv', index = False, header=True)
        print("ddsdjsk")
        BANK_DETAILS = {
            'BOB' : {
                'Date': 1,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'KOTAK': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No':2,
                'Amount': 3,
                'Debit': 4,
                'Credit':4,
                'Balance': 5
            },
            'HDFC': {
                'Date':0,
                'Description':1,
                'Cat': None,
                'Cheque No':2 ,
                'Debit': 4,
                'Credit':5,
                'Balance':6
        },
            'ICICI': {
                'Date': 3,
                'Description': 1,
                'Cat': None,
                'Cheque No': 2,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'SBI': {
                'Date':0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'BOI': {
                'Date': 1,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            
            'UNION': {
                'Date': 0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 1,
                'Debit': 3,
                'Credit': 4,
                'Balance': 5
            },
            'IDBI': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No': 2,
                'Debit': 3,
                'Credit': 4,
                
                'Balance': 5
            },
            'CBOI': {
                'Date': 0,
                'Description': 4,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 5,
                'Credit': 6,
                'Balance': 7
            },
            'CORP': {
                'Date': 0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'PNB': {
                'Date': 0,
                'Description': 5,
                'Cat': None,
                'Cheque No': 1,
                'Debit': 2,
                'Credit': 3,
                'Balance': 4
            },
            'UBOI': {
                'Date': 1,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'AXIS': {
                'Date': 0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 1,
                'Debit': 3,
                'Credit': 4,
                'Balance': 5
            },
        'INDIAN': {
                'Date': 1,
                'Description': 3,
                'Cat': None,
                'Cheque No': 4,
                'Debit': 5,
                'Credit': 6,
                'Balance': 7
            }
            ,
            'INDUSIND': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No': 2,
                'Debit': 3,
                'Credit': 4,
                'Balance': 5
            },
            'YES': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No':5,
                'Debit': 2,
                'Credit': 3,
                'Balance': 4
            },



        }

        if(bankname=="YES"):
            dfs[5]=""

        date_idx = BANK_DETAILS[bankname]['Date']
        date_colname = dfs.columns[date_idx]
        desc_idx = BANK_DETAILS[bankname]['Description']
        desc_colname = dfs.columns[desc_idx]

        cat_idx = BANK_DETAILS[bankname]['Cat']
        if(cat_idx):
            cat_colname = dfs.columns[cat_idx]

        chq_idx = BANK_DETAILS[bankname]['Cheque No']
        if(chq_idx):
            chq_colname = dfs.columns[chq_idx]
        

        deb_idx = BANK_DETAILS[bankname]['Debit']
        deb_colname = dfs.columns[deb_idx]

        cred_idx = BANK_DETAILS[bankname]['Credit']
        cred_colname = dfs.columns[cred_idx]

        bal_idx = BANK_DETAILS[bankname]['Balance']
        bal_colname = dfs.columns[bal_idx]


        if bankname!='CBOI':
            dfs = dfs.dropna(subset=[date_idx])
            dfs[date_idx] = dfs[date_idx].astype(str)
            dfs = dfs[dfs[date_idx] != ""]
            print("***********************************")
            tmp_rows = dfs.shape[0]
            dfs.drop_duplicates(keep = False, inplace = True)
            dfs.reset_index(inplace=True)
            dfs.drop("index",axis=1,inplace=True)

            if(tmp_rows == dfs.shape[0]):
                dfs.drop(dfs.index[:0], inplace=True)
        
        if(bankname =='CORP'):
            dfs.drop(dfs.index[:0], inplace=True)




        dfs[deb_colname] = dfs[deb_colname].astype(str)
        dfs[cred_colname] = dfs[cred_colname].astype(str)
        dfs[bal_colname] = dfs[bal_colname].astype(str)
        
        if(bankname == "KOTAK"):
            cred_colname = 'credit'
            dfs[cred_colname] = ""
            for i,row in dfs.iterrows():
                print(i)
                print(row)
                tmp = re.search("\((.*?)\)", row[deb_colname])


                if(tmp == 'cr'):
                    row[cred_colname] = row[deb_colname]
                    row[deb_colname] = ""

        if(bankname=="SBI"):
            dfs[date_colname] = dfs[date_colname].str.replace('\n','/')
            dfs[date_colname] = dfs[date_colname].str.replace('\s','/')
                    
        dfs[date_colname] = dfs[date_colname].str.replace('\n','')
        dfs[date_colname] = dfs[date_colname].str.replace(r'\b(\w+)(\s+\1)+\b', r'\1')
        dfs[date_colname] = dfs[date_colname].str.replace(r'\([^)]\n*\)', '')
        dfs[date_colname] = dfs[date_colname].str.replace(r'-', '/')
        
        dfs[date_colname] = [' '.join(OrderedDict.fromkeys(x).keys()) for x in dfs[date_colname].str.split()]

        dfs[deb_colname] = dfs[deb_colname].str.replace(r'\D', '')
        dfs[cred_colname] = dfs[cred_colname].str.replace(r'\D', '')
        dfs[bal_colname] = dfs[bal_colname].str.replace(r'\D', '')
        
        

        
        
        if(bankname=="IDBI"):
            print(dfs.tail(20))
            for i in dfs.index:
                if dfs.loc[i,5]=="":
                    dfs.loc[i,[2,3,4,5,]]=dfs.loc[i,[2,3,4,5,]].shift(periods=1,fill_value="")

        dfs[deb_colname]=pd.to_numeric(dfs[deb_colname], errors='coerce')
        dfs[cred_colname]=pd.to_numeric(dfs[cred_colname], errors='coerce')
        dfs[bal_colname]=pd.to_numeric(dfs[bal_colname], errors='coerce')

        dfs[deb_colname]=dfs[deb_colname].fillna(0)
        dfs[cred_colname]=dfs[cred_colname].fillna(0)
        dfs[bal_colname]=dfs[bal_colname].fillna(0)

        dfs[deb_colname]=dfs[deb_colname].apply(lambda x: x/100)
        dfs[cred_colname]=dfs[cred_colname].apply(lambda x: x/100)
        dfs[bal_colname]=dfs[bal_colname].apply(lambda x: x/100)

        
                    
        dfs.to_csv (r'dat1.csv', index = False, header=True)
        #Exception
        
        
        if(bankname=="ICICI"):
            dfs=dfs.drop(index=[0,1])
            dfs.reset_index(drop=True)
        if(bankname == "SBI"):

            dfs.drop(dfs.index[:1], inplace=True)
            dfs[date_colname]=dfs[date_colname]
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%y-%m-%d'))
            #dfs[date_colname]=dfs[date_colname].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S') if type(x)==str else np.NaN)
            
            print("chekx=========================")
        print(dfs[date_colname])

        if(bankname == "HDFC"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%Y/%m/%d'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)

        if(bankname == "ICICI"):
            #dfs.drop(dfs.index[:3], inplace=True)
            #dfs.drop(dfs.index[-3:], inplace=True)
            dfs[date_colname] = pd.to_datetime(dfs[date_colname],format=('%d/%m/%Y'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
            
        if(bankname == "BOB"):
            dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
        
        if(bankname == "CORP"):
            #dfs.drop(dfs.index[:1], inplace=True)
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)
        if(bankname == "IDBI"):
            dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "YES"):
            dfs=dfs[1:]
            dfs[date_colname] = pd.to_datetime(dfs[date_colname],format=('%d/%m/%Y'),errors='coerce')
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
            dfs.dropna(inplace=True)
            dfs=dfs.sort_values(by=[date_colname])
            dfs.reset_index(drop=True,inplace=True)
        #if(bankname == "HDFC"):
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            #dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
        #if(bankname == "KOTAK"):
            #dfs.drop(dfs.index[:1], inplace=True)
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            #dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "BOI"):
            #dfs.drop(dfs.index[:1], inplace=True)
            dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "INDIAN"):
            #dfs.drop(dfs.index[:1], inplace=True)
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'))
        
        if(bankname == "AXIS"):
            dfs.drop(dfs.index[:1], inplace=True)
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "INDUSIND"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%b/%Y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)

        if(bankname == "CBOI"):
            #dfs.drop(dfs.index[:1], inplace=True)
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
            dfs=dfs.drop_duplicates(subset=[date_idx,desc_idx,chq_idx,deb_idx,cred_idx,bal_idx])

        if(bankname == "SBI"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%b/%Y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)

    elif(act_type=="CURRENT"):
        rt=2
        flavor = 'lattice'
        if passkey==""  :
            passkey=None

        if(bankname == 'IDBI' or bankname == 'KOTAK' or bankname== 'INDUSIND' or bankname=='YES'):
            flavor = 'stream'

        if flavor=='stream':
            if(bankname=="KOTAK"):
                tables=camelot.read_pdf(filepath, pages='all',flavor=flavor,password=passkey,row_tol=10,columns=['82,200,360,499,605,687,784'])
            elif(bankname=="INDUSIND"):
                tables=camelot.read_pdf(filepath, pages='all',flavor=flavor, password=passkey, split_text = True,row_tol=25,edge_tol=500)
            elif(bankname=="IDBI"):
                tables=camelot.read_pdf(filepath,pages='all',password=passkey,flavor='stream',row_tol=10,edge_tol=500,split_text = True)
            elif(bankname=="YES"):
                tables=camelot.read_pdf(filepath, pages='all',flavor='stream',row_tol=10,password=passkey,edge_tol=500,split_text = True)
            else:
                tables=camelot.read_pdf(filepath, pages='all',flavor=flavor, password=passkey, split_text = True,row_tol=rt)

        else:
            tables=camelot.read_pdf(filepath, pages='all',flavor=flavor, password=passkey, split_text = True)
        
        dfs = pd.DataFrame()
        
    

        if(bankname == 'IC' or bankname == 'SI'):
            tables = tables[:1]
        
    
        

        


        for table in tables:
            dfs = dfs.append(table.df)
        print('section2')
        print(dfs)
        print(dfs.head(10))

        '''if(bankname=="AXIS"):
            for i,row in dfs.iterrows():
                if(row[5] == "DR"):
                    row[deb_colname] = row[cred_colname]
                    row[cred_colname] = ""
                else:
                    row[deb_colname] = ""'''

        if (bankname=="KOTAK"):
            df=dfs
            df=df.reset_index(drop=True)
            df=df.drop_duplicates(keep='first')
            df[[0,1]]=df[[0,1]].replace('',np.nan)
            blocks=df[[0,1]].notna().all(axis=1).cumsum()
            dfs=(df.groupby(blocks,as_index=False).agg(
                {1:'first',2:' '.join,3:'first',4:'first',5:'first',6:'first'}))
            dfs[1] = pd.to_datetime(dfs[1], errors='coerce')
            dfs =dfs.dropna(subset=[1])
            dfs.columns=range(0,len(dfs.columns))

        if (bankname=="YES"):
            df=dfs
            df=df.drop(index=0)
            df=df.drop(columns=0)
            df=df.reset_index(drop=True)
            df=df.replace("",np.nan)
            blocks=df[[1]].notna().all(axis=1).cumsum()
            df=df.replace(np.nan,'')
            dfs=(df.groupby(blocks,as_index=False).agg({1:'first',2:' '.join,3:'first',4:'first',5:'first'}))
            dfs.columns = range(dfs.shape[1])
        
        if(bankname=="SBI"):
            dfs=dfs.reset_index(drop=True)

        if(bankname=='CBOI'):
            dfs=dfs.dropna()
            dfs.drop(index=0,inplace=True)
            dfs.reset_index(inplace=True,drop=True)
            
        if(bankname=="INDIAN"):
            dfs.drop(index=0,inplace=True)
            dfs=dfs.reset_index(drop=True)
            dfs[1] = dfs[1].str.replace('\n','')
            dfs.drop(index=0,inplace=True)
            dfs=dfs.reset_index(drop=True)



        dfs.to_csv (r'dat.csv', index = False, header=True)
        print("ddsdjsk")
        BANK_DETAILS = {
            'BOB' : {
                'Date': 1,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'KOTAK': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No':2,
                'Amount': 3,
                'Debit': 4,
                'Credit':4,
                'Balance': 5
            },
            'HDFC': {
                'Date':0,
                'Description':1,
                'Cat': None,
                'Cheque No':2 ,
                'Debit': 4,
                'Credit':5,
                'Balance':6
        },
            'ICICI': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No': 2,
                'Debit': 3,
                'Credit': 4,
                'Balance': 7
            },
            'SBI': {
                'Date':0,
                'Description': 1,
                'Cat': None,
                'Cheque No': 2,
                'Debit': 3,
                'Credit': 4,
                'Balance': 7
            },
            'BOI': {
                'Date': 1,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            
            'UNION': {
                'Date': 0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 1,
                'Debit': 3,
                'Credit': 4,
                'Balance': 5
            },
            'IDBI': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No': 2,
                'Debit': 3,
                'Credit': 4,
                
                'Balance': 5
            },
            'CBOI': {
                'Date': 0,
                'Description': 4,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 5,
                'Credit': 6,
                'Balance': 7
            },
            'CORP': {
                'Date': 0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'PNB': {
                'Date': 0,
                'Description': 5,
                'Cat': None,
                'Cheque No': 1,
                'Debit': 2,
                'Credit': 3,
                'Balance': 4
            },
            'UBOI': {
                'Date': 1,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 4,
                'Credit': 5,
                'Balance': 6
            },
            'AXIS': {
                'Date': 0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 3,
                'Debit': 3,
                'Credit': 4,
                'Balance': 5
            },
        'INDIAN': {
                'Date': 1,
                'Description': 3,
                'Cat': None,
                'Cheque No': 4,
                'Debit': 5,
                'Credit': 6,
                'Balance': 7
            }
            ,
            'INDUSIND': {
                'Date': 0,
                'Description': 2,
                'Cat': None,
                'Cheque No': 1,
                'Debit': 3,
                'Credit': 4,
                'Balance': 5
            },
            'YES': {
                'Date': 0,
                'Description': 1,
                'Cat': None,
                'Cheque No':None,
                'Debit': 2,
                'Credit': 3,
                'Balance': 4
            },



        }

        if(bankname=="YES"):
            dfs[5]=""

        date_idx = BANK_DETAILS[bankname]['Date']
        date_colname = dfs.columns[date_idx]
        desc_idx = BANK_DETAILS[bankname]['Description']
        desc_colname = dfs.columns[desc_idx]

        cat_idx = BANK_DETAILS[bankname]['Cat']
        if(cat_idx):
            cat_colname = dfs.columns[cat_idx]

        chq_idx = BANK_DETAILS[bankname]['Cheque No']
        if(chq_idx):
            chq_colname = dfs.columns[chq_idx]
        

        deb_idx = BANK_DETAILS[bankname]['Debit']
        deb_colname = dfs.columns[deb_idx]

        cred_idx = BANK_DETAILS[bankname]['Credit']
        cred_colname = dfs.columns[cred_idx]

        bal_idx = BANK_DETAILS[bankname]['Balance']
        bal_colname = dfs.columns[bal_idx]


        if bankname!='CBOI':
            dfs = dfs.dropna(subset=[date_idx])
            dfs[date_idx] = dfs[date_idx].astype(str)
            dfs = dfs[dfs[date_idx] != ""]
            print("***********************************")
            tmp_rows = dfs.shape[0]
            dfs.drop_duplicates(keep = False, inplace = True)
            dfs.reset_index(inplace=True)
            dfs.drop("index",axis=1,inplace=True)

            if(tmp_rows == dfs.shape[0]):
                dfs.drop(dfs.index[:0], inplace=True)
        
        if(bankname =='CORP'):
            dfs.drop(dfs.index[:0], inplace=True)




        dfs[deb_colname] = dfs[deb_colname].astype(str)
        dfs[cred_colname] = dfs[cred_colname].astype(str)
        dfs[bal_colname] = dfs[bal_colname].astype(str)
    

        
        
        if(bankname == "KOTAK"):
            cred_colname = 'credit'
            dfs[cred_colname] = ""
            for i,row in dfs.iterrows():
                print(i)
                print(row)
                tmp = re.search("\((.*?)\)", row[deb_colname])


                if(tmp == 'cr'):
                    row[cred_colname] = row[deb_colname]
                    row[deb_colname] = ""

        if(bankname=="SBI"):
            dfs[date_colname] = dfs[date_colname].str.replace('\n','/')
            dfs[date_colname] = dfs[date_colname].str.replace('\s','/')

                    
        dfs[date_colname] = dfs[date_colname].str.replace('\n','')
        dfs[date_colname] = dfs[date_colname].str.replace(r'\b(\w+)(\s+\1)+\b', r'\1')
        dfs[date_colname] = dfs[date_colname].str.replace(r'\([^)]\n*\)', '')
        dfs[date_colname] = dfs[date_colname].str.replace(r'-', '/')
        
        dfs[date_colname] = [' '.join(OrderedDict.fromkeys(x).keys()) for x in dfs[date_colname].str.split()]

        dfs[deb_colname] = dfs[deb_colname].str.replace(r'\D', '')
        dfs[cred_colname] = dfs[cred_colname].str.replace(r'\D', '')
        dfs[bal_colname] = dfs[bal_colname].str.replace(r'\D', '')


        

        
        
        if(bankname=="IDBI"):
            print(dfs.tail(20))
            for i in dfs.index:
                if dfs.loc[i,5]=="":
                    dfs.loc[i,[2,3,4,5,]]=dfs.loc[i,[2,3,4,5,]].shift(periods=1,fill_value="")

        dfs[deb_colname]=pd.to_numeric(dfs[deb_colname], errors='coerce')
        dfs[cred_colname]=pd.to_numeric(dfs[cred_colname], errors='coerce')
        dfs[bal_colname]=pd.to_numeric(dfs[bal_colname], errors='coerce')

        dfs[deb_colname]=dfs[deb_colname].fillna(0)
        dfs[cred_colname]=dfs[cred_colname].fillna(0)
        dfs[bal_colname]=dfs[bal_colname].fillna(0)

        dfs[deb_colname]=dfs[deb_colname].apply(lambda x: x/100)
        dfs[cred_colname]=dfs[cred_colname].apply(lambda x: x/100)
        dfs[bal_colname]=dfs[bal_colname].apply(lambda x: x/100)

        
                    
        dfs.to_csv (r'dat1.csv', index = False, header=True)
        #Exception
        if(bankname == "INDUSIND"):
            dfs[chq_colname]=""
            
            print("chekx=========================")
        print(dfs[date_colname])

        if(bankname == "HDFC"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)
            
        if(bankname == "ICICI"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)
        if(bankname == "HDFC"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)
        if(bankname == "BOB"):
            dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
        
        if(bankname == "CORP"):
            #dfs.drop(dfs.index[:1], inplace=True)
            dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
        if(bankname == "IDBI"):
            dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "YES"):
            dfs=dfs[1:]
            dfs[date_colname] = pd.to_datetime(dfs[date_colname],format=('%d/%m/%Y'),errors='coerce')
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
            dfs.dropna(inplace=True)
            dfs=dfs.sort_values(by=[date_colname])
            dfs.reset_index(drop=True,inplace=True)
        #if(bankname == "HDFC"):
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            #dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
        #if(bankname == "KOTAK"):
            #dfs.drop(dfs.index[:1], inplace=True)
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            #dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "BOI"):
            #dfs.drop(dfs.index[:1], inplace=True)
            dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "INDIAN"):
            #dfs.drop(dfs.index[:1], inplace=True)
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'))
        
        if(bankname == "AXIS"):
            dfs.drop(dfs.index[:1], inplace=True)
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')

        if(bankname == "INDUSIND"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d %b %Y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs=dfs.sort_values(by=[date_colname])
            dfs.reset_index(drop=True,inplace=True)

        if(bankname == "CBOI"):
            #dfs.drop(dfs.index[:1], inplace=True)
            #dfs[date_colname] = dfs[date_colname].apply(lambda x: pd.Timestamp(x).strftime('%Y-%d-%m'))
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%m/%Y'))
            dfs[date_colname]=pd.to_datetime(dfs[date_colname],dayfirst=True,errors='coerce')
            dfs=dfs.drop_duplicates(subset=[date_idx,desc_idx,chq_idx,deb_idx,cred_idx,bal_idx])

        if(bankname == "SBI"):
            dfs[date_idx]=pd.to_datetime(dfs[date_idx],format=('%d/%b/%Y'),dayfirst=True,errors='coerce')
            dfs=dfs.dropna()
            dfs.reset_index(drop=True,inplace=True)



    else:
        print("account type is saving and current")
    combined = pd.DataFrame()
    combined['date'] = dfs[date_colname]
    combined['description'] = dfs[desc_colname]
    if(cat_idx):
        combined['cat'] = dfs[cat_colname]
    else:
        combined['cat'] = "NA"
    if(chq_idx):
        combined['chequeNumber'] = dfs[chq_colname]
    else:
        combined['chequeNumber']="NA"
    combined['debit'] = dfs[deb_colname]
    combined['credit'] = dfs[cred_colname]
    combined['balance'] = dfs[bal_colname]
    combined.reset_index(inplace=True)
    combined.drop("index",axis=1,inplace=True)
    combined['description'] = combined['description'].astype(str)
    #combined["date"]=pd.to_datetime(combined["date"],dayfirst=False,errors='coerce')
    #combined["date"]=combined["date"].dt.strftime('%m/%d/%Y')
    #df['DOB1'] = df['DOB'].dt.strftime('%d/%m/%Y')
    print('section3')
    print(combined.head(10))
    combined.to_csv (r'dat3.csv', index = False, header=True)
    return combined
