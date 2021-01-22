from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.db.models import Model
from django.db.models.signals import post_save






LABEL_CHOICES = [
    ('P', 'primary'),
    ('S', 'secondary'),
    ('O', 'other')

]

CATEGORY_CHOICES = [
    ('NW', 'New'),
    ('SH', 'Secondhand'),
    ('A', 'Accesories')
]




class Kind(models.Model):
    sign = models.CharField(max_length=50)
    dn = models.IntegerField()


    def get_all_kinds():
        return Kind.objects.all()

    def __str__(self):
        return self.sign

class Grinch(models.Model):
    name = models.CharField(max_length=50)

    def get_all_grinchs():
        return Grinch.objects.all()

    def __str__(self):
        return self.name



class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    kind = models.ForeignKey(Kind, on_delete=models.CASCADE, default=1)
    grinch = models.ForeignKey(Grinch, on_delete=models.CASCADE, default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    image = models.ImageField(upload_to='images_axuto')
    description = models.TextField(max_length=100)
    add_info = models.TextField(max_length=120)
    slug = models.SlugField()



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


    @staticmethod
    def get_all_items():
        return Item.objects.all()


    @staticmethod
    def get_all_items_by_kinddn(kind_dn):
        if kind_dn:
            return Item.objects.filter(kind=kind_dn)
        else:
            return Item.get_all_items()

    @staticmethod
    def get_items_by_id(ids):
        return Item.objects.filter(id__in=ids)

    @staticmethod
    def get_all_items():
        return Item.objects.all()

    @staticmethod
    def get_all_items_by_grinchid(grinch_id):
        if grinch_id:
            return Item.objects.filter(grinch=grinch_id)
        else:
            return Item.get_all_items()

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()




class Order(models.Model):

    user  = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
