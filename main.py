import requests as requests
from bs4 import BeautifulSoup
from pathlib import Path
from sec_api import ExtractorApi
import input


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
dict = {'1': 'Business','1A': 'Risk Factors','1B':'Unresolved Staff Comments','2':'Properties','3':'Legal Proceedings',
        '4':'Mine Safety Disclosures','5':"Market for Registrant's Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities",
        '6':'Reserved','7':'Management’s Discussion and Analysis of Financial Condition and Results of Operations','7A':'Quantitative and Qualitative Disclosures About Market Risk',
        '8':'Financial Statements and Supplementary Data','9':'Changes in and Disagreements with Accountants on Accounting and Financial Disclosure','9A':'Controls and Procedures ',
        '9B':'Other Information','9C':'Disclosure Regarding Foreign Jurisdictions that Prevent Inspections','10':'Directors, Executive Officers and Corporate Governance',
        '11':'Executive Compensation','12':'Security Ownership of Certain Beneficial Owners and Management and Related Shareholder Matters',
        '13':'Certain Relationships and Related Transactions, and Director Independence','14':'Principal Accounting Fees and Services','15':'Exhibits, Financial Statement Schedules',
        '16':'Form 10-K Summary'}

item_list =['1','1A','1B','2','3','4','5','6','7','7A','8','9','9A','9B','10','11','12','13','14','15','16']

def extractApi(url,item):
    response = requests.get(url,headers=headers)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    text = text.replace('\t', ' ')
    text = text.replace('\u00A0',' ')

    risk_factor_text = ''
    start = False

    substring1_list=[]
    substring2_list=[]
    item_start_low = 'Item '+item+"."
    item_start_up = item_start_low.upper()
    substring1_list.append(item_start_low+dict[item])
    substring2_list.append(item_start_up+dict[item].upper())
    for space in range(1,6):
        sub_1 = item_start_low
        sub_2 = item_start_up
        for j in range(0, space):
            sub_1 += ' '
            sub_2 += ' '
        sub_1 += dict[item]
        sub_2 += dict[item].upper()
        substring1_list.append(sub_1)
        substring2_list.append(sub_2)
    start_index = 0

    for i in range(len(substring1_list)):
        for j in range(len(text) - len(substring1_list[i]) + 1):
            if text[j:j+len(substring1_list[i])] == substring1_list[i]:
                start = True
            if start:
                if text[j:j+len(substring1_list[i])] == substring1_list[i]:
                    start_index = j


    for i in range(len(substring2_list)):
        for j in range(len(text) - len(substring2_list[i]) + 1):
            if text[j:j + len(substring2_list[i])] == substring2_list[i]:
                start = True

            if start:
                if text[j:j + len(substring2_list[i])] == substring2_list[i]:
                    start_index = max(j,start_index)

    #print(start_index)
    start =False

    substring3_list=[]
    substring4_list=[]

    find = False
    item_end = None
    for i in range(0,len(item_list)):
        if item_list[i] == item:
            find = True
        elif find:
            if text.__contains__(item_list[i]):
                item_end = item_list[i]
                break

    item_end_low = 'Item ' + item_end + "."
    item_end_up = item_end_low.upper()
    substring3_list.append(item_end_low+dict[item_end])
    substring4_list.append(item_end_up+dict[item_end].upper())

    for space in range(1,6):
        sub_3 = item_end_low
        sub_4 = item_end_up
        for j in range(0, space):
            sub_3 += ' '
            sub_4 += ' '
        sub_3 += dict[item_end]
        sub_4 += dict[item_end].upper()
        substring3_list.append(sub_3)
        substring4_list.append(sub_4)

    end_index = 0
    for i in range(len(substring3_list)):
        for j in range(len(text) - len(substring3_list[i]) + 1):
            if text[j:j+len(substring3_list[i])] == substring3_list[i]:
                start = True

            if start:
                if text[j:j+len(substring3_list[i])] == substring3_list[i]:
                    end_index = j

    for i in range(len(substring4_list)):
        for j in range(len(text) - len(substring4_list[i]) + 1):
            if text[j:j + len(substring4_list[i])] == substring4_list[i]:
                start = True

            if start:
                if text[j:j + len(substring4_list[i])] == substring4_list[i]:
                    end_index = max(j,end_index)

    #print(end_index)

    risk_factor_text = None
    if start_index > end_index:
        risk_factor_text = text[start_index:len(text)-1]
    else:
        risk_factor_text = text[start_index:end_index]

    #print(text)
    #dir = Path("sde.txt")
    #f = open(dir, "w+", encoding="utf-8")
    #f.write(text)
    print(risk_factor_text)

extractApi(input.url,input.item)