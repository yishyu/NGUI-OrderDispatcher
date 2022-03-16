from django import forms
import crispy_forms.helper as cripsy_helper
import crispy_forms.layout as crispy_layout
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        min_length=8, required=True,
        widget=forms.PasswordInput,
        label="Password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = cripsy_helper.FormHelper()
        self.helper.form_id = 'id-form-login'
        self.helper.form_method = 'post'

        self.helper.layout = crispy_layout.Layout(
            crispy_layout.Fieldset(
                'Log In',
                crispy_layout.Column('email', css_class='form-group col-sm-12 mb-0'),
                crispy_layout.Column('password', css_class='form-group col-sm-12 mb-3'),
            ),
            crispy_layout.Submit('submit', 'Log in')
        )
