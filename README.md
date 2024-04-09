Страницы на сайте:

'/' - Главная\
'/auth/'- Авторизация\
'/register/'- Регистрация\
'/albums/' - Все альбомы\
'/albums/add_album/' - Добавление альбома\
'/albums/user/' - Альбомы текущего пользователя\
'/albums/{id}/' - Детальная альбома\
'/albums/{id}/edit/' - Редактирование альбома

Альбомы отображаются в порядке их изменения (updated_at).

Прописаны редиректы, чтобы пользователи не смогли попасть на 
недоступные страницы.

Прописана логика для пользователей. Неавторизованные пользователи
не могут добавлять/редактировать альбомы. У альбомов существует привязка к пользователю -
пользователь не может отредактировать чужой альбом.

При редактировании прописана логика изменения фотографий (помимо названия
и описания альбома): 

можно обновить обложку альбома;\
отредактировать старые описания фото, либо добавить новые фотографии с 
новым описанием (старые фотографии при этом полностью удаляются).