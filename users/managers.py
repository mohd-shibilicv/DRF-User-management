from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, dob=None, mobile_number=None, profile_picture=None):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if not username:
            raise ValueError('Users must have a username')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, dob=dob, mobile_number=mobile_number, profile_picture=profile_picture)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(email=email, username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
