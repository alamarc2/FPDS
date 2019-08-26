#!/usr/bin/env python
import pandas as pd
pd.set_option('mode.chained_assignment', None)
print("Packages read.")


import pandas as pd
import requests
from xml.etree import ElementTree


#link="https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=PIID:HC101317FH400&start=0"
#link="https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=PRINCIPAL_NAICS_CODE:517210&start=0"
def keep_going_till_end(ID):
    status="ongoing"
    number=0
    attempts=0
    ID = ID
    #agency ="DEFENSE SECURITY COOPERATION AGENCY"
    #ID = ":%229700%22"
    #Dates =":[2018/04/19,2019/04/19]"
    df4=pd.DataFrame()
    while status=="ongoing":
            while attempts<1000:
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


    return(df4)
    
def take_number_get_df(number,ID):

    
    link=f"https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=CONTRACTING_AGENCY_ID:{ID}+SIGNED_DATE:[2017/10/02,2018/09/30]&start={number}"
    print(link)
    
    response = requests.get(link)

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
    
    #awardContractElm = entryElm.find(".//{https://www.fpds.gov/FPDS}awardContractID")
    #agencyIDElm = awardContractElm.find(".//{https://www.fpds.gov/FPDS}agencyID")
    #entry['agencyID'] = getText(agencyIDElm)
    
    #referencedIDVIDElm = entryElm.find(".//{https://www.fpds.gov/FPDS}referencedIDVID")
    #referencedIDVID = referencedIDVIDElm.find(".//{https://www.fpds.gov/FPDS}agencyID")
    #entry['ReferencedagencyID'] = getText(referencedIDVID)
  
    awardContractID = entryElm.find(".//{https://www.fpds.gov/FPDS}awardContractID")
    entry['awardContractID'] = getText(awardContractID)
    
    contractingOfficeAgencyID = entryElm.find(".//{https://www.fpds.gov/FPDS}contractingOfficeAgencyID")
    entry['contractingOfficeAgencyID'] = getText(contractingOfficeAgencyID)
   
    fundingRequestingAgencyIDElm=entryElm.find(".//{https://www.fpds.gov/FPDS}fundingRequestingAgencyID")
    entry['fundingRequestingAgencyID'] = getText(fundingRequestingAgencyIDElm)
    
    signeddateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}signedDate")
    entry['signedDate'] = getText(signeddateElm)
    
    accountcode = entryElm.find(".//{https://www.fpds.gov/FPDS}mainAccountCode")
    entry['TreasuryAccountCode'] = getText(accountcode)
#    lastModifiedDateElm=entryElm.find(".//{https://www.fpds.gov/FPDS}lastModifiedDate")
#    entry['lastModifiedDate'] = getText(lastModifiedDateElm)
#    
#    currentCompletionDateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}currentCompletionDate")
#    entry['currentCompletionDate'] = getText(currentCompletionDateElm)
#    
#    ultimateCompletionDateElm = entryElm.find(".//{https://www.fpds.gov/FPDS}ultimateCompletionDate")
#    entry['ultimateCompletionDate'] = getText(ultimateCompletionDateElm)
#
#    vendorNameElm = entryElm.find(".//{https://www.fpds.gov/FPDS}vendorName")
#    entry['vendorName']=getText(vendorNameElm)
#    
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

    #entry['agencyIDName'] = try_except_get(agencyIDElm)
    entry['awardContractIDName'] =  try_except_get(awardContractID)
    entry['fundingAgencyName'] = try_except_get(fundingRequestingAgencyIDElm)
    entry['contractingAgencyName'] = try_except_get(contractingOfficeAgencyID)
    #entry['contractingOfficeCountry'] = try_except_get(contractingOfficeIDElm, "country")
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

agencies = ['1700','2100','2100','5700','9700','9748','9758','97SD','9761','9763','97AB','97AD','97AE','97AK','97AR','97AS','97AT','97AV','97AZ','97BJ','97BZ','97CG','97DH','97DL','97EX','97F1','97F2','97F5','97JC','97ZS']


def wrap_it_up():
    for i in agencies:
        df=keep_going_till_end(i)
        df.to_excel(str(i)+'.xlsx')
        
wrap_it_up()        


