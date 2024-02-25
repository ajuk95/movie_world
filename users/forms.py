from django import forms
from django.contrib.auth.models import User

from movies.models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'slug', 'description', 'release_date', 'category', 'image', 'actors', 'trailer_link']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the 'user' parameter from the kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.uploaded_by = self.user
        if commit:
            instance.save()
        return instance


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
