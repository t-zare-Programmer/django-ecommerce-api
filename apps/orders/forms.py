from django import forms
from .models import PaymentType


class OrderForm(forms.Form):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
        error_messages={'required': 'این فیلد نمی تواند خالی باشد'}
    )
    family = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
        error_messages={'required': 'این فیلد نمی تواند خالی باشد'}
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
        required=False
    )
    phone_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
        required=False
    )
    address = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس'}),
        error_messages={'required': 'این فیلد نمی تواند خالی باشد'}
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیحات'}),
        required=False
    )
    payment_type = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect(),
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_type'].choices = [
            (item.pk, item.payment_title) for item in PaymentType.objects.all()
        ]
