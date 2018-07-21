from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','url','text']
        widgets={'text':forms.Textarea(attrs={'cols':98,'rows':10})}
