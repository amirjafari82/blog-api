from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None):
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, last_name, password=None):
        user = self.create_user(
            phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=11,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='First Name',
        max_length=20
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=20
    )
    is_active = models.BooleanField(default=True)
    is_vip = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name","last_name","password"]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)