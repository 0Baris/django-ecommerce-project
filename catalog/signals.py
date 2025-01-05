from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ProductImage, Slide

@receiver(post_delete, sender=ProductImage)
def delete_product_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

@receiver(post_delete, sender=Slide)
def delete_slide_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)