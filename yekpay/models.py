# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from hashid_field import HashidField

from .config import CURRENCY_CHOICES, TRANSACTION_STATUS_CHIOCES, YEKPAY_START_GATEWAY
from .exceptions import *
from .managers import TransactionManager


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    authority_start = models.CharField(max_length=100,blank=True,null=True) #by module
    authority_verify = models.CharField(max_length=100,blank=True,null=True) #by module
    description = models.TextField()
    callback_url = models.CharField(max_length=100)
    from_currency_code = models.CharField(max_length=4, choices= CURRENCY_CHOICES, default='EUR')
    to_currency_code = models.CharField(max_length=4, choices= CURRENCY_CHOICES, default= 'EUR')
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    mobile = models.CharField(max_length=225)

    order_number = HashidField(
        allow_int_lookup=True,
        blank=True,
        null=True
    )
    address = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    postal_code= models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) #by module
    status = models.CharField(max_length=100,choices= TRANSACTION_STATUS_CHIOCES) # by module
    failure_reason = models.CharField(max_length=100,blank=True,null=True) # by module
    simulation = models.BooleanField(default=False)
    objects = TransactionManager()

    def __repr__(self):
        return '<yekpay id:{0}>'.format(self.order_number)

    def __str__(self):
        return "yekpay: {0}".format(self.order_number)

    def get_transaction_start_url(self):
        if self.simulation is True:
            return YEKPAY_START_GATEWAY + self.authority_start
        else:
            return reverse(
                'yekpay:sandbox-payment',
                kwargs={
                    'authority_start': self.authority_start
                }
            )
    
    def get_client_callback_url(self):
        if self.callback_url:
            return self.callback_url + f'?orederNumber={self.callback_url}'
        else:
            raise CallbackUrlNotProvided(
                f"Callback url is not set in transaction with order number {self.order_number.hashid}"
            )
