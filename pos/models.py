from django.db import models
from datetime import datetime

# Create your models here.
from django.contrib.auth.models import User

#stock items models
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    model = models.CharField(max_length=30, unique=True)
    manufacturer = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name

#contains suppliers
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    nic = models.CharField(max_length=10, unique=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name

#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='purchasesupplier')

    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total

#contains the purchase stocks made
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

#contains the other details in the purchases bill
class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')

    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    acno = models.CharField(max_length=50, blank=True, null=True)

    add = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)



#contains the sale bills made
class SaleBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    nic = models.CharField(max_length=15)

    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)

    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total
    class Meta:
        ordering = ['nic']

#contains the sale stocks made
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

#contains the other details in the sales bill
class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='saledetailsbillno')

    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)


    add = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    birth_date = models.DateField(default=datetime.now, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    nic = models.CharField(max_length=10, unique=True)
    joined_date = models.DateField(default=datetime.now, blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name

class EmployeeAttendence(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name='employeeattendence')
    status = models.BooleanField(default=False)
