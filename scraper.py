import json
import requests
from lxml import etree
import argparse
import re

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

# FIlTER Augument
parser.add_argument('--quere', default="cse", type=str,help='the keyword you want to search (default is "cse")')
parser.add_argument('--campus', default="col", type=str,help='which campus are you going to take the class (default is "col")')
parser.add_argument('--term', default="1228", type=str,help='which semaster are you searching for (default is 1228,which is 2022au)')
parser.add_argument('--career', default="ugrd", type=str,help='what kind of student is that class offering (default is ugrd, which is undergraduate)')
parser.add_argument('--subject', default="", type=str,help='the subject you are searching for')
parser.add_argument('--catalog', default="", type=str,help='the class number catalog (e.g 1xxxx is for course that has a course number start with 1)')

args = parser.parse_args()

# FIlTER adjusment
if args.subject != "":
    args.subject="&subject="+args.subject
if args.catalog != "":
    args.catalog="&catalog-number="+args.catalog

# Prerequest
def Prereq(des): 
    # findall() 查找匹配正则表达式的字符串
    index = des.find("Prereq: ")
    if(index==-1):
        return ""
    else:
        return (temp[index+8:])   

url = 'https://www.cnblogs.com/xyxuan/p/14336276.html'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}


URL_HEAD="https://content.osu.edu/v2/classes/search?q=%s&campus=%s&term=%s&academic-career=%s" %(args.quere,args.campus,args.term,args.career) +args.subject+args.catalog
print(URL_HEAD)

json_file = requests.get(URL_HEAD,headers = headers).content.decode('utf-8')
data = json.loads(json_file)
data=data['data']
for item in data['courses']:
    course= item['course']
    temp=course["description"]
    course.update({'Prereq':Prereq(temp)})
    item.update({'course':course})
    


result=json.dumps(data,sort_keys=True, indent=2, separators=(',', ': '))

with open("classes.json", "w") as outfile:
    outfile.write(result)