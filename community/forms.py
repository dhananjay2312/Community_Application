from django import forms
from .models import Post
from .models import QueryForm
from .models import Answer,Question
from django.forms import ModelForm

class PostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('Nmae_of_service_provider','title','text','Price','Contact_number','created_date','published_date')



class Queryform(forms.ModelForm):

    class Meta:
        model = QueryForm
        fields = ('name', 'email', 'quetion_category','quetion_details')

class AnswerForm(ModelForm):
    class Meta:
        model=Answer
        fields=('detail',)

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields=('title','detail','tags')

"""class ProfileForm(ModelForm):
    class Meta:
        fields=('first_name','last_name','username')"""
