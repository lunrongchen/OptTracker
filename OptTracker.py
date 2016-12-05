import sys
import csv
import time
import requests
from bs4 import BeautifulSoup

def GetCaseStatusByID(_caseNum):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    request_url = "https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum=" + _caseNum
    caseStatus_html = requests.get(request_url, headers=headers)
    soup = BeautifulSoup(caseStatus_html.text, "html.parser")
    statusDiv = soup.find("div", { "class" : "rows text-center" })
    statusDivList = statusDiv.text.split('\n')
    caseStatusValid = len(statusDivList[1])
    if(caseStatusValid == 0):
        return "unValid", "caseId"
    caseStatus = statusDivList[1]
    caseDateList = statusDivList[2].split(',')
    caseDateString = caseDateList[0][3:] + caseDateList[1]
    receivedDate = time.strftime('%m/%d/%Y', time.strptime(caseDateString, "%B %d %Y"))
    return caseStatus, receivedDate

def main():
    file  = open(time.strftime("%m-%d-%Y") + '-Opt_Record.csv', 'wt')
    preId = 1790000000
    endId = 1790052000
    try:
        writer = csv.writer(file)
        writer.writerow( ('caseId', 'receivedDate', 'caseStatus') )
        while (preId < endId):
            caseId = "YSC" + str(preId)
            caseStatus, receivedDate =  GetCaseStatusByID(caseId)
            if(caseStatus != "unValid"):
                writer.writerow( (caseId, receivedDate, caseStatus) )
                result = caseId + "\t" + receivedDate + "\t" + caseStatus
                print result
            preId = preId + 1
    finally:
        file.close()

if __name__ == '__main__':
    main()
