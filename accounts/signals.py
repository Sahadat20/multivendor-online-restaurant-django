
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)

def create_profile_receiver(sender,instance,created, **kwargs):
    # post save receiver of signals
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('User profile created ')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create uer profile if not exists
            UserProfile.objects.create(user=instance)

    