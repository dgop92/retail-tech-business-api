import datetime
from calendar import monthrange

import pytz
from account.custom_auth import BearerTokenAuthentication
from django.db.models.expressions import ExpressionWrapper, F
from django.db.models import Sum, Q
from django.db.models.fields import DecimalField
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from dashboard.custom_permissions import IsSuperUser
from dashboard.models import Entry, Exit, Product, Sale

DASHBOARD_AUTH_CLASSES = (BearerTokenAuthentication,)


@api_view(["GET"])
@authentication_classes(DASHBOARD_AUTH_CLASSES)
@permission_classes([IsSuperUser])
def monthly_status(request, month):

    month = int(month)

    monthly_sold = 0
    exits_in_month = Exit.objects.filter(created_date__month=month)

    for exit in exits_in_month:
        monthly_sold += exit.total_amount_sold()

    monthly_spent = 0
    entries_in_month = Entry.objects.filter(created_date__month=month)

    for entry in entries_in_month:
        monthly_spent += entry.total_amount_spent()

    monthly_profit = monthly_sold - monthly_spent

    return Response(
        {
            "monthly_sold": monthly_sold,
            "monthly_spent": monthly_spent,
            "monthly_profit": monthly_profit,
        }
    )


@api_view(["GET"])
@authentication_classes(DASHBOARD_AUTH_CLASSES)
@permission_classes([IsSuperUser])
def daily_sales_by_month(request, month):

    month = int(month)

    today = datetime.date.today()
    number_of_days = monthrange(today.year, month)[1]

    month_days = [i for i in range(1, number_of_days + 1)]
    daily_sales = []
    for day in month_days:
        start_date = datetime.datetime(today.year, month, day).replace(tzinfo=pytz.utc)
        end_date = start_date + datetime.timedelta(days=1)
        daily_exits = Exit.objects.filter(created_date__range=(start_date, end_date))
        daily_sold = 0
        for exit in daily_exits:
            daily_sold += exit.total_amount_sold()
        daily_sales.append(daily_sold)

    return Response(
        {
            "month_days": month_days,
            "daily_sales": daily_sales,
        }
    )


@api_view(["GET"])
@authentication_classes(DASHBOARD_AUTH_CLASSES)
@permission_classes([IsSuperUser])
def best_products(request):

    results_by_sales = Sale.objects.values('product__code', 'product__name').annotate(
        sold=ExpressionWrapper(
            Sum(F("amount") * F("unit_price")), output_field=DecimalField()
        )
    ).order_by("-sold")[:5]

    products = [s['product__name'] for s in results_by_sales]
    prices = [s['sold'] for s in results_by_sales]

    remainder = 5 - len(products)
    for _ in range(remainder):
        products.append("No Producto")
        prices.append(0)

    return Response(
        {
            "best_product_by_sales": {
                "products": products,
                "prices": prices,
            },
        }
    )

    
@api_view(["GET"])
@authentication_classes(DASHBOARD_AUTH_CLASSES)
@permission_classes([IsSuperUser])
def product_with_few_stocks(request):

    results = Product.objects.filter(Q(stock__gt=0) & Q(stock__lte=10))[:5]
    products = [p.name for p in results]
    stocks = [p.stock for p in results]
    
    remainder = 5 - len(products)
    for _ in range(remainder):
        products.append("No Producto")
        stocks.append(0)
    
    return Response(
        {
            "products": products,
            "stocks": stocks,
        }
    )