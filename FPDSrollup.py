# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:04:03 2019

@author: admin
"""

#import os
#
#my_dir=r'H:\_MyComputer\Documents\Git Repos\FPDS'
#os.chdir(my_dir)



import pandas as pd
pd.set_option('mode.chained_assignment', None)
print("Packages read.")
import timeit


import requests
from xml.etree import ElementTree


def wrap_it_up(agency):
    start=timeit.timeit()
    ID = str(agency)
    def iterateOverEntries(entries):
        list_of_dicts=[]

        for entryElement in entries:
            entry = getEntry(entryElement)
            list_of_dicts.append(entry)
            return(list_of_dicts)
    
    def getText(elm):
        return ("".join(elm.itertext())) if elm is not None else ""    
        
    def getEntry(entryElm):
        entry = {}
        titleElement = entryElm.find('{http://www.w3.org/2005/Atom}title')
        entry['title'] = getText(titleElement)
    
        effectiveDateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}effectiveDate")
        entry['effectiveDate'] = getText(effectiveDateElm)
  
        awardContractID = entryElm.find(".//{https://www.fpds.gov/FPDS}awardContractID")
        entry['awardContractID'] = getText(awardContractID)
    
        contractingOfficeAgencyID = entryElm.find(".//{https://www.fpds.gov/FPDS}contractingOfficeAgencyID")
        entry['contractingOfficeAgencyID'] = getText(contractingOfficeAgencyID)
   
        fundingRequestingAgencyIDElm=entryElm.find(".//{https://www.fpds.gov/FPDS}fundingRequestingAgencyID")
        entry['fundingRequestingAgencyID'] = getText(fundingRequestingAgencyIDElm)
    
        signeddateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}signedDate")
        entry['signedDate'] = getText(signeddateElm)
    
        contractingOfficeIDElm = entryElm.find(".//{https://www.fpds.gov/FPDS}contractingOfficeID")
        entry['contractingOfficeID'] = getText(contractingOfficeIDElm)
    
        fundingRequestingOfficeIDElm = entryElm.find(".//{https://www.fpds.gov/FPDS}fundingRequestingOfficeID")
        entry['fundingRequestingOfficeID '] = getText(fundingRequestingOfficeIDElm)

        totalObligatedAmountElm=entryElm.find(".//{https://www.fpds.gov/FPDS}totalObligatedAmount")
        entry['totalObligatedAmount'] = getText(totalObligatedAmountElm)
        totalBaseAndExercisedOptionsValueElm=entryElm.find(".//{https://www.fpds.gov/FPDS}totalBaseAndExercisedOptionsValue")
        entry['totalBaseAndExercisedOptionsValue'] = getText(totalBaseAndExercisedOptionsValueElm)
        totalBaseAndAllOptionsValueElm=entryElm.find(".//{https://www.fpds.gov/FPDS}totalBaseAndAllOptionsValue")
        entry['totalBaseAndAllOptionsValue'] = getText(totalBaseAndAllOptionsValueElm)
    
        ObligatedAmountElm=entryElm.find(".//{https://www.fpds.gov/FPDS}obligatedAmount")
        entry['ObligatedAmount'] = getText(ObligatedAmountElm)
        BaseAndExercisedOptionsValueElm=entryElm.find(".//{https://www.fpds.gov/FPDS}baseAndExercisedOptionsValue")
        entry['BaseAndExercisedOptionsValue'] = getText(BaseAndExercisedOptionsValueElm)
        BaseAndAllOptionsValueElm=entryElm.find(".//{https://www.fpds.gov/FPDS}baseAndAllOptionsValue")
        entry['BaseAndAllOptionsValue'] = getText(BaseAndAllOptionsValueElm)

        entry['awardContractIDName'] =  try_except_get(awardContractID)
        entry['fundingAgencyName'] = try_except_get(fundingRequestingAgencyIDElm)
        entry['contractingAgencyName'] = try_except_get(contractingOfficeAgencyID)
        entry['fundingOfficeName'] = try_except_get(fundingRequestingOfficeIDElm)
        entry['contractingOfficeName'] = try_except_get(contractingOfficeIDElm)

        return entry

    def try_except_get(attribute, field='name'):
        try:
            return(attribute.attrib[field])
        except:
            return""
     
        def getText(elm):
            return ("".join(elm.itertext())) if elm is not None else ""

    def keep_going_till_end(ID):
            status="ongoing"
            number=0
            attempts=0

            df4=pd.DataFrame()
            while status=="ongoing":
                    while attempts<5:
                        try:
                            print("attempts="+str(attempts))
                            df_temp=take_number_get_df(number,ID)
                            print(number)
                
                
                            if len(df_temp)==0:
                                status=="done"
                                return(df4)
                            else:
                                df4=df4.append(df_temp, ignore_index=True)
                                number=number+10
                        except:
                            attempts=attempts+1
    
    
    def take_number_get_df(number,ID):

        link=f"https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=CONTRACTING_AGENCY_ID:{ID}+SIGNED_DATE:[2017/10/02,2018/09/30]&start={number}"
        print(link)
    
        response = requests.get(link)

        root = ElementTree.fromstring(response.content)

        entries = root.findall('{http://www.w3.org/2005/Atom}entry')   
        dicts=iterateOverEntries(entries)
        df=pd.DataFrame(dicts)
        return(df)                        
                        
    df=keep_going_till_end(ID)
    end = timeit.timeit()
    timelapse = end-start
    print(timelapse)
    return(df,timelapse)





