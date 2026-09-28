from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Введённые пароли не совпадают.")

        user = CustomUser(email=self.cleaned_data.get("email"))
        validate_password(password2, user=user)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "city", "bio")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        bio = cleaned_data.get("bio")
        if not city:
            self.add_error("city", "Укажите город.")
        if not bio:
            self.add_error("bio", "Заполните описание.")
        return cleaned_data
