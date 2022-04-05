from django.utils import timezone

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
# from product.models import Products

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **other_fields):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        user = self.model(
            email=self.normalize_email(email), name=name, **other_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password, **other_fields):
        """
        Creates and saves a staff user with the given email and password.
        """

        other_fields.setdefault("is_staff", True) 
        user = self.create_user(
            email,
            name,
            password=password,
            **other_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **other_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        other_fields.setdefault("is_active", True) 
        other_fields.setdefault("is_staff", True) 
        other_fields.setdefault('is_superuser', True)

        user = self.create_user(
            email,
            name,
            password=password,
            **other_fields
        )
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=150)
    created_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_superuser = models.BooleanField(default=False) # a superuser

    objects = UserManager()
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['name'] # Email & Password are required by default.

    def get_name(self):
        # The user is identified by their name
        return self.name

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

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.staff

    # @property
    # def is_admin(self):
    #     "Is the user a admin member?"
    #     return self.admin




# from product.models import Products

class Seller(AbstractBaseUser):
    shop_name = models.CharField(max_length=150)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # products = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)
    

    objects = UserManager()
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['shop_name', 'full_name', 'phone_number'] # Email & Password are required by default.

    def __str__(self):
        return self.email