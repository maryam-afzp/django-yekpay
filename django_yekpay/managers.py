from django.conf import settings
from django.db import models

from .exceptions import *

class TransactionManager(models.Manager):
    """ Manager for :class:`Transaction` """

    def create_transaction(self, transaction_data):
        transaction_data['status'] = 'PENDING'
        createdTransaction = self.create(**transaction_data)
        createdTransaction.orderNumber = createdTransaction.id
        createdTransaction.save(update_fields=['orderNumber'])
        return createdTransaction
