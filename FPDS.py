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


import pandas as pd
import requests
from xml.etree import ElementTree


#link="https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=PIID:HC101317FH400&start=0"
#link="https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=PRINCIPAL_NAICS_CODE:517210&start=0"
def keep_going_till_end():
    status="ongoing"
    number=0
    ID = ":%229700%22"
    Dates =":[2018/04/19,2019/04/19]"
    df=pd.DataFrame()
    while status=="ongoing":
        try:
            df_temp=take_number_get_df(number,ID,Dates)
            print(number,ID,Dates)
            if len(df_temp)==0:
                status="done"
            else:
                df=df.append(df_temp, ignore_index=True)
                number=number+10
        except:
            status="done"
    return(df)
    
def take_number_get_df(number,ID,Dates):
    #link=f"https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=REF_IDV_PIID:%22N0024418D0001%22&start={str(number)}"
    #link=f"https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=REF_IDV_PIID:%22N0024418D0001%22&CONTRACTING_AGENCY_NAME%3ADEPT+OF+THE+AIR+FORCE&start={str(number)}"
    #link=f'https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=CONTRACTING_AGENCY_ID:%229700%22&start={str(number)}'
    link=f'https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q+CONTRACTING_AGENCY_ID={str(ID)}&q=REF_IDV_PIID:%22N0024418D0001%22&start={str(number)}&SIGNED_DATE={str(Dates)}'
    
    print(link)
    response = requests.get(link)


    #resp_data = xmltodict.parse(response.text, process_namespaces=True, namespaces={'http://www.fpds.gov/FPDS': None, 'http://www.w3.org/2005/Atom': None})
    #r = records[0]['content']['award']

    root = ElementTree.fromstring(response.content)
    #print(response.content)
    #print(root)
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')   
    dicts=iterateOverEntries(entries)
    df=pd.DataFrame(dicts)
    return(df)


def iterateOverEntries(entries):
    list_of_dicts=[]
    #print(len(entries))
    for entryElement in entries:
        entry = getEntry(entryElement)
        list_of_dicts.append(entry)
    return(list_of_dicts)
         
        
def getEntry(entryElm):
    entry = {}
    titleElement = entryElm.find('{http://www.w3.org/2005/Atom}title')
    entry['title'] = getText(titleElement)
    
    effectiveDateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}effectiveDate")
    entry['effectiveDate'] = getText(effectiveDateElm)
    
    awardContractElm = entryElm.find(".//{https://www.fpds.gov/FPDS}awardContractID")
    agencyIDElm = awardContractElm.find(".//{https://www.fpds.gov/FPDS}agencyID")
    entry['agencyID'] = getText(agencyIDElm)
    
    referencedIDVIDElm = entryElm.find(".//{https://www.fpds.gov/FPDS}referencedIDVID")
    referencedIDVID = referencedIDVIDElm.find(".//{https://www.fpds.gov/FPDS}agencyID")
    entry['ReferencedagencyID'] = getText(referencedIDVID)
  
    awardContractID = entryElm.find(".//{https://www.fpds.gov/FPDS}awardContractID")
    entry['awardContractID'] = getText(awardContractID)
    
    contractingOfficeAgencyID = entryElm.find(".//{https://www.fpds.gov/FPDS}contractingOfficeAgencyID")
    entry['contractingOfficeAgencyID'] = getText(contractingOfficeAgencyID)
   
    fundingRequestingAgencyIDElm=entryElm.find(".//{https://www.fpds.gov/FPDS}fundingRequestingAgencyID")
    entry['fundingRequestingAgencyID'] = getText(fundingRequestingAgencyIDElm)
    
    signeddateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}signedDate")
    entry['signedDate'] = getText(signeddateElm)
    
    lastModifiedDateElm=entryElm.find(".//{https://www.fpds.gov/FPDS}lastModifiedDate")
    entry['lastModifiedDate'] = getText(lastModifiedDateElm)
    
    currentCompletionDateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}currentCompletionDate")
    entry['currentCompletionDate'] = getText(currentCompletionDateElm)
    
    ultimateCompletionDateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}ultimateCompletionDate")
    entry['ultimateCompletionDate'] = getText(ultimateCompletionDateElm)

    vendorNameElm = entryElm.find(".//{https://www.fpds.gov/FPDS}vendorName")
    entry['vendorName']=getText(vendorNameElm)
    
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

    entry['agencyIDName'] = try_except_get(agencyIDElm)
    entry['awardContractIDName'] =  try_except_get(awardContractID)
    entry['fundingAgencyName'] = try_except_get(fundingRequestingAgencyIDElm)
    entry['contractingAgencyName'] = try_except_get(contractingOfficeAgencyID)
    entry['contractingOfficeCountry'] = try_except_get(contractingOfficeIDElm, "country")
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

def wrap_it_up():
    df=keep_going_till_end()
    return(df)


df=wrap_it_up()


