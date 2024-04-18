import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import MyUser, Album, Photo
from .utils import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'phone', 'password1', 'password2', 'birthday')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['phone'].label = 'Телефон'

        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['birthday'].label = 'Дата рождения'

        for fieldname in ['email', 'phone', 'password1', 'password2']:
            self.fields[fieldname].error_messages = {'required': 'Это поле не может быть пустым.'}

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not 3 <= len(password1) <= 64:
            raise ValidationError("Пароль должен быть минимум из 3 символов и максимум из 64 символов.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password2')
        if not 3 <= len(password1) <= 64:
            raise ValidationError("Пароль должен быть минимум из 3 символов и максимум из 64 символов.")
        return password1

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r"^\+7\d{10}$", phone):
            raise ValidationError("Номер телефона должен быть в формате +7XXXXXXXXXX (X - цифра).")
        if len(phone) < 12:
            raise ValidationError("Некорректная длина номера, проверьте ввод.")
        if MyUser.objects.filter(phone=phone).exists():
            raise ValidationError("Пользователь с таким номером телефона уже зарегистрирован.", code='unique')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError("Такой пользователь уже зарегистрирован", code='unique')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Введите корректный адрес электронной почты.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Пароли не совпадают.")

        return cleaned_data

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if not birthday:
            return birthday
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', birthday):
            raise ValidationError("Введите дату в формате DD.MM.YYYY или оставьте поле пустым.")
        if not compare_date(birthday):
            raise ValidationError("Дата не может быть больше текущей.")
        if not is_valid_date(birthday):
            raise ValidationError("Введенная дата некорректна.")
        return birthday


class CustomLoginForm(forms.Form):
    email = forms.CharField(max_length=254, label='Адрес электронной почты')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['password'].label = 'Пароль'
        for fieldname in ['email', 'password']:
            self.fields[fieldname].error_messages = {
                'required': 'Это поле не может быть пустым.',
            }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Введите корректный адрес электронной почты.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not 3 <= len(password) <= 64:
            raise ValidationError("Пароль должен быть минимум из 3 символов и максимум из 64 символов.")
        return password


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'cover']

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Название альбома'
        self.fields['description'].label = 'Описание'
        self.fields['cover'].label = 'Обложка'
        for fieldname in ['title', 'description', 'cover']:
            self.fields[fieldname].error_messages = {'required': 'Это поле не может быть пустым.'}


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'description']
        widgets = {'image': forms.ClearableFileInput()}
