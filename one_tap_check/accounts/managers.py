from django.contrib.auth.base_user import BaseUserManager
# Todo: add feature to authenticate the rfid card of the user
# TODO: make the manager implements custom permissions


class OneTapUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_student_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_student", True)
        
        return self.create_user(email, password, **extra_fields)
    
    def create_staff_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        
        return self.create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields['is_superuser'] is not True:
            raise ValueError("Superuser must be is_superuser=True")

        return self.create_user(email, password, **extra_fields)
