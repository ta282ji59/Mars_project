from django import forms
from .models import CustomUser, Project

# class ProjectCreationForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         # super().__init__(*args, **kwargs)

#         # self.fields['admin'].widget.attrs['disabled'] = 'disabled'
#         # self.fields['admin'].widget = forms.HiddenInput()

#         self.request = kwargs.pop('request')
#         super(ProjectCreationForm, self).__init__(*args, **kwargs)
#         self.fields['admin'].queryset = CustomUser.objects.filter(username=self.request.user)

#         # name = forms.CharField()
#         # admin = forms.ModelMultipleChoiceField(
#         #     queryset=CustomUser.objects.filter(id=request.user.id),
#         #     # queryset=None,
#         #     # queryset=CustomUser.objects.all(),
#         #     widget=forms.CheckboxSelectMultiple
#         # )
#         # self.fields['admin'].queryset = CustomUser.objects.filter(id=self.request.user.id)

#     class Meta():
#         model = Projects
#         fields = ('name','admin',)
#         # labels = {'name':"Name", 'admin':"Admin",}
#         # widgets = {'admin': forms.CheckboxSelectMultiple}


#     name = forms.CharField()
#     admin = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
#     password = forms.CharField(widget=forms.PasswordInput)

class ProjectCreationForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class ProjectJoinForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)