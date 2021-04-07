from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.hashers import make_password

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

class User1(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=100, null=True, unique= True)
	email = models.EmailField(max_length=100, unique= True)
	first_name = models.CharField(max_length=100, null=True)
	last_name = models.CharField(max_length=100, null=True)
	# addressLine = models.CharField(max_length=100, null=True)
	# city = models.CharField(max_length=100, null=True)
	# zipcode = models.CharField(max_length=100, null=True)
	# country = models.CharField(max_length=100, null=True)
	# state = models.CharField(max_length=100, null=True)
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


class Product(models.Model):
	# TAXRULE = (
	# 	('No tax', 'No tax'), 
	# 	('Tax (9%)', 'Tax (9%)'),
	# 	('Tax (12%)', 'Tax (12%)'),
	# 	('Tax (15%)', 'Tax (15%)'),
	# 	('Tax (18%)', 'Tax (18%)'),
	# )
	image = models.ImageField(null=True,blank=True)
	name = models.CharField(max_length=100, null=True)
	# reference = models.CharField(max_length=100, null=True)
	# category =  models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
	price = models.IntegerField(null=True)
	slug = models.SlugField(blank=True, null=True)
	# taxexcl =  models.IntegerField(null=True)
	# taxincl = models.IntegerField(null=True)
	# taxrule = models.CharField(max_length=100, choices= TAXRULE,null=True)
	# quantity = models.IntegerField(null=True)
	status = models.CharField(max_length=6, default='Active')
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse("product", kwargs={
            'slug': self.slug
			})

class Order(models.Model):
	customer = models.ForeignKey(User1, on_delete=models.CASCADE,blank=True, null=True)
	# total = models.IntegerField(null=True)
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		# print(orderitems)
		d = 0
		for i in orderitems:
			d += i.product.price * i.quantity
			print(d)
		# total =  sum([i.get_total for i in orderitems])
		return d
	
	
	@property
	def get_item_total(self):
		orderitems = self.orderitem_set.all()
		return  sum([i.quantity for i in orderitems])
	
	def __str__(self):
		return str(self.id)
class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(null=True, default=0)
	status = models.CharField(max_length=6, default='Active')
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	# @proprety
	def get_total(self):
		return self.product.price * self.quantity

class Shipping(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	customer = models.ForeignKey(User1, on_delete=models.CASCADE, null=True)
	address = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100, null=True)
	zipcode = models.CharField(max_length=100, null=True)
	country = models.CharField(max_length=100, null=True)
	state = models.CharField(max_length=100, null=True)
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.address
