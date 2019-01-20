from django import forms


class FileForm(forms.Form):
    """
    上传文件表单
    """
    file = forms.FileField(required=True)

    def clean_file(self):
        return self.cleaned_data['file']
