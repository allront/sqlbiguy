"""
Created on 22.02.2018
@author: artem.glazkov @allront
"""

import pandas as pd
import pyodbc
import datetime
from time import sleep

conn_str =( r'Driver={SQL Server};'
            r'Server=YourServer;'
            r'Database=YourDB;'
            r'Trusted_Connection=yes;')

excelPlace=r"\\YourFolder\YourXLSname.xlsx"
listNames=pd.ExcelFile(excelPlace).sheet_names ## Get sheet Names
colsList=[0,1,2,3,4,5,6,7,8] + list (range(10, 10+12)) ## str + timeFrame

def UpdateXLSquota(listNames):
    for s in listNames:        
        excelDF = pd.DataFrame()
        excelDF = pd.read_excel (io=excelPlace, sheetname=s, usecols=colsList)       
        for i in range(9, 9 + 12):  
            excelDF.columns.values[i] = '2018'+('0'+str(i-8))[-2:]+'01'        
        excelDF=excelDF.fillna(0)
        excelDF=excelDF.melt(id_vars=excelDF.columns[:-12])
        excelDF.rename(columns={'variable': 'RepDate','value': 'ValueEUR'}, inplace=True)  
        excelDF['excelList']=s
        excelDF=excelDF.values.tolist()
        
        cnxn = pyodbc.connect(conn_str);cursorD = cnxn.cursor();
        cursorD.execute("DELETE FROM [base].[dbo].[quota] WHERE [extDate]= CAST (GETDATE() as date)") 
        print (cursorD.rowcount, 'rows deleted');
        cnxn.commit(); cnxn.close();
        
        cnxn = pyodbc.connect(conn_str);cursorIn = cnxn.cursor();
        cursorIn.executemany(""" INSERT INTO [base].[dbo].[quota]  
            ( [str1]
              ,[str2]
              ,[str3]
              ,[str4]
              ,[str5]
              ,[str6]
              ,[str7]
              ,[str8]
              ,[str9]
              ,[RepDate]
              ,[ValueEUR]
              ,[excelList]
              ,[extDate])
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,CAST(GETDATE() as date))"""
            ,excelDF)
        cnxn.commit(); cnxn.close();
        
        cnxn = pyodbc.connect(conn_str);cursorD = cnxn.cursor();
        cursorD.execute(""" UPDATE [base].[dbo].[quota] 
                        SET [str9] = NULL 
                        WHERE [extDate]= CAST (GETDATE() as date) AND [str9]=0 """) 
        print (cursorD.rowcount, 'rows updated');
        cnxn.commit(); cnxn.close();       
    return 

def startquestion():
    print ('Do you want to update all quota lists or single one?')
    print ('Please choose')
    print ('0   : to update all lists in excel')
    print ('4   : to update update single April list e.g.')  
    updtype = input ("Type 0 or month number in MM fromat:    ")
    if  str(updtype) == '0' :
        print ('updating all lists')
        for Xlist in listNames[:]:
            if not(Xlist[-5:] =='.2018'and Xlist[:3] =='01.'): 
                listNames.remove(Xlist)
        return listNames
    elif int(updtype) >=1 and int(updtype) <=12 :
        print ('updating ',('0'+str(updtype))[-2:],' month')
        return [('01.'+('0'+str(updtype))[-2:]+'.2018')]
    else :
        print ("oops, enter value in correct format")
        startquestion()

def main():    
    print ('job started at')
    print (datetime.datetime.now().strftime('%H:%M:%S'))
    UpdateXLSquota(listNames=startquestion())
    print ('Job done at')
    print (datetime.datetime.now().strftime('%H:%M:%S'))
    sleep(30)

if __name__ == '__main__':
    main()
