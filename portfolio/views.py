from django.utils import timezone
from .models import *
from efsblog import settings
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum ,F
from django.core.mail import send_mail, BadHeaderError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from io import BytesIO
from reportlab.pdfgen import canvas
from .forms import EmailForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail,  EmailMessage
from django.shortcuts import render, get_object_or_404, render_to_response


def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})


@login_required
def customer_list(request):
   customer = Customer.objects.filter(created_date__lte=timezone.now())
   return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
       # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_new(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           customers = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customers})
   else:
       form = CustomerForm()
       # print("Else")
   return render(request, 'portfolio/customer_new.html', {'form': form})


@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def investment_list(request):
   investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments,
                                                             })


@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})


@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           investment.updated_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
   else:
       # print("else")
       form = InvestmentForm(instance = investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})


@login_required
def investment_delete(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   investment.delete()
   investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   mutual_funds = Mutual_Funds.objects.filter(customer=pk)
   sum_purchase_value = Stock.objects.filter(customer=pk).aggregate(total=(Sum(F('purchase_price')*F('shares'))))['total']
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   # sum_fund_purchase_price = Mutual_Funds.objects.filter(customer=pk).aggregate(Sum('purchase_price'))
   # sum_fund_current_price= Mutual_Funds.objects.filter(customer=pk).aggregate(Sum('current_price'))
   # Initialize the value of the stocks
   sum_current_stocks_value = 0
   sum_of_initial_stock_value = 0
   sum_fund_purchase_price =0
   sum_fund_current_price=0

   # Loop through each stock and add the value to the total
   for stock in stocks:
       sum_current_stocks_value += stock.current_stock_value()
       sum_of_initial_stock_value += stock.initial_stock_value()
    # Loop through each Mutual Fund and add the value to the total
   for mutual_fund in mutual_funds:
       sum_fund_purchase_price +=  mutual_fund.initial_mutual_fund_value()
       sum_fund_current_price += mutual_fund.current_mutual_fund_price()

   return render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                      'stocks': stocks, 'customer':customer,
                                                       'mutual_funds':mutual_funds,
                                                       'sum_fund_current_price':sum_fund_purchase_price,
                                                       'sum_fund_purchase_price':sum_fund_current_price,
                                                      'sum_acquired_value': sum_acquired_value,
                                                       'sum_purchase_value': sum_purchase_value,
                                                       'sum_recent_value':sum_recent_value,
                                                       'sum_current_stocks_value': sum_current_stocks_value,
                                                       'sum_of_initial_stock_value': sum_of_initial_stock_value
                                                       })


# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)



@login_required
def mutual_funds_list(request):
   mutual_funds = Mutual_Funds.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/mutual_funds_list.html', {'mutual_funds': mutual_funds,})


@login_required
def mutual_funds_new(request):
   if request.method == "POST":
       form = MutualFundsForm(request.POST)
       if form.is_valid():
           mutual_fund = form.save(commit=False)
           mutual_fund.created_date = timezone.now()
           mutual_fund.save()
           mutual_funds = Mutual_Funds.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/mutual_funds_list.html',
                         {'mutual_funds': mutual_funds})
   else:
       form = MutualFundsForm()
       # print("Else")
   return render(request, 'portfolio/mutual_funds_new.html', {'form': form})

@login_required
def mutual_funds_edit(request, pk):
   mutual_fund = get_object_or_404(Mutual_Funds, pk=pk)
   if request.method == "POST":
       form = MutualFundsForm(request.POST, instance=mutual_fund)
       if form.is_valid():
           mutual_fund = form.save()
           mutual_fund.updated_date = timezone.now()
           mutual_fund.save()
           mutual_funds = Mutual_Funds.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/mutual_funds_list.html', {'mutual_funds': mutual_funds})
   else:
       # print("else")
       form = MutualFundsForm(instance = mutual_fund)
   return render(request, 'portfolio/mutual_funds_edit.html', {'form': form})

@login_required
def mutual_funds_delete(request, pk):
   mutual_fund = get_object_or_404(Mutual_Funds, pk=pk)
   mutual_fund.delete()
   mutual_funds = Mutual_Funds.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/mutual_funds_list.html', {'mutual_funds': mutual_funds})


# def share(request):
#     template = 'portfolio/share.html'
#
#     if request.method == 'POST':
#         form = EmailForm(request.POST, request.FILES)
#         if form.is_valid():
#             # subject = form.cleaned_data['subject']
#             # message = form.cleaned_data['message']
#             # email = form.cleaned_data['email']
#             # attach = request.FILES['attach']
#             # mail = EmailMessage(subject, message, 'msdfall2017team3@gmail.com', [email])
#             # mail.attach(attach.name, attach.read(), attach.content_type)
#             # mail.send()
#             pass
#
#     else:
#         form = EmailForm()
#         return render(request,template, {'form': form})
