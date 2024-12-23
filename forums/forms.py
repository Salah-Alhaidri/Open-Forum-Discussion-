from django import forms
from .models import ForumSectionModel , CommentModel
from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",  # Bootstrap class
                "placeholder": "Your e-mail",
                "aria-label": "Email",
            }
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",  # Bootstrap class
                "placeholder": "Subject",
                "aria-label": "Subject",
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",  # Bootstrap class
                "placeholder": "Your message",
                "aria-label": "Message",
                "rows": 5,  # Adjust height
            }
        )
    )

class NewTopicForm(forms.ModelForm):

    massg = forms.CharField(widget=forms.Textarea(
        attrs={'rows':5,'placeholder':'What is on your mind?'}
    ),
    max_length=4000,
    help_text='The max length of the text is 4000')

    class Meta:
        model = ForumSectionModel
        fields = ['SectionSubject','massg']


class PostForm(forms.ModelForm):

    class Meta:
        model = CommentModel
        fields = ['massg',]