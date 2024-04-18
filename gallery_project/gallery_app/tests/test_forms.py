from django.test import TestCase

from ..forms import CustomUserCreationForm, CustomLoginForm, AlbumForm, PhotoForm
from ..models import MyUser, Photo
from ..utils import create_test_image
from unittest.mock import MagicMock

class RegistrationForm(TestCase):
    def test_form_labels(self):
        """Проверка подписей"""
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['email'].label, 'Адрес электронной почты')
        self.assertEqual(form.fields['phone'].label, 'Телефон')
        self.assertEqual(form.fields['password1'].label, 'Пароль')
        self.assertEqual(form.fields['password2'].label, 'Подтверждение пароля')
        self.assertEqual(form.fields['birthday'].label, 'Дата рождения')

    def test_required_fields(self):
        """Обязательные поля"""
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('Это поле не может быть пустым.', form.errors['email'])
        self.assertIn('Это поле не может быть пустым.', form.errors['phone'])
        self.assertIn('Это поле не может быть пустым.', form.errors['password1'])
        self.assertIn('Это поле не может быть пустым.', form.errors['password2'])

    def test_password_validation(self):
        """Валидация пароля"""
        form = CustomUserCreationForm(data={
            'email': 'test@example.com',
            'phone': '+71234567890',
            'password1': '12',
            'password2': '12',
            'birthday': '01.01.2000'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Пароль должен быть минимум из 3 символов и максимум из 64 символов.', form.errors['password1'])

    def test_phone_validation(self):
        """Валидация телефона"""
        form = CustomUserCreationForm(data={
            'email': 'test@example.com',
            'phone': '+7123456789',
            'password1': 'password',
            'password2': 'password',
            'birthday': '01.01.2000'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Номер телефона должен быть в формате +7XXXXXXXXXX (X - цифра).', form.errors['phone'])

    def test_clean_email_unique(self):
        """Уникальность email"""
        MyUser.objects.create(email='unique@example.com', phone='+71234567890', password='123')
        form = CustomUserCreationForm(data={
            'email': 'unique@example.com',
            'phone': '+79876543210',
            'password1': 'password',
            'password2': 'password',
            'birthday': '01.01.2000'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Такой пользователь уже зарегистрирован', form.errors['email'])

    def test_successful_registation(self):
        """Отправка формы"""
        form = CustomUserCreationForm(data={
            'email': 'new@example.com',
            'phone': '+71234567890',
            'password1': '123',
            'password2': '123',
            'birthday': '01.01.2000'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(user.email, 'new@example.com')


class AuthorizationForm(TestCase):

    def test_form_labels(self):
        """Подписи к форме"""
        form = CustomLoginForm()
        self.assertEqual(form.fields['email'].label, 'Адрес электронной почты')
        self.assertEqual(form.fields['password'].label, 'Пароль')

    def test_email_validation(self):
        """Валидация email"""
        form = CustomLoginForm(data={'email': 'test', 'password': '123'})
        self.assertFalse(form.is_valid())
        self.assertIn('Введите корректный адрес электронной почты.', form.errors['email'])

    def test_required_fields(self):
        """Проверка обязательных полей"""
        form = CustomLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('Это поле не может быть пустым.', form.errors['email'])
        self.assertIn('Это поле не может быть пустым.', form.errors['password'])

    def test_successful_login(self):
        """Вход"""
        form = CustomLoginForm(data={'email': 'valid@example.com', 'password': '123'})
        self.assertTrue(form.is_valid())


class AlbumFormTest(TestCase):
    def test_form_labels(self):
        """Подписи"""
        form = AlbumForm()
        self.assertEqual(form.fields['title'].label, 'Название альбома')
        self.assertEqual(form.fields['description'].label, 'Описание')
        self.assertEqual(form.fields['cover'].label, 'Обложка')

    def test_custom_error_messages(self):
        """Ошибки"""
        form = AlbumForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], ['Это поле не может быть пустым.'])
        self.assertEqual(form.errors['description'], ['Это поле не может быть пустым.'])
        self.assertEqual(form.errors['cover'], ['Это поле не может быть пустым.'])

    def test_valid_data(self):
        "Корректные данные"
        cover_image = create_test_image()
        form = AlbumForm(data={
            'title': 'Название',
            'description': 'Описание'
        }, files={'cover': cover_image})
        self.assertTrue(form.is_valid())


class PhotoFormTest(TestCase):

    def test_valid_data(self):
        """Корректные данные"""
        photo = create_test_image()
        form = PhotoForm(data={
            'description': 'Описание фото'
        }, files={
            'image': photo
        })
        self.assertTrue(form.is_valid())
