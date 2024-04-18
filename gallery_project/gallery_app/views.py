from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import CustomUserCreationForm, CustomLoginForm, AlbumForm
from .models import Album, Photo


def anonymous_required(function=None, redirect_url='/'):
    actual_decorator = user_passes_test(
        lambda x: x.is_anonymous,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def latest_albums(request):
    all_albums = Album.objects.all()
    latest_albums = all_albums.order_by('-updated_at')[:10]
    return render(request, 'latest_albums.html', {'latest_albums': latest_albums, 'title': 'Главная'})


def albums(request):
    all_albums = Album.objects.all()
    latest_albums = all_albums.order_by('-updated_at')[:10]
    return render(request, 'latest_albums.html', {'latest_albums': latest_albums, 'title': 'Альбомы'})


@anonymous_required(redirect_url='/')
def register(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_final_submit = request.POST.get('isFinalSubmit') == 'true'
        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and is_final_submit:
            form.save()
            return JsonResponse({"success": True})
        elif form.is_valid():
            return JsonResponse({"success": True})
        else:
            errors = {field: error.get_json_data() for field, error in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors})
    else:
        if request.method == 'POST':
            return HttpResponseBadRequest("Invalid request")
        else:
            form = CustomUserCreationForm()
            return render(request, 'register.html', {'form': form})


@anonymous_required(redirect_url='/')
def auth(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CustomLoginForm(request.POST)
        if 'validateOnly' in request.POST and form.is_valid():
            return JsonResponse({"success": True})
        elif 'validateOnly' in request.POST:
            errors = {field: error.get_json_data() for field, error in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors})
        else:
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({"success": True})
                else:  # сомнительно, но окэй
                    errors = {
                        "password": [
                            {
                                "message": "Пользователь не найден или неверный пароль.",
                                "code": ""
                            }
                        ]
                    }
                    return JsonResponse({"success": False, "errors": errors})
            else:
                errors = {field: error.get_json_data() for field, error in form.errors.items()}
                return JsonResponse({"success": False, "errors": errors})
    else:
        if request.method == 'POST':
            return HttpResponseBadRequest("Ошибка запроса")
        else:
            form = CustomLoginForm()
            return render(request, 'auth.html', {'form': form})


@login_required(login_url='/auth/')
def add_album(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        album_form = AlbumForm(request.POST, request.FILES)
        errors = {field: error.get_json_data() for field, error in album_form.errors.items()}
        photos_files = request.FILES.getlist('photos')

        if not photos_files:
            errors["image"] = [{"message": "Добавьте фотографии в альбом.", "code": ""}]

        if album_form.is_valid() and not errors:
            new_album = album_form.save(commit=False)
            new_album.user = request.user
            new_album.save()
            album_form.save_m2m()

            descriptions = [request.POST.get(f'description_{i}', '') for i in range(len(photos_files))]
            for file, description in zip(photos_files, descriptions):
                Photo.objects.create(album=new_album, image=file, description=description)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': errors})
    else:
        album_form = AlbumForm()

    return render(request, 'add_album.html', {'album_form': album_form})


@login_required(login_url='/auth/')
def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        album_form = AlbumForm(request.POST, request.FILES, instance=album)
        if album_form.is_valid():
            album.updated_at = timezone.now()
            updated_album = album_form.save()
            photos_files = request.FILES.getlist('photos')

            if photos_files:
                Photo.objects.filter(album=updated_album).delete()
                for i, file in enumerate(photos_files):
                    description_key = f'description_new_{i}'
                    description = request.POST.get(description_key,
                                                   '')  # если нужно, чтобы alt не был пустым - or updated_album.title
                    Photo.objects.create(album=updated_album, image=file, description=description)
            else:
                for key, value in request.POST.items():
                    if key.startswith('description_') and not key.startswith('description_new_'):
                        photo_id = key.split('_')[1]
                        photo = Photo.objects.get(id=photo_id, album=updated_album)
                        photo.description = value  # здесь тоже - or updated_album.title
                        photo.save()

            return JsonResponse({'success': True})
        else:
            errors = {field: error.get_json_data() for field, error in album_form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    else:
        album_form = AlbumForm(instance=album)
        existing_photos = Photo.objects.filter(album=album)
        return render(request, 'edit_album.html',
                      {'album_form': album_form, 'album': album, 'existing_photos': existing_photos})


def detail_album(request, album_id):
    album = Album.objects.get(id=album_id)
    return render(request, 'detail_album.html', {'album': album})


@login_required(login_url='/auth/')
def user_albums(request):
    user_albums = Album.objects.all().filter(user=request.user).order_by('-updated_at')[:10]
    return render(request, 'latest_albums.html', {'latest_albums': user_albums, 'title': 'Мои альбомы'})


def user_logout(request):
    logout(request)
    return redirect('/')
