from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from .models import Robot
from .utils import send_notification_email


@receiver(post_save, sender=Robot)
def robot_created(sender, instance, created, **kwargs):
    if created:
        ''' Ищем заказы на созданный робот. Если заказы на робот были, то отправляем всем заказавшим сообщения'''
        matching_orders = Order.objects.filter(robot_serial=instance.serial)
        if matching_orders.exists():
            for order in matching_orders:
                send_notification_email(order.customer.email, instance)
