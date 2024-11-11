from django.db import models
from django.contrib.auth.models import User 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.user.username}'s profile"


class FaceImage(models.Model):
    image_name = models.CharField(max_length=255)
    image_data = models.BinaryField()

    def __str__(self):
        return self.image_name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('3c_digital', '3C数码'),
        ('clothing', '服装百货'),
        ('supermarket', '生活超市'),
    ]
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='details')
    banner_image = models.ImageField(upload_to='products/details/', blank=True, null=True)
    title = models.CharField(max_length=255)
    description_image = models.ImageField(upload_to='products/details/', blank=True, null=True)
    price_text = models.CharField(max_length=255)

    def __str__(self):
        return f"Details for {self.product.name}"

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

class Photo(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
