from django.db.models.signals import pre_delete, post_migrate
from django.dispatch import receiver
from .models import Account, Destination,Role


@receiver(pre_delete, sender=Account)
def delete_related_destinations(sender, instance, **kwargs):
    Destination.objects.filter(account=instance).delete()


# Signal to create roles automatically after migrations
@receiver(post_migrate)
def create_roles(sender, **kwargs):
    # Check if roles already exist before creating them
    if not Role.objects.filter(role_name='Admin').exists():
        Role.objects.create(role_name='Admin')

    if not Role.objects.filter(role_name='Normal user').exists():
        Role.objects.create(role_name='Normal user')
