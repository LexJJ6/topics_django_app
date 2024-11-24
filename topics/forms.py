from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CommentForm(forms.Form):
    text = forms.CharField(label="Texto", max_length=500, widget=forms.Textarea)
    author = forms.CharField(label="Autor", max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Comentar', css_class='btn btn-primary'))