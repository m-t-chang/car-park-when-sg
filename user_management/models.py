from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have a valid email.')

        # normalize_email makes it all lowercase
        user = self.model(email=self.normalize_email(email),
                          name="",
                          surname="")
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.name = ""
        user.surname = ""
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True, null=False)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    # note: these 4 boolean fields are NEEDED for Django's admin system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # my field
    is_subscriber = models.BooleanField(default=False)

    # this says, when creating Account, use the AccountManager()
    objects = AccountManager()

    # override the username field, used for logging in
    USERNAME_FIELD = 'email'

    # this function returns what will be printed out when you do print(CLASS)
    # defines a string representation of the class
    def __str__(self):
        return f'{self.surname}, {self.name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
