from django import forms


class UploadTaskForm(forms.Form):

    task_file = forms.FileField()
