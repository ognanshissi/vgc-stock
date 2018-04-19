from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from account.models import Profile
from .utils import reference_generator
from django.conf import settings
from django.core.mail import send_mail


class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lens:types-list')


class Product(models.Model):
    VALUE_CHOICES = (
        ('N', 'Négatif'),
        ('P', 'Positif')
    )
    LENS_TYPE_CHOICES = (
        ('SF + PH + AR', 'Simple Foyer Photogray Anti-Reflet'),
        ('DFB', 'Double Foyer Blanc'),
        ('SFB', 'Simple Foyer Blanc'),
        ('DF + PH + AR', 'Double Foyer Photogray Anti-Reflet'),
        ('PB', 'Progressif Blanc'),
        ('P + PH + AR', 'Progressif Photogray Anti-Reflet'),
    )
    reference = models.CharField(max_length=255, null=True, blank=True, unique=True)
    # type = models.CharField(max_length=25, choices=LENS_TYPE_CHOICES)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    sphere = models.FloatField(default=0.00, null=True, blank=True)
    cylindre = models.FloatField(default=0.00, null=True, blank=True)
    axe = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    addition = models.PositiveSmallIntegerField(null=True, blank=True, default=0.00)
    in_stock = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.reference)

    @property
    def sphere_text(self):
        if self.sphere:
            if self.sphere > 0.00:
                return "+{}".format(self.sphere)
            return self.sphere
        else:
            return "0.00"

    @property
    def axis(self):
        if self.axe:
            return "Axe: {}°".format(self.axe)
        else:
            return ''

    @property
    def cylindre_text(self):
        if self.cylindre:
            if self.cylindre > 0.00:
                return "+{}".format(self.cylindre)
            return self.cylindre
        else:
            return "0.00"

    @property
    def add_text(self):
        if self.addition:
            return "ADD +{}".format(self.addition)
        else:
            return ""


def pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.reference is None:
        instance.reference = reference_generator(instance)


pre_save.connect(pre_save_receiver, sender=Product)


class Entry(models.Model):
    provider = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField()
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} paire on été ajouté dans le stock".format(self.qty)

    class Meta:
        ordering = ['-entry_date']


    @property
    def addition(self):
        if self.product.addition:
            return "+ {}".format(self.product.addition)
        else:
            return "Sans addition"


class Exit(models.Model):
    provider = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField()
    exit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-exit_date']

    @property
    def addition(self):
        if self.product.addition:
            return "+ {}".format(self.product.addition)
        else:
            return "Sans addition"


class Stock(models.Model):

    WARNING = (100, 200)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField()

    def __str__(self):
        return "Il y a {0} paire de {1} en stock".format(self.qty, self.product.reference)

    @property
    def addition(self):
        if self.product.addition:
            return "+ {}".format(self.product.addition)
        else:
            return "Sans addition"


def entry_update_stock_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qty_ = instance.qty
        qs = Stock.objects.filter(product=instance.product)
        pd = Product.objects.filter(pk=instance.product.pk)
        if pd.exists() and pd.count() == 1:
            prod = pd.first()
            prod.in_stock = True
            prod.save()
        if qs.exists() and qs.count() == 1:
            stck = qs.first()
            stck.qty = stck.qty + qty_
            stck.save()
        else:
            Stock.objects.create(product=instance.product, qty=qty_)


post_save.connect(entry_update_stock_receiver, sender=Entry)


def exit_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qty_ = instance.qty
        qs = Stock.objects.filter(product=instance.product)
        if qs.exists() and qs.count() == 1:
            print(qs.first)
            stck = qs.first()
            stck.qty = stck.qty - qty_
            if stck.qty <= 0.0:
                pd = Product.objects.filter(pk=stck.product.pk)
                if pd.exists() and pd.count() == 1:
                    prod = pd.first()
                    prod.in_stock = False
                    prod.save()
            # check for less quantity in the stock and send email
            stck.save()
            # if stck.qty <= settings.PRODUCT_LESS_VALUE:
            #     send_mail(
            #         'Subject here',
            #         'Here is the message.',
            #         'from@example.com',
            #         ['to@example.com'],
            #         fail_silently=False,
            #     )
                # check for less quantity in the stock and send email


post_save.connect(exit_post_save_receiver, sender=Exit)