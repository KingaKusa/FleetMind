from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {"title": "Tytuł posta", "content": "Treść posta"}
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Podaj tytuł"}),
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Podaj treść posta", "rows": 5}),
        }

class ChatForm(forms.Form):
    prompt = forms.CharField(label="Prompt")
    conversation_history = forms.CharField(required=False, widget=forms.HiddenInput())