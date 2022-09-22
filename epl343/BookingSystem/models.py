from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models

    
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name, last_name, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,

            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=100, default='TestUser', unique=True)
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    class locations(models.TextChoices):
        from django.utils.translation import gettext_lazy as _
        ONLINE = 'ON', _('Online')
        PUBLIC = 'PU', _('Public/Cafe')
        PRIVATE = 'PI', _('Private/Home')
        OTHER = 'OT', _('Unknown')

    class years(models.TextChoices):
        from django.utils.translation import gettext_lazy as _
        one = 'one', _('1')
        two = 'two', _('2')
        three = 'three', _('3')
        four = 'four', _('4')
        five = 'five', _('5')
        six = 'six', _('6')
        six_plus = 'six_p', _('6+')
        other = 'OT', _('Other')

    class payments(models.TextChoices):
        from django.utils.translation import gettext_lazy as _
        cash = 'c', _('Cash')
        Paypal = 'paypal', _('Paypal')
        card = 'card', _('Card')
        revolut = 'rev', _('Revolut')
    
    first_name = models.CharField(verbose_name='first_name', max_length=255, default='Please add first name')
    last_name = models.CharField(verbose_name='last_name', max_length=255, default='Please add last name')
    preferred_loc = models.CharField(verbose_name='preferred_loc', max_length=255, choices=locations.choices, default=locations.PRIVATE)
    year = models.CharField(verbose_name='year', max_length=255, choices=years.choices, default=years.one)
    pay = models.CharField(verbose_name='pay', max_length=255, choices=payments.choices, default=payments.cash)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Username & Password are required by default.

    objects = MyUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
