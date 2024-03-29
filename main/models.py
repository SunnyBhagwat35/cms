from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, BaseUserManager

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


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




class CmsUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=10, null=False)
    address = models.TextField(null=True)   
    city = models.CharField(max_length=60, null=True)
    state = models.CharField(max_length=60, null=True)
    country = models.CharField(max_length=60, null=True)
    pincode = models.CharField(max_length=6, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email



class Content(TimeStampMixin):
    user = models.ForeignKey(CmsUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=False)
    body = models.CharField(max_length=300, null=False)
    summary = models.CharField(max_length=60, null=False)
    doc = models.FileField(blank=False)
    category = models.CharField(max_length=100)

    def __str__(self) :
        return self.title