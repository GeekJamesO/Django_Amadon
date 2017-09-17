from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
import bcrypt
def getProducts():
    return [
    {'id' : 1, 'item':'Shoes', 'price':49.99} ,
    {'id' : 2, 'item':'Pants', 'price':70.00} ,
    {'id' : 3, 'item':'Drone', 'price':329.99}
    ]

def index(request):
    context = { 'products' : getProducts() }
    return render(request, "shopping_app/index.html", context)

def process(request, methods=['POST']):
    prodId = request.POST['ProdId']

    print "Prod Id:", prodId
    catalog = getProducts()
    item = None
    price = None
    quantity = request.POST['quantity']

    for prod in catalog:
        if str(prod['id']) == str(prodId):
            item = prod['item']
            price = prod['price']
            break;
    # if quantity <= 0:
    #     quantity = 1;

    request.session['item'] = item
    request.session['price'] = float(price)
    request.session['id'] = prodId
    request.session['quantity'] = int(quantity)
    InvoicePrice = float(price) * int(quantity)
    request.session['InvoicePrice'] = InvoicePrice
    try:
        request.session['TotalOrders'] += int(quantity)
        request.session['TotalPrice'] += InvoicePrice
    except Exception as e:
        request.session['TotalOrders'] = int(quantity)
        request.session['TotalPrice'] = InvoicePrice
    return redirect ('/checkout')

def checkout(request):
    return render(request, "shopping_app/checkout.html")

def reset(request, methods=['POST']):
    request.session['TotalOrders'] = 0
    request.session['TotalPrice'] = 0
    return redirect ('/')
