from django.core.exceptions import ValidationError

from .import models


def is_admin_validator(user_in):
    user = models.User.objects.get(id=user_in)
    if user.is_admin:
        return user_in
    else:
        raise ValidationError('User is not an admin')
