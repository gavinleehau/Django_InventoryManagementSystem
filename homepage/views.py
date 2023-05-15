from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.db.models import Sum, F, FloatField, Count, IntegerField
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractWeek, ExtractWeekDay
from django.utils.timezone import datetime, timedelta
from datetime import date
import random

import locale

from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill, SaleItem


class HomeView(View):

    bills = SaleBill.objects.order_by('-billno')
    paginate_by = 10

    # lấy giá trị get_total_price gán cho totalPrice
    for sale in bills:
        sale.totalPrice=sale.get_total_price()
        sale.save()

     
    def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)

        sales = SaleBill.objects.order_by('-billno')
        purchases = PurchaseBill.objects.order_by('-time')

        # Thống kê doanh thu theo tháng
        output = (SaleBill.objects.annotate(month=ExtractMonth("time"))
                    .values("month")
                    .annotate(total=Sum(F("totalPrice"),output_field=IntegerField()))
                    .order_by("month")
        )


        # Thống kê doanh thu ngày/tháng
        now = datetime.now()
        current_month = now.month
        current_year = now.year

        first_day = datetime(current_year, current_month, 1)
        last_day = first_day + timedelta(days=31)
    
        output_day = (SaleBill.objects.filter(time__gte=first_day, time__lt=last_day)
                        .annotate(day=ExtractDay('time')) 
                        .values('day') 
                        .annotate(total=Sum(F("totalPrice"),output_field=IntegerField())) 
                        # .order_by('day')
        )

        

        
        # Thông kê theo tuần
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        current_week = datetime.today().weekday()
        output_week = (
            SaleBill.objects.annotate(week=ExtractWeek('time'))
            .values('week')
            .annotate(total=Sum(F("totalPrice"), output_field=IntegerField()))
            .order_by('week')
        )

        week_data_list = []
        for week_data in output_week:
            week_number = week_data['week']
            year = 2023  # Set the desired year
            start_of_year = date(year, 1, 1)
            start_of_week = start_of_year + timedelta(weeks=week_number, days=-start_of_year.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            locale.setlocale(locale.LC_ALL, 'vi_VN')
            total = locale.currency(week_data['total'], grouping=True, symbol='₫')
    
            week_data_list.append({
                'week_number': week_number,
                'start_of_week': start_of_week,
                'end_of_week': end_of_week,
                'total': total
            })
            # print(f"Week {week_number}:")
            # print(f"Start of Week: {start_of_week}")
            # print(f"End of Week: {end_of_week}")
            # print(f"End of Week: {total}")
            # print("--------------------")


        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

            total_amount = SaleBill.objects.filter(time__range=(start_datetime, end_datetime)).aggregate(total=Sum('totalPrice'))

            output_many_days = {
                'start_date': start_datetime,
                'end_date': end_datetime - timedelta(days=1),
                'total_amount': total_amount['total'] if total_amount['total'] is not None else 0
            }
            # print(f"start_date: {start_date}:")
            # print(f"End date {end_date}")
            # print(f"End of Week: {total_amount}")
        else:
            output_many_days = None


        
        
        return render(
            request, 
            template_name = "home.html", 
            context = {
                'labels'    : labels,
                'data'      : data,
                'sales'     : sales,
                'purchases' : purchases,
                'output': output,
                'output_day': output_day,
                'current_month': current_month,
                'output_week' : output_week,
                'current_week': current_week,
                'week_data_list': week_data_list,
                'start_of_week': start_of_week,
                'end_of_week': end_of_week,
                'output_many_days': output_many_days,
                'start_date': start_date,
                'end_date': end_date,
                # 'total_amount': total_amount,

            }
        )

