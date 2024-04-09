import hashlib
import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone=None, password=None, birthday=None):
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            birthday=birthday
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.CharField(verbose_name='email address', max_length=255, unique=True)
    phone = models.CharField(max_length=12, unique=True)
    birthday = models.CharField(max_length=10, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']


def new_file_name(instance, filename):
    if isinstance(instance, Album):
        base_path = 'albums/covers/'
        file_field = instance.cover
    elif isinstance(instance, Photo):
        base_path = 'albums/photos/'
        file_field = instance.image
    else:
        base_path = 'uploads/'
    file_content = file_field.file.read()
    hash_md5 = hashlib.md5(file_content).hexdigest()[:30]
    file_field.file.seek(0)
    _, ext = os.path.splitext(filename)
    new_filename = f'{hash_md5}{ext}'

    return os.path.join(base_path, new_filename)

class Album(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(upload_to=new_file_name, max_length=1000)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=new_file_name, max_length=1000)
    description = models.TextField(blank=True)
