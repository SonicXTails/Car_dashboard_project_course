from django import forms
from .models import Card
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

from django import forms
from .models import Card

from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'title', 'image', 'price', 'description', 'brand', 'model_name', 
            'year', 'mileage', 'engine_volume', 'fuel_type', 'transmission', 
            'drive_type', 'color'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название карточки'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 3}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Модель'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год выпуска'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Пробег'}),
            'engine_volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Объем двигателя'}),
            'fuel_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тип топлива'}),
            'transmission': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Коробка передач'}),
            'drive_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Привод'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цвет'}),
        }
        labels = {
            'title': 'Название',
            'image': 'Изображение',
            'price': 'Цена',
            'description': 'Описание',
            'brand': 'Марка',
            'model_name': 'Модель',
            'year': 'Год выпуска',
            'mileage': 'Пробег',
            'engine_volume': 'Объем двигателя',
            'fuel_type': 'Тип топлива',
            'transmission': 'Коробка передач',
            'drive_type': 'Привод',
            'color': 'Цвет',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False