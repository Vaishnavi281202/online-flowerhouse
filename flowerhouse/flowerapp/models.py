from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models

class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    fragrance = models.CharField(max_length=100)
    image = models.ImageField(upload_to='flower_images/', null=True, blank=True)
    isAvail = models.BooleanField(default=True)  # Added availability status

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField() 
    phno = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customerid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    flowerid = models.ForeignKey(Flower, on_delete=models.CASCADE)
    orderdate = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    status = models.TextField()

    def __str__(self):
        return f"Order {self.id} by {self.customerid.name}"

class PaymentType(models.Model):
    name = models.CharField(max_length=25, null=False)

    def __str__(self):
        return self.name

class Payment(models.Model):
    orderid = models.OneToOneField(Order, on_delete=models.CASCADE)  # One payment per order
    paymentmethod = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True)
    status = models.TextField(default="Pending")
    transactionid = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Payment for Order {self.orderid.id}"
    

class delivery_staff(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.IntegerField()
    salary=models.IntegerField()
    joining_date=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=20)
    dob=models.CharField(max_length=100)
  


    def __str__(self):
        return self.name



class delivery(models.Model):
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    delivery_staff_id=models.ForeignKey(delivery_staff,on_delete=models.CASCADE,null=True)
    start_delivery=models.DateTimeField()
    delivered_datetime=models.DateTimeField()

    def __str__(self):
        return self.order_id



# **Signal to Create Payment Automatically**
@receiver(post_save, sender=Order)
def create_payment(sender, instance, created, **kwargs):
    if created:
        Payment.objects.create(orderid=instance, paymentmethod=PaymentType.objects.first(), status="Pending")