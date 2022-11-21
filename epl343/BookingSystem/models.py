from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
#############################################################
#Galery code
class PhotoSection(models.Model):#subjects
    SectionName = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return self.SectionName
class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    belongs = models.ForeignKey(PhotoSection, on_delete=models.CASCADE)
###############################################################
# Testimonial models #################################################################
class Testimonial(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 20.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    author = models.CharField(max_length=60)
    author_school_and_year = models.CharField(max_length=255, null=True, blank=True)
    author_profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    author_profile_link = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    show = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)




# Teaching Experience models #################################################################
class Teaching_experience(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 20.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    title = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    associated_with = models.CharField(max_length=255, null=True, blank=True)
    association_pic = models.ImageField(null=True, blank=True, upload_to="images/") # this can lead to duplicate uploads
    description = models.TextField(null=True, blank=True)
    show = models.BooleanField(default=True)





# My User models #################################################################
class locations(models.TextChoices):
    from django.utils.translation import gettext_lazy as _
    NOT_SPECIFIED = 'NS', _('Not Specified')
    ONLINE = 'ON', _('Online')
    PUBLIC = 'PU', _('Public/Cafe')
    PRIVATE = 'PI', _('Private/Home')
    OTHER = 'OT', _('Other')
    TEACHER = 'NA', _('Not Available')


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
    TEACHER = 'NA', _('Not Available')


class payments(models.TextChoices):
    from django.utils.translation import gettext_lazy as _
    cash = 'c', _('Cash')
    Paypal = 'paypal', _('Paypal')
    card = 'card', _('Card')
    revolut = 'rev', _('Revolut')
    TEACHER = 'NA', _('Not Available')


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
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    # username = models.CharField(
    #     verbose_name='username', max_length=100, default='TestUser', unique=True)
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    first_name = models.CharField(
        verbose_name='first_name', max_length=255, default='Please add first name')
    last_name = models.CharField(
        verbose_name='last_name', max_length=255, default='Please add last name')
    preferred_loc = models.CharField(
        verbose_name='preferred_loc', max_length=255, choices=locations.choices, default=locations.NOT_SPECIFIED)
    year = models.CharField(
        verbose_name='year', max_length=255, choices=years.choices, default=years.one)
    pay = models.CharField(verbose_name='pay', max_length=255,
                           choices=payments.choices, default=payments.cash)
    is_student = models.BooleanField(verbose_name='is_student', default=False)
    USERNAME_FIELD = 'email'
    # Username & Password are required by default.
    REQUIRED_FIELDS = ['first_name', 'last_name']

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



# Booking System models #################################################################
class Appointment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    description = models.TextField(blank=False, default="")
    issued_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    location = models.CharField(
        verbose_name='preferred_loc', max_length=255, choices=locations.choices, default=locations.NOT_SPECIFIED)
    payment_method = models.CharField(verbose_name='pay', max_length=255,
                           choices=payments.choices, default=payments.cash)
    duration = models.DurationField(blank=False)
    start_dateTime = models.DateTimeField(primary_key= True, default=datetime.now())
    end_dateTime = models.DateTimeField(blank=False, default=datetime.now())

    # not sure if this is correct
    def save(self, *args, **kwargs):
        self.end_dateTime = self.start_dateTime + self.duration
        super().save(*args, **kwargs)


class Schedule(models.Model):  # working hours
    Day = models.IntegerField()  # 0-6
    Opening = models.TimeField()  
    Closing = models.TimeField() 

class Offs (models.Model): # day offs interval
    start_dateTime = models.DateTimeField()
    end_dateTime = models.DateTimeField()

    class Meta :
        unique_together = (('start_dateTime', 'end_dateTime'),)
