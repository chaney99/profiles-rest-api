from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """

    def create_user(self, email, name, password=None):
        """ Create a new user profile """
        """ password = None will force Django to request one if there is not one """
        if not email :
            raise ValueError ( "Users must have an email address")

        # Make sure email domain is lowercase
        email = self.normalize_email(email)
        user = self.mode(email= email, name= name)

        # Password needs to be stored as a hash
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser ( self, email, name, password ) :
        """ Create and save a new superuser with given details """
        """ password not existing is a no-go here """
        """ is_superuser is automatically created from PermissionsMixin """

        user = self.create_user(email, name, password )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


# He is overwritting the default user class to have email=name

class UserProfile(AbstractBaseUser, PermissionsMixin) :
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True )
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Retrieve full name of user """
        return self.name

    def get_short_name(self):
        """ Retrieve short name of user """
        return self.name

    def __str__(self):
        """ Retrieve string representation of our user """
        return self.email
