from django.shortcuts import render, redirect
from .models import Inventory, Customer, Admin, Employee, Cart, Order, Delivery
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from datetime import datetime
from django.db.models import Q
from django.core import serializers

def home(request):
	if request.method == "POST":
		medname = request.POST['search']
		obj = Inventory.objects.filter(Q (med_name__icontains = medname) | Q(med_generic__icontains = medname))
		context = { }
		if obj:
			context = {'all': obj}
		else:
			context = {'noresults': "No Medicine found"}
		return render(request, 'home.html', context)
	else:
		obj = Inventory.objects.all()
		context = {'all': obj}
		return render(request, 'home.html', context)

def about(request):
	return render(request, 'about.html', {})

def customerPortal(request):
	obj = Inventory.objects.all()
	context = {'all': obj}
	return render(request, 'customer.html', context)

def loginC(request):
	if request.session.is_empty():
		return render(request, 'loginportal.html', {})
	else:
		return redirect('customerx')


def loginCustomer(request):
	obj = Inventory.objects.all()
	context = {'all': obj}
	if request.method == "POST":
		username = request.POST['email']
		password = request.POST['password']
		if Customer.objects.filter(customer_email = username).exists():
			userX = Customer.objects.get(customer_email = username)
			if password == userX.customer_password:
				request.session['userId'] = userX.customer_id
				request.session['username'] = userX.customer_name
				request.session.set_expiry(3000)
				return render(request, 'customer.html', context)
			else:
				return HttpResponse("invalid password")
		elif Employee.objects.filter(employee_email = username).exists():
			userE = Employee.objects.get(employee_email = username)
			if password == userE.employee_password:
				request.session['userId'] = userE.pharmacy_id
				request.session['username'] = userE.owner_name
				request.session.set_expiry(3000)
				response = redirect('pharmacypage')
				return response
			else:
				return HttpResponse("invalid password")
		elif Admin.objects.filter(admin_email = username).exists():
			userA = Admin.objects.get(admin_email = username)
			if password == userA.admin_password:
				request.session['userId'] = userA.admin_id
				request.session['username'] = userA.admin_name
				request.session.set_expiry(3000)
				response = redirect('adminpage')
				return response
			else:
				return HttpResponse("invalid password")
		else:
			return HttpResponse("invalid email")
	else:
		if request.session.is_empty():
			response = redirect('loginC')
			return response
		elif request.session['userId']:
			return render(request, 'customer.html', context)
		else:
			request.session.set_test_cookie()
			response = redirect('loginC')
			return response

def loginE(request):
	obj = Inventory.objects.filter(pharmacy_id = request.session['userId'])
	context = {'all': obj}
	return render(request, 'employee.html', context)

def loginA(request):
	return render(request, 'admin.html', {})

def logoutC(request):
	try:
		request.session.flush()
		messages.success(request, ('Logged out Successfully'))
		return redirect('home')
	except KeyError:
		pass
	messages.success(request, ('Logged out Successfully'))
	return redirect('home')

def registerC(request):
	if request.method == "POST":
		obj = Inventory.objects.all()
		context = {'all': obj}
		customerName = request.POST['username']
		customerEmail = request.POST['email']
		customerPassword = request.POST['password']
		customerAddress = request.POST['address']
		customerPhone = request.POST['phone']
		customerYear = request.POST['year']
		customerMonth = request.POST['month']
		customerDay = request.POST['day']
		customerlongT = request.POST['userLongT']
		customerlatiT = request.POST['userLatiT']
		objX = Customer(customer_name = customerName, birthdate = ''+customerYear+'-'+customerMonth+'-'+customerDay+'', customer_address = customerAddress, customer_password = customerPassword, customer_email = customerEmail, customer_phone = customerPhone, customer_longT = customerlongT, customer_latiT = customerlatiT)
		objX.save()
		response = redirect('loginC')
		return response
	else:
		return render(request, 'register.html', {})


def settingsC(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Customer.objects.filter(customer_id = request.session['userId'])
		context = {'all': obj, }
		return render(request, 'settingsC.html', context)
	

def add_cart(request, list_id):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		quantity = request.GET['quantity']
		obj = Inventory.objects.get(med_id = list_id)
		objC = Cart(pharmacy_id = obj.pharmacy_id, customer_id =  Customer.objects.get(customer_id = request.session['userId']), adding_quantity = quantity, med_id = obj)
		objC.save()
		messages.success(request, ('Item added to the cart'))
		return redirect('loginCustomer')

def remv_cart(request, list_id):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		Cart.objects.filter(cart_id = list_id).delete()
		messages.success(request, ('Item removed from the cart'))
		return redirect('cart')

def catagorize(request, foo):
	obj = Inventory.objects.filter(med_catagory = foo)
	context = { 'all': obj, }
	return render(request, 'catagorize.html',context)

def catagorizeC(request, food):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Inventory.objects.filter(med_catagory = food)
		context = { 'all': obj, }
		return render(request, 'catagorize.html',context)


def cart(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Cart.objects.filter(customer_id = request.session['userId'])
		all_cost = 10
		for k in obj:
			tl_cost = k.med_id.med_price * k.adding_quantity
			all_cost = tl_cost + all_cost
		context = {'all': obj, 'price_of': all_cost}
		return render(request, 'cart.html', context)

def checkoutOrder(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Cart.objects.filter(customer_id = request.session['userId'])
		all_cost = 10
		for k in obj:
			all_cost = k.med_id.med_price + all_cost
		objD = Delivery.objects.filter(DS_status = True)
		context = {'all': obj, 'price_of': all_cost, 'deliveryTime': objD}
		return render(request, 'checkout.html', context)

def addItemA(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		return render(request, 'addItemE.html', context)

def orderHistoryE(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Order.objects.filter(pharmacy_id = request.session['userId'])
		context = {'all': obj}
		return render(request, 'orderHistoryE.html', context)

def orderC(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		if request.method == "POST":
			deliverTime = request.POST['deliveryTime']
			deliverNote = request.POST['deliveryNote']
			obj = Cart.objects.filter(customer_id = request.session['userId'])
			all_cost = 10
			itemQuantity = 0
			for k in obj:
				all_cost = k.med_id.med_price + all_cost
			for i in obj:
				itemQuantity += 1
			# deliveryTime = deliverTime.split("-")
			# startTime = datetime.strptime(deliveryTime[0], '%I:%M%p')
			# stopTime = datetime.strptime(deliveryTime[1], '%I:%M%p')
			orderlongT = request.POST['userLongT']
			orderlatiT = request.POST['userLatiT']
			objX = Order( customer_id=  obj[0].customer_id, delivery_id= Delivery.objects.get(DS_id = deliverTime), rating= 0, order_quantity= itemQuantity, delivery_note= deliverNote, order_cost = all_cost, order_longT = orderlongT, order_latiT = orderlatiT)
			objX.save()
			for med in obj:
				objX.med_ids.add(med.med_id)
			for shops in obj:
				objX.pharmacy_id.add(shops.pharmacy_id)
			
			messages.success(request, ('Order is processing, check order status in orders option on your account'))
			return redirect('home')

def orderHistoryC(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Order.objects.filter(customer_id = request.session['userId'])
		context = {'all': obj}
		return render(request, 'orderHistoryC.html', context)

def opRouteE(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		ob = Order.objects.filter(pharmacy_id = request.session['userId'])
		# for item in ob:
		# 	item['order'] = model_to_dict(item['order'])
		obj = serializers.serialize('json',ob)
		objx = Employee.objects.filter(pharmacy_id = request.session['userId'])
		context = {'all': obj, 'pharmacyLongT': objx[0].employee_longT, 'pharmacyLatiT': objx[0].employee_latiT}
		return render(request, 'opRouteE.html', context)

def profileC(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		counter = 0
		ob = Customer.objects.get(customer_id = request.session['userId'])
		if request.method == "POST":
			name = request.POST['username']
			email = request.POST['email']
			phone = request.POST['phone']
			cpass = request.POST['cpassword']
			npass = request.POST['npassword']
			address = request.POST['address']
			if len(npass) > 1:
				if cpass == ob.customer_password:
					ob.customer_password = npass
					counter+=1
				else:
					messages.success(request, ('Current Password is wrong'))
					return redirect('settingsC')
			if name != ob.customer_name:
				ob.customer_name = name
				counter+=1
			if email != ob.customer_email:
				ob.customer_email = email
				counter+=1
			if phone != ob.customer_phone:
				ob.customer_phone = phone
				counter+=1
			if address != ob.customer_address:
				ob.customer_address = address
				counter+=1
		if counter > 0:
			ob.save()
			messages.success(request, ('Profile Changes has been Saved Successfully'))
			return redirect('loginCustomer')
		else:
			return redirect('loginCustomer')

def prescript(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		return render(request, 'prescript.html', {})