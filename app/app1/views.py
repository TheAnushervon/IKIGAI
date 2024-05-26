from django.shortcuts import render
import requests
import json 

# Create your views here.
def get_company(request): 
    if request.method == 'POST': 
        INN = request.POST.get('INN')   
        url = 'https://api-fns.ru/api/egr'
        params = {
            'req': INN,
            'key': '90bc98530dabe4d2d36c8082223e8efc56382a1f' 
        }

        response = requests.get(url, params=params)

        data = response.json()
        if response.status_code == 200:
            data = response.json()
            value = data["items"][0]["ЮЛ"]["Руководитель"]
            return value
        else:
            return None
