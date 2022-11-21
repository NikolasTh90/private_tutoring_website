from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.core.exceptions import ValidationError
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
    ONLINE = 'ON', _('Online')
    PUBLIC = 'PU', _('Public/Cafe')
    PRIVATE = 'PI', _('Private/Home')
    OTHER = 'OT', _('Unknown')
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
        verbose_name='preferred_loc', max_length=255, choices=locations.choices, default=locations.PRIVATE)
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
    request = models.TextField(blank=True)
    for_date = models.DateTimeField()
    sent_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)
    Duration = models.DurationField()


class MonthException(models.Model):
    # YearException = models.TextField()
    MonthException = models.TextField()


class DayMonthException(models.Model):
    MonthException = models.TextField()
    DayException = models.TextField()  # monos arithmos mpenei 0 mprosta panta


class DayException(models.Model):
    DayException = models.TextField()


# class ForDaysException(models.Model):
#     MonthException = models.TextField()
#     StartingTime = models.TimeField()
#     EndingTime = models.TimeField()


class TimeException(models.Model):  # na valw je mina
    Day = models.IntegerField()
    Opening = models.TimeField()  # : format :
    Closing = models.TimeField()  # : format


class Schedule(models.Model):  # subjects
    Day = models.IntegerField()  # 0-7
    Opening = models.TimeField()  # : format :
    Closing = models.TimeField()  # : format
