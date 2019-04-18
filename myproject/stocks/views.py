from django.shortcuts import render

from django.views.generic import UpdateView,ListView, View
# from .models import Stock
import json
from django.http import HttpResponse

import tushare as ts
import pandas as pd
import json

mytoken = 'f78629cf67fcc2923a7feeed2000b1e63760507375d34391ad7b9bc6'

# data = ts.get_hist_data('600848', start='2018-01-05', end='2018-01-09')
#
# column_list = []
# for row in data:
#     column_list.append(row)
# jsonlist = []
# for index in range(data[column_list[0]].size):
#     dict = {}
#     for row in data:
#         dict[row] = data[row][index]
#     jsonlist.append(dict)
#
# def stockhome(request):
#     return HttpResponse(json.dumps(jsonlist))

###################################################

# class StockListView(ListView):
#     model = Stock
#     context_object_name = 'stocks'
#     template_name = 'stock_home.html'

###################################################

data = ts.get_hist_data('600848', start='2017-06-05', end='2018-01-09')
data.reset_index(inplace=True)
data.sort_index(ascending=False,inplace=True)
data.reset_index(drop=True, inplace=True)

# api = ts.pro_api(mytoken)
# data = api.daily(ts_code='000001.SZ',start_date='20180101',end_date='20190101')
# data = data.sort_index(ascending=False)
# data['trade_date']=pd.to_datetime(data['trade_date']).dt.strftime('%m/%d/%Y')

column_list = []
for row in data:
    column_list.append(row)
jsonlist = []
for index in range(data[column_list[0]].size):
    dict = {}
    for row in data:
        dict[row] = data[row][index]
    jsonlist.append(dict)

def stockhome(request):

     return render(request,"stock_home.html",{'stock': json.dumps(jsonlist)})


