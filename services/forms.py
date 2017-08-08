from django import forms
from services.models import Profile

from table import Table
from table.columns import *

import datetime

class FileTable(Table):
    field = CheckboxColumn(field=False, header="")
    name = LinkColumn(field='name', links=[Link(field="name", "index")], header="Name")
    date = DatetimeColumn(field='date', header="Date")

    print("Here")

class UserForm(forms.Form):
    class Meta():
        model = Profile
        fields = ('username', 'password', 'profile_pic')

class UploadFileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class File(object):
    def __init__(self, temp_file):
        self.name = str(temp_file)
        self.date = datetime.datetime.now()

    def __str__(self):
        return self.name
