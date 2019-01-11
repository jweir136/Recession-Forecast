from django.shortcuts import render
from django.http import HttpResponse

from .models import Updates
from datetime import datetime
import os

import pickle
import requests
from bs4 import BeautifulSoup
import html5lib
import quandl
# Create your views here.

def index(requests):
	# if the system was not updated today...
	obj = Updates.objects.all()
	last_day = int(obj.values('last_update')[0]['last_update'])
	vix = quandl.get("CHRIS/CBOE_VX1", paginate=True)
	vix_close = vix.values[len(vix) - 1][4] - vix.values[len(vix) - 32][4]
	yield_curve = quandl.get("FRED/IOER", paginate=True)
	yield_data = yield_curve.values[len(yield_curve) - 1][0] - yield_curve.values[len(yield_curve) - 32][0]
	dir = os.getcwd()
	filename = r"{}\forecaster\model.sav".format(dir)
	file = open(filename, "rb")
	model = pickle.load(file)
	status = model.predict([[yield_data, vix_close]])
	return render(requests, "forecaster/index.html", {'status':status})