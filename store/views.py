from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def store(request):
    products = Product.objects.all()
    order, created = Order.objects.get_or_create(customer=request.user.customer,complete=False)
    print(order,created)
    context = {
        'products':products,
        'order':order
    }
    return render(request,'store/store.html',context)


def cart(request):
    order, created = Order.objects.get_or_create(customer=request.user.customer,complete=False)
    context={'order':order}
    return render(request,'store/cart.html',context)

def checkout(request):
    order,created = Order.objects.get_or_create(customer=request.user.customer,complete=False)
    context={
       'order':order 
    }
    return render(request,'store/checkout.html',context)


def gotoCart(request):
    data = json.loads((request.body))
    order , created = Order.objects.get_or_create(customer=request.user.customer,complete=False)
    print(order,created,request.user,request.user.customer)
    
    for item in data['orders']:
        product = get_object_or_404(Product,id=item['id'])
        quantity = item['quantity']
        orderItem ,created = OrderItem.objects.get_or_create(product=product,order=order)
        if created:
            orderItem.order = order
            orderItem.quantity = quantity
            orderItem.save()
        else:
            orderItem.quantity +=quantity
            orderItem.save()
    context = {
        'order': order
    }
    order.save()
    return render(request,'store/cart.html',context)


def updatecart(request):
    order , created = Order.objects.get_or_create(customer=request.user.customer,complete=False)
    # print(order,created,request.user,request.user.customer)
    data = json.loads(request.body)
    # print(data)
    for item in data['orderitems']:
        id = item['id']
        quantity = item['quantity']
        product=get_object_or_404(Product,id=id)
        orderitem , orderitem_created = OrderItem.objects.get_or_create(product=product,order=order)
        if quantity == 0:
            orderitem.delete()
        else:
            orderitem.quantity=quantity
            orderitem.save()
    order.save()
    context={
        'order':order
    }
    return render(request,'store/store.html',context)
    
        
    # else:
    #     
    


def gotocheckout(request):
    order , created = Order.objects.get_or_create(customer=request.user.customer,complete=False)
    data = json.loads(request.body)
    print(data)
    for item in data['orderitems']:
        id = item['id']
        quantity = item['quantity'];
        product=get_object_or_404(Product,id=id)
        orderitem , orderitem_created = OrderItem.objects.get_or_create(product=product,order=order)
        if quantity == 0:
            orderitem.delete()
        else:
            orderitem.quantity=quantity
            orderitem.save()
    order.save()
    context={
        'order':order
    }
    return render(request,'store/checkout.html',context)

def complete(request):
    customer = request.user.customer
    order = get_object_or_404(Order,customer=customer,complete=False)
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    shippingaddress = ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address = address,
        city = city,
        state = state,
        zipcode = zipcode
        )
    shippingaddress.save()
    order.complete = True
    order.save()
    return render(request,'store/complete.html')