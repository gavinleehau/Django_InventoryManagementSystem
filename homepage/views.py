from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill


class HomeView(View):
     
    def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)

        sales = SaleBill.objects.order_by('-time')
        purchases = PurchaseBill.objects.order_by('-time')
        
        return render(
            request, 
            template_name = "home.html", 
            context = {
                'labels'    : labels,
                'data'      : data,
                'sales'     : sales,
                'purchases' : purchases
            }
        )

