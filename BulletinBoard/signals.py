from django.template.loader import render_to_string

from django.conf import settings

from .models import Advert, User

from django.db.models.signals import post_save

from django.core.mail import EmailMultiAlternatives

from django.dispatch import receiver

from datetime import datetime


@receiver(post_save, sender=Advert)
def notify_advert_create(instance, created, **kwargs):
    if created:
        subject = f"'{instance.createTime.strftime('%H:%M:%S')} {instance.createTime.strftime('%d-%m-%Y')}: User: '{instance.author}' created a new advert"
    else:
        subject = f"'{datetime.now().strftime('%H:%M:%S')} {datetime.now().strftime('%d-%m-%Y')}: User: '{instance.author}' changed the Post"
    
    users = User.objects.filter()
    for user in users: 
        html_content = render_to_string(
            'BulletinBoard/advert_created_email.html',
            {
                'title': instance.preview(),
                'author': instance.author,
                'link': f"{settings.SITE_URL}/advert/{instance.pk}",
                'category': f"{instance.category}",
            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
