from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Профиль пользователя"""

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name="Аватар", upload_to='images/lms/userprofile/', blank=True, null=True)
    # coins

# class History()
#     owner = User

    # https://www.youtube.com/watch?v=MFkfi9yy_Ts&t=2756s
    # https://github.com/glebmikha/django-rest-framework-bank/tree/master/web/app/bank

    # https://github.com/F4R4N/shop-django-rest-framework