from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from ..forms import CustomUserCreationForm
from ..models import MyUser, Album, Photo
from ..utils import create_test_image


class LatestAlbumsTestCase(TestCase):
    def test_latest_albums_view(self):
        # """Просмотр альбомов"""
        response = self.client.get(reverse('latest_albums'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'latest_albums.html')


class RegisterTestCase(TestCase):
    def test_register_get(self):
        """Страница регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_post_valid(self):
        """Отправка данных для регистрации"""
        data = {
            'email': 'newuser@example.com',
            'phone': '+79999999999',
            'password1': '123',
            'password2': '123'
        }
        response = self.client.post(reverse('register'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('success', False))

    def test_register_post_invalid(self):
        """Некорректнцые данные"""
        response = self.client.post(reverse('register'), {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn('errors', response.json())


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@test.ru', password='123', phone='+70000000000')

    def test_auth_post_valid(self):
        """Корректная авторизация"""
        data = {'email': 'testuser@test.ru', 'password': '123'}
        response = self.client.post(reverse('auth'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_auth_post_invalid(self):
        """Некорректная авторизация """
        data = {'email': 'testuser@test.ru', 'password': 'wrongpassword'}
        response = self.client.post(reverse('auth'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])


class AddAlbumTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@test.ru', password='123', phone='+70000000000')
        self.client.login(email='testuser@test.ru', password='123')

    def tearDown(self): # удаление сгенеренных картинок для теста
        albums = Album.objects.all()
        for album in albums:
            album.cover.delete()
        photos = Photo.objects.all()
        for photo in photos:
            photo.image.delete()

    def test_add_album_post_valid(self):
        """Корректный альбом"""
        cover = create_test_image()
        photo = create_test_image()
        data = {
            'title': 'Тест',
            'description': 'Описание',
            'cover': cover,
            'photos': [cover, photo]
        }

        response = self.client.post(reverse('add_album'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_add_album_post_invalid(self):
        """Некорректный альбом"""
        response = self.client.post(reverse('add_album'), {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])


class EditAlbumTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@test.ru', password='123', phone='+70000000000')
        self.album = Album.objects.create(title="Тест", description='Test', user=self.user, updated_at=timezone.now())
        self.client.login(email='testuser@test.ru', password='123')

    def tearDown(self):
        albums = Album.objects.all()
        for album in albums:
            album.cover.delete()
        photos = Photo.objects.all()
        for photo in photos:
            photo.image.delete()

    def test_edit_album_post_valid(self):
        """Корректное редактирование альбома"""
        data = {
            'title': 'Обновление',
            'description': '213',
            'cover': create_test_image()
        }
        response = self.client.post(reverse('edit', args=[self.album.id]), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_edit_album_post_invalid(self):
        """Некорректное редактирование альбома"""
        data = {
            'title': 'Обновление',
            'description': '213'
        }
        response = self.client.post(reverse('edit', args=[self.album.id]), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])

    def test_edit_album_get(self):
        response = self.client.get(reverse('edit', args=[self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_album.html')


class DetailAlbumTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@test.ru', password='123', phone='+70000000000')
        self.album = Album.objects.create(title="Тест", description='Test', user=self.user, updated_at=timezone.now())

    def test_detail_album_view(self):
        """Просмотр деталки"""
        response = self.client.get(reverse('detail_album', args=[self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_album.html')


class UserAlbumsTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@test.ru', password='123', phone='+70000000000')
        self.album = Album.objects.create(title="Тест", description='Test', user=self.user, cover=create_test_image(),
                                          updated_at=timezone.now())
        Album.objects.create(title="Тест", description='Test', user=self.user, cover=create_test_image(),
                             updated_at=timezone.now())
        self.client.login(email='testuser@test.ru', password='123')

    def tearDown(self):
        albums = Album.objects.all()
        for album in albums:
            album.cover.delete()
        photos = Photo.objects.all()
        for photo in photos:
            photo.image.delete()

    def test_user_albums_view(self):
        """Просмотр альбомов пользователя"""
        response = self.client.get(reverse('user_albums'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'latest_albums.html')


class UserLogoutTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@test.ru', password='123', phone='+70000000000')
        self.client.login(email='testuser@test.ru', password='123')

    def test_user_logout(self):
        """Выход из аккаунта"""
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
