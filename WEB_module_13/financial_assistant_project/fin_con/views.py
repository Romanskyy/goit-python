from django.shortcuts import render
from django.http import HttpResponse
from .models import Spending, Income
from datetime import datetime


def home(request):
    info_comment = 'no comment'

    # all what in is to take request
    raw_income = request.POST.get('income')
    income = raw_income if raw_income != None else False

    if income:
        income_date = datetime.strptime(
            request.POST.get('income_date'), "%Y-%m-%d")
        raw_comment = request.POST.get('comment')
        comment = raw_comment if raw_comment else info_comment
        date_info = datetime.now().strftime("%Y-%m-%d")

        income_date = income_date if income_date != '' else date_info

        new_data = Income(amount=income, comment=comment,
                          date_of_deposit=income_date)

        new_data.save()
    return render(request, 'fin_con/home.html')


def spending(request):
    info_comment = 'no comment'

    raw_spending = request.POST.get('spending')
    raw_comment = request.POST.get('comment')

    spended_sum = raw_spending if raw_spending else False

    if spended_sum:
        comment = raw_comment if raw_comment else info_comment
        date_info = datetime.now().date().strftime("%Y-%m-%d")

        new_data = Spending(category=request.POST.get(
            'category'), expenses_amount=spended_sum, expenses_comment=comment, date_of_expenses=date_info)
        new_data.save()

    return render(request, 'fin_con/spending.html')


def report(request):
    if request.method == "GET":

        report_type = dict(request.GET.items()).get('report_type', False)

        start_date = dict(request.GET.items()).get('start_date', False)
        start_date = start_date if start_date != '' else False

        end_date = dict(request.GET.items()).get('end_date', False)
        end_date = end_date if end_date != '' else False

        category = dict(request.GET.items()).get('category', False)

        if report_type == 'income':
            if not start_date or not end_date:
                income_data = Income.objects.all().order_by('date_of_deposit')
                result = []
                header = f'|{"date of income":<20}|{"comment":<35}|{"sum":>20}|'
                full_sum = 0.0
                result.append(header)
                for el in income_data:
                    el = str(el).split(',')
                    date = el[0].split(' ')[0]
                    result.append(f'|{date:<20}|{el[-1]:<35}|{el[1]:>20}|')
                    full_sum += float(el[1])
                result.append(f'|Total income: {full_sum:>63}|')

            elif start_date and end_date:
                income_data = Income.objects.filter(date_of_deposit__range=(
                    start_date, end_date)).order_by('date_of_deposit')
                result = []
                header = f'|{"date of income":<20}|{"comment":<35}|{"sum":>20}|'
                full_sum = 0.0
                result.append(header)
                for el in income_data:
                    el = str(el).split(',')
                    date = el[0].split(' ')[0]
                    result.append(f'|{date:<20}|{el[-1]:<35}|{el[1]:>20}|')
                    full_sum += float(el[1])

                result.append(f'|Total income: {full_sum:>63}|')
        else:
            result = []
            result.append('You choose no rport type')

    return render(request, 'fin_con/report.html', {'info': result})
