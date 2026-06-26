from django import forms
from .models import Furniture


class FurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        fields = ['title', 'description', 'price', 'category', 'emoji', 'image_url']
        labels = {
            'title': 'Назва меблів',
            'description': 'Опис',
            'price': 'Ціна, грн',
            'category': 'Категорія',
            'emoji': 'Emoji',
            'image_url': 'Посилання на фото',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Наприклад: Диван Oslo'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Короткий опис товару'}),
            'price': forms.NumberInput(attrs={'min': 1, 'placeholder': '12000'}),
            'emoji': forms.TextInput(attrs={'maxlength': 10, 'placeholder': '🛋️'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }


class CheckoutForm(forms.Form):
    DELIVERY_CHOICES = [
        ('nova_poshta', 'Нова пошта'),
        ('ukrposhta', 'Укрпошта'),
        ('meest', 'Meest Пошта'),
        ('courier', 'Курʼєр до дверей'),
    ]

    full_name = forms.CharField(label='ПІБ отримувача', max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Іваненко Іван Іванович'}))
    phone = forms.CharField(label='Телефон', max_length=30, widget=forms.TextInput(attrs={'placeholder': '+380 XX XXX XX XX'}))
    city = forms.CharField(label='Місто', max_length=80, widget=forms.TextInput(attrs={'placeholder': 'Київ'}))
    delivery_service = forms.ChoiceField(label='Служба доставки', choices=DELIVERY_CHOICES)
    department = forms.CharField(label='Відділення / адреса доставки', max_length=160, widget=forms.TextInput(attrs={'placeholder': 'Відділення №12 або вул. Хрещатик, 1'}))
    comment = forms.CharField(label='Коментар до замовлення', required=False, widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Зручний час дзвінка, підйом на поверх тощо'}))
