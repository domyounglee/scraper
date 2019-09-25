#-*- coding:utf-8 -*-
import urllib3
import json
import pprint as pp
import urllib
import sys
import mysql.connector
import time
import pickle
import random
from bs4 import BeautifulSoup

fw = open("brunch_IT트렌트.txt","w")
http = urllib3.PoolManager()

def parse_brunch(fw, data_app):
	for data in data_app["data"]:

		if "text" in data:
			fw.write(data["text"]+" ")

		if "data" in data:
			parse_brunch(fw,data)

cat_query="33" # IT 트렌드   
#print(query)
#encodedcat_query=urllib.parse.quote(query)
#UTC 1443448410000 ~ now 
#10000000 (10000sec) 단위로 request  
profileID_no=""
for t in range(1443448410000,1569294879000,20000000):
	print(t)
	boardURL = "https://api.brunch.co.kr/v1/top/keyword/group/"+cat_query+"?publishTime="+str(t)+"&pickContentId="
	headers={"Content-Type": "text/html; charset=UTF-8"}
	response = http.request("GET",boardURL,headers=headers)
	result = json.loads(response.data.decode())

	
	if result['code'] == 200:
		for i,article in enumerate(result['data']['articleList']):

			#save the first ID to prevent from duplication
			#stop if it has already scraped 
			if profileID_no == article['profile']['profileId']+"_"+str(article['article']['no']) :
				break
			if i==0:
				profileID_no_new =article['profile']['profileId']+"_"+str(article['article']['no'])
			#print(profileID_no)
			print(article['profile']['profileId'])
			print(article['article']['no'])

			fw.write(article['article']['title']+" "+article['article']['subTitle']+"\n")

			encodedcat_query=urllib.parse.quote(article['profile']['profileId'])
			#https://brunch.co.kr/@profile[profileId]/article[no]
			blogURL = "https://brunch.co.kr/@"+encodedcat_query+"/"+str(article['article']['no'])
			#openApiURL = "https://brunch.co.kr/keyword/"+encodedquery+"?q=g"
			headers={"Content-Type": "text/html; charset=UTF-8"}

			response = http.request("GET",blogURL,headers=headers)

			result = response.data.decode()

			soup = BeautifulSoup(result, "lxml")
			#print(soup)
			paragraphs=soup.find_all(['p','h3','blockquote'],attrs={'class':'wrap_item item_type_text'})
			for p in paragraphs:

				j=p.attrs["data-app"]
				try:
					data_app = json.loads(j)
					parse_brunch(fw, data_app)
					fw.write("\n")
				except:
					continue 


	

				"""
				if len(json.loads(j)["data"])!=0 and "text" in json.loads(j)["data"][0] :
					fw.write(json.loads(j)["data"][0]["text"]+"\n")
				elif len(json.loads(j)["data"])!=0 and "data" in json.loads(j)["data"][0]  :
					if len(json.loads(j)["data"][0]["data"])!=0 and "text" in json.loads(j)["data"][0]["data"][0]:
						fw.write(json.loads(j)["data"][0]["data"][0]["text"]+"\n")
				else:
					continue
				"""

			fw.write("\n"+"=*=*="+"\n")
		profileID_no = profileID_no_new

fw.close()