from django.db.utils import IntegrityError
from django.test import TestCase
from faker import Faker

from ..models import MyUser, Album, Photo
from ..utils import generate_phone_number


class MyUserModelTest(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.valid_email = self.fake.email()
        self.valid_phone = generate_phone_number()
        self.valid_password = self.fake.password()
        self.valid_birthday = '10.10.1990'
        self.user = MyUser.objects.create_user(
            email=self.valid_email,
            phone=self.valid_phone,
            password=self.valid_password,
            birthday=self.valid_birthday
        )

    def test_email_normalization(self):
        """Нормализация от django"""
        email = "test@TEST.COM"
        user = MyUser.objects.create_user(email=email, phone=self.fake.phone_number(), password=self.valid_password)
        self.assertEqual(user.email, email.lower())

    def test_user_email_unique(self):
        """Ошибка при повторяющемся email"""
        with self.assertRaises(IntegrityError):
            MyUser.objects.create_user(email=self.valid_email, phone=self.fake.phone_number(),
                                       password=self.fake.password())

    def test_user_without_phone(self):
        """Проверка, что создание пользователя без телефона вызывает ошибку"""
        with self.assertRaises(ValueError):
            MyUser.objects.create_user(email=self.fake.email(), phone=None, password=self.fake.password())

    def test_create_user_success(self):
        """Проверка создания пользователя с валидными данными"""
        birthday = '10.10.1990'
        self.assertEqual(self.user.email, self.valid_email)
        self.assertEqual(self.user.phone, self.valid_phone)
        self.assertTrue(self.user.check_password(self.valid_password))
        self.assertEqual(self.user.birthday, birthday)

    def test_user_phone_unique(self):
        """Ошибка при повторяющемся номере телефона"""
        with self.assertRaises(IntegrityError):
            MyUser.objects.create_user(email=self.fake.email(), phone=self.valid_phone, password=self.fake.password())

    def test_user_without_email(self):
        """Проверка ошибки при создании пользователя без email"""
        with self.assertRaises(ValueError):
            MyUser.objects.create_user(email=None, phone=self.fake.phone_number(), password=self.fake.password())

    def test_optional_birthday_field(self):
        """Проверка, что пользователь создается с пустой датой рождения"""
        user = MyUser.objects.create_user(email=self.fake.email(), phone=generate_phone_number(),
                                          password=self.fake.password())
        self.assertIsNone(user.birthday)


class AlbumModelTestCase(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.valid_email = self.fake.email()
        self.valid_phone = generate_phone_number()
        self.valid_password = self.fake.password()
        self.valid_birthday = '10.10.1990'
        self.user = MyUser.objects.create_user(
            email=self.valid_email,
            phone=self.valid_phone,
            password=self.valid_password,
            birthday=self.valid_birthday
        )

    def test_create_album(self):
        """Создание альбома"""
        album = Album.objects.create_album(title='Test Album', description='Test Description', cover='test.jpg',
                                           user=self.user)
        self.assertEqual(album.title, 'Test Album')
        self.assertEqual(album.description, 'Test Description')
        self.assertEqual(album.cover, 'test.jpg')
        self.assertEqual(album.user, self.user)

    def test_create_album_empty_title(self):
        """Создание альбома с пустым названием"""
        with self.assertRaises(ValueError):
            Album.objects.create_album(title='', description='Test Description', cover='test.jpg', user=self.user)


class PhotoModelTestCase(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.valid_email = self.fake.email()
        self.valid_phone = generate_phone_number()
        self.valid_password = self.fake.password()
        self.valid_birthday = '10.10.1990'
        self.user = MyUser.objects.create_user(
            email=self.valid_email,
            phone=self.valid_phone,
            password=self.valid_password,
            birthday=self.valid_birthday
        )
        self.album = Album.objects.create(title='Test Album', description='Test Description', cover='test.jpg',
                                          user=self.user)

    def test_create_photo(self):
        """Добавление фото в альбом"""
        photo = Photo.objects.create_photo(album=self.album, image='test.jpg', description='Test Description')
        self.assertEqual(photo.album, self.album)
        self.assertEqual(photo.image, 'test.jpg')
        self.assertEqual(photo.description, 'Test Description')

    def test_create_photo_empty_album(self):
        """Добавление фото без альбома"""
        with self.assertRaises(ValueError):
            Photo.objects.create_photo(album=None, image='test.jpg', description='Test Description')
