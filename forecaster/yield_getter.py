import requests
import html5lib
from bs4 import BeautifulSoup

def get():
	con = 0
	
	while con == 0:
		try:
			url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yieldAll"
			data = requests.get(url).text
			soup = BeautifulSoup(data, 'html5lib')
			
			main_table = soup.find_all("table")[1]
			
			today_yield = main_table.find_all("tr")[len(main_table.find_all("tr")) - 1]
			month_ago_yield = main_table.find_all("tr")[len(main_table.find_all("tr")) - 21]
		
			con = 1
			
			return float(today_yield.find_all("td")[5].text) - float(month_ago_yield.find_all("td")[5].text)
		except:
			pass		
			
def vix():
	con = 0
	
	while con == 0:
		try:
			url = "https://finance.yahoo.com/quote/%5EVIX/history?period1=1538895600&period2=1546848000&interval=1d&filter=history&frequency=1d"
			data = requests.get(url).text
			soup = BeautifulSoup(data, 'html5lib')
			
			main_table = soup.find_all("table")[0]
			
			main_tbody = main_table.find("tbody")
			
			vix_close1 = float(main_tbody.find_all("tr")[0].find_all("td")[5].text)
			vix_close2 = float(main_tbody.find_all("tr")[21].find_all("td")[5].text)
			
			con = 1
			
			return vix_close1 - vix_close2
		except:
			pass