from django.shortcuts import render
from django.http import HttpResponse

from .models import Updates
from datetime import datetime

import pickle
import requests
from bs4 import BeautifulSoup
import html5lib
# Create your views here.

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

def index(requests):
	# if the system was not updated today...
	obj = Updates.objects.all()
	last_day = int(obj.values('last_update')[0]['last_update'])
	
	if last_day != int(datetime.now().day):
		print(True)
		# run the scaping functions
		delta_yield, delta_vix = get(), vix()
		# add values into model
		obj.delete()
		print(delta_yield, delta_vix)
		new_obj = Updates.objects.create(last_update=str(datetime.now().day), delta_yield=str(delta_yield), delta_vix=str(delta_vix))
		new_obj.save()
	else:
		delta_yield = float(obj.values('delta_yield')[0]['delta_yield'])
		delta_vix = float(obj.values('delta_vix')[0]['delta_vix'])
		print(delta_yield, delta_vix)
		
	model = pickle.load(open(r"C:\Users\jweir\Data Science Practice 1\datasets\basic_regression\AAPL1\recession_forecast\recession_forecast\forecaster/recession_model.sav", "rb"))
	status = model.predict([[delta_yield, delta_vix]])
		
	return render(requests, "forecaster/index.html", {"status":status})