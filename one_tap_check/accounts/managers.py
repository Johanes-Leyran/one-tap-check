from django.contrib.auth.base_user import BaseUserManager


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
    
    def create_staff_user(self, email, password=None, is_teacher=False, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_teacher", is_teacher)
        
        return self.create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_teacher", True)
        extra_fields.setdefault("is_student", True)
        
        if extra_fields['is_staff'] is not True:
            raise ValueError("Superuser must be is_staff=True")
        if extra_fields['is_superuser'] is not True:
            raise ValueError("Superuser must be is_superuser=True")
        if extra_fields['is_teacher'] is not True:
            raise ValueError("Superuser must be is_teacher=True")

        return self.create_user(email, password, **extra_fields)
