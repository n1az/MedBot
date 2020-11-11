from django.db import models


class Employee(models.Model):
	pharmacy_id = models.BigAutoField(primary_key = True)
	pharmacy_address = models.CharField(max_length = 254)
	owner_name = models.CharField(max_length = 100)
	pharmacy_name = models.CharField(max_length = 100)
	pharmacy_reg_id = models.CharField(max_length = 100)
	employee_password = models.CharField(max_length = 100)
	pharmacy_rating = models.FloatField(max_length=3, null=True)
	pharmacy_rating_count = models.PositiveIntegerField(default = 0)
	employee_email = models.EmailField(max_length = 254)
	employee_phone = models.CharField(max_length = 15)
	employee_longT = models.CharField(max_length = 20, default= "90.40")
	employee_latiT = models.CharField(max_length = 20, default= "20.40")

	def __str__(self):
		return self.pharmacy_name

class Inventory(models.Model):
	"""docstring for Inventory"""
	MUSTPRESCRIBED = 'MP'
	MUSTNOTPRESCRIBE = 'MNP'
	MEDICINESTATUS = [
		(MUSTPRESCRIBED, 'Must be Prescribed'),
		(MUSTNOTPRESCRIBE, 'Must not be Prescribed'),
	]

	GENERAL = 'A'
	BLOOD = 'B'
	DIGESTIVE = 'D'
	EYE = 'F'
	EAR = 'H'
	CIRCULATORY = 'K'
	MUSCULOSKELETAL = 'L'
	NEUROLOGICAL = 'N'
	PSYCHOLOGICAL = 'P'
	RESPIRATORY = 'R'
	SKIN = 'S'
	ENDORCRINE = 'T'
	UROLOGY = 'U'
	PREGNANCY = 'W'
	FEMALEGENITAL = 'X'
	MALEGENITAL = 'Y'
	SOCIALPROB = 'Z'


	MEDICINECATAGORIES = [
		(GENERAL, 'General and unspecified'),
		(BLOOD, 'Blood, blood forming organs, lymphatics, spleen'),
		(DIGESTIVE, 'Digestive'),
		(EYE, 'Eye'),
		(EAR, 'Ear'),
		(CIRCULATORY, 'Circulatory'),
		(MUSCULOSKELETAL, 'Musculoskeletal'),
		(NEUROLOGICAL, 'Neorological'),
		(PSYCHOLOGICAL, 'Psychological'),
		(RESPIRATORY, 'Respiratory'),
		(SKIN, 'Skin'),
		(ENDORCRINE, 'Endocrine, metabolic and nutritional'),
		(UROLOGY, 'Urology'),
		(PREGNANCY, 'Pregnancy, childbirth, family planning'),
		(FEMALEGENITAL, 'Female genital system and breast'),
		(MALEGENITAL, 'Male genital system'),
		(SOCIALPROB, 'Social problems'),
	]
			
	med_name = models.CharField(max_length = 200)
	med_id = models.BigAutoField(primary_key = True, serialize=False)
	med_price = models.FloatField(max_length = 10)
	med_quantity = models.PositiveIntegerField()
	med_status = models.CharField(max_length = 3, choices = MEDICINESTATUS, default=MUSTPRESCRIBED)
	med_catagory = models.CharField(max_length = 2, choices = MEDICINECATAGORIES, default = GENERAL)
	med_generic = models.CharField(max_length = 100)
	pharmacy_id = models.ForeignKey(Employee, on_delete = models.CASCADE)

	def is_upperclass(self):
		return self.year_in_school in {self.MUSTPRESCRIBED, self.MUSTNOTPRESCRIBE}

	def __str__(self):
		return self.med_name

class Customer(models.Model):
	customer_name = models.CharField(max_length = 100)
	customer_id = models.BigAutoField(primary_key = True, serialize = False)
	birthdate = models.DateField()
	customer_address = models.CharField(max_length = 254)
	customer_password = models.CharField(max_length = 100)
	customer_email = models.EmailField(max_length = 254)
	customer_phone = models.CharField(max_length = 15)
	customer_longT = models.CharField(max_length = 20, default= "90.40")
	customer_latiT = models.CharField(max_length = 20, default= "20.40")

	def __str__(self):
		return self.customer_name

class Delivery(models.Model):
	DS_id = models.AutoField(primary_key = True)
	DS_start_time = models.TimeField()
	DS_stop_time = models.TimeField()
	DS_capacity = models.IntegerField(default = 15)
	DS_status = models.BooleanField(default = True)

	def __str__(self):
		return str(self.DS_id)

class Cart(models.Model):

	cart_id = models.BigAutoField(primary_key = True)
	pharmacy_id = models.ForeignKey(Employee, on_delete = models.CASCADE)
	customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
	adding_quantity = models.IntegerField(default= 5)
	med_id = models.ForeignKey(Inventory, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.cart_id)

class OrderedCart(models.Model):

	order_cart_id = models.BigAutoField(primary_key = True)
	pharmacy_id = models.ForeignKey(Employee, on_delete = models.CASCADE)
	customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
	adding_quantity = models.IntegerField(default= 5)
	med_id = models.ForeignKey(Inventory, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.order_cart_id)

class Order(models.Model):
	ONPROCESS = 'OP'
	ONTHEWAY = 'OTW'
	DELIVERED = 'DV'

	DELIVERYSTATUS = [
		(ONPROCESS, 'Processing'),
		(ONTHEWAY, 'On the way'),
		(DELIVERED, 'Medicine Delivered')
	]

	CASHONDELVRY = 'COD'
	BKASH = 'BKS'
	ROCKET = 'RKT'
	CARD = 'CRD'
	PAYPAL = 'PPL'

	PAYMENTOPTIONS = [
		(CASHONDELVRY, 'Cash On Delivery'),
		(BKASH, 'Bkash'),
		(ROCKET, 'Rocket'),
		(CARD, 'ATM Card'),
		(PAYPAL, 'PayPal')
	]

	order_id = models.BigAutoField(primary_key = True)
	order_date = models.DateTimeField(auto_now_add=True)
	pharmacy_id = models.ManyToManyField(Employee)
	customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
	delivery_id = models.ForeignKey(Delivery, on_delete = models.CASCADE)
	delivery_status = models.CharField(max_length = 3, choices = DELIVERYSTATUS, default = ONPROCESS)
	rating = models.IntegerField()
	order_quantity = models.IntegerField(default= 5)
	med_ids = models.ManyToManyField(Inventory)
	order_status = models.BooleanField(default=False)
	order_type = models.CharField(max_length = 3, choices = PAYMENTOPTIONS, default = CASHONDELVRY)
	delivery_note = models.CharField(max_length = 100, default = "Call me when you arrive")
	order_cost = models.CharField(max_length = 10, default = "10")
	order_longT = models.CharField(max_length = 20, default= "90.40")
	order_latiT = models.CharField(max_length = 20, default= "20.40")
	orered_cart = models.ManyToManyField(OrderedCart)

	def __str__(self):
		return str(self.order_id)




class Admin(models.Model):
	admin_name = models.CharField(max_length = 100)
	admin_password = models.CharField(max_length = 100)
	admin_id = models.AutoField(primary_key = True)
	admin_designation = models.CharField(max_length = 50)
	admin_phone = models.CharField(max_length = 15)
	admin_email = models.EmailField(max_length = 254)

	def __str__(self):
		return self.admin_name
		
class Prescription(models.Model):
	pres_id = models.BigAutoField(primary_key = True)
	customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
	pres_status = models.BooleanField(default=False)
	order_id = models.ForeignKey(Order, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.pres_id)

class Coupon(models.Model):
	coupon_id = models.BigAutoField(primary_key = True)
	coupon_code = models.CharField(max_length = 10)
	coupon_amount = models.IntegerField()
	med_id = models.ForeignKey(Inventory, on_delete = models.CASCADE)

	def __str__(self):
		return self.coupon_code
