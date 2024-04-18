from django.test import SimpleTestCase
from django.urls import resolve, reverse

from gallery_app import views


class TestUrls(SimpleTestCase):

    def test_latest_albums_url_resolves(self):
        url = reverse('latest_albums')
        self.assertEquals(resolve(url).func, views.latest_albums)

    def test_auth_url_resolves(self):
        url = reverse('auth')
        self.assertEquals(resolve(url).func, views.auth)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, views.register)

    def test_albums_url_resolves(self):
        url = reverse('albums')
        self.assertEquals(resolve(url).func, views.albums)

    def test_add_album_url_resolves(self):
        url = reverse('add_album')
        self.assertEquals(resolve(url).func, views.add_album)

    def test_user_albums_url_resolves(self):
        url = reverse('user_albums')
        self.assertEquals(resolve(url).func, views.user_albums)

    def test_detail_album_url_resolves(self):
        url = reverse('detail_album', kwargs={'album_id': '123'})
        self.assertEquals(resolve(url).func, views.detail_album)

    def test_edit_album_url_resolves(self):
        url = reverse('edit', kwargs={'album_id': '123'})
        self.assertEquals(resolve(url).func, views.edit_album)

    def test_user_logout_url_resolves(self):
        url = reverse('user_logout')
        self.assertEquals(resolve(url).func, views.user_logout)
