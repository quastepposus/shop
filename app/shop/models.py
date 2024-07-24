from django.db import models

from shop.validators import more_than_zero


class Product(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Title")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Description")
    image = models.CharField(null=False, blank=False, verbose_name="Image")
    choices = (('drinks', 'Drinks'), ('meat', 'Meat'), ('frozen', 'Frozen'), ('food', 'Food'), ('drinks', 'Drinks'))
    category = models.CharField(max_length=200, default="Other", choices=choices,
                                null=False, blank=False, verbose_name="Category")
    count = models.IntegerField(default=0, null=False, blank=False,
                                verbose_name="Count", validators=(more_than_zero, ))
    price = models.DecimalField(null=False, blank=False, max_digits=9,
                                decimal_places=2, verbose_name="Price", validators=(more_than_zero, ))

    def __int__(self):
        return self.price

    def __str__(self):
        return self.title


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    count = models.IntegerField(default=1, null=False, blank=False,
                                verbose_name="Count", validators=(more_than_zero, ))
    total = models.DecimalField(null=True, blank=True, max_digits=12,
                                decimal_places=2, verbose_name="Total", validators=(more_than_zero, ))
    is_deleted = models.BooleanField(default="False", verbose_name='Is Deleted')

    def __str__(self):
        return self.product.title

    def __int__(self):
        return self.count


class Order(models.Model):
    products = models.ManyToManyField(ShoppingCart, related_name='orders', verbose_name='Products', blank=True,
                                      through='ShoppingCartForOrder', through_fields=('order', 'product'))

    user = models.CharField(null=False, blank=False, verbose_name='User')
    phone = models.CharField(null=False, blank=False, verbose_name='Phone')
    address = models.CharField(null=False, blank=False, verbose_name='Address')

    date = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    def __str__(self):
        return f'{self.user}, {self.phone}, {self.address}'


class ShoppingCartForOrder(models.Model):
    product = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, verbose_name="Product")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    is_deleted = models.BooleanField(default="False", verbose_name='Is Deleted')



