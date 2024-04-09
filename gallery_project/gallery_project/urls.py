from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from gallery_app import views

urlpatterns = [
    path('', views.latest_albums, name='latest_albums'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('albums/', views.albums, name='albums'),
    path('albums/add_album/', views.add_album, name='add_album'),
    path('albums/user/', views.user_albums, name='user_albums'),
    path('albums/<album_id>/', views.detail_album, name='detail_album'),
    path('albums/<album_id>/edit/', views.edit_album, name='edit'),
    path('logout/', views.user_logout, name='user_logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
