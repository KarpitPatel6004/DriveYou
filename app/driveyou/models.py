from django.db import models
from django.contrib.gis.db import models as geomodel
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from validators import validate_mobile_number, validate_date_travel_date

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    # Common fields for both client and driver
    phone = models.CharField(max_length=10, unique=True, validators=[validate_mobile_number])
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=10, validators=[validate_mobile_number])

    # Extra fields for drivers
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # location = geomodel.PointField(srid=4326)
    licence_verification_status = models.BooleanField(default=False)
    earnings = models.FloatField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    is_client = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    has_insurance = models.BooleanField(default=False)
    registration_number = models.CharField(max_length=20, unique=True)
    registration_date = models.DateField()
    registration_expiry_date = models.DateField()

class SearchRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_results')
    start_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_lat = models.DecimalField(max_digits=9, decimal_places=6)
    start_lon = models.DecimalField(max_digits=9, decimal_places=6)
    # start_point = geomodel.PointField(srid=4326)
    end_lat = models.DecimalField(max_digits=9, decimal_places=6)
    end_lon = models.DecimalField(max_digits=9, decimal_places=6)
    distance = models.FloatField()
    duration = models.FloatField()
    price = models.FloatField()
    user_travel_time = models.DateTimeField(validators=[validate_date_travel_date])
    search_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} - {self.start_location} to {self.destination} at {self.user_travel_time}'
