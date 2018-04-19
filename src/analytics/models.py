from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db.models.signals import pre_save, post_save

from .utils import get_client_ip
from .signals import user_logged_in_signal, user_logged_out_signal

User = get_user_model()


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.CharField(max_length=200, null=True, blank=True)
    session_key = models.CharField(max_length=150, null=True, blank=True)
    user_agent = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)
    ended_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.ended_at = timezone.now()
        except:
            pass
        return self.ended
    
    def __str__(self):
        return "%s is logged in on %s" %(self.user, self.timestamp)


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(pk=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()


post_save.connect(post_save_session_receiver, sender=UserSession)
    
    
def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    ip_address = get_client_ip(request)
    session_key = request.session.session_key  
    
    UserSession.objects.create(
        user=instance,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in_signal.connect(user_logged_in_receiver)

# def user_logged_out_receiver(sender, instance, request, *args, **kwargs):
#     ip_address = get_client_ip(request)
#     session_key = request.session.session_key

