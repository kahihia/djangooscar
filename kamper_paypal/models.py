from django.db import models


class PaypalCheckoutTransaction(models.Model):
    payment_id = models.CharField(max_length=255)
    intent = models.CharField(max_length=20)
    state = models.CharField(max_length= 20)
    payment_method = models.CharField(max_length=20)

    transactions_total = models.CharField(max_length=20)
    transactions_description = models.TextField()
    transactions_custom = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=255)

    basket = models.ForeignKey()
    date_created = models.DateTimeField(auto_now_add=True)
    created_time = models.DateTimeField()

    user = models.ForeignKey()
    token = models.CharField(max_length=32, null=True, blank=True)


    class Meta:
        ordering = ('-date_created',)
        app_label = 'paypal'

    def save(self, *args, **kwargs):
        return super(PaypalCheckoutTransaction, self).save(*args, **kwargs)

    @property
    def is_successful(self):
        return self.ack in (self.SUCCESS, self.SUCCESS_WITH_WARNING)

    def __str__(self):
        return 'method: %s: token: %s' % (
            self.method, self.token)

# # paypal 웹훅으로 온 기록을 볼 수 있다
# class PaypalNotification(models.Model):
#     webhook_id
#     pass
