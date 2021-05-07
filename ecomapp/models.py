from django.db import models
import random
import os

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.hashers import make_password

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ecomapp import signals


def get_file_extension(filepath):
    basename = os.path.basename(filepath)
    name, ext = basename.split('.')
    return name, ext

def upload_file_path(instance, filename):
    new_filename = random.randint(1, 464654165)
    name, ext = get_file_extension(filename)
    final_filename = f'{new_filename}.{ext}'
    return f'products/{new_filename}/{final_filename}'

class UserManager(BaseUserManager):

	def create_user(self, email, username, password=None):
		"""Create a User """
		if not email :
			raise ValueError('User must have an Email Address')

		email = self.normalize_email(email)
		user = self.model(email=email ,username=username)
		# password = make_password(password)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):

		user = self.create_user(email, username, password)
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=100, null=True, unique= True)
	email = models.EmailField(max_length=100, unique= True)
	first_name = models.CharField(max_length=100, null=True)
	last_name = models.CharField(max_length=100, null=True)
	# addressLine = models.CharField(max_length=100, null=True)
	# city = models.CharField(max_length=100, null=True)
	# zipcode = models.CharField(max_length=100, null=True)
	# country = models.CharField(max_length=100, null=True)
	# state = models.CharField(max_length=100, null=True)
	is_forget = models.BooleanField(default = False) 
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)

	objects = UserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	
	def get_full_name(self):
		return self.name

	def __str__(self):
		return self.email


	def has_module_perms(self, app_label):
		return True

class Category(models.Model):
	name = models.CharField(max_length=100, null=True)
	status = models.CharField(max_length=6, default='Active')
	parent = models.ForeignKey('self',blank=True, null=True,related_name='child', on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	# TAXRULE = (
	# 	('No tax', 'No tax'), 
	# 	('Tax (9%)', 'Tax (9%)'),
	# 	('Tax (12%)', 'Tax (12%)'),
	# 	('Tax (15%)', 'Tax (15%)'),
	# 	('Tax (18%)', 'Tax (18%)'),
	# )
	image = models.ImageField(upload_to=upload_file_path, null=True)
	name = models.CharField(max_length=100, null=True)
	# reference = models.CharField(max_length=100, null=True)
	category =  models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
	price = models.IntegerField(null=True)
	slug = models.SlugField(blank=True, null=True)
	# taxexcl =  models.IntegerField(null=True)
	# taxincl = models.IntegerField(null=True)
	# taxrule = models.CharField(max_length=100, choices= TAXRULE,null=True)
	# quantity = models.IntegerField(null=True)
	views = models.IntegerField(null=True, blank=True, default=0)
	status = models.CharField(max_length=6, default='Active')
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse("product", kwargs={
            'slug': self.slug
			})


PAYMENT = (
	("Debit Cart", "Debit Cart"),
	("Credit Cart", "Credit Cart"),
	("Cash On Delivery", "Cash On Delivery"),
)
class Shipping(models.Model):
	# order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	address = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100, null=True)
	zipcode = models.CharField(max_length=100, null=True)
	country = models.CharField(max_length=100, null=True)
	phoneNo = models.IntegerField(null=True,blank=True)
	payment = models.CharField(max_length=100,default='Cash on Delivery', choices=PAYMENT)
	state = models.CharField(max_length=100, null=True)
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.address

class Cart(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
	# payment = models.CharField(max_length=100, null=True)
	# address = models.ForeignKey(Shipping, on_delete=models.CASCADE,blank=True, null=True)
	# product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	is_completed = models.BooleanField(default=False, null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		# print(orderitems)
		d = 0
		for i in orderitems:
			if self.is_completed == False:
				d += i.product.price * i.quantity
		# total =  sum([i.get_total for i in orderitems])
		return d

	@property
	def get_item_total(self):
		orderitems = self.orderitem_set.all()
		cart = 0
		for j in orderitems:
			if self.is_completed == False:
				cart = sum([i.quantity for i in orderitems])
		return cart
	
	# def __str__(self):
	# 	return str(self.id)
class OrderItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(null=True, default=0)
	# is_completed = models.BooleanField(default=False, null=True, blank=True)
	status = models.CharField(max_length=6, default='Active')
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	# @property
	# def get_cart_total(self):
	# 	orderitems = self.order_set.all()
	# 	# print(orderitems)
	# 	d = 0
	# 	for i in orderitems:
	# 		if i.is_completed == False:
	# 			d += self.product.price * self.quantity
	# 	# total =  sum([i.get_total for i in orderitems])
	# 	return d

	# @property
	# def get_item_total(self):
	# 	orderitems = self.order_set.all()
	# 	cart = 0
	# 	for j in orderitems:
	# 		if j.is_completed == False:
	# 			cart = sum([self.quantity for i in orderitems])
	# 	return cart


	# @proprety
	def get_total(self):
		return self.product.price * self.quantity
class Order(models.Model):
	def increment_order_number():
		last_orderNo = Order.objects.all().order_by('id').last()
		if not last_orderNo:
		     return 'XXX0001'
		orderNo = last_orderNo.orderNo
		invoice_int = int(orderNo.split('XXX')[-1])
		width = 4
		new_invoice_int = invoice_int + 1
		formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
		new_order_no = 'XXX' + str(formatted)
		return new_order_no
	# orderNo = models.CharField(max_length=100, null=True)
	orderNo = models.CharField(max_length=500, default=increment_order_number, null=True, blank=True)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
	total = models.IntegerField(null=True, default=0)
	method = models.CharField(max_length=100, null=True)
	address = models.ForeignKey(Shipping, on_delete=models.CASCADE, null=True)
	status = models.CharField(max_length=6, default='Active')
	created_on = models.DateTimeField(auto_now_add=True, null=True)




	




# ----------------------
class ProductViewed(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address      = models.CharField(max_length=220, null=True, blank=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_object}"[:20]#" : - Viewed on {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

class Track(models.Model):
	customer= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	order= models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
	ordered= models.CharField(max_length=100, null=True, blank=True, default="active")
	packed= models.CharField(max_length=100, null=True, blank=True)
	shipped= models.CharField(max_length=100, null=True, blank=True)
	delivery= models.CharField(max_length=100, null=True, blank=True)
	status = models.CharField(max_length=100, null=True, blank=True, default="Ordered Confirmed")

	def __str__(self):
		return self.order.orderNo

def product_viewed_signal_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    user = None
    if request.user.is_authenticated:
        user = request.user
    new_object_view_object = ProductViewed.objects.create(
        user = user,
        ip_address = request.META.get('REMOTE_ADDR', None),
        content_type = c_type,
        object_id = instance.id,
    )

signals.product_viewed_signal.connect(product_viewed_signal_receiver)
