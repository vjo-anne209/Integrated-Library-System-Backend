from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Memberuser, Fine

def  member_profile(sender, instance, created, **kwargs):
	if created:
		Memberuser.objects.create(
			user=instance,
			user_id = instance.id,
			username=instance.username,
			memberpassword = instance.password,
			)
		member = Memberuser.objects.get(user_id = instance.id)
		Fine.objects.create(memberid = member)
		print('Profile created!')

post_save.connect(member_profile, sender=User)