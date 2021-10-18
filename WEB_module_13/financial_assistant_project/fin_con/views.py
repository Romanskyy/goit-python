from django.shortcuts import render
from django.http import HttpResponse
from .models import Spending, Income
from datetime import datetime


# Create your views here
# def home(request):

#     print(request.method)

#     # all what in is to take request

#     income = request.GET.get('income') if request.GET.get('income') != None else False
#     comment = request.GET.get('comment')
#     date_info = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print('=' * 80)
#     print(income)
#     print(comment)
#     print(date_info)
#     print('=' * 80)
#     if income != None:
#         new = Income(amount=income, comment=comment,
#                      date_of_deposit=date_info)
#         new.save()

#     info = [income, comment]

#     # return render(request, 'fin_con/home.html', {'info': info})
#     return render(request, 'fin_con/home.html')

def home(request):

    print(request.method)
    info_comment = 'no comment'

    # all what in is to take request
    raw_income = request.GET.get('income')
    income = raw_income if raw_income != None else False
    if income:
        raw_comment = request.GET.get('comment')
        comment = raw_comment if raw_comment else info_comment
        print('=' * 80)
        print(income)
        print(raw_comment)
        print(comment)
        print('=' * 80)
        date_info = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print('=' * 80)
    # print(income)
    # print(comment)
    # print(date_info)
    # print('=' * 80)
    # if income != None:
        new = Income(amount=income, comment=comment,
                     date_of_deposit=date_info)
        new.save()

    # info = [income, comment]

    # return render(request, 'fin_con/home.html', {'info': info})
    return render(request, 'fin_con/home.html')


def spending(request):
    return HttpResponse('<h1>Spending page</h1>')


def report(request):
    return HttpResponse('<h1>Report will be shown here</h1>')
