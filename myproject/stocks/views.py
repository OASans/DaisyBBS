from django.shortcuts import render, redirect

from django.views.generic import UpdateView,ListView, View
# from .models import Stock
import json
from django.http import HttpResponse

import tushare as ts
import pandas as pd
import json
import time
import datetime
from dateutil.relativedelta import relativedelta
from django import forms

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

# data = ts.get_hist_data('600848', start='2017-06-05', end='2018-01-09')
# data.reset_index(inplace=True)
# data.sort_index(ascending=False,inplace=True)
# data.reset_index(drop=True, inplace=True)

#api = ts.pro_api(mytoken)
# data = api.daily(ts_code='000001.SZ',start_date='20180101',end_date='20190101')
# data = data.sort_index(ascending=False)
# data['trade_date']=pd.to_datetime(data['trade_date']).dt.strftime('%m/%d/%Y')

pro = ts.pro_api()
stock_list = pro.query('stock_basic', exchange='', list_status='L',
                       fields='ts_code,symbol,name,area,industry,market')

def trans_json(arr):
    column_list = []
    for row in arr:
        column_list.append(row)
    jsonlist = []
    for index in range(arr[column_list[0]].size):
        dict = {}
        for row in arr:
            dict[row] = arr[row][index]
        jsonlist.append(dict)
    return jsonlist

def stockinfo(request, stock_id):
    date = datetime.date.today()
    pre_date = date - relativedelta(days=+1)
    id = stock_id[0:6]
    #+'.'+stock_id[6:]
    info_id = stock_id
    data = ts.get_hist_data(id)
    info = pro.daily_basic(ts_code=info_id, trade_date=pre_date.strftime('%Y%m%d'))
    day = pro.daily(ts_code=info_id, start_date=pre_date.strftime('%Y%m%d'))
    #name = pro.namechange(ts_code=info_id, end_date='None', fields='name')
    name = pro.namechange(ts_code=info_id, fields='name')
    data.reset_index(inplace=True)
    data.sort_index(ascending=False,inplace=True)
    data.reset_index(drop=True, inplace=True)
    print(info_id)
    print(name)
    return render(request,"stock_info.html", {'stock': json.dumps(trans_json(data)), 'info': trans_json(info),
                                              'name': trans_json(name), 'day': trans_json(day)})



def stockhome(request):
    print("test")
    if request.method == 'POST':
        print("post success")
        ts_code = request.POST.get('ts_code')
        return stockinfo(request, ts_code)
    print("not success")

    return render(request,"stock_home.html", {'stocklist': trans_json(stock_list)})



def news(request):
    date=datetime.date.today()
    pre_date=date-relativedelta(days=-1)
    print(date.strftime('%Y%m%d'))
    print(pre_date.strftime('%Y%m%d'))
    df = pro.news(src='sina', start_date=date.strftime('%Y%m%d'), end_date=pre_date.strftime('%Y%m%d'))
    print(df)
    return render(request,"news.html",{'news':trans_json(df)})



# def check(request):
#     print('test')
#     if request.method == 'POST':
#         ts_code = request.POST.get('ts_code')
#         return redirect('stockinfo', ts_code)
#     return render(request,"stock_home.html", {'stocklist': trans_json(stock_list)})




