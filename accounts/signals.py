from .models import MyUser, Otp
from .sms import send_sms
from django.db.models import signals
from django.dispatch import receiver

@receiver(signals.post_save, sender=MyUser)
def create_MyUser(sender, instance, created, **kwargs):
    # if created and instance.phone_number:
    print("hello")
    otp = Otp.objects.create(user = instance)
    print(otp)
    


@receiver(signals.post_save, sender=Otp)
def created_sms(sender, instance, created, **kwargs):
    if created:
        send_sms(instance.user.phone_number, instance.code)
    

    
