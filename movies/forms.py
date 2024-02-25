from django.forms import ModelForm

from movies.models import Comment, Rating


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['value']