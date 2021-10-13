from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main(request):
	return render(request,'index.html')

def POST_crawl(request):

	keywords = request.POST["title"]

	#水利署網頁
	url = "https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx"

	options = Options()
	#關閉瀏覽器跳出訊息
	prefs = {
	    'profile.default_content_setting_values' :
	        {
	        'notifications' : 2
	         }
	}
	options.add_experimental_option('prefs',prefs)
	options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
	options.add_argument("--incognito")           #開啟無痕模式


	driver = webdriver.Chrome("/Users/zhonghaoli/Downloads/chromedriver",options=options) #你的本地爬蟲瀏覽器位置

	driver.get(url)
	sel = driver.find_element_by_id('ctl00_cphMain_gvList')
	pool = driver.find_elements_by_xpath("//*[contains(text(), \'"+keywords+"\')]/following-sibling::td")
	print(pool[0].get_attribute('innerHTML'))

	text = {"Name": "", "Water": ""};
	text["Name"] = keywords
	text["Water"] = pool[0].get_attribute('innerHTML')
	
    #把爬蟲玩的資訊送去前端
	return render(request,'result.html',locals())