import hashlib
import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone=None, password=None, birthday=None):
        if not email:
            raise ValueError('Поле не может быть пустым')
        if phone is None:
            raise ValueError('Поле не может быть пустым')
        if not password:
            raise ValueError('Поле не может быть пустым')
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

class AlbumManager(models.Manager):
    def create_album(self, title, description, cover, user):
        if not title:
            raise ValueError('Поле не может быть пустым')
        if not description:
            raise ValueError('Поле не может быть пустым')
        if not cover:
            raise ValueError('Поле не может быть пустым')
        if not user:
            raise ValueError('Поле не может быть пустым')
        album = self.model(
            title=title,
            description=description,
            cover=cover,
            user=user
        )
        album.save()
        return album

class PhotoManager(models.Manager):
    def create_photo(self, album, image, description):
        if not album:
            raise ValueError('Поле не может быть пустым')
        if not image:
            raise ValueError('Поле не может быть пустым')
        photo = self.model(
            album=album,
            image=image,
            description=description
        )
        photo.save()
        return photo

class Album(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(upload_to=new_file_name, max_length=1000)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = AlbumManager()

class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=new_file_name, max_length=1000)
    description = models.TextField(blank=True)

    objects = PhotoManager()