from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from sorl.thumbnail import ImageField


# here there is an option to add customized fields for the user
class User(AbstractUser):
    age = models.PositiveSmallIntegerField()
    avatar = ImageField()

    def save(self, *args, **kwargs):
        created = self.id is None
        super(User, self).save(*args, **kwargs)
        if created:
            group = Group.objects.get(name='common users')
            self.groups.add(group)
            self.save()


class Profile(models.Model):
    """
    This is the Profile with the connection
    one to one which prevents us to create multiple profiles for one user.
    """

    user = models.OneToOneField(User, models.CASCADE)
    avatar = ImageField()
    nickname = models.CharField(max_length=20)
