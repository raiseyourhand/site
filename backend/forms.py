from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='nome de usuário', max_length=100)
    password = forms.CharField(label='senha', max_length=100,
                               widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput())


class CreateClassForm(forms.Form):
    name = forms.CharField(label='nome da turma', max_length=100)
    file = forms.FileField()
